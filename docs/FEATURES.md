# Egy360 Features Guide

A complete guide to all user-facing features on the Egy360 platform.

## Table of Contents
1. [Homepage](#homepage)
2. [Accommodations](#accommodations)
3. [Tours](#tours)
4. [User Accounts](#user-accounts)
5. [Dashboard](#dashboard)
6. [Booking System](#booking-system)
7. [Reviews](#reviews)
8. [Destinations](#destinations)
9. [Blog](#blog)

---

## Homepage

**URL:** `/`

### Features
- **Hero Section**: Eye-catching banner with search functionality
- **Featured Accommodations**: Top-rated hotels and resorts
- **Featured Tours**: Popular tour packages
- **Destination Highlights**: Quick links to cities
- **Why Choose Us**: Trust indicators and benefits
- **Newsletter Signup**: Email subscription for deals

### How It Works
1. Users land on the homepage
2. Quick search allows filtering by destination, dates, guests
3. Featured items showcase best offerings
4. Call-to-action buttons lead to listings

---

## Accommodations

### Listing Page
**URL:** `/accommodations/`

#### Search Filters
| Filter | Description |
|--------|-------------|
| Search | Text search by name |
| City | Filter by destination |
| Type | Hotel, resort, cruise, etc. |
| Star Rating | 1-5 stars |
| Price Range | Min/max per night |
| Amenities | Pool, WiFi, spa, etc. |

#### Sorting Options
- Featured (default)
- Price: Low to High
- Price: High to Low
- Rating: Highest First
- Newest First

#### Results Display
- Grid view with cards
- Image, name, location, price, rating
- Quick "View Details" button
- Pagination (12 per page)

### Detail Page
**URL:** `/accommodations/<slug>/`

#### Sections
1. **Image Gallery**: Main image + thumbnails
2. **Property Info**: Name, type, star rating, location
3. **Description**: Full property description
4. **Amenities**: Icons with amenity list
5. **Room Types**: Available rooms with prices
6. **Location**: Map with address
7. **Reviews**: Guest reviews and ratings
8. **Booking Widget**: Select dates, book now

#### Booking Options
- **Affiliate Links**: Booking.com, Agoda, Hotels.com
- **Direct Booking**: On-site checkout flow

---

## Tours

### Listing Page
**URL:** `/tours/`

#### Search Filters
| Filter | Description |
|--------|-------------|
| Search | Text search by name |
| Tour Type | Cultural, adventure, desert, etc. |
| Difficulty | Easy, moderate, challenging |
| Duration | Min/max days |
| Price Range | Per person |
| Departure City | Starting location |

#### Sorting Options
- Featured (default)
- Price: Low to High
- Price: High to Low
- Rating: Highest
- Duration: Shortest/Longest
- Most Popular

### Detail Page
**URL:** `/tours/<slug>/`

#### Sections
1. **Hero Image**: Tour main photo
2. **Overview**: Name, type, duration, difficulty
3. **Highlights**: Key attractions
4. **Itinerary**: Day-by-day schedule
5. **What's Included**: List of inclusions
6. **What's Excluded**: List of exclusions
7. **Meeting Point**: Departure location
8. **Reviews**: Traveler reviews
9. **Booking Widget**: Select date, travelers

#### Affiliate Integration
- Viator links
- GetYourGuide links
- Travelpayouts integration

---

## User Accounts

### Registration
**URL:** `/accounts/register/`

#### Methods
1. **Email Registration**
   - First name, last name
   - Email address
   - Password (with strength indicator)
   - Terms & conditions checkbox

2. **Social Registration**
   - Google Sign-In
   - Facebook Login
   - Apple Sign-In

### Login
**URL:** `/accounts/login/`

#### Methods
1. **Email/Password Login**
2. **Social Login** (Google, Facebook, Apple)
3. **Phone + OTP Login**
   - Enter phone number
   - Receive SMS code
   - Verify code

### Two-Factor Authentication
**URL:** `/accounts/2fa/setup/`

#### Options
1. **Authenticator App (TOTP)**
   - Scan QR code with Google Authenticator
   - Enter 6-digit code
   - Save backup codes

2. **SMS Authentication**
   - Receive codes via SMS
   - Enter code on login

### Password Management
- **Forgot Password**: `/accounts/password/reset/`
- **Change Password**: `/accounts/password/change/`

---

## Dashboard

### Overview
**URL:** `/dashboard/`

#### Stats Cards
- Total Bookings
- Reviews Written
- Saved Items
- Account status

#### Sections
- Quick Actions (new booking, write review)
- Recent Bookings (last 5)
- Travel Tips

### Bookings
**URL:** `/dashboard/bookings/`

#### Features
- View all bookings
- Filter by status (pending, confirmed, completed, cancelled)
- Booking details (reference, dates, amount)
- Cancel booking option
- View booking confirmation

#### Booking Statuses
| Status | Description |
|--------|-------------|
| Pending | Awaiting confirmation |
| Confirmed | Booking confirmed |
| Completed | Trip completed |
| Cancelled | Booking cancelled |

### Reviews
**URL:** `/dashboard/reviews/`

#### Features
- View all your reviews
- Review status (pending, approved, rejected)
- Review statistics
- Edit pending reviews

### Saved Items (Wishlist)
**URL:** `/dashboard/saved/`

#### Features
- View saved accommodations and tours
- Filter by type
- Add personal notes
- Remove from saved
- Quick book button

### Account Settings
**URL:** `/dashboard/settings/`

#### Tabs
1. **Profile**
   - Name, email, phone
   - Profile picture
   - Nationality, passport

2. **Security**
   - Change password
   - Enable 2FA
   - View login history

3. **Preferences**
   - Language
   - Currency
   - Newsletter opt-in

4. **Notifications**
   - Email notifications
   - SMS alerts
   - Marketing preferences

---

## Booking System

### Checkout Flow

#### Step 1: Select Item
- Choose accommodation or tour
- Select dates/travelers
- Click "Book Now"

#### Step 2: Checkout Page
**URL:** `/bookings/checkout/<type>/<id>/`

**Accommodation Checkout:**
- Check-in/check-out dates
- Number of guests
- Number of rooms
- Contact information
- Special requests

**Tour Checkout:**
- Tour date
- Number of participants
- Contact information
- Special requests

#### Step 3: Confirmation
**URL:** `/bookings/confirmation/<id>/`

- Booking reference number
- Booking details summary
- Email confirmation sent
- Link to view booking

### Email Notifications
- Booking confirmation email (HTML template)
- Status update emails
- Reminder emails (before trip)

---

## Reviews

### Writing a Review
**URL:** `/reviews/submit/<type>/<id>/`

#### Requirements
- Must be logged in
- One review per item per user
- Can only review after booking (verified reviews)

#### Review Form
1. **Overall Rating**: 1-5 stars
2. **Detailed Ratings**:
   - Cleanliness
   - Location
   - Value
   - Service
3. **Review Title**: Summary (required)
4. **Review Text**: Detailed experience (required)

### Review Display

#### On Item Pages
- Rating summary (average, total count)
- Rating distribution (bar chart)
- Category averages
- Individual reviews with:
  - User avatar and name
  - Date posted
  - Star rating
  - Review text
  - "Verified Stay" badge (if applicable)
  - Helpful votes

### Review Interactions
- **Vote Helpful**: Mark review as helpful
- **Report**: Flag inappropriate reviews
- **Property Response**: Owner can reply

### Review Moderation
Reviews go through moderation:
1. User submits review (status: pending)
2. Admin reviews content
3. Admin approves or rejects
4. Approved reviews appear on site

---

## Destinations

### City Pages
**URL:** `/destinations/<slug>/`

#### Content
- City overview
- Popular attractions
- Best accommodations in city
- Tours starting from city
- Travel tips
- Map with key locations

### Features
- Filter accommodations by city
- Filter tours by departure city
- Related blog posts

---

## Blog

### Blog Listing
**URL:** `/blog/`

#### Features
- Article grid
- Category filtering
- Search articles
- Featured posts

### Article Page
**URL:** `/blog/<slug>/`

#### Sections
- Article title and metadata
- Featured image
- Article content
- Author info
- Related articles
- Social sharing buttons
- Comments (if enabled)

### Categories
- Travel Tips
- Destination Guides
- Culture & History
- Food & Drink
- Adventure
- Budget Travel

---

## Mobile Responsiveness

All features are mobile-friendly:

| Screen Size | Behavior |
|-------------|----------|
| Desktop (>1200px) | Full layout, sidebar filters |
| Tablet (768-1199px) | Adjusted grid, collapsible filters |
| Mobile (<768px) | Single column, bottom navigation |

---

## Search Functionality

### Global Search
Available from navbar:
- Search accommodations
- Search tours
- Search destinations
- Search blog posts

### Filter Persistence
- Filters saved in URL params
- Shareable filter URLs
- Back button preserves filters

---

## Performance Features

- **Lazy Loading**: Images load as you scroll
- **Pagination**: Results split into pages
- **Caching**: Frequently accessed data cached
- **Optimized Images**: Responsive image sizes

---

## Accessibility

- **Keyboard Navigation**: Tab through elements
- **Screen Reader Support**: ARIA labels
- **Color Contrast**: WCAG compliant
- **Alt Text**: All images have descriptions

---

## Future Features

Planned enhancements:
- [ ] Real-time availability checking
- [ ] Price comparison widget
- [ ] Itinerary builder
- [ ] Trip sharing
- [ ] Loyalty program
- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)
