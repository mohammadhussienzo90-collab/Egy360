# Egy360 Deployment Credentials & Information

**KEEP THIS FILE SAFE AND PRIVATE!**
**DO NOT commit this file to GitHub!**

---

## 🔐 SECRET_KEY (For Production)

```
SECRET_KEY=+2=31w#0=!xo0jxh@go8i@@v!6n!kghf0m%d5yh^z1oal4#)2e
```

**⚠️ Use this in Railway environment variables!**

---

## 🌐 Domain Name

**Domain purchased:** ____________________________

**Registrar:** Namecheap / Google Domains / Other: ______________

**Login email:** ____________________________

**Purchase date:** ____________________________

**Renewal date:** ____________________________

**Cost:** ____________________________

---

## 🐙 GitHub

**Username:** ____________________________

**Email:** ____________________________

**Repository:** https://github.com/____________/egy360

**Personal Access Token:**
```
____________________________________________________
```

**Token created:** ____________________________

**Token expires:** ____________________________

---

## 🚂 Railway

**Email:** ____________________________

**Project name:** egy360

**Project URL:** https://railway.app/project/____________

**PostgreSQL database:** ✅ Included

**Generated domain:** https://egy360-production.up.railway.app

---

## ⚙️ Environment Variables (Railway)

Copy these to Railway Variables tab:

```bash
# Core Settings
SECRET_KEY=+2=31w#0=!xo0jxh@go8i@@v!6n!kghf0m%d5yh^z1oal4#)2e
DEBUG=False
DJANGO_SETTINGS_MODULE=Egy360.settings_production

# Domain Settings (UPDATE WITH YOUR DOMAIN!)
ALLOWED_HOSTS=.railway.app,yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (Automatic from Railway PostgreSQL)
DATABASE_URL=postgresql://... (automatically set by Railway)

# Email (Optional - Configure later)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Egy360 <noreply@yourdomain.com>

# Redis (Optional - Add later if needed)
REDIS_URL=redis://...

# Payment Gateway (Configure later)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Security
SECURE_SSL_REDIRECT=True
```

---

## 📧 Email Configuration (Gmail)

**How to get App Password:**

1. Go to Google Account: https://myaccount.google.com/
2. Security → 2-Step Verification (must be enabled first)
3. App passwords
4. Select app: Mail
5. Select device: Other (Custom name) → "Egy360"
6. Generate
7. Copy 16-character password
8. Use this in `EMAIL_HOST_PASSWORD`

**Gmail SMTP Settings:**
- Host: smtp.gmail.com
- Port: 587
- TLS: True
- Limit: 500 emails/day (free)

---

## 💳 Stripe Payment Gateway (Setup Later)

**Test Mode:**
1. Create account: https://stripe.com
2. Dashboard → Developers → API keys
3. Copy:
   - Publishable key: `pk_test_...`
   - Secret key: `sk_test_...`
4. Add to Railway variables

**Live Mode:**
- Complete business verification
- Switch to live keys
- Update Railway variables

---

## 🌍 DNS Configuration (Namecheap)

**Once you have Railway domain:**

1. Login to Namecheap
2. Domain List → Manage
3. Advanced DNS tab
4. Add records:

**Record 1:**
- Type: CNAME
- Host: www
- Value: egy360-production.up.railway.app
- TTL: Automatic

**Record 2:**
- Type: CNAME
- Host: @
- Value: egy360-production.up.railway.app
- TTL: Automatic

**DNS Propagation:** 5-30 minutes

**Check propagation:** https://dnschecker.org

---

## 🔗 Important URLs

**Website (Production):**
- https://www.yourdomain.com
- https://yourdomain.com

**Admin Panel:**
- https://www.yourdomain.com/admin/

**API:**
- https://www.yourdomain.com/api/

**Railway Dashboard:**
- https://railway.app/project/your-project-id

**GitHub Repository:**
- https://github.com/your-username/egy360

---

## 👤 Admin Account (Production)

**Create after deployment:**

```bash
railway run python manage.py createsuperuser
```

**Username:** ____________________________

**Email:** ____________________________

**Password:** ____________________________ (STRONG PASSWORD!)

---

## 📊 Costs Summary

| Service | Cost | Frequency |
|---------|------|-----------|
| Domain | ~370 EGP | Annual |
| Railway | ~620 EGP | Monthly |
| **Total Month 1** | **990 EGP** | |
| **Total Year 1** | **~7,810 EGP** | |

---

## 🚨 Security Checklist

- [ ] `.env` file is in `.gitignore` ✅
- [ ] SECRET_KEY is unique and not the default
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS/SSL certificate active
- [ ] Strong admin password set
- [ ] GitHub repository is Private
- [ ] Personal Access Token saved securely
- [ ] Database has strong password (Railway auto-generates)

---

## 📝 Quick Commands Reference

### Local Development
```bash
# Run local server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Git Commands
```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest code
git pull
```

### Railway CLI (Optional - Install later)
```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Run command on production
railway run python manage.py migrate

# View logs
railway logs

# Open dashboard
railway open
```

---

## 🆘 Emergency Contacts & Support

**Railway Support:**
- Discord: https://discord.gg/railway
- Email: team@railway.app
- Docs: https://docs.railway.app

**GitHub Support:**
- https://support.github.com

**Namecheap Support:**
- Live Chat (24/7)
- https://www.namecheap.com/support/

**Stripe Support:**
- https://support.stripe.com
- Email: support@stripe.com

---

## 📅 Important Dates

**Domain Registration:** ____________________________

**Domain Renewal:** ____________________________ (Mark in calendar!)

**Railway Started:** ____________________________

**First Deployment:** ____________________________

**GitHub Token Expires:** ____________________________

**SSL Certificate:** Auto-renews (Railway handles it)

---

## 🎯 Post-Deployment Checklist

### Day 1 (After Deployment)
- [ ] Website loads successfully
- [ ] Admin panel accessible
- [ ] Create admin account
- [ ] Add 5 sample accommodations
- [ ] Add 3 sample tours
- [ ] Test search functionality
- [ ] Test booking flow
- [ ] Verify email notifications work

### Week 1
- [ ] Add 20+ real accommodations
- [ ] Add 10+ real tours
- [ ] Write 3 blog posts
- [ ] Set up Google Analytics
- [ ] Test on multiple devices
- [ ] Get feedback from 5 friends

### Month 1
- [ ] 50+ accommodations listed
- [ ] 20+ tours available
- [ ] Professional photography complete
- [ ] Legal registration done
- [ ] Payment gateway (test mode) configured
- [ ] Soft launch to limited audience

---

## 💡 Pro Tips

1. **Backup regularly:** Railway has automatic backups, but export database weekly
2. **Monitor costs:** Check Railway usage dashboard weekly
3. **Test before pushing:** Always test changes locally first
4. **Use branches:** Create git branches for big features
5. **Document changes:** Write clear commit messages
6. **Check logs:** Review Railway logs if anything breaks
7. **Update regularly:** Keep dependencies updated (security)

---

**Date Created:** November 16, 2025

**Last Updated:** ____________________________

**Notes:**
________________________________
________________________________
________________________________

---

**⚠️ KEEP THIS FILE SAFE - Contains sensitive information!**
