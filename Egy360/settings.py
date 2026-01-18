"""
Egy360 - Egypt Travel & Tourism Platform
=========================================

Django settings for the Egy360 project.

This file contains all configuration settings for the Django application including:
- Security settings (SECRET_KEY, ALLOWED_HOSTS, CSRF)
- Database configuration (PostgreSQL on Railway, SQLite locally)
- Authentication (Django allauth with Google, Facebook, Apple OAuth)
- Email configuration (SMTP settings for transactional emails)
- Payment gateway (PayMob for Egyptian market)
- Static/Media files (WhiteNoise for static file serving)
- Third-party integrations (Twilio SMS, REST Framework)

Environment Variables Required for Production:
----------------------------------------------
- SECRET_KEY: Django secret key for cryptographic signing
- DATABASE_URL: PostgreSQL connection string (provided by Railway)
- EMAIL_HOST_USER: SMTP username for sending emails
- EMAIL_HOST_PASSWORD: SMTP password/app password
- GOOGLE_CLIENT_ID: OAuth client ID from Google Cloud Console
- GOOGLE_CLIENT_SECRET: OAuth client secret from Google
- FACEBOOK_APP_ID: App ID from Facebook Developers
- FACEBOOK_APP_SECRET: App secret from Facebook Developers
- PAYMOB_API_KEY: API key from PayMob dashboard
- PAYMOB_HMAC_SECRET: HMAC secret for webhook verification

For local development, copy .env.example to .env and fill in values.

Author: Egy360 Team
Website: https://360egy.com
"""

import os
from pathlib import Path

# =============================================================================
# BASE CONFIGURATION
# =============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a new key: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key-replace-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG=False in production environment variables
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# =============================================================================
# ALLOWED HOSTS & SECURITY
# =============================================================================

# Hosts/domain names that this Django site can serve
# Add your custom domain and Railway domains here
ALLOWED_HOSTS = [
    '*',  # Allow all hosts (Railway handles routing)
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Railway deployment domains
    'healthcheck.railway.app',  # Railway health checks
    '360egy.com',  # Production domain
    'www.360egy.com',  # www subdomain
]

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',  # Admin interface
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static file management
    'django.contrib.sites',  # Multi-site framework (required for allauth)

    # Third-party packages
    'rest_framework',  # Django REST Framework for API
    'django_filters',  # Filtering for REST API
    'corsheaders',  # Cross-Origin Resource Sharing

    # OAuth & Social Authentication (django-allauth)
    # Documentation: https://django-allauth.readthedocs.io/
    'allauth',  # Core allauth functionality
    'allauth.account',  # Email/password authentication
    'allauth.socialaccount',  # Social account authentication
    'allauth.socialaccount.providers.google',  # Google OAuth2
    # 'allauth.socialaccount.providers.facebook',  # Facebook OAuth2 (disabled temporarily)
    # 'allauth.socialaccount.providers.apple',  # Apple Sign-In (uncomment when configured)

    # Two-Factor Authentication (optional, uncomment to enable)
    # 'django_otp',  # One-Time Password framework
    # 'django_otp.plugins.otp_totp',  # Time-based OTP (Google Authenticator)
    # 'django_otp.plugins.otp_static',  # Static backup codes

    # Project apps - Core business logic
    'accounts',  # User profiles, authentication extensions
    'accommodations',  # Hotels, resorts, Airbnb listings
    'api',  # REST API endpoints
    'blog',  # Travel blog, guides, articles
    'bookings',  # Booking management system
    'core',  # Shared utilities, base models
    'dashboard',  # User dashboard
    'destinations',  # Egyptian cities and attractions
    'home',  # Homepage, landing pages
    'payments',  # PayMob payment integration
    'reviews',  # User reviews and ratings
    'tours',  # Tour packages and experiences
    'transportation',  # Flights, transfers, car rentals
]

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    # Custom middleware - must be first to handle health checks
    'Egy360.middleware.HealthCheckMiddleware',  # Railway health check handler

    # Security middleware
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving

    # Session and authentication
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session support
    'corsheaders.middleware.CorsMiddleware',  # CORS headers
    'django.middleware.common.CommonMiddleware',  # Common operations
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth support
    'allauth.account.middleware.AccountMiddleware',  # Allauth middleware

    # Optional: Two-Factor Authentication middleware
    # 'django_otp.middleware.OTPMiddleware',  # Uncomment to enable 2FA

    # Message and security
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================

