# Egy360 - Egypt Travel Platform

A comprehensive travel booking platform for Egypt, featuring accommodations, tours, transportation, and destination guides.

**Live Site:** [360egy.com](https://360egy.com)

## Overview

Egy360 is a Django-based travel platform that helps travelers discover and book:
- Hotels, resorts, and Nile cruises
- Guided tours and experiences
- Airport transfers and transportation
- Destination guides and travel blog

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 5.1 |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Frontend | Bootstrap 5, vanilla JavaScript |
| Authentication | django-allauth (Google, Facebook, Apple) |
| 2FA | django-otp (TOTP, SMS) |
| API | Django REST Framework |
| Hosting | Railway |
| Static Files | WhiteNoise |

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/egy360.git
cd egy360

# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the site.

## Project Structure

```
Egy360/
├── accommodations/     # Hotels, resorts, cruises
├── accounts/           # User authentication & profiles
├── api/                # REST API endpoints
├── blog/               # Travel blog
├── bookings/           # Booking management
├── core/               # Shared utilities (email, etc.)
├── dashboard/          # User dashboard
├── destinations/       # City & destination guides
├── Egy360/             # Project settings
├── home/               # Homepage & landing pages
├── payments/           # Payment processing
├── reviews/            # Review system
├── tours/              # Tours & experiences
├── transportation/     # Airport transfers
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── docs/               # Documentation
```

## Key Features

### For Travelers
- **Search & Filter**: Find accommodations by city, type, price, amenities
- **Tour Booking**: Browse and book guided tours
- **User Dashboard**: Manage bookings, saved items, reviews
- **Reviews**: Read and write reviews with ratings
- **Wishlist**: Save favorite accommodations and tours

### For Administrators
- **Django Admin**: Full content management
- **Booking Management**: View and manage all bookings
- **Review Moderation**: Approve/reject user reviews
- **Analytics**: Track bookings and revenue

### Monetization
- Affiliate links (Booking.com, Viator, GetYourGuide)
- Direct booking commissions
- Partner integrations (Travelpayouts)

## Environment Variables

Create a `.env` file with:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

# Social Auth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=

# SMS (optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Project structure and design
- [Models Reference](docs/MODELS.md) - Database schema
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Features Guide](docs/FEATURES.md) - User features walkthrough

## URL Structure

| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/accommodations/` | Hotel listings |
| `/tours/` | Tour listings |
| `/destinations/` | Destination guides |
| `/blog/` | Travel blog |
| `/accounts/login/` | User login |
| `/accounts/register/` | User registration |
| `/dashboard/` | User dashboard |
| `/admin/` | Django admin |

## API Endpoints

The REST API is available at `/api/`:

```
GET  /api/                    # API root
GET  /accommodations/         # List accommodations
GET  /tours/                  # List tours
GET  /destinations/           # List destinations
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
Follow PEP 8 for Python code.

### Making Changes
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Deployment

The project is configured for Railway deployment:

```bash
# Build command
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start command
gunicorn Egy360.wsgi:application
```

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For support, email support@360egy.com or open an issue in the repository.
