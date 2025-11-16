# Deploy Egy360 TODAY - Step-by-Step Guide

**Goal: Get your site live with HTTPS in the next 2-3 hours!**

---

## ✅ **CHECKLIST - Follow in Order**

### Part 1: Domain Name (15 minutes)
- [ ] Choose domain name
- [ ] Check availability
- [ ] Purchase domain (~370 EGP)

### Part 2: Git Setup (10 minutes)
- [ ] Install Git
- [ ] Configure Git
- [ ] Initialize repository

### Part 3: GitHub (10 minutes)
- [ ] Create GitHub account
- [ ] Create repository
- [ ] Push code to GitHub

### Part 4: Railway Deployment (20 minutes)
- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL database
- [ ] Configure environment variables

### Part 5: Domain Connection (15 minutes)
- [ ] Connect domain to Railway
- [ ] Wait for DNS propagation
- [ ] SSL certificate (automatic)

### Part 6: Testing (30 minutes)
- [ ] Test website works
- [ ] Create admin account
- [ ] Add sample data
- [ ] Test booking flow

**Total Time: 1.5 - 2 hours**

---

## 🌐 STEP 1: Choose & Buy Domain Name

### Check Availability

Go to: **https://www.namecheap.com** (Recommended - Cheapest)

**Try these names in order:**
1. `egytravel360.com`
2. `discoveregypt360.com`
3. `egyexplore.com`
4. `egyptholidays360.com`
5. `travelegy360.com`
6. `egytrips.com`
7. `egypttours360.com`

**How to check:**
1. Go to namecheap.com
2. Type domain in search box
3. Click "Search"
4. If available → Shows price
5. If taken → Shows "Not available"

### Purchase Domain (10 minutes)

**Once you find available domain:**