ROOT_URLCONF = 'Egy360.urls'

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-wide templates
        'APP_DIRS': True,  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =============================================================================
# WSGI APPLICATION
# =============================================================================

WSGI_APPLICATION = 'Egy360.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Uses PostgreSQL in production (Railway), SQLite for local development
# Railway automatically provides DATABASE_URL environment variable

try:
    import dj_database_url
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Production: Use PostgreSQL from Railway
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=0  # Disable persistent connections for Railway
            )
        }
    else:
        # Development: Use SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3'
            }
        }
except Exception:
    # Fallback to SQLite if dj_database_url fails
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    }

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# =============================================================================
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static file directories
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'  # Compression

# =============================================================================
# MEDIA FILES (User uploads)
# =============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# =============================================================================
# AUTHENTICATION CONFIGURATION
# =============================================================================

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # Where to redirect after login
LOGOUT_REDIRECT_URL = '/'  # Where to redirect after logout

# Authentication backends - order matters!
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django auth
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth (OAuth)
]

# Required for django-allauth
SITE_ID = 1

# =============================================================================
# DJANGO-ALLAUTH SETTINGS
# =============================================================================
# Documentation: https://django-allauth.readthedocs.io/en/latest/configuration.html

# Account settings
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # Auto-login after email confirm
ACCOUNT_LOGOUT_ON_GET = True  # Allow logout via GET request
ACCOUNT_EMAIL_REQUIRED = True  # Email is required for registration
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory', 'optional', or 'none'
ACCOUNT_USERNAME_REQUIRED = False  # Don't require username (use email)
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Login with email, not username
ACCOUNT_UNIQUE_EMAIL = True  # Each email can only be used once
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True  # Auto-login after password reset
ACCOUNT_SESSION_REMEMBER = True  # Remember me by default

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True  # Auto-create account on social login
SOCIALACCOUNT_EMAIL_REQUIRED = True  # Require email from social provider
SOCIALACCOUNT_QUERY_EMAIL = True  # Request email from social provider
SOCIALACCOUNT_LOGIN_ON_GET = True  # Allow social login via GET request

# =============================================================================
# OAUTH PROVIDER SETTINGS
# =============================================================================
# Configure OAuth credentials in Railway environment variables

SOCIALACCOUNT_PROVIDERS = {
    # Google OAuth2
    # Setup: https://console.cloud.google.com/apis/credentials
    # 1. Create OAuth 2.0 Client ID
    # 2. Add authorized redirect URI: https://360egy.com/accounts/google/login/callback/
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'key': '',
        }
    },

    # Facebook OAuth2 (disabled temporarily - uncomment when you have credentials)
    # Setup: https://developers.facebook.com/apps/
    # 1. Create App > Consumer type
    # 2. Add Facebook Login product
    # 3. Add redirect URI: https://360egy.com/accounts/facebook/login/callback/
    # 'facebook': {
    #     'METHOD': 'oauth2',
    #     'SCOPE': ['email', 'public_profile'],
    #     'FIELDS': ['id', 'email', 'name', 'first_name', 'last_name'],
    #     'APP': {
    #         'client_id': os.environ.get('FACEBOOK_APP_ID', ''),
    #         'secret': os.environ.get('FACEBOOK_APP_SECRET', ''),
    #         'key': '',
    #     }
    # },

    # Apple Sign-In (optional)
    # Setup: https://developer.apple.com/account/resources/identifiers/
    # 'apple': {
    #     'APP': {
    #         'client_id': os.environ.get('APPLE_CLIENT_ID', ''),
    #         'secret': os.environ.get('APPLE_SECRET', ''),
    #         'key': os.environ.get('APPLE_KEY_ID', ''),
    #         'certificate_key': os.environ.get('APPLE_PRIVATE_KEY', ''),
    #     }
    # }
}

