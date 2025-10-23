from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    for Egy360 tourism platform
    """

    # User type choices
    USER_TYPE_CHOICES = (
        ('tourist', _('Tourist')),
        ('provider', _('Service Provider')),
        ('admin', _('Administrator')),
    )

    # Gender choices
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    )

    # Basic Information
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='tourist',
        help_text=_('Type of user account')
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Contact phone number')
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        help_text=_('User gender')
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text=_('Date of birth')
    )

    nationality = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_('User nationality')
    )

    # Address Information
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Street address')
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('City')
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('State/Province')
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Postal code')
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Country')
    )

    # Profile Information
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text=_('User profile picture')
    )

    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text=_('User biography')
    )

    website = models.URLField(
        blank=True,
        null=True,
        help_text=_('Personal or business website')
    )

    # Account Status
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Email verified status')
    )

    is_phone_verified = models.BooleanField(
        default=False,
        help_text=_('Phone number verified status')
    )

    is_identity_verified = models.BooleanField(
        default=False,
        help_text=_('Identity verification status')
    )

    # Provider-specific fields
    business_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Business name (for providers)')
    )

    business_license = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Business license number')
    )

    is_licensed = models.BooleanField(
        default=False,
        help_text=_('License verification status')
    )

    # Preferences
    language_preference = models.CharField(
        max_length=10,
        choices=[
            ('en', _('English')),
            ('ar', _('Arabic')),
            ('fr', _('French')),
            ('de', _('German')),
        ],
        default='en',
        help_text=_('Preferred language')
    )

    receive_notifications = models.BooleanField(
        default=True,
        help_text=_('Receive email notifications')
    )

    receive_sms = models.BooleanField(
        default=False,
        help_text=_('Receive SMS notifications')
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Account creation date')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Last update date')
    )

    last_login_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('Last login timestamp')
    )

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"

    def get_user_type_display(self):
        """Get human-readable user type"""
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, 'Unknown')

    def is_tourist(self):
        """Check if user is a tourist"""
        return self.user_type == 'tourist'

    def is_provider(self):
        """Check if user is a service provider"""
        return self.user_type == 'provider'

    def is_admin_user(self):
        """Check if user is an admin"""
        return self.user_type == 'admin' or self.is_staff