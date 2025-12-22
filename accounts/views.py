# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    UserUpdateForm,
)
from .models import UserProfile
from .sms import send_otp_sms, validate_phone_number


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Save phone number if provided
            phone_number = request.POST.get('phone_number')
            country_code = request.POST.get('country_code', '+20')
            if phone_number:
                profile = user.profile
                profile.phone = f"{country_code}{phone_number}"
                profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('homepage')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Check if 2FA is enabled
            if hasattr(user, 'profile') and user.profile.two_factor_enabled:
                # Store user ID in session for 2FA verification
                request.session['pending_2fa_user_id'] = user.id
                return redirect('accounts:verify_2fa')

            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect(request.GET.get('next', 'homepage'))
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('homepage')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': request.user.profile if hasattr(request.user, 'profile') else None
    })


@login_required
def update_profile(request):
    """Update user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile if hasattr(request.user, 'profile') else None
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(
            instance=request.user.profile if hasattr(request.user, 'profile') else None
        )

    return render(request, 'accounts/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Phone OTP Login Views

def phone_login_view(request):
    """Phone number entry for OTP login"""
    if request.method == 'POST':
        country_code = request.POST.get('country_code', '+20')
        phone_number = request.POST.get('phone_number', '')

        # Validate and format phone number
        full_phone = f"{country_code}{phone_number}"
        is_valid, formatted_phone, error = validate_phone_number(full_phone)

        if not is_valid:
            messages.error(request, error or 'Invalid phone number')
            return render(request, 'accounts/phone_login.html')

        # Find user with this phone number
        try:
            profile = UserProfile.objects.get(phone=formatted_phone)
            user = profile.user
        except UserProfile.DoesNotExist:
            messages.error(request, 'No account found with this phone number. Please register first.')
            return render(request, 'accounts/phone_login.html')

        # Generate and send OTP
        otp_code = profile.generate_otp()
        success, message, _ = send_otp_sms(formatted_phone, otp_code)

        if success:
            request.session['phone_login_phone'] = formatted_phone
            request.session['phone_login_user_id'] = user.id
            messages.success(request, 'Verification code sent to your phone.')
            return redirect('accounts:phone_verify')
        else:
            messages.error(request, message)

    return render(request, 'accounts/phone_login.html')


def phone_verify_view(request):
    """Verify OTP code for phone login"""
    phone = request.session.get('phone_login_phone')
    user_id = request.session.get('phone_login_user_id')

    if not phone or not user_id:
        messages.error(request, 'Please enter your phone number first.')
        return redirect('accounts:phone_login')

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '')

        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, 'Invalid session. Please try again.')
            return redirect('accounts:phone_login')

        success, message = profile.verify_otp(otp_code)

        if success:
            # Clear session data
            del request.session['phone_login_phone']
            del request.session['phone_login_user_id']

            # Log in the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Login successful!')
            return redirect('homepage')
        else:
            messages.error(request, message)

    return render(request, 'accounts/phone_verify.html', {
        'phone_number': phone
    })


def resend_otp_view(request):
    """Resend OTP code"""
    phone = request.session.get('phone_login_phone')
    user_id = request.session.get('phone_login_user_id')

    if not phone or not user_id:
        return JsonResponse({'success': False, 'message': 'Invalid session'})

    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'User not found'})

    otp_code = profile.generate_otp()
    success, message, _ = send_otp_sms(phone, otp_code)

    return JsonResponse({'success': success, 'message': message})


# Two-Factor Authentication Views

@login_required
def setup_2fa_view(request):
    """Setup 2FA with authenticator app"""
    profile = request.user.profile

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '')

        # Verify the TOTP code
        try:
            from django_otp.plugins.otp_totp.models import TOTPDevice

            device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
            if device and device.verify_token(otp_code):
                device.confirmed = True
                device.save()

                profile.two_factor_enabled = True
                profile.two_factor_method = 'totp'
                profile.save()

                # Generate backup codes
                backup_codes = profile.generate_backup_codes()

                messages.success(request, 'Two-factor authentication has been enabled!')
                return render(request, 'accounts/backup_codes.html', {
                    'backup_codes': backup_codes,
                    'first_time': True
                })
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        except Exception as e:
            messages.error(request, f'Error setting up 2FA: {str(e)}')

    # Generate or get TOTP device
    try:
        from django_otp.plugins.otp_totp.models import TOTPDevice

        device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            confirmed=False,
            defaults={'name': 'Authenticator App'}
        )

        # Generate QR code
        totp_uri = device.config_url
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        qr_code_url = f"data:image/png;base64,{qr_code_base64}"

        # Get secret key for manual entry
        secret_key = base64.b32encode(device.bin_key).decode('utf-8')
        # Format secret key with spaces for readability
        secret_key_formatted = ' '.join([secret_key[i:i+4] for i in range(0, len(secret_key), 4)])

    except ImportError:
        messages.error(request, 'Two-factor authentication is not properly configured.')
        return redirect('accounts:security_settings')

    return render(request, 'accounts/2fa_setup.html', {
        'qr_code_url': qr_code_url,
        'secret_key': secret_key_formatted
    })


def verify_2fa_view(request):
    """Verify 2FA during login"""
    user_id = request.session.get('pending_2fa_user_id')

    if not user_id:
        messages.error(request, 'Please log in first.')
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, 'Invalid session. Please try again.')
        return redirect('accounts:login')

    if request.method == 'POST':
        method = request.POST.get('method', 'totp')
        otp_code = request.POST.get('otp_code', '')
        backup_code = request.POST.get('backup_code', '')
        remember_device = request.POST.get('remember_device', False)

        verified = False

        if method == 'totp':
            # Verify TOTP code
            try:
                from django_otp.plugins.otp_totp.models import TOTPDevice
                device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
                if device and device.verify_token(otp_code):
                    verified = True
            except Exception:
                pass

        elif method == 'sms':
            # Verify SMS code
            success, message = profile.verify_otp(otp_code)
            verified = success

        elif method == 'backup':
            # Verify backup code
            verified = profile.verify_backup_code(backup_code)

        if verified:
            del request.session['pending_2fa_user_id']
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # TODO: Handle remember device

            messages.success(request, 'Login successful!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'accounts/2fa_verify.html', {
        'phone_masked': profile.get_masked_phone()
    })


@login_required
def disable_2fa_view(request):
    """Disable 2FA"""
    if request.method == 'POST':
        password = request.POST.get('password', '')

        # Verify password
        if request.user.check_password(password):
            profile = request.user.profile
            profile.two_factor_enabled = False
            profile.two_factor_method = None
            profile.backup_codes = []
            profile.save()

            # Delete TOTP device
            try:
                from django_otp.plugins.otp_totp.models import TOTPDevice
                TOTPDevice.objects.filter(user=request.user).delete()
            except Exception:
                pass

            messages.success(request, 'Two-factor authentication has been disabled.')
        else:
            messages.error(request, 'Invalid password.')

    return redirect('accounts:security_settings')


@login_required
def backup_codes_view(request):
    """View or regenerate backup codes"""
    profile = request.user.profile

    if request.method == 'POST':
        # Regenerate backup codes
        backup_codes = profile.generate_backup_codes()
        messages.success(request, 'New backup codes have been generated.')
        return render(request, 'accounts/backup_codes.html', {
            'backup_codes': backup_codes,
            'first_time': False
        })

    return render(request, 'accounts/backup_codes.html', {
        'backup_codes': profile.backup_codes,
        'first_time': False
    })


@login_required
def security_settings_view(request):
    """Security settings page"""
    profile = request.user.profile

    # Get connected social accounts
    social_accounts = []
    try:
        from allauth.socialaccount.models import SocialAccount
        social_accounts = SocialAccount.objects.filter(user=request.user)
    except ImportError:
        pass

    return render(request, 'accounts/security_settings.html', {
        'profile': profile,
        'social_accounts': social_accounts,
        'two_factor_enabled': profile.two_factor_enabled,
        'two_factor_method': profile.two_factor_method,
        'backup_codes_count': len(profile.backup_codes) if profile.backup_codes else 0,
        'phone_verified': profile.phone_verified,
        'phone_masked': profile.get_masked_phone()
    })
