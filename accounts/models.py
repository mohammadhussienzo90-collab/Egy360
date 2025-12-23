# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string
import hmac


class UserProfile(models.Model):
    """Extended user profile for additional information"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)

    # Verification status
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    identity_verified = models.BooleanField(default=False)

    # Phone OTP fields
    phone_otp = models.CharField(max_length=6, blank=True, null=True)
    phone_otp_created = models.DateTimeField(blank=True, null=True)
    phone_otp_attempts = models.IntegerField(default=0)

    # Two-Factor Authentication
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_method = models.CharField(
        max_length=20,
        choices=[('totp', 'Authenticator App'), ('sms', 'SMS')],
        blank=True,
        null=True
    )
    backup_codes = models.JSONField(default=list, blank=True)

    # Security settings
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_device = models.CharField(max_length=255, blank=True, null=True)
    trusted_devices = models.JSONField(default=list, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} - Profile"

    @property
    def is_fully_verified(self):
        return all([
            self.email_verified,
            self.phone_verified,
            self.identity_verified
        ])

    def generate_otp(self):
        """Generate a 6-digit OTP code"""
        self.phone_otp = ''.join(random.choices(string.digits, k=6))
        self.phone_otp_created = timezone.now()
        self.phone_otp_attempts = 0
        self.save()
        return self.phone_otp

    def verify_otp(self, otp_code):
        """Verify the OTP code"""
        if not self.phone_otp or not self.phone_otp_created:
            return False, "No OTP code generated"

        # Check if OTP is expired (5 minutes)
        time_diff = timezone.now() - self.phone_otp_created
        if time_diff.total_seconds() > 300:
            self.phone_otp = None
            self.phone_otp_created = None
            self.save()
            return False, "OTP code has expired"

        # Check attempts limit
        if self.phone_otp_attempts >= 3:
            self.phone_otp = None
            self.phone_otp_created = None
            self.save()
            return False, "Too many attempts. Please request a new code"

        self.phone_otp_attempts += 1
        self.save()

        # Use constant-time comparison to prevent timing attacks
        if hmac.compare_digest(str(self.phone_otp), str(otp_code)):
            self.phone_otp = None
            self.phone_otp_created = None
            self.phone_verified = True
            self.save()
            return True, "OTP verified successfully"

        return False, "Invalid OTP code"

    def generate_backup_codes(self):
        """Generate 10 backup codes for 2FA"""
        codes = []
        for _ in range(10):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            code = f"{code[:4]}-{code[4:]}"
            codes.append(code)
        self.backup_codes = codes
        self.save()
        return codes

    def verify_backup_code(self, code):
        """Verify and consume a backup code with constant-time comparison"""
        for stored_code in self.backup_codes:
            if hmac.compare_digest(str(stored_code), str(code)):
                self.backup_codes.remove(stored_code)
                self.save()
                return True
        return False

    def get_masked_phone(self):
        """Return masked phone number for display"""
        if not self.phone:
            return None
        if len(self.phone) > 4:
            return f"***-***-{self.phone[-4:]}"
        return "***-***-****"



# accounts/models.py (bottom part - uncomment these lines)

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()