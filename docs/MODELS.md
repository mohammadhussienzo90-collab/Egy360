# Egy360 Database Models Reference

This document describes all database models, their fields, and relationships.

## Table of Contents
1. [Accommodations](#accommodations)
2. [Tours](#tours)
3. [Bookings](#bookings)
4. [Reviews](#reviews)
5. [Accounts](#accounts)
6. [Dashboard](#dashboard)
7. [Destinations](#destinations)

---

## Accommodations

### Accommodation
Hotels, resorts, Nile cruises, and other lodging.

**Location:** `accommodations/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(200) | Property name |
| `slug` | SlugField | URL-friendly identifier |
| `accommodation_type` | CharField | hotel, resort, hostel, apartment, villa, camp, cruise |
| `description` | TextField | Full description |
| `city` | CharField(100) | Location city |
| `address` | CharField(255) | Street address |
| `latitude` | DecimalField | GPS latitude |
| `longitude` | DecimalField | GPS longitude |
| `star_rating` | IntegerField(1-5) | Hotel star rating |
| `total_rooms` | IntegerField | Number of rooms |
| `check_in_time` | TimeField | Standard check-in |
| `check_out_time` | TimeField | Standard check-out |
| `price_per_night` | DecimalField | Base price |
| `weekend_surcharge` | DecimalField | Weekend price addition |
| `is_featured` | BooleanField | Show on homepage |
| `is_verified` | BooleanField | Verified property |
| `is_active` | BooleanField | Published status |
| `main_image` | ImageField | Primary photo |
| `image_url` | URLField | External image URL |
| `booking_com_url` | URLField | Affiliate link |
| `agoda_url` | URLField | Affiliate link |
| `hotels_com_url` | URLField | Affiliate link |
| `average_rating` | DecimalField | Calculated from reviews |
| `total_reviews` | IntegerField | Review count |

**Relationships:**
- Has many `Room` objects
- Has many `Amenity` through M2M
- Has many `Review` (via ContentType)
- Has many `Booking` (via ContentType)

**Methods:**
```python
get_primary_booking_url()    # Returns best affiliate URL
has_booking_options()        # True if any booking links exist
get_all_booking_options()    # List of (name, url) tuples
```

---

### Room
Room types within an accommodation.

| Field | Type | Description |
|-------|------|-------------|
| `accommodation` | ForeignKey | Parent property |
| `room_type` | CharField | single, double, twin, suite, family, deluxe |
| `name` | CharField(100) | Room name |
| `description` | TextField | Room details |
| `max_occupancy` | IntegerField | Max guests |
| `beds` | CharField(100) | Bed configuration |
| `room_size` | IntegerField | Square meters |
| `base_price` | DecimalField | Room price |
| `total_rooms` | IntegerField | How many of this type |
| `available_rooms` | IntegerField | Currently available |
| `has_air_conditioning` | BooleanField | - |
| `has_wifi` | BooleanField | - |
| `has_tv` | BooleanField | - |
| `has_minibar` | BooleanField | - |
| `has_safe` | BooleanField | - |
| `has_balcony` | BooleanField | - |

---

### Amenity
Property amenities (pool, gym, etc.)

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(100) | Amenity name |
| `icon` | CharField(50) | Font Awesome class |
| `accommodations` | ManyToMany | Properties with this amenity |

---

## Tours

### Tour
Tour packages and experiences.

**Location:** `tours/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(200) | Tour name |
| `slug` | SlugField | URL identifier |
| `tour_type` | CharField | cultural, adventure, desert, cruise, diving, religious, luxury, budget |
| `description` | TextField | Full description |
| `highlights` | TextField | Key highlights |
| `duration_days` | IntegerField | Trip length (days) |
| `duration_nights` | IntegerField | Overnight stays |
| `departure_city` | CharField(100) | Start location |
| `destinations` | JSONField | List of destinations |
| `difficulty_level` | CharField | easy, moderate, challenging |
| `min_group_size` | IntegerField | Minimum travelers |
| `max_group_size` | IntegerField | Maximum travelers |
| `price_per_person` | DecimalField | Adult price |
| `child_discount` | DecimalField | Discount percentage |
| `includes` | JSONField | What's included |
| `excludes` | JSONField | What's not included |
| `languages` | JSONField | Available languages |
| `main_image` | ImageField | Primary photo |
| `image_url` | URLField | External image |
| `viator_url` | URLField | Viator affiliate |
| `getyourguide_url` | URLField | GYG affiliate |
| `travelpayouts_url` | URLField | TP affiliate |
| `is_featured` | BooleanField | Homepage display |
| `is_active` | BooleanField | Published |
| `average_rating` | DecimalField | From reviews |
| `total_reviews` | IntegerField | Review count |
| `booking_count` | IntegerField | Times booked |

**Methods:**
```python
get_primary_affiliate_url()   # Best affiliate link
has_affiliate_options()       # True if any links
get_all_affiliate_options()   # List of affiliate dicts
```

---

### TourItinerary
Day-by-day tour schedule.

| Field | Type | Description |
|-------|------|-------------|
| `tour` | ForeignKey | Parent tour |
| `day` | IntegerField | Day number |
| `title` | CharField(200) | Day title |
| `description` | TextField | Activities |
| `meals_included` | CharField(100) | B/L/D |
| `overnight_location` | CharField(100) | Where staying |

---

### TourBooking
Legacy tour booking model (see Booking for new system).

| Field | Type | Description |
|-------|------|-------------|
| `tour` | ForeignKey | Tour booked |
| `user` | ForeignKey | Customer |
| `booking_date` | DateTimeField | When booked |
| `tour_date` | DateField | Travel date |
| `number_of_adults` | IntegerField | Adult count |
| `number_of_children` | IntegerField | Child count |
| `total_price` | DecimalField | Total amount |
| `status` | CharField | pending, confirmed, cancelled, completed |
| `contact_name` | CharField(100) | Contact person |
| `contact_email` | EmailField | Email |
| `contact_phone` | CharField(20) | Phone |
| `special_requests` | TextField | Notes |

---

## Bookings

### Booking
Unified booking system for all item types.

**Location:** `bookings/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Customer |
| `content_type` | ForeignKey(ContentType) | Type of item |
| `object_id` | PositiveIntegerField | Item ID |
| `content_object` | GenericForeignKey | The booked item |
| `booking_type` | CharField | accommodation, tour, transportation |
| `booking_reference` | CharField(20) | Unique reference (EGY-XXXXXXXX) |
| `booking_date` | DateTimeField | When created |
| `check_in_date` | DateField | Start date |
| `check_out_date` | DateField | End date (accommodations) |
| `total_amount` | DecimalField | Total price |
| `paid_amount` | DecimalField | Amount paid |
| `status` | CharField | pending, confirmed, cancelled, completed |
| `payment_status` | CharField | unpaid, partial, paid, refunded |
| `contact_name` | CharField(100) | Contact person |
| `contact_email` | EmailField | Email |
| `contact_phone` | CharField(20) | Phone |
| `special_requests` | TextField | Notes |

**Methods:**
```python
confirm()     # Set status to confirmed
cancel()      # Set status to cancelled
complete()    # Set status to completed
```

---

### AccommodationBooking
Additional details for accommodation bookings.

| Field | Type | Description |
|-------|------|-------------|
| `booking` | OneToOneField(Booking) | Parent booking |
| `accommodation` | ForeignKey | Property |
| `room` | ForeignKey | Room type (optional) |
| `number_of_guests` | IntegerField | Guest count |
| `number_of_rooms` | IntegerField | Rooms booked |

---

## Reviews

### Review
User reviews for accommodations and tours.

**Location:** `reviews/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Reviewer |
| `content_type` | ForeignKey(ContentType) | Item type |
| `object_id` | PositiveIntegerField | Item ID |
| `content_object` | GenericForeignKey | Reviewed item |
| `title` | CharField(200) | Review title |
| `comment` | TextField | Review text |
| `rating` | IntegerField(1-5) | Overall rating |
| `cleanliness_rating` | IntegerField(1-5) | Optional |
| `location_rating` | IntegerField(1-5) | Optional |
| `value_rating` | IntegerField(1-5) | Optional |
| `service_rating` | IntegerField(1-5) | Optional |
| `is_verified_booking` | BooleanField | From actual booking |
| `status` | CharField | pending, approved, rejected |
| `moderated_by` | ForeignKey(User) | Admin who moderated |
| `moderated_at` | DateTimeField | When moderated |
| `helpful_count` | IntegerField | Helpful votes |
| `not_helpful_count` | IntegerField | Not helpful votes |

**Constraint:** One review per user per item (`unique_together`)

**Methods:**
```python
approve(moderator)           # Approve and update item rating
reject(moderator, notes)     # Reject with reason
update_object_rating()       # Recalculate item's average
```

---

### ReviewResponse
Property owner replies to reviews.

| Field | Type | Description |
|-------|------|-------------|
| `review` | OneToOneField(Review) | Parent review |
| `response_text` | TextField | Reply text |
| `responded_by` | ForeignKey(User) | Responder |

---

### ReviewHelpful
Tracks helpful/not helpful votes.

| Field | Type | Description |
|-------|------|-------------|
| `review` | ForeignKey(Review) | Review voted on |
| `user` | ForeignKey(User) | Voter |
| `is_helpful` | BooleanField | True=helpful, False=not |

**Constraint:** One vote per user per review (`unique_together`)

---

### ReviewReport
Reports for inappropriate reviews.

| Field | Type | Description |
|-------|------|-------------|
| `review` | ForeignKey(Review) | Reported review |
| `reported_by` | ForeignKey(User) | Reporter |
| `reason` | CharField | spam, offensive, fake, irrelevant, personal_info, other |
| `details` | TextField | Additional info |
| `is_reviewed` | BooleanField | Admin reviewed |
| `action_taken` | TextField | Resolution notes |

---

## Accounts

### UserProfile
Extended user information.

**Location:** `accounts/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField(User) | Django user |
| `phone` | CharField(20) | Phone number |
| `date_of_birth` | DateField | Birthday |
| `nationality` | CharField(100) | Country |
| `passport_number` | CharField(50) | For bookings |
| `profile_picture` | ImageField | Avatar |
| `bio` | TextField | About me |
| `preferences` | JSONField | Settings |
| `email_verified` | BooleanField | Email confirmed |
| `phone_verified` | BooleanField | Phone confirmed |
| `identity_verified` | BooleanField | ID verified |
| `phone_otp` | CharField(6) | Current OTP |
| `phone_otp_created` | DateTimeField | OTP timestamp |
| `two_factor_enabled` | BooleanField | 2FA active |
| `two_factor_method` | CharField | totp or sms |
| `backup_codes` | JSONField | 2FA backup codes |
| `last_login_ip` | IPAddressField | Security tracking |
| `trusted_devices` | JSONField | Known devices |

**Methods:**
```python
is_fully_verified         # All verifications complete
generate_otp()            # Create 6-digit code
verify_otp(code)          # Validate OTP
generate_backup_codes()   # Create 10 backup codes
verify_backup_code(code)  # Use backup code
get_masked_phone()        # Return ***-***-1234
```

**Auto-creation:** Profile created automatically when User is created (via signal).

---

## Dashboard

### SavedItem
User wishlist/saved items.

**Location:** `dashboard/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | Owner |
| `content_type` | ForeignKey(ContentType) | Item type |
| `object_id` | PositiveIntegerField | Item ID |
| `content_object` | GenericForeignKey | Saved item |
| `notes` | TextField | User notes |
| `created_at` | DateTimeField | When saved |

---

### UserActivity
Activity tracking for dashboard.

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey(User) | User |
| `activity_type` | CharField | view, booking, review, save |
| `content_type` | ForeignKey(ContentType) | Related item type |
| `object_id` | PositiveIntegerField | Related item ID |
| `description` | TextField | Activity description |
| `metadata` | JSONField | Additional data |
| `created_at` | DateTimeField | When occurred |

---

## Destinations

### City
Egyptian cities and destinations.

**Location:** `destinations/models.py`

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(100) | City name |
| `slug` | SlugField | URL identifier |
| `description` | TextField | About the city |
| `region` | CharField | nile_valley, coastal, desert, delta |
| `latitude` | DecimalField | GPS |
| `longitude` | DecimalField | GPS |
| `main_image` | ImageField | City photo |
| `is_featured` | BooleanField | Homepage display |
| `is_active` | BooleanField | Published |

---

## Entity Relationship Diagram

```
┌──────────────────┐     ┌──────────────────┐
│      User        │     │  UserProfile     │
│  (Django Auth)   │────▶│                  │
└──────────────────┘     └──────────────────┘
         │
         │ owns
         ▼
┌──────────────────┐     ┌──────────────────┐
│    Booking       │────▶│ Accommodation    │
│ (GenericFK)      │     │     or Tour      │
└──────────────────┘     └──────────────────┘
         │
         │ has
         ▼
┌──────────────────┐
│ AccommodationBook│
│  (extra details) │
└──────────────────┘

┌──────────────────┐     ┌──────────────────┐
│    Review        │────▶│ Accommodation    │
│ (GenericFK)      │     │     or Tour      │
└──────────────────┘     └──────────────────┘
         │
         ├──────────────────┐
         ▼                  ▼
┌──────────────────┐ ┌──────────────────┐
│ ReviewResponse   │ │  ReviewHelpful   │
└──────────────────┘ └──────────────────┘
```

---

## Database Indexes

All models have optimized indexes for common queries:

```python
# Accommodation
Index(['city'])
Index(['accommodation_type'])
Index(['is_active'])
Index(['is_featured'])
Index(['city', 'is_active', 'accommodation_type'])
Index(['average_rating'])

# Tour
Index(['tour_type'])
Index(['is_active'])
Index(['departure_city'])
Index(['average_rating'])

# Booking
Index(['user', 'status'])
Index(['content_type', 'object_id'])
Index(['booking_date'])

# Review
Index(['content_type', 'object_id', 'status'])
Index(['user', '-created_at'])
Index(['-rating', '-created_at'])
```

---

## Migrations

Apply migrations in order:

```bash
python manage.py makemigrations
python manage.py migrate
```

Check migration status:

```bash
python manage.py showmigrations
```
