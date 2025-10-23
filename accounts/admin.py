from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom User Admin with additional fields
    """

    # Display fields in list view
    list_display = (
        'username',
        'email',
        'get_full_name',
        'user_type',
        'is_verified',
        'is_licensed',
        'is_active',
        'created_at',
    )

    list_filter = (
        'user_type',
        'is_verified',
        'is_phone_verified',
        'is_identity_verified',
        'is_licensed',
        'is_active',
        'created_at',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'business_name',
    )

    ordering = ('-created_at',)

    # Fieldsets for add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Fieldsets for change form
    fieldsets = (
        (_('Personal Information'), {
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'gender',
                'date_of_birth',
                'nationality',
            )
        }),
        (_('Account Type'), {
            'fields': (
                'user_type',
                'password',
            )
        }),
        (_('Address'), {
            'fields': (
                'address',
                'city',
                'state',
                'postal_code',
                'country',
            ),
            'classes': ('collapse',),
        }),
        (_('Profile'), {
            'fields': (
                'profile_picture',
                'bio',
                'website',
                'language_preference',
            ),
            'classes': ('collapse',),
        }),
        (_('Verification & Security'), {
            'fields': (
                'is_verified',
                'is_phone_verified',
                'is_identity_verified',
                'is_licensed',
            ),
        }),
        (_('Business Information'), {
            'fields': (
                'business_name',
                'business_license',
            ),
            'classes': ('collapse',),
        }),
        (_('Notifications'), {
            'fields': (
                'receive_notifications',
                'receive_sms',
            ),
            'classes': ('collapse',),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',),
        }),
        (_('Important Dates'), {
            'fields': (
                'last_login',
                'last_login_at',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login_at',
    )

    def get_full_name(self, obj):
        """Display full name in list view"""
        return obj.get_full_name() or obj.username

    get_full_name.short_description = _('Full Name')