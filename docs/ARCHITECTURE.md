# Egy360 Architecture Guide

This document explains the project structure, design patterns, and how different components work together.

## Table of Contents
1. [Overview](#overview)
2. [Django Apps](#django-apps)
3. [Design Patterns](#design-patterns)
4. [Data Flow](#data-flow)
5. [Authentication](#authentication)
6. [Email System](#email-system)
7. [Template Structure](#template-structure)

---

## Overview

Egy360 follows Django's MTV (Model-Template-View) architecture with a modular app structure. Each app handles a specific domain of functionality.

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  (Bootstrap 5 + JavaScript)                                  │
├─────────────────────────────────────────────────────────────┤
│                     Django Views                             │
│  (Class-based & Function-based views)                        │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Accommodations│    Tours    │   Bookings   │    Reviews     │
├──────────────┴──────────────┴──────────────┴────────────────┤
│                    Core Services                             │
│  (Email, Utilities, Template Tags)                           │
├─────────────────────────────────────────────────────────────┤
│                   Django ORM                                 │
├─────────────────────────────────────────────────────────────┤
│                PostgreSQL / SQLite                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Django Apps

### Core Business Apps

| App | Purpose | Key Models |
|-----|---------|------------|
| `accommodations` | Hotels, resorts, cruises | Accommodation, Room, Amenity |
| `tours` | Tour packages & bookings | Tour, TourItinerary, TourBooking |
| `bookings` | Unified booking system | Booking, AccommodationBooking |
| `reviews` | User reviews & ratings | Review, ReviewResponse, ReviewHelpful |
| `destinations` | City guides | City, Attraction |

### Supporting Apps

| App | Purpose | Key Models |
|-----|---------|------------|
| `accounts` | User management | UserProfile |
| `dashboard` | User dashboard | SavedItem, UserActivity |
| `blog` | Travel articles | BlogPost, Category |
| `transportation` | Airport transfers | TransportService |
| `payments` | Payment processing | Payment, Transaction |
| `home` | Homepage & static pages | - |
| `core` | Shared utilities | - |
| `api` | REST API endpoints | - |

---

## Design Patterns

### 1. Generic Foreign Keys (Polymorphic Relationships)

Used for models that can relate to multiple types (accommodations OR tours):

```python
# bookings/models.py
class Booking(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

**Used in:**
- `Booking` - can book accommodations or tours
- `Review` - can review accommodations or tours
- `SavedItem` - can save any item to wishlist

### 2. Class-Based Views with Mixins

List and detail views use Django's generic CBVs:

```python
# accommodations/views.py
class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'accommodation_search.html'
    context_object_name = 'accommodations'
    paginate_by = 12
```

### 3. Function-Based Views for Complex Logic

Used when business logic is complex:

```python
# bookings/views.py
@login_required
def booking_checkout(request, booking_type, item_id):
    # Complex checkout logic
```

### 4. Django Signals

Auto-create user profiles when users register:

```python
# accounts/models.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

---

## Data Flow

### Booking Flow

```
1. User browses accommodations/tours
   └── ListView displays listings with filters

2. User views detail page
   └── DetailView shows item info + reviews

3. User clicks "Book Now"
   └── Redirects to checkout (login required)

4. User fills booking form
   └── Form validated, Booking created

5. Confirmation email sent
   └── core/email.py sends HTML email

6. User sees confirmation page
   └── Booking visible in dashboard
```

### Review Flow

```
1. User visits item detail page
   └── reviews_section.html included

2. User clicks "Write Review"
   └── Redirects to submit_review.html

3. User submits review
   └── Review created with status='pending'

4. Admin approves in Django admin
   └── Review.approve() updates item ratings

5. Review appears on detail page
   └── Only approved reviews shown
```

---

## Authentication

### Providers

Egy360 uses django-allauth for authentication:

| Method | Provider |
|--------|----------|
| Email/Password | Built-in |
| Google | allauth.socialaccount.providers.google |
| Facebook | allauth.socialaccount.providers.facebook |
| Apple | allauth.socialaccount.providers.apple |

### Two-Factor Authentication

Uses django-otp for 2FA:

- **TOTP**: Authenticator apps (Google Authenticator, Authy)
- **SMS**: Twilio integration for SMS codes
- **Backup Codes**: 10 one-time codes generated

### URL Routes

```
/accounts/login/           # Email login
/accounts/register/        # Registration
/auth/google/login/        # Google OAuth
/auth/facebook/login/      # Facebook OAuth
/accounts/2fa/setup/       # Enable 2FA
```

---

## Email System

### Location
`core/email.py`

### Available Functions

| Function | Purpose |
|----------|---------|
| `send_booking_confirmation()` | Booking confirmation email |
| `send_booking_status_update()` | Status change notification |
| `send_contact_notification()` | Admin notification for contact form |
| `send_newsletter_welcome()` | Welcome new subscribers |

### Email Templates

```
templates/emails/
├── booking_confirmation.html
├── accommodation_booking_confirmation.html
└── tour_booking_confirmation.html
```

### Configuration

Set in `settings.py` or environment:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

## Template Structure

### Base Template Hierarchy

```
templates/
├── base.html                 # Main layout (navbar, footer)
├── base_dashboard.html       # Dashboard layout
│
├── accommodations/
│   └── ...
├── tours/
│   └── ...
├── dashboard/
│   ├── dashboard.html        # Main dashboard
│   ├── bookings.html         # User bookings
│   ├── reviews.html          # User reviews
│   ├── saved_items.html      # Wishlist
│   └── settings.html         # Account settings
│
├── reviews/
│   ├── reviews_section.html  # Reusable component
│   └── submit_review.html    # Review form
│
└── emails/
    └── ...                   # Email templates
```

### Template Inheritance

```html
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Page content here -->
{% endblock %}

{% block extra_js %}
    <!-- Page-specific JavaScript -->
{% endblock %}
```

### Reusable Components

Include components with context:

```html
{% include 'reviews/reviews_section.html' with
   reviews_data=reviews_data
   item_type='accommodation'
   item=accommodation
%}
```

---

## Static Files

### Structure

```
static/
├── css/
│   └── styles.css
├── js/
│   └── main.js
└── images/
    └── ...
```

### Collection

WhiteNoise serves static files in production:

```bash
python manage.py collectstatic
```

Files collected to `staticfiles/` directory.

---

## Database Indexes

Performance optimized with indexes on frequently queried fields:

```python
class Meta:
    indexes = [
        models.Index(fields=['city'], name='accommodation_city_idx'),
        models.Index(fields=['is_active'], name='accommodation_active_idx'),
        models.Index(fields=['is_featured'], name='accommodation_featured_idx'),
    ]
```

---

## Caching

Local memory cache configured (suitable for single-server deployment):

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'egy360-cache',
    }
}
```

For high-traffic, consider Redis.

---

## API Architecture

REST API built with Django REST Framework:

```python
# Serializers convert models to JSON
class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'

# ViewSets provide CRUD endpoints
class AccommodationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accommodation.objects.filter(is_active=True)
    serializer_class = AccommodationSerializer
```

---

## Security Measures

1. **CSRF Protection**: Enabled on all forms
2. **XSS Prevention**: Template auto-escaping
3. **SQL Injection**: ORM parameterized queries
4. **Password Hashing**: Argon2 (Django default)
5. **HTTPS**: Enforced in production
6. **Session Security**: Secure cookies enabled

---

## Next Steps

- [Models Reference](MODELS.md) - Database schema details
- [Deployment Guide](DEPLOYMENT.md) - Production setup
- [Features Guide](FEATURES.md) - User features
