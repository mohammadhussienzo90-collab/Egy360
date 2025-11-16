# Egy360 Deployment Guide

**Complete step-by-step guide for deploying Egy360 to production**

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Domain name purchased
- [ ] Hosting server (with root access)
- [ ] PostgreSQL database
- [ ] Redis server
- [ ] Email SMTP credentials
- [ ] SSL certificate
- [ ] Payment gateway account (Stripe)
- [ ] Backup strategy planned

---

## 🎯 Deployment Options

Choose one deployment method:

1. **Traditional VPS** (DigitalOcean, Linode, AWS EC2) - Recommended for full control
2. **Platform-as-a-Service** (Heroku, Railway, Render) - Easier but less control
3. **Containerized** (Docker + Kubernetes) - For advanced users

This guide covers **Traditional VPS** deployment (most flexible).

---

## 🔧 Server Requirements

### Minimum Specifications
- **OS:** Ubuntu 22.04 LTS (recommended)
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 20GB SSD
- **CPU:** 2 cores
- **Bandwidth:** Unlimited or high limit

### Recommended Providers
- **DigitalOcean** - $12/month (2GB RAM)
- **Linode** - $12/month (2GB RAM)
- **AWS Lightsail** - $10/month (2GB RAM)
- **Vultr** - $12/month (2GB RAM)

---

## 📦 Step 1: Server Setup

### 1.1 Connect to Your Server

```bash
ssh root@your-server-ip
```

### 1.2 Update System

```bash
apt update && apt upgrade -y
```

### 1.3 Create Non-Root User

```bash
adduser egy360
usermod -aG sudo egy360
su - egy360
```

### 1.4 Install Required Software

```bash
# Install Python and system dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Install Redis
sudo apt install -y redis-server

# Install Nginx (web server)
sudo apt install -y nginx

# Install other dependencies
sudo apt install -y git curl build-essential
```

---

## 🗄️ Step 2: Database Setup

### 2.1 Create PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE egy360_db;
CREATE USER egy360_user WITH PASSWORD 'your-strong-password';
ALTER ROLE egy360_user SET client_encoding TO 'utf8';
ALTER ROLE egy360_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE egy360_user SET timezone TO 'Africa/Cairo';
GRANT ALL PRIVILEGES ON DATABASE egy360_db TO egy360_user;
\q
```

### 2.2 Configure Redis

```bash
# Edit Redis config
sudo nano /etc/redis/redis.conf

# Find and modify:
supervised systemd
bind 127.0.0.1
maxmemory 256mb
maxmemory-policy allkeys-lru

# Save and restart Redis
sudo systemctl restart redis
sudo systemctl enable redis
```

---

## 📥 Step 3: Deploy Application

### 3.1 Clone Repository

```bash
cd /home/egy360
git clone <your-repository-url> Egy360
cd Egy360
```

### 3.2 Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn dj-database-url
```

### 3.4 Configure Environment Variables

```bash
nano .env
```

**Paste this and fill in YOUR actual values:**

```bash
# Security
SECRET_KEY=<generate-new-key-below>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://egy360_user:your-strong-password@localhost:5432/egy360_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Egy360 <noreply@yourdomain.com>

# CORS & CSRF
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis
REDIS_URL=redis://127.0.0.1:6379/0

# Payment
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# API Keys
GOOGLE_MAPS_API_KEY=your-google-maps-key

# SSL
SECURE_SSL_REDIRECT=True
```

**Generate SECRET_KEY:**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and paste it as your SECRET_KEY value.

### 3.5 Run Migrations

```bash
# Use production settings
export DJANGO_SETTINGS_MODULE=Egy360.settings_production

# Run migrations
python manage.py migrate
```

### 3.6 Create Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: your-email@domain.com
- Password: (strong password)

### 3.7 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3.8 Create Required Directories

```bash
mkdir -p logs media
chmod 755 logs media
```

---

## 🚀 Step 4: Configure Gunicorn

### 4.1 Test Gunicorn

```bash
gunicorn Egy360.wsgi:application --bind 0.0.0.0:8000
```

Visit: `http://your-server-ip:8000`

If it works, press Ctrl+C.

### 4.2 Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/egy360.service
```

**Paste this:**

```ini
[Unit]
Description=Egy360 Gunicorn Daemon
After=network.target

[Service]
User=egy360
Group=www-data
WorkingDirectory=/home/egy360/Egy360
Environment="PATH=/home/egy360/Egy360/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=Egy360.settings_production"
EnvironmentFile=/home/egy360/Egy360/.env
ExecStart=/home/egy360/Egy360/venv/bin/gunicorn \
          --workers 3 \
          --timeout 120 \
          --bind unix:/home/egy360/Egy360/gunicorn.sock \
          Egy360.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.3 Start Gunicorn

```bash
sudo systemctl start egy360
sudo systemctl enable egy360
sudo systemctl status egy360
```

---

## 🌐 Step 5: Configure Nginx

### 5.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/egy360
```

**Paste this:**

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /home/egy360/Egy360/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/egy360/Egy360/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/egy360/Egy360/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 5.2 Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/egy360 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Step 6: SSL Certificate (HTTPS)

### 6.1 Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 6.2 Get SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow prompts:
- Enter email
- Agree to terms
- Choose redirect (option 2)

### 6.3 Auto-Renewal

```bash
sudo systemctl status certbot.timer
```

Certbot automatically renews certificates.

---

## 📊 Step 7: Configure Celery (Background Tasks)

### 7.1 Create Celery Worker Service

```bash
sudo nano /etc/systemd/system/celery.service
```

**Paste this:**

```ini
[Unit]
Description=Egy360 Celery Worker
After=network.target

