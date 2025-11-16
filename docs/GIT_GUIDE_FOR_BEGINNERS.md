# Git Guide for Beginners - Egy360

**Simple, step-by-step guide to using Git for your project**

---

## 🤔 What is Git?

**Git** is like a "save system" for your code that:
- Tracks all changes you make
- Lets you go back to previous versions
- Allows collaboration with others
- Backs up your code online (GitHub)

Think of it like:
- **Git** = Version control software on your computer
- **GitHub** = Online storage for your code (like Google Drive for code)

---

## 📋 Quick Setup (5 minutes)

### Step 1: Install Git

**Check if Git is already installed:**
```bash
git --version
```

If not installed, download from: https://git-scm.com/download/win

**During installation:**
- Click "Next" on everything (defaults are fine)
- Choose "Use Git from the Windows Command Prompt"

### Step 2: Configure Git (First Time Only)

Open Command Prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Replace with your actual name and email.

**Example:**
```bash
git config --global user.name "Mohamed Ahmed"
git config --global user.email "mohamed@example.com"
```

---

## 🎯 Basic Git Workflow (What You'll Use Daily)

### The 3-Step Save Process

```
1. ADD    → Select what to save
2. COMMIT → Save with a message
3. PUSH   → Upload to GitHub
```

**Think of it like:**
1. **ADD** = Put items in shopping cart
2. **COMMIT** = Checkout and pay
3. **PUSH** = Items delivered to your home

---

## 🚀 Your First Git Commands

### Initialize Git in Your Project

```bash
cd "C:\Users\Egypt Store\Egy360"
git init
```

**What this does:** Turns your folder into a Git repository.

### Check Status (See What Changed)

```bash
git status
```

**What this shows:**
- Files you've changed (red)
- Files ready to save (green)

### Add Files to Save

**Add all files:**
```bash
git add .
```

**Add specific file:**
```bash
git add filename.py
```

The `.` means "everything"

### Commit (Save with Message)

```bash
git commit -m "Your message here"
```

**Good messages:**
- ✅ "Add payment integration"
- ✅ "Fix booking bug"
- ✅ "Update homepage design"

**Bad messages:**
- ❌ "changes"
- ❌ "stuff"
- ❌ "asdf"

### Push to GitHub

```bash
git push origin main
```

**What this does:** Uploads your code to GitHub.

---

## 🌐 Setting Up GitHub (One Time)

### Step 1: Create GitHub Account

1. Go to: https://github.com
2. Click "Sign up"
3. Choose username (example: `mohamed-egy360`)
4. Use your email
5. Create strong password
6. Verify email

**Free account is perfect for you!**

### Step 2: Create New Repository

1. Click the **"+"** icon (top right)
2. Select **"New repository"**
3. Fill in:
   - **Repository name:** `egy360`
   - **Description:** "Egyptian Tourism Platform"
   - **Private** or **Public** (choose Private for now)
   - **DON'T** check "Initialize with README"
4. Click **"Create repository"**

### Step 3: Connect Your Local Code to GitHub

GitHub will show you commands. Use these:

```bash
cd "C:\Users\Egypt Store\Egy360"
git remote add origin https://github.com/your-username/egy360.git
git branch -M main
git push -u origin main
```

**Replace `your-username` with your actual GitHub username!**

---

## 📝 Daily Git Workflow

### When You Make Changes

```bash
# 1. Check what changed
git status

# 2. Add files to save
git add .

# 3. Commit with message
git commit -m "Describe what you changed"

# 4. Push to GitHub
git push
```

**Example:**
```bash
git status
git add .
git commit -m "Add 10 new Cairo hotels"
git push
```

---

## 🔄 Common Tasks

### Download Latest Code (if working from multiple computers)

```bash
git pull
```

### See History of Changes

```bash
git log
```

Press `q` to exit.

### Undo Changes (Before Commit)

```bash
git checkout -- filename.py
```

Or undo everything:
```bash
git checkout -- .
```

### Create a Backup Branch

```bash
git branch backup-nov-16
git checkout -b development
```

This creates a safe copy before making big changes.

---

## 🚫 What NOT to Commit

**NEVER commit these files:**
- `.env` (contains passwords!)
- `db.sqlite3` (database file)
- `__pycache__/` (temporary Python files)
- `*.pyc` (compiled Python)
- `logs/` (log files)
- `media/` (user uploads - too large)

**Why?** Security and size.

### Your .gitignore File

You already have a `.gitignore` file that handles this!

