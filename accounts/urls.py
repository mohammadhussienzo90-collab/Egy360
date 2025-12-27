# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from . import views

app_name = 'accounts'

def debug_view(request):
    """Simple debug endpoint"""
    return JsonResponse({'status': 'ok', 'app': 'accounts'})

urlpatterns = [
    # Debug endpoint
    path('debug/', debug_view, name='debug'),

    # Basic Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # Phone OTP Login
    path('phone-login/', views.phone_login_view, name='phone_login'),
    path('phone-verify/', views.phone_verify_view, name='phone_verify'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),

    # Two-Factor Authentication
    path('2fa/setup/', views.setup_2fa_view, name='setup_2fa'),
    path('2fa/verify/', views.verify_2fa_view, name='verify_2fa'),
    path('2fa/disable/', views.disable_2fa_view, name='disable_2fa'),
    path('2fa/backup-codes/', views.backup_codes_view, name='backup_codes'),

    # Security Settings
    path('security/', views.security_settings_view, name='security_settings'),

    # Password Reset (rate limited)
    path('password-reset/',
         views.RateLimitedPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
