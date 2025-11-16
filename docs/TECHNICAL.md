# Egy360 Technical Documentation

**Complete technical reference for developers**

---

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Apps Overview](#apps-overview)
3. [Database Models](#database-models)
4. [API Endpoints](#api-endpoints)
5. [Settings Configuration](#settings-configuration)
6. [Code Quality](#code-quality)
7. [Known Issues & Fixes](#known-issues--fixes)

---

## 🏗️ Project Structure

```
Egy360/
├── Egy360/                 # Project configuration
│   ├── settings.py         # Development settings
│   ├── settings_production.py  # Production settings ⭐ USE IN PRODUCTION
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI application
├── accounts/               # User management
├── accommodations/         # Hotels, resorts, etc.
├── tours/                  # Tour packages
├── destinations/           # Cities and attractions
├── bookings/               # Unified booking system
├── reviews/                # Review and rating system
├── payments/               # Payment processing
├── transportation/         # Transportation services
├── blog/                   # Content management
├── dashboard/              # User dashboard
├── api/                    # API routing
├── core/                   # Shared utilities
├── home/                   # Main website pages
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── media/                  # User uploads
├── logs/                   # Application logs
├── docs/                   # Documentation ⭐
├── requirements.txt        # Python dependencies
├── manage.py               # Django management
├── Procfile                # Deployment configuration
├── .env.example            # Environment variables template
└── .env                    # Actual environment (never commit!)
```

---

## 📦 Apps Overview

### 1. **accounts** - User Management

**Purpose:** Handle user authentication and profiles

**Models:**
- `UserProfile` - Extended user information

**Key Features:**
- User registration/login
- Profile management
- Verification status (email, phone, identity)
- User preferences (JSON field)

**Files:**
- `accounts/models.py:8-66` - UserProfile model
- `accounts/forms.py` - User forms (Note: file has typo - `froms.py`)

### 2. **accommodations** - Lodging Services

**Purpose:** Manage hotels, resorts, and other accommodations

**Models:**
- `Accommodation` - Main accommodation entity
- `Room` - Individual rooms/units
- `Amenity` - Facilities (pool, WiFi, etc.)

**Types Supported:**
- hotel, resort, hostel, apartment, villa, desert_camp, nile_cruise

**Key Features:**
- Star ratings (1-5)
- Price management
- Room-level booking
- Amenity management
- Featured listings

**Files:**
- `accommodations/models.py` - All models
- `accommodations/views.py` - ViewSets and views
- `accommodations/serializers.py` - API serializers

### 3. **tours** - Tour Packages

**Purpose:** Manage multi-day tour packages

**Models:**
- `Tour` - Main tour entity
- `TourItinerary` - Day-by-day schedule
- `TourBooking` - Tour bookings

**Tour Types:**
- cultural, adventure, desert_safari, nile_cruise, diving, religious, luxury, budget, family, photography

**Key Features:**
- Multi-day itineraries
- Group size management (min/max)
- Child pricing
- Includes/excludes tracking
- Difficulty levels

**Files:**
- `tours/models.py` - All models
- `tours/views.py` - ViewSets
- `tours/tests.py` - Comprehensive tests (1,013 lines!)

### 4. **destinations** - Locations

**Purpose:** Manage Egyptian cities, attractions, and travel information

**Models:**
- `Country` - Country information
- `City` - Egyptian cities
- `Attraction` - Tourist attractions
- `TravelGuide` - City guides

**Key Features:**
- Geographic coordinates
- Best time to visit
- UNESCO site tracking
- Climate information
- Transportation info

**Files:**
- `destinations/models.py` - All models
- `destinations/views.py` - Custom actions (popular, must_see)

### 5. **bookings** - Unified Booking System

**Purpose:** Handle all types of bookings

**Models:**
- `Booking` - Generic booking (uses ContentTypes)
- `AccommodationBooking` - Accommodation-specific details
- `BookingModification` - Change history
- `BookingCancellation` - Cancellation details

**Booking Statuses:**
- pending, confirmed, cancelled, completed

**Key Features:**
- Unique booking references
- Generic relations (can book anything)
- Modification tracking
- Cancellation management
- Refund tracking

**Files:**
- `bookings/models.py:7-95` - All models
- `bookings/serializers.py` - Complex serializers (709 lines)
- `bookings/models.py:62-75` - Status methods (confirm, cancel, complete)

### 6. **reviews** - Review System

**Purpose:** Comprehensive review and rating system

**Models:**
- `Review` - Main review entity (generic - can review anything)
- `ReviewImage` - Photo uploads
- `ReviewResponse` - Provider responses
- `ReviewHelpful` - Helpful votes
- `ReviewReport` - Fake review reporting

**Key Features:**
- Generic review system (ContentTypes)
- Multi-criteria ratings (cleanliness, location, value, service)
- Verification badges (verified purchase)
- Photo uploads
- Provider responses
- Community voting (helpful/not helpful)
- Report mechanism

**Files:**
- `reviews/models.py:17-143` - All models
- `reviews/serializers.py` - Well-documented serializers ⭐
- `reviews/views.py` - Custom actions (mark_helpful, report, respond)

**Fixed Issues:**
- ✅ Changed `CustomUser` → `User` (reviews/serializers.py:3)
- ✅ Changed `ReviewRating` → `Review` (reviews/serializers.py:4)
- ✅ Changed `user.user_type` → `user.is_staff` (reviews/views.py:318)

### 7. **payments** - Payment Processing

**Purpose:** Handle payments, refunds, and transactions

**Models:**
- `Payment` - Payment records
- `Refund` - Refund records
- `PaymentMethod` - Saved payment methods
- `Invoice` - Invoice generation
- `Transaction` - Transaction log

**Payment Methods:**
- credit_card, debit_card, paypal, stripe, bank_transfer, cash

**Payment Statuses:**
- pending, processing, completed, failed, refunded, partially_refunded

**Key Features:**
- Multiple payment gateways
- Full refund workflow
- Transaction logging
- Invoice generation
- Payment references

**Files:**
- `payments/models.py` - All models with indexes
- `payments/views.py` - Custom actions (process, confirm, refund)
- `payments/models.py:102-106` - mark_completed() method

**Fixed Issues:**
- ✅ Added `confirm()` method to Booking model (bookings/models.py:62-65)

### 8. **transportation** - Transport Services

**Purpose:** Manage transportation bookings

**Models:**
- `TransportationService` - Vehicle services
- `Driver` - Driver profiles
- `TransportBooking` - Transport bookings

**Service Types:**
- airport_transfer, private_car, taxi, bus_tour, minivan, limousine, vintage_car

**Key Features:**
- Vehicle capacity management
- Driver ratings
- Pickup/dropoff locations
- Fleet management

**Files:**
- `transportation/models.py` - All models
- `transportation/views.py` - ViewSets

### 9. **blog** - Content Management

**Purpose:** Blog posts and content

**Models:**
- `BlogPost` - Blog articles
- `BlogCategory` - Post categories
- `BlogComment` - Comments

**Key Features:**
- Rich content editing
- Comment moderation
- View counting
- Category organization
- Featured posts

**Files:**
- `blog/models.py` - All models
- `blog/views.py` - Blog views

### 10. **dashboard** - User Dashboard

**Purpose:** User account management interface

**Features:**
- My bookings
- My reviews
- Account settings
- Statistics

**Files:**
- `dashboard/views.py` - Dashboard views
- `dashboard/templates/` - Dashboard templates

### 11. **api** - API Router

**Purpose:** Aggregate all API endpoints

**Features:**
- RESTful API routing
- Centralized API configuration

**Files:**
- `api/urls.py` - Main API router

### 12. **core** - Shared Utilities

**Purpose:** Shared code across apps

**Status:** Currently minimal (empty models)

### 13. **home** - Main Website

**Purpose:** Homepage and static pages

**Pages:**
- Homepage
- About
- Contact
- FAQ
- Error pages (404, 500, 403)

**Features:**
- Newsletter subscription
- Contact form

**Files:**
- `home/views.py` - All views
- `templates/` - HTML templates

**Incomplete Features:**
- `home/views.py:185` - Newsletter integration TODO

---

## 🗄️ Database Models

### Model Relationships

```
User (Django built-in)
  ├─ One-to-One → UserProfile
  ├─ One-to-Many → Booking
  ├─ One-to-Many → Review
  ├─ One-to-Many → Payment
  └─ One-to-Many → TourBooking

Country
  └─ One-to-Many → City
      ├─ One-to-Many → Attraction
      ├─ One-to-Many → TravelGuide
      └─ One-to-Many → Accommodation

Accommodation
  ├─ Many-to-Many → Amenity
  └─ One-to-Many → Room

Tour
  └─ One-to-Many → TourItinerary

Booking (Generic)
  ├─ Generic FK → Accommodation/Tour/Transport
  ├─ One-to-One → AccommodationBooking
  ├─ One-to-Many → BookingModification
  ├─ One-to-One → BookingCancellation
  └─ One-to-Many → Payment

Review (Generic)
  ├─ Generic FK → Any model
  ├─ One-to-Many → ReviewImage
  ├─ One-to-One → ReviewResponse
  ├─ Many-to-Many → ReviewHelpful
  └─ One-to-Many → ReviewReport

Payment
  ├─ FK → Booking
  ├─ FK → User
  ├─ One-to-One → Invoice
  ├─ One-to-Many → Refund
  └─ One-to-Many → Transaction
```

### Key Indexes

**Performance-critical indexes already configured:**

**reviews/models.py:101-105**
```python
indexes = [
    models.Index(fields=['content_type', 'object_id', 'status']),
    models.Index(fields=['user', '-created_at']),
    models.Index(fields=['-rating', '-created_at']),
]
```

**payments/models.py:77-82**
```python
indexes = [
    models.Index(fields=['payment_reference']),
    models.Index(fields=['booking', '-created_at']),
    models.Index(fields=['user', '-created_at']),
    models.Index(fields=['status', '-created_at']),
]
```

**Recommended Additional Indexes:**
- `Accommodation`: slug, city, is_active
- `Tour`: slug, tour_type, is_active
- `City`: slug, is_popular
- `BlogPost`: slug, published_at

---

## 🔌 API Endpoints

**Base URL:** `/api/`

### Accommodations API

```
GET    /api/accommodations/              # List all
GET    /api/accommodations/{id}/         # Details
POST   /api/accommodations/              # Create (admin)
PUT    /api/accommodations/{id}/         # Update (admin)
DELETE /api/accommodations/{id}/         # Delete (admin)
```

**Filters:**
- `?city=Cairo` - Filter by city
- `?type=hotel` - Filter by type
- `?min_price=100&max_price=500` - Price range
- `?rating=4` - Minimum rating
- `?search=pyramids` - Search query

### Tours API

```
GET    /api/tours/                       # List all
GET    /api/tours/{id}/                  # Details
POST   /api/tours/                       # Create (admin)
```

**Filters:**
- `?tour_type=cultural` - Filter by type
- `?duration=3` - Filter by days
- `?min_price=200` - Minimum price

### Destinations API

```
GET    /api/destinations/cities/         # All cities
GET    /api/destinations/cities/{id}/    # City details
GET    /api/destinations/attractions/    # All attractions
GET    /api/destinations/cities/popular/ # Popular cities
```

### Reviews API

```
GET    /api/reviews/                     # All approved reviews
POST   /api/reviews/                     # Create review
GET    /api/reviews/{id}/                # Review details
PUT    /api/reviews/{id}/                # Update own review
DELETE /api/reviews/{id}/                # Delete own review

GET    /api/reviews/my_reviews/          # User's reviews
POST   /api/reviews/{id}/mark_helpful/   # Vote helpful
POST   /api/reviews/{id}/report/         # Report review
POST   /api/reviews/{id}/respond/        # Provider response
GET    /api/reviews/by_content/?content_type=accommodation&object_id=1
GET    /api/reviews/top_rated/           # Top rated
GET    /api/reviews/verified_only/       # Verified only
GET    /api/reviews/with_photos/         # With photos
```

### Payments API

```
GET    /api/payments/                    # All payments (admin)
GET    /api/payments/{id}/               # Payment details
POST   /api/payments/process/            # Create payment
POST   /api/payments/{id}/confirm/       # Confirm (staff only)
POST   /api/payments/refund/             # Request refund
GET    /api/payments/my_payments/        # User's payments
GET    /api/payments/{id}/download_invoice/  # Download invoice
```

### Bookings API

```
GET    /api/bookings/                    # All bookings
POST   /api/bookings/                    # Create booking
GET    /api/bookings/{id}/               # Booking details
PUT    /api/bookings/{id}/               # Update booking
```

### API Configuration

**Authentication:**
- Session Authentication (default)
- Token Authentication (ready to enable)

**Permissions:**
- IsAuthenticatedOrReadOnly (default)
- Custom permissions per endpoint

**Pagination:**
- 20 items per page
- Page number pagination

**Filtering:**
- DjangoFilterBackend
- SearchFilter
- OrderingFilter

**Rate Limiting (Production):**
- Anonymous: 100/hour
- Authenticated: 1000/hour

**Files:**
- `Egy360/settings_production.py:165-185` - REST Framework config

---

## ⚙️ Settings Configuration

### Development Settings

**File:** `Egy360/settings.py`

⚠️ **DO NOT use in production!**

**Key Settings:**
- `DEBUG = True` (shows error details)
- `SECRET_KEY = 'dev-key'` (insecure)
- `ALLOWED_HOSTS = ['*']` (allows all)
- `DATABASES = SQLite` (not production-ready)
- `EMAIL_BACKEND = console` (doesn't send emails)

### Production Settings ⭐

**File:** `Egy360/settings_production.py`

✅ **Use this in production!**

**How to use:**

```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=Egy360.settings_production

# Or in .env
DJANGO_SETTINGS_MODULE=Egy360.settings_production
```

**Key Differences:**
- `DEBUG = False` (secure)
- `SECRET_KEY` from environment (secure)
- `ALLOWED_HOSTS` from environment (specific domains)
- `DATABASES = PostgreSQL` (production-ready)
- `EMAIL_BACKEND = SMTP` (real emails)
- Security headers enabled
- HTTPS redirect enabled
- Caching configured (Redis)
- Rate limiting enabled

**Security Headers:**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = 'DENY'
```

### Environment Variables

**Template:** `.env.example`
**Actual:** `.env` (never commit!)

**Critical Variables:**
```bash
SECRET_KEY=<generate-new>
DEBUG=False
DATABASE_URL=postgresql://...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
STRIPE_SECRET_KEY=...
```

**Generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## ✅ Code Quality

### Strengths

1. **Well-organized structure** - 13 distinct apps
2. **Django best practices** - Follows conventions
3. **Comprehensive models** - All relationships properly defined
4. **Good use of indexes** - Performance optimized
5. **Generic relations** - Flexible review/booking system
6. **RESTful API** - Clean API design
7. **Detailed serializers** - reviews/serializers.py has excellent documentation

### Code Statistics

- **Total Python Files:** ~50+
- **Total Lines of Code:** ~17,150 lines
- **Largest Files:**
  - `tours/tests.py` - 1,013 lines
  - `bookings/serializers.py` - 709 lines
- **Test Coverage:** Test files exist for major apps

### Naming Conventions

✅ **Correct:**
- Models: PascalCase (Accommodation, UserProfile)
- Variables: snake_case (booking_reference, total_amount)
- URLs: kebab-case (accommodation-detail)
- Methods: snake_case (mark_completed, confirm)

### Comment Philosophy

**Current state:** Inconsistent
- **Over-commented:** reviews/serializers.py (very detailed)
- **Under-commented:** accommodations/models.py (minimal)

**Recommendation:** Light but meaningful comments
- Explain WHY, not WHAT
- Document business logic
- Remove obvious comments

---

## 🐛 Known Issues & Fixes Applied

### Fixed Issues ✅

1. **reviews/serializers.py:3-4**
   - ❌ Was: `from accounts.models import CustomUser`
   - ✅ Fixed: `from django.contrib.auth.models import User`
   - ❌ Was: `from .models import ReviewRating`
   - ✅ Fixed: `from .models import Review`

2. **reviews/views.py:318**
   - ❌ Was: `if request.user.user_type != 'provider'`
   - ✅ Fixed: `if not request.user.is_staff`

3. **bookings/models.py:62-75**
   - ❌ Was: Missing `confirm()` method
   - ✅ Fixed: Added `confirm()`, `cancel()`, `complete()` methods

4. **Procfile**
   - ❌ Was: Empty file
   - ✅ Fixed: Added Gunicorn and Celery configuration

### Incomplete Features (TODOs)

1. **home/views.py:185**
   ```python
   # TODO: Add email to newsletter service (MailChimp, SendGrid, etc.)
   ```
   **Impact:** Newsletter doesn't integrate with email service
   **Priority:** Low (can add post-launch)

2. **payments/views.py:137-138**
   ```python
   # Here you would integrate with payment gateway
   # For now, we'll create a pending payment
   ```
   **Impact:** Manual payment gateway integration needed
   **Priority:** HIGH (required for production)

3. **payments/views.py:284**
   ```python
   # Here you would generate PDF invoice
   ```
   **Impact:** Invoice PDF generation not implemented
   **Priority:** Medium (can use HTML invoices initially)

---

## 🔒 Security Considerations

### CRITICAL (Must Fix Before Production)

1. **SECRET_KEY** - Generate new, store in .env
2. **DEBUG** - Set to False
3. **ALLOWED_HOSTS** - Specific domains only
4. **CORS** - Specific origins only
5. **Database** - Use PostgreSQL
6. **HTTPS** - SSL certificate required

### Implemented Security

✅ Password validators
✅ CSRF protection
✅ SQL injection protection (Django ORM)
✅ XSS protection (template auto-escaping)
✅ Clickjacking protection (X-Frame-Options)
✅ Session security
✅ Input validation

### Recommended Additions

- Rate limiting (configured in production settings)
- API authentication tokens
- Two-factor authentication (2FA)
- Security monitoring (Sentry)
- Regular security audits

---

## 🚀 Performance Optimization

### Database Optimization

**Already Optimized:**
- Indexes on critical fields
- `select_related()` in some views

**Recommendations:**
```python
# Use select_related for ForeignKey
Accommodation.objects.select_related('city', 'country')

# Use prefetch_related for ManyToMany
Accommodation.objects.prefetch_related('amenities')

# Use only() to limit fields
Accommodation.objects.only('name', 'price', 'rating')
```

### Caching Strategy

**Configured in production settings:**
- Redis caching
- 5-minute default timeout

**Recommended Cache:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def homepage(request):
    # ...
```

**What to cache:**
- Homepage (15 minutes)
- Destination lists (1 hour)
- Popular tours (30 minutes)
- Static data (1 day)

### Query Optimization

**File:** `home/views.py:28-40`

❌ **Current (N+1 queries):**
```python
'featured_accommodations': Accommodation.objects.filter(
    is_featured=True, is_active=True
)[:6]
```

✅ **Optimized:**
```python
'featured_accommodations': Accommodation.objects.filter(
    is_featured=True, is_active=True
).select_related('city').prefetch_related('amenities')[:6]
```

---

## 📚 Additional Resources

### Django Documentation
- https://docs.djangoproject.com/
- https://www.django-rest-framework.org/

### Dependencies Documentation
- Django 5.0: https://docs.djangoproject.com/en/5.0/
- DRF: https://www.django-rest-framework.org/
- Celery: https://docs.celeryproject.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Redis: https://redis.io/documentation

---

## 🔧 Development Commands

### Common Tasks

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Run tests
pytest

# Check for issues
python manage.py check
```

### Database Commands

```bash
# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate app_name migration_name

# Database shell
python manage.py dbshell
```

---

## 📞 Support

For technical issues, consult:
1. This documentation
2. Django documentation
3. Stack Overflow
4. Project issues tracker

---

**Last Updated:** November 15, 2025
**Version:** 1.0.0
**Maintained by:** Egy360 Development Team