Check it:
```bash
cat .gitignore
```

---

## 🆘 Troubleshooting

### "Permission denied"

**If using HTTPS, GitHub will ask for username/password.**

**Better solution:** Use Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Copy token (save it somewhere!)
5. Use token as password when pushing

### "Repository not found"

**Check remote URL:**
```bash
git remote -v
```

**Fix if wrong:**
```bash
git remote set-url origin https://github.com/your-username/egy360.git
```

### "Merge conflict"

**If you see this:**
```bash
git status
# Find conflicted files
# Edit them manually to fix
git add .
git commit -m "Resolve conflicts"
git push
```

---

## 📚 Git Cheat Sheet

### Essential Commands

| Command | What It Does |
|---------|-------------|
| `git status` | See what changed |
| `git add .` | Add all changes |
| `git add file.py` | Add specific file |
| `git commit -m "message"` | Save changes |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| `git log` | See history |
| `git clone URL` | Download a repository |

### Checking Things

| Command | What It Shows |
|---------|--------------|
| `git status` | Current changes |
| `git log` | Commit history |
| `git diff` | What changed |
| `git remote -v` | GitHub connection |
| `git branch` | Available branches |

---

## 🎯 Your First Git Session (Practice)

**Let's do this together:**

```bash
# 1. Navigate to your project
cd "C:\Users\Egypt Store\Egy360"

# 2. Initialize Git (if not done)
git init

# 3. Check status
git status

# 4. Add everything
git add .

# 5. Make first commit
git commit -m "Initial commit - Egy360 tourism platform"

# 6. Create GitHub repository (do this on github.com)

# 7. Connect to GitHub
git remote add origin https://github.com/YOUR-USERNAME/egy360.git

# 8. Push to GitHub
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub! 🎉

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets

**Before your first commit, verify .gitignore:**

```bash
# Check if .env is listed
cat .gitignore | grep .env
```

### 2. Check Before Pushing

```bash
git status
```

**Look for:**
- ❌ `.env` file (should NOT be there)
- ❌ Database files
- ✅ `.py` files (OK)
- ✅ `.md` files (OK)

### 3. If You Accidentally Committed Secrets

**Remove from Git history:**
```bash
git rm --cached .env
git commit -m "Remove .env file"
git push
```

**Then change all passwords immediately!**

---

## 🚀 Next Steps After Git Setup

Once your code is on GitHub:

1. ✅ Choose hosting provider (Railway, Heroku, DigitalOcean)
2. ✅ Connect GitHub to hosting
3. ✅ Hosting auto-deploys when you push
4. ✅ You're live!

**Git makes deployment automatic!**

---

## 💡 Pro Tips

### Commit Often

**Good:**
- Small commits after each feature
- Clear messages
- Easy to find bugs

**Bad:**
- One huge commit with everything
- Hard to track what changed

### Use Branches for Big Features

```bash
# Create branch for new feature
git checkout -b feature-payment-gateway

# Work on feature...
git add .
git commit -m "Add Stripe integration"

# When done, merge back
git checkout main
git merge feature-payment-gateway
git push
```

### Write Good Commit Messages

**Template:**
```
[Type] Short description

- Detail 1
- Detail 2
```

**Example:**
```
[Feature] Add user dashboard

- Create dashboard template
- Add booking history view
- Add user profile edit
```

---

## 📞 Quick Reference

### I Want To...

**...save my work**
```bash
git add .
git commit -m "Your message"
```

**...upload to GitHub**
```bash
git push
```

**...download latest code**
```bash
git pull
```

**...see what I changed**
```bash
git status
git diff
```

**...undo my changes**
```bash
git checkout -- .
```

---

## 🎓 Learning More

Once comfortable with basics:

- **GitHub Desktop** - Visual Git client (easier than command line)
- **VSCode Git** - Built-in Git features in VSCode
- **Git branches** - For advanced workflows

**But the basics above are 90% of what you'll use!**

---

## ✅ Checklist: Are You Ready?

Before proceeding to deployment:

- [ ] Git installed
- [ ] Git configured (name and email)
- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Local code initialized with `git init`
- [ ] .gitignore file present
- [ ] First commit made
- [ ] Code pushed to GitHub

**Once all checked, you're ready to deploy!**

---

**Remember:** Git seems scary at first, but you'll use the same 5-6 commands 95% of the time. You've got this! 💪

**Next:** `DEPLOYMENT_OPTIONS.md` - Choose your hosting provider

---

**Last Updated:** November 16, 2025
