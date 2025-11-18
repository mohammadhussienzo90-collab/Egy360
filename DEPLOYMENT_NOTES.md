# 🚀 360egy.com Deployment Notes

**Domain:** 360egy.com
**Purchased:** November 17, 2025
**Platform:** Railway.app
**Database:** PostgreSQL (Railway managed)

---

## 🔑 Production SECRET_KEY

**IMPORTANT:** Add this to Railway environment variables:

```
SECRET_KEY=+&c#erq(dyb*0=qw1bw7-5vttbp4c^imc3h^ll0zqcjr3vtf^n
```

---

## 🌐 Domain Configuration

**Primary Domain:** 360egy.com
**With WWW:** www.360egy.com
**Railway URL:** 360egy.up.railway.app

---

## 📋 Environment Variables for Railway

Copy these to Railway dashboard:

```
SECRET_KEY=+&c#erq(dyb*0=qw1bw7-5vttbp4c^imc3h^ll0zqcjr3vtf^n
DEBUG=False
ALLOWED_HOSTS=360egy.com,www.360egy.com,360egy.up.railway.app
DJANGO_SETTINGS_MODULE=Egy360.settings_production
```

Railway will auto-provide:
- `DATABASE_URL` (PostgreSQL)
- `PORT`

---

## 🔧 DNS Settings (Namecheap)

**After Railway deployment, add these DNS records in Namecheap:**

### A Record:
- **Type:** A
- **Host:** @
- **Value:** [Railway will provide IP]
- **TTL:** Automatic

### CNAME Record:
- **Type:** CNAME
- **Host:** www
- **Value:** 360egy.up.railway.app
- **TTL:** Automatic

---

## ✅ Post-Deployment Checklist

```
[ ] GitHub repository created
[ ] Code pushed to GitHub
[ ] Railway project created
[ ] Environment variables configured
[ ] Database migrated
[ ] Static files collected
[ ] Domain connected
[ ] SSL enabled (automatic)
[ ] Admin password changed from default
[ ] Test bookings working
[ ] Email notifications working
```

---

## 📊 Initial Content

**Accommodations:** 56 hotels across 6 cities
**Tours:** 20 packages
**Attractions:** 33 locations
**Blog Posts:** 6 articles
**Cities:** Cairo, Luxor, Aswan, Alexandria, Sharm El Sheikh, Hurghada

---

## 🔒 Admin Credentials

**URL:** https://360egy.com/admin/
**Username:** admin
**Password:** admin123 (CHANGE THIS IMMEDIATELY!)

---

**Deployment Date:** November 17, 2025
**Status:** Ready for deployment
