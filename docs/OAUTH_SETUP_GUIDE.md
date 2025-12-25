# OAuth & SMS Setup Guide for Egy360

## Quick Links

| Provider | Console Link |
|----------|--------------|
| Google | https://console.cloud.google.com/apis/credentials |
| Facebook | https://developers.facebook.com/apps/ |
| Apple | https://developer.apple.com/account/resources/identifiers/list |
| Twilio | https://console.twilio.com/ |

---

## 1. GOOGLE OAuth Setup

### Step 1.1: Create Project (if needed)
- Go to https://console.cloud.google.com/
- Click the project dropdown at the top
- Click "New Project"
- Name: `Egy360`
- Click "Create"

### Step 1.2: Configure OAuth Consent Screen
- Go to: **APIs & Services > OAuth consent screen**
- Select **External** > Create
- Fill in:
  - App name: `Egy360`
  - User support email: Select your email
  - App domain: `https://360egy.com`
  - Authorized domains: Click "Add Domain" → `360egy.com`
  - Developer contact: Your email
- Click **Save and Continue** through all steps

### Step 1.3: Create OAuth Client
- Go to: **APIs & Services > Credentials**
- Click **+ Create Credentials > OAuth client ID**
- Application type: **Web application**
- Name: `Egy360 Web Client`
- Authorized JavaScript origins: `https://360egy.com`
- Authorized redirect URIs:
  ```
  https://360egy.com/auth/google/login/callback/
  ```
- Click **Create**
- **COPY** the Client ID and Client Secret

### Step 1.4: Add to Django
```bash
python manage.py setup_social_apps --provider google --client-id "YOUR_CLIENT_ID" --secret "YOUR_CLIENT_SECRET"
```

---

## 2. FACEBOOK OAuth Setup

### Step 2.1: Create App
- Go to https://developers.facebook.com/
- Click **My Apps** > **Create App**
- Use case: **Authenticate and request data from users with Facebook Login**
- App name: `Egy360`
- Click **Create App**

### Step 2.2: Configure Facebook Login
- In sidebar: **Use cases** > **Customize** (under Authentication)
- Click **Go to settings**
- Add Valid OAuth Redirect URIs:
  ```
  https://360egy.com/auth/facebook/login/callback/
  ```
- Click **Save Changes**

### Step 2.3: Get Credentials
- Go to **App settings > Basic**
- Copy the **App ID** and **App Secret**

### Step 2.4: Add to Django
```bash
python manage.py setup_social_apps --provider facebook --client-id "YOUR_APP_ID" --secret "YOUR_APP_SECRET"
```

---

## 3. APPLE Sign In Setup

**Requires Apple Developer Account ($99/year)**

### Step 3.1: Create App ID
- Go to https://developer.apple.com/account/
- Navigate to **Certificates, Identifiers & Profiles > Identifiers**
- Click **+** to create new
- Select **App IDs** > **App**
- Description: `Egy360`
- Bundle ID: `com.360egy.web`
- Enable **Sign In with Apple**

### Step 3.2: Create Service ID
- Go to **Identifiers > +**
- Select **Services IDs**
- Identifier: `com.360egy.web.service`
- Enable **Sign In with Apple**
- Configure:
  - Domains: `360egy.com`
  - Return URLs: `https://360egy.com/auth/apple/login/callback/`

### Step 3.3: Create Key
- Go to **Keys > +**
- Name: `Egy360 Sign In Key`
- Enable **Sign In with Apple**
- Download the `.p8` file

### Step 3.4: Add to Django
```bash
python manage.py setup_social_apps --provider apple --client-id "com.360egy.web.service" --secret "CONTENT_OF_P8_FILE" --key "YOUR_TEAM_ID"
```

---

## 4. TWILIO SMS Setup

### Step 4.1: Create Account
- Go to https://console.twilio.com/
- Sign up and verify email/phone

### Step 4.2: Get Credentials
From the Dashboard, copy:
- **Account SID**: Starts with `AC...`
- **Auth Token**: Click to reveal

### Step 4.3: Get Phone Number
- Go to **Phone Numbers > Manage > Buy a number**
- Or use trial number

### Step 4.4: Add to Railway
Add these environment variables in Railway:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890
```

---

## After Adding Credentials

Commit and push to deploy:
```bash
git add .
git commit -m "Add OAuth provider credentials"
git push origin main
```

Test the social login buttons on:
- https://360egy.com/accounts/login/
- https://360egy.com/accounts/register/
