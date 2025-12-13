# Google Analytics GA4 Setup Instructions for 360egy.com

## Status
✅ Code Implementation: COMPLETE
⏳ Google Analytics Account Setup: **YOU NEED TO DO THIS**
⏳ Railway Environment Variable: **YOU NEED TO DO THIS**

---

## What I've Done (Complete)

1. ✅ Added Google Analytics tracking code to base.html template
2. ✅ Configured Django settings to read GA ID from environment variable
3. ✅ Set up context processor to make GA ID available to all templates
4. ✅ Implemented custom event tracking for affiliate links:
   - Booking.com clicks
   - Agoda clicks
   - Hotels.com clicks
   - Travelpayouts clicks
5. ✅ Pushed code to GitHub
6. ✅ Railway will auto-deploy the code

---

## What You Need To Do (30 minutes)

### Step 1: Create Google Analytics Account (10 minutes)

1. Go to https://analytics.google.com/
2. Sign in with your Google account (or create one)
3. Click "Start measuring"
4. Fill in Account details:
   - **Account name**: "Egy360" or "Egyptian Tourism"
   - Check all data sharing settings (recommended)
   - Click "Next"

5. Fill in Property details:
   - **Property name**: "360egy.com"
   - **Reporting time zone**: "(GMT+02:00) Cairo"
   - **Currency**: "Egyptian Pound (EGP)"
   - Click "Next"

6. Business Information:
   - **Industry category**: "Travel"
   - **Business size**: Select your size
   - **How you plan to use Google Analytics**: Check all that apply
   - Click "Create"

7. Accept Terms of Service
   - Check the boxes
   - Click "I Accept"

### Step 2: Get Your Measurement ID (5 minutes)

1. After creating your property, you'll see **"Web"** as a data stream option
2. Click "Web"
3. Fill in:
   - **Website URL**: https://360egy.com
   - **Stream name**: "Egy360 Main Site"
4. Click "Create stream"

5. **COPY YOUR MEASUREMENT ID**
   - You'll see something like: **G-XXXXXXXXXX**
   - **This is your GOOGLE_ANALYTICS_ID**
   - Keep this window open or copy it somewhere safe

### Step 3: Add to Railway (5 minutes)

1. Go to https://railway.app/
2. Go to your "Egy360" project
3. Click on your service
4. Go to the **"Variables"** tab
5. Click **"+ New Variable"**
6. Add:
   - **Variable name**: `GOOGLE_ANALYTICS_ID`
   - **Value**: Your Measurement ID (e.g., `G-XXXXXXXXXX`)
7. Click "Add"

### Step 4: Redeploy (Optional - 2 minutes)

Railway should automatically redeploy when you add an environment variable. If not:

1. In Railway, go to your service
2. Click **"Deploy"** → **"Redeploy"**

---

## Verify It's Working (5 minutes)

### Option 1: Real-Time Reports (Instant)

1. Go back to Google Analytics
2. Click **"Reports"** → **"Realtime"**
3. Open your website: https://360egy.com
4. You should see yourself appear in the real-time report within 30 seconds
5. Click around your site - especially click accommodation links
6. You should see "affiliate_click" events appearing

### Option 2: Check Page Source (Instant)

1. Visit https://360egy.com
2. Right-click → "View Page Source"
3. Search for "gtag" (Ctrl+F)
4. You should see your Measurement ID in the code

---

## What Google Analytics Will Track

### Automatic Tracking:
- **Page views**: Every page visit
- **User sessions**: How long people stay
- **Geographic data**: Where visitors are from
- **Device data**: Mobile vs Desktop
- **Traffic sources**: How people find your site

### Custom Events (Affiliate Links):
- **Booking.com clicks**: When someone clicks a Booking.com link
- **Agoda clicks**: When someone clicks an Agoda link
- **Hotels.com clicks**: When someone clicks a Hotels.com link
- **Travelpayouts clicks**: When someone clicks tour/travel links

---

## View Your Reports

After 24-48 hours of data collection, you can view:

### Traffic Reports:
1. Go to https://analytics.google.com/
2. Click **"Reports"** → **"Acquisition"** → **"Traffic acquisition"**
3. See where your visitors come from (Google, direct, social media, etc.)

### Affiliate Click Reports:
1. Go to **"Reports"** → **"Engagement"** → **"Events"**
2. Look for **"affiliate_click"** event
3. Click on it to see which affiliate links get the most clicks

### Popular Pages:
1. Go to **"Reports"** → **"Engagement"** → **"Pages and screens"**
2. See which pages are most popular

---

## For Future Affiliate Applications

When applying to affiliate programs, you can now provide:

- **Monthly visitors**: From GA4 dashboard
- **Page views**: From GA4 engagement reports
- **Geographic breakdown**: Where your audience is from
- **Affiliate link performance**: Custom event data showing clicks

---

## Troubleshooting

### Analytics not showing in real-time:
1. Check Railway environment variables are set correctly
2. Make sure Railway redeployed after adding the variable
3. Clear your browser cache and visit the site again
4. Check browser console for errors (F12 → Console tab)

### Still not working:
1. Make sure your Measurement ID starts with "G-" (GA4)
2. Not "UA-" (old Universal Analytics - discontinued)
3. Verify the ID is exactly as shown in Google Analytics

---

## Next Steps After Setup

Once Analytics is live for 1-2 weeks:

1. Apply to **Viator** affiliate program (no follower requirement)
2. Complete **Travelpayouts** registration
3. Apply to **Klook** affiliate program
4. Use traffic data to show value to affiliate partners

---

## Questions?

If you need help:
1. Take a screenshot of the issue
2. Check the Railway logs for errors
3. Verify your Measurement ID is correct in Railway variables

Your site is already configured - you just need to add the Google Analytics ID!