1. Click "Add to Cart"
2. **Important Options:**
   - Domain Privacy: ✅ YES (Free on Namecheap)
   - Auto-renew: ✅ YES (so you don't lose it)
   - PremiumDNS: ❌ NO (not needed)

3. Checkout
   - Use your email
   - Create account
   - Pay (~370 EGP / $12)

**Payment methods:**
- Credit/Debit card
- PayPal
- Some accept Egyptian cards

**⚠️ IMPORTANT: Don't configure DNS yet! We'll do that later.**

**✅ Once purchased, write down your domain here:**

**My domain: ________________.com**

---

## 💻 STEP 2: Install & Configure Git

### 2.1 Check if Git is Installed

Open **Command Prompt** (Windows):
- Press `Windows Key + R`
- Type: `cmd`
- Press Enter

In Command Prompt, type:
```cmd
git --version
```

**If you see version number:** Git is installed ✅ Skip to Step 2.2

**If you see error:** Install Git ⬇️

### 2.2 Install Git (if needed)

1. Download: https://git-scm.com/download/win
2. Run installer
3. Click "Next" on everything (defaults are fine)
4. Restart Command Prompt

### 2.3 Configure Git (First Time)

```cmd
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

**Replace with YOUR actual name and email!**

Example:
```cmd
git config --global user.name "Mohamed Ahmed"
git config --global user.email "mohamed@gmail.com"
```

**Verify it worked:**
```cmd
git config --global user.name
git config --global user.email
```

**✅ Done with Git setup!**

---

## 📁 STEP 3: Prepare Your Code for GitHub

### 3.1 Navigate to Your Project

```cmd
cd "C:\Users\Egypt Store\Egy360"
```

### 3.2 Initialize Git Repository

```cmd
git init
```

**You should see:** `Initialized empty Git repository`

### 3.3 Check .gitignore File

Let me verify your .gitignore is correct:

```cmd
type .gitignore
```

**Make sure it includes:**
- `*.pyc`
- `__pycache__/`
- `.env`
- `db.sqlite3`
- `media/`
- `logs/`

**If .gitignore is missing or incorrect, I'll create it for you.**

### 3.4 Add All Files

```cmd
git add .
```

**Note: The dot (.) means "everything"**

### 3.5 Create First Commit

```cmd
git commit -m "Initial commit - Egy360 tourism platform"
```

**You should see:** List of files added

**✅ Your code is ready for GitHub!**

---

## 🌍 STEP 4: Create GitHub Account & Repository

### 4.1 Create GitHub Account

1. Go to: **https://github.com**
2. Click "Sign up"
3. Enter:
   - Email address
   - Create password
   - Choose username (example: `mohamed-egy360`)
4. Verify email (check your inbox)
5. Choose "Free" plan

**✅ Account created!**

### 4.2 Create New Repository

1. Click the **"+"** icon (top right)
2. Select **"New repository"**
3. Fill in:

**Repository name:** `egy360`

**Description:** `Egyptian Tourism Platform - Hotels, Tours & Travel`

**Privacy:**
- ⚪ Public (anyone can see code)
- 🔘 **Private** ← Choose this (only you can see)

**Initialize repository:**
- ❌ DON'T check "Add a README"
- ❌ DON't add .gitignore (we already have one)
- ❌ DON't choose a license

4. Click **"Create repository"**

**✅ Repository created!**

### 4.3 Connect Local Code to GitHub

GitHub will show you commands. **Copy these exactly but replace `YOUR-USERNAME`:**

```cmd
git remote add origin https://github.com/YOUR-USERNAME/egy360.git
git branch -M main
git push -u origin main
```

**Example (if your username is mohamed-egy360):**
```cmd
git remote add origin https://github.com/mohamed-egy360/egy360.git
git branch -M main
git push -u origin main
```

**GitHub will ask for credentials:**
- Username: Your GitHub username
- Password: **Use Personal Access Token (not your GitHub password)**

**To get Personal Access Token:**
1. GitHub → Click your profile (top right) → Settings
2. Scroll down → Developer settings (bottom left)
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. Note: "Egy360 deployment"
6. Expiration: 1 year
7. Scopes: Check ✅ **repo** (all sub-options)
8. Click "Generate token"
9. **COPY THE TOKEN** (you'll never see it again!)
10. Use this as password when pushing

**✅ Code is now on GitHub!**

Go to: `https://github.com/YOUR-USERNAME/egy360`

You should see all your files!

---

## 🚂 STEP 5: Deploy to Railway

### 5.1 Create Railway Account

1. Go to: **https://railway.app**
2. Click "Login" or "Start a New Project"
3. Sign up with GitHub (easiest)
4. Click "Authorize Railway" when asked
5. Verify your email

**✅ Railway account created!**

### 5.2 Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Find and click your `egy360` repository
4. Railway will start deploying!

**Railway auto-detects Django!** ✅

### 5.3 Add PostgreSQL Database

1. In your Railway project, click **"New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway creates database automatically

**✅ PostgreSQL database created!**

Railway automatically creates `DATABASE_URL` environment variable.

### 5.4 Configure Environment Variables

1. Click on your **web service** (django app)
2. Go to **"Variables"** tab
3. Click **"New Variable"**

**Add these variables ONE BY ONE:**

```
SECRET_KEY=<paste the secret key I'll generate>
DEBUG=False
ALLOWED_HOSTS=.railway.app
DJANGO_SETTINGS_MODULE=Egy360.settings_production
```

**Let me generate a SECRET_KEY for you:**

I'll create this in the next step.

### 5.5 Add More Variables

```
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

**Replace `yourdomain.com` with your actual domain!**

**Optional (for now):**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**✅ Environment variables configured!**

### 5.6 Deploy

Railway automatically deploys when you push to GitHub.

**Check deployment:**
1. Go to "Deployments" tab
2. Wait for status: ✅ Success
3. Click "View Logs" if there are errors

**You'll get a URL like:**
`https://egy360.up.railway.app`

**✅ Your site is LIVE!**

---

## 🌐 STEP 6: Connect Your Domain

### 6.1 Get Railway Domain Settings

1. In Railway, click your web service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. Click **"Generate Domain"**
5. You'll see: `egy360.up.railway.app`

### 6.2 Add Custom Domain

1. Still in "Domains" section
2. Click **"Custom Domain"**
3. Enter your domain: `www.yourdomain.com`
4. Click "Add"

**Railway will show you DNS records to add:**
- Type: `CNAME`
- Name: `www`
- Value: `egy360.up.railway.app`

### 6.3 Configure Domain DNS (Namecheap)

1. Log into Namecheap
2. Click "Manage" next to your domain
3. Go to **"Advanced DNS"** tab
4. Add new record:
   - Type: **CNAME Record**
   - Host: **www**
   - Value: **egy360.up.railway.app**
   - TTL: **Automatic**
5. Click "Save"

6. Add another record for root domain:
   - Type: **CNAME Record**
   - Host: **@**
   - Value: **egy360.up.railway.app**
   - TTL: **Automatic**
7. Click "Save"

**⚠️ DNS takes 5-30 minutes to propagate!**

### 6.4 SSL Certificate (Automatic!)

Railway automatically provisions SSL certificate.

Once DNS propagates:
- ✅ `https://www.yourdomain.com` works
- ✅ Secure padlock shows
- ✅ Automatic redirect from HTTP to HTTPS

**✅ DONE! Your site is live with HTTPS!**

---

## 🧪 STEP 7: Test Your Live Site

### 7.1 Run Migrations on Production

In Railway:
1. Click your web service
2. Go to **"Settings"**
3. Scroll to **"Deploy"** section
4. Under "Custom Start Command" add:

```
python manage.py migrate && gunicorn Egy360.wsgi
```

Or run manually in Railway CLI.

### 7.2 Create Superuser

You need to create admin account on production:

**Option A: Railway CLI**
```cmd
railway run python manage.py createsuperuser
```

**Option B: Django Console** (if Railway provides it)

### 7.3 Collect Static Files

Should happen automatically, but verify in logs:
```
python manage.py collectstatic --noinput
```

### 7.4 Test Website

Visit: `https://www.yourdomain.com`

**Check:**
- [ ] Homepage loads ✅
- [ ] CSS and images work ✅
- [ ] Navigation works ✅
- [ ] Can search accommodations ✅
- [ ] Admin panel works: `/admin/` ✅

**If anything doesn't work:**
- Check Railway logs
- Check environment variables
- Verify DNS has propagated

---

## 🎉 CONGRATULATIONS!

**You now have:**
✅ Professional domain name with HTTPS
✅ Code on GitHub (version controlled)
✅ Live website on Railway
✅ PostgreSQL database
✅ SSL certificate (secure)
✅ Auto-deployment (push to GitHub = live update)

**Your site:** `https://www.yourdomain.com`

---

## 📝 Next Steps After Deployment

### Immediate (Today):
1. [ ] Create admin account
2. [ ] Add 5-10 sample accommodations
3. [ ] Add 3-5 sample tours
4. [ ] Test booking flow
5. [ ] Share link with friends for feedback

### This Week:
1. [ ] Set up email notifications
2. [ ] Configure Stripe (test mode)
3. [ ] Add real content (50+ listings)
4. [ ] Professional photography
5. [ ] Security audit

### This Month:
1. [ ] Soft launch to limited audience
2. [ ] Start marketing campaigns
3. [ ] Legal registration
4. [ ] Gather user feedback

---

## 🆘 Troubleshooting

### "Site doesn't load"
- Check DNS propagation: https://dnschecker.org
- Verify Railway deployment succeeded
- Check environment variables

### "Static files (CSS) not loading"
- Run `collectstatic` command
- Check `STATIC_ROOT` in settings
- Verify WhiteNoise is installed

### "Database connection error"
- Check `DATABASE_URL` is set
- Verify PostgreSQL is running in Railway
- Check migrations ran successfully

### "Admin panel 404"
- Check `urls.py` includes admin
- Verify `ALLOWED_HOSTS` includes your domain
- Check migrations ran

---

## 💰 Total Cost for Today

| Item | Cost |
|------|------|
| Domain (1 year) | 370 EGP ($12) |
| Railway (Month 1) | 620 EGP ($20) |
| **Total** | **990 EGP** |

**Monthly recurring:** 620 EGP ($20)

---

## 📞 Quick Reference

**Your Details:**
- Domain: ________________.com
- GitHub: github.com/________________/egy360
- Live Site: https://www.________________.com
- Railway: railway.app
- Admin: https://www.________________.com/admin/

**Credentials:**
- GitHub username: ________________
- GitHub token: ________________ (keep safe!)
- Railway email: ________________
- Domain registrar: Namecheap
- Domain login: ________________

---

**Ready to start? Let's go through each step together!**

**Tell me when you're ready for Step 1 (Domain name)** 🚀

---

**Last Updated:** November 16, 2025
**Status:** Ready to deploy!