[Service]
User=egy360
Group=www-data
WorkingDirectory=/home/egy360/Egy360
Environment="PATH=/home/egy360/Egy360/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=Egy360.settings_production"
EnvironmentFile=/home/egy360/Egy360/.env
ExecStart=/home/egy360/Egy360/venv/bin/celery -A Egy360 worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

### 7.2 Create Celery Beat Service (Scheduled Tasks)

```bash
sudo nano /etc/systemd/system/celerybeat.service
```

**Paste this:**

```ini
[Unit]
Description=Egy360 Celery Beat
After=network.target

[Service]
User=egy360
Group=www-data
WorkingDirectory=/home/egy360/Egy360
Environment="PATH=/home/egy360/Egy360/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=Egy360.settings_production"
EnvironmentFile=/home/egy360/Egy360/.env
ExecStart=/home/egy360/Egy360/venv/bin/celery -A Egy360 beat --loglevel=info

[Install]
WantedBy=multi-user.target
```

### 7.3 Start Celery Services

```bash
sudo systemctl start celery celerybeat
sudo systemctl enable celery celerybeat
sudo systemctl status celery celerybeat
```

---

## 🔍 Step 8: Testing

### 8.1 Test Website

1. Visit: `https://yourdomain.com`
2. Check homepage loads
3. Test navigation
4. Check static files load (CSS, images)

### 8.2 Test Admin

1. Visit: `https://yourdomain.com/admin/`
2. Log in with superuser credentials
3. Check all sections

### 8.3 Test API

```bash
curl https://yourdomain.com/api/destinations/
```

Should return JSON data.

### 8.4 Test Email

In Django shell:

```bash
python manage.py shell

from django.core.mail import send_mail
send_mail('Test', 'Test email', 'from@domain.com', ['to@domain.com'])
```

Check if email arrives.

---

## 📈 Step 9: Monitoring & Logging

### 9.1 View Application Logs

```bash
# Gunicorn logs
sudo journalctl -u egy360 -f

# Celery logs
sudo journalctl -u celery -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Django logs
tail -f /home/egy360/Egy360/logs/django.log
```

### 9.2 Set Up Log Rotation

```bash
sudo nano /etc/logrotate.d/egy360
```

**Paste this:**

```
/home/egy360/Egy360/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 egy360 egy360
    sharedscripts
}
```

---

## 🔄 Step 10: Updates & Maintenance

### Deploying Updates

```bash
cd /home/egy360/Egy360
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart egy360 celery celerybeat
```

### Database Backup

```bash
# Backup script
sudo nano /home/egy360/backup.sh
```

**Paste this:**

```bash
#!/bin/bash
BACKUP_DIR="/home/egy360/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U egy360_user egy360_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/egy360/Egy360/media

# Keep only last 30 backups
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

**Make executable and schedule:**

```bash
chmod +x /home/egy360/backup.sh
crontab -e

# Add this line (backup daily at 2 AM):
0 2 * * * /home/egy360/backup.sh
```

---

## 🆘 Troubleshooting

### Site Not Loading

```bash
# Check services
sudo systemctl status egy360 nginx redis

# Restart all
sudo systemctl restart egy360 nginx redis
```

### 502 Bad Gateway

```bash
# Check Gunicorn socket
ls -l /home/egy360/Egy360/gunicorn.sock

# Check Gunicorn logs
sudo journalctl -u egy360 -n 50
```

### Static Files Not Loading

```bash
# Re-collect static files
python manage.py collectstatic --noinput

# Check Nginx permissions
sudo chown -R www-data:www-data /home/egy360/Egy360/staticfiles
```

### Database Connection Error

```bash
# Test PostgreSQL connection
psql -U egy360_user -d egy360_db -h localhost

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Restart application
sudo systemctl restart egy360

# View logs
sudo journalctl -u egy360 -f

# Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### File Locations

- **Application:** `/home/egy360/Egy360`
- **Logs:** `/home/egy360/Egy360/logs`
- **Static Files:** `/home/egy360/Egy360/staticfiles`
- **Media Files:** `/home/egy360/Egy360/media`
- **Nginx Config:** `/etc/nginx/sites-available/egy360`
- **Environment:** `/home/egy360/Egy360/.env`

---

## ✅ Post-Deployment Checklist

- [ ] Website loads over HTTPS
- [ ] Admin panel accessible
- [ ] API endpoints working
- [ ] Email sending works
- [ ] Static files loading
- [ ] Media uploads work
- [ ] Database backups scheduled
- [ ] SSL certificate auto-renewal working
- [ ] Monitoring set up
- [ ] Error tracking configured
- [ ] Payment gateway tested
- [ ] Load testing completed

---

**Congratulations!** 🎉 Your Egy360 platform is now live!

**Next Steps:**
1. Populate with real data (accommodations, tours)
2. Test all booking flows
3. Set up payment gateway
4. Monitor performance
5. Marketing and user acquisition

---

**Last Updated:** November 15, 2025
**Version:** 1.0.0