# =============================================================================
# TWILIO SMS SETTINGS (for OTP/2FA)
# =============================================================================
# Setup: https://console.twilio.com/
# Used for SMS verification and two-factor authentication

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')

# =============================================================================
# CORS (Cross-Origin Resource Sharing)
# =============================================================================

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (adjust for production)

# =============================================================================
# CSRF (Cross-Site Request Forgery Protection)
# =============================================================================

CSRF_TRUSTED_ORIGINS = [
    'https://360egy.com',
    'https://www.360egy.com',
    'https://*.railway.app',
]

# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# =============================================================================
# CACHING
# =============================================================================
# Using local memory cache (consider Redis for production scaling)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'egy360-cache',
    }
}

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
# For production, use a transactional email service:
# - Gmail SMTP (with App Password)
# - SendGrid
# - Amazon SES
# - Mailgun
#
# Gmail Setup:
# 1. Enable 2FA on your Google account
# 2. Generate App Password: https://myaccount.google.com/apppasswords
# 3. Use App Password as EMAIL_HOST_PASSWORD
#
# Custom Domain Email (noreply@360egy.com):
# Option 1: Google Workspace - https://workspace.google.com/
# Option 2: Zoho Mail Free - https://www.zoho.com/mail/
# Option 3: Mailgun - https://www.mailgun.com/

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'  # Console output for dev
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# From email address for system emails
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Egy360 <noreply@360egy.com>')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'errors@360egy.com')  # For error emails
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@360egy.com')

# =============================================================================
# PAYMOB PAYMENT CONFIGURATION (Egypt's #1 Payment Gateway)
# =============================================================================
# PayMob supports:
# - Credit/Debit Cards (Visa, Mastercard, Meeza)
# - Mobile Wallets (Vodafone Cash, Orange Money, Etisalat Cash, WE Pay)
# - Fawry (Cash payments at 200,000+ retail locations)
#
# Get your credentials from: https://accept.paymob.com/portal2/en/login
# Documentation: https://docs.paymob.com/docs/accept-standard-redirect
#
# Setup Steps:
# 1. Create PayMob account at https://accept.paymob.com/
# 2. Get API Key from Dashboard > Settings > Account Info
# 3. Create Payment Integrations for each method (Card, Wallet, Fawry)
# 4. Create iFrame for card payments
# 5. Add environment variables to Railway

# API Key from PayMob Dashboard > Settings > Account Info
PAYMOB_API_KEY = os.environ.get('PAYMOB_API_KEY', '')

# HMAC Secret for webhook verification (Dashboard > Settings > Account Info)
PAYMOB_HMAC_SECRET = os.environ.get('PAYMOB_HMAC_SECRET', '')

# Integration IDs from PayMob Dashboard > Developers > Payment Integrations
# Each payment method (card, wallet, fawry) has its own integration ID
PAYMOB_CARD_INTEGRATION_ID = os.environ.get('PAYMOB_CARD_INTEGRATION_ID', '')
PAYMOB_WALLET_INTEGRATION_ID = os.environ.get('PAYMOB_WALLET_INTEGRATION_ID', '')
PAYMOB_FAWRY_INTEGRATION_ID = os.environ.get('PAYMOB_FAWRY_INTEGRATION_ID', '')

# Iframe ID for card payments (Dashboard > Developers > iframes)
PAYMOB_IFRAME_ID = os.environ.get('PAYMOB_IFRAME_ID', '')

# =============================================================================
# MAILCHIMP EMAIL MARKETING
# =============================================================================
# Setup: https://mailchimp.com/ (free up to 500 contacts)
# API Key: Account > Extras > API keys
# Audience ID: Audience > Settings > Audience name and defaults

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_AUDIENCE_ID = os.environ.get('MAILCHIMP_AUDIENCE_ID', '')
MAILCHIMP_SERVER_PREFIX = os.environ.get('MAILCHIMP_SERVER_PREFIX', '')  # e.g., 'us21'

# =============================================================================
# SECURITY SETTINGS (Production)
# =============================================================================
# Uncomment these for production deployment

if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Other security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
