# accounts/urls.py
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

app_name = 'accounts'

def placeholder_view(request):
    """Placeholder view for debugging"""
    return HttpResponse("Account feature temporarily unavailable", status=503)

def debug_view(request):
    """Simple debug endpoint"""
    return JsonResponse({'status': 'ok', 'app': 'accounts'})

def test_import(request):
    """Test what import is failing"""
    errors = []

    try:
        from .models import UserProfile
        errors.append(f"models: OK")
    except Exception as e:
        errors.append(f"models: {str(e)}")

    try:
        from .forms import UserLoginForm
        errors.append(f"forms: OK")
    except Exception as e:
        errors.append(f"forms: {str(e)}")

    try:
        from .sms import send_otp_sms
        errors.append(f"sms: OK")
    except Exception as e:
        errors.append(f"sms: {str(e)}")

    try:
        from core.rate_limit import rate_limit_login
        errors.append(f"rate_limit: OK")
    except Exception as e:
        errors.append(f"rate_limit: {str(e)}")

    try:
        from . import views
        errors.append(f"views: OK")
    except Exception as e:
        errors.append(f"views: {str(e)}")

    return JsonResponse({'imports': errors})

urlpatterns = [
    path('debug/', debug_view, name='debug'),
    path('test-import/', test_import, name='test_import'),
    path('register/', placeholder_view, name='register'),
    path('login/', placeholder_view, name='login'),
    path('logout/', placeholder_view, name='logout'),
    path('profile/', placeholder_view, name='profile'),
    path('profile/update/', placeholder_view, name='update_profile'),
    path('phone-login/', placeholder_view, name='phone_login'),
    path('phone-verify/', placeholder_view, name='phone_verify'),
    path('resend-otp/', placeholder_view, name='resend_otp'),
    path('2fa/setup/', placeholder_view, name='setup_2fa'),
    path('2fa/verify/', placeholder_view, name='verify_2fa'),
    path('2fa/disable/', placeholder_view, name='disable_2fa'),
    path('2fa/backup-codes/', placeholder_view, name='backup_codes'),
    path('security/', placeholder_view, name='security_settings'),
    path('password-reset/', placeholder_view, name='password_reset'),
    path('password-reset/done/', placeholder_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', placeholder_view, name='password_reset_confirm'),
    path('reset/done/', placeholder_view, name='password_reset_complete'),
]
