# Egy360 - Egyptian Tourism Platform

**Version:** 1.0.0
**Status:** Production Ready (pending security configuration)
**Last Updated:** 2025-11-15

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Documentation Index](#documentation-index)
4. [System Requirements](#system-requirements)
5. [Support](#support)

---

## 🎯 Project Overview

**Egy360** is a comprehensive tourism platform for Egypt that connects travelers with:
- 🏨 **Accommodations** (hotels, resorts, hostels, villas, desert camps)
- 🗺️ **Tours** (cultural, adventure, desert safari, Nile cruises, diving)
- 🚗 **Transportation** (airport transfers, private cars, guided tours)
- ⭐ **Reviews** (verified reviews from real travelers)
- 💳 **Payments** (secure payment processing with refund support)
- 📝 **Blog** (travel guides and destination information)

### Key Features

✅ **Multi-Service Booking System**
✅ **Verified Review System** with photo uploads
✅ **Secure Payment Processing** (Stripe integration ready)
✅ **Admin Dashboard** for managing bookings and services
✅ **RESTful API** for mobile apps and integrations
✅ **Responsive Design** for all devices
✅ **Multi-language Support** (ready to expand)

### Technology Stack

- **Backend:** Django 5.0.2 + Django REST Framework
- **Database:** PostgreSQL (production) / SQLite (development)
- **Caching:** Redis
- **Task Queue:** Celery
- **Server:** Gunicorn + WhiteNoise
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

---

## 🚀 Quick Start

### For Developers

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Egy360

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your actual values

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

Visit: http://localhost:8000

### For Admins

See: [Admin User Manual](ADMIN_MANUAL.md)

### For Deployment

See: [Deployment Guide](DEPLOYMENT.md)

---

## 📚 Documentation Index

### For Everyone
- **[Admin User Manual](ADMIN_MANUAL.md)** - Step-by-step guide for managing the platform

### For Developers
- **[Technical Documentation](TECHNICAL.md)** - Complete technical reference
- **[API Documentation](API.md)** - REST API endpoints and usage
- **[Database Schema](DATABASE.md)** - Models and relationships
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment steps

### For Business
- **[Features List](FEATURES.md)** - Complete feature breakdown
- **[Quick Wins](QUICK_WINS.md)** - Easy wins to build momentum
- **[Scalability Plan](SCALABILITY.md)** - Growth and scaling strategies

### Reference
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Security Guide](SECURITY.md)** - Security best practices
- **[Testing Guide](TESTING.md)** - How to test the application

---

## 💻 System Requirements

### Minimum Requirements
- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- 2GB RAM
- 10GB Storage

### Recommended for Production
- Python 3.11
- PostgreSQL 14+
- Redis 7+
- 4GB RAM
- 20GB+ Storage
- SSL Certificate
- Domain name

---

## 🔧 Development Tools

- **Django Debug Toolbar** - SQL query analysis
- **pytest** - Testing framework
- **Celery** - Background tasks
- **Django Extensions** - Management command extensions

---

## 📱 API Access

The platform provides a full REST API:

**Base URL:** `http://yourdomain.com/api/`

**Available Endpoints:**
- `/api/accommodations/` - Accommodation search and booking
- `/api/tours/` - Tour packages and bookings
- `/api/destinations/` - Cities and attractions
- `/api/reviews/` - Review management
- `/api/payments/` - Payment processing
- `/api/transportation/` - Transportation services

See [API Documentation](API.md) for complete reference.

---

## 🆘 Support

### Getting Help

1. **Check Documentation** - Most questions are answered in the docs
2. **Troubleshooting Guide** - See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. **Admin Manual** - See [ADMIN_MANUAL.md](ADMIN_MANUAL.md)

### Reporting Issues

- **Technical Issues:** Check logs in `logs/django.log`
- **Security Issues:** Critical priority
- **Feature Requests:** Document in project planning

---

## 📈 Project Status

### ✅ Completed
- Core booking system
- Review and rating system
- Payment processing framework
- Admin dashboard
- RESTful API
- User authentication
- Email notifications (configured)

### ⚠️ Before Production
- [ ] Configure production environment variables
- [ ] Set up PostgreSQL database
- [ ] Configure email SMTP
- [ ] Set up payment gateway (Stripe)
- [ ] Configure SSL certificate
- [ ] Run security audit
- [ ] Load testing
- [ ] Set up monitoring

### 🔜 Future Enhancements
- Mobile app (iOS/Android)
- Multi-language support (Arabic, French, German)
- AI-powered tour recommendations
- Real-time chat support
- Social media integration
- Loyalty program

---

## 📄 License

Copyright © 2025 Egy360. All rights reserved.

---

## 👥 Team

- **Development:** AI-assisted development
- **Platform Management:** Solo founder
- **Strategy:** Agile development approach

---

**Last Updated:** November 15, 2025
**Document Version:** 1.0.0
