# Egy360 Admin User Manual

**Simple Guide for Platform Administrators**

This manual is written for non-technical users who need to manage the Egy360 platform.

---

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Managing Accommodations](#managing-accommodations)
3. [Managing Tours](#managing-tours)
4. [Managing Bookings](#managing-bookings)
5. [Managing Reviews](#managing-reviews)
6. [Managing Users](#managing-users)
7. [Managing Payments](#managing-payments)
8. [Writing Blog Posts](#writing-blog-posts)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### How to Access the Admin Panel

1. Open your web browser
2. Go to: `https://yourdomain.com/admin/`
3. Enter your username and password
4. Click "Log in"

**First Time?** Ask your developer to create an admin account for you.

---

## 🏨 Managing Accommodations

### Adding a New Hotel/Accommodation

1. Click **"Accommodations"** in the left menu
2. Click **"Add Accommodation"** button (top right)
3. Fill in the details:

**Basic Information:**
- **Name:** e.g., "Pyramids View Hotel"
- **Type:** Select from dropdown (hotel, resort, etc.)
- **City:** Select the city
- **Address:** Full address
- **Description:** Detailed description of the property

**Pricing:**
- **Price per night:** Enter the base price
- **Currency:** USD (default)

**Features:**
- **Star rating:** 1-5 stars
- **Check boxes:** Pool, WiFi, Restaurant, etc.

**Images:**
- Click "Choose File" to upload photos
- Upload at least 3-5 high-quality photos

**Status:**
- **Is Active:** Check this box to make it visible on the website
- **Is Featured:** Check to show on homepage

4. Click **"Save"** button at the bottom

### Editing an Accommodation

1. Click **"Accommodations"** → **"Accommodations"**
2. Find the accommodation in the list
3. Click on its name
4. Make your changes
5. Click **"Save"**

### Deleting an Accommodation

⚠️ **Warning:** This will permanently delete the accommodation.

1. Click **"Accommodations"** → **"Accommodations"**
2. Check the box next to the accommodation
3. Select "Delete selected" from the dropdown
4. Click **"Go"**
5. Confirm deletion

---

## 🗺️ Managing Tours

### Adding a New Tour

1. Click **"Tours"** in the left menu
2. Click **"Add Tour"** button
3. Fill in the details:

**Basic Information:**
- **Name:** e.g., "Cairo Day Tour"
- **Tour Type:** Cultural, Adventure, etc.
- **Duration:** Number of days
- **Description:** What's included in the tour

**Pricing:**
- **Price per person:** Base price
- **Child price:** Discounted price for children
- **Group size:** Minimum and maximum people

**What's Included:**
- **Includes:** Transportation, Guide, Lunch, etc.
- **Excludes:** Personal expenses, Tips, etc.

**Itinerary:**
Scroll to "Tour Itineraries" section:
- **Day 1:** Click "Add another Tour Itinerary"
  - Day number: 1
  - Title: "Pyramids Visit"
  - Description: What happens this day
- **Day 2:** Add another itinerary
- Continue for all days

**Status:**
- **Is Active:** Make visible
- **Is Featured:** Show on homepage

4. Click **"Save"**

### Managing Tour Bookings

1. Click **"Tours"** → **"Tour bookings"**
2. You'll see all tour bookings
3. Click on a booking to view details
4. Change status:
   - **Pending:** New booking, needs confirmation
   - **Confirmed:** Accepted and confirmed
   - **Cancelled:** Customer cancelled
   - **Completed:** Tour finished

---

## 📅 Managing Bookings

### View All Bookings

1. Click **"Bookings"** in the left menu
2. You'll see all bookings (accommodations, tours, transportation)

### Booking Details

Each booking shows:
- **Booking Reference:** Unique code (e.g., BK20250115ABC)
- **Customer Name:** Who booked
- **Type:** Accommodation, Tour, or Transportation
- **Status:** Pending, Confirmed, Cancelled, Completed
- **Amount:** Total price
- **Dates:** Check-in and check-out

### Confirming a Booking

1. Click on the booking
2. Change **Status** to "Confirmed"
3. Click **"Save"**
4. Customer will receive confirmation email

### Cancelling a Booking

1. Click on the booking
2. Scroll to "Booking Cancellation" section
3. Click **"Add Cancellation"**
4. Fill in:
   - **Reason:** Why it's cancelled
   - **Refund Amount:** How much to refund
   - **Refund Status:** Pending/Processed
5. Change booking **Status** to "Cancelled"
6. Click **"Save"**

---

## ⭐ Managing Reviews

### Moderating Reviews

All new reviews need approval to prevent spam.

1. Click **"Reviews"** → **"Reviews"**
2. You'll see all reviews with status:
   - **Pending:** Waiting for approval
   - **Approved:** Live on website
   - **Rejected:** Not shown

### Approving a Review

1. Click on the review
2. Read the review content
3. Check if it's appropriate (no spam, no offensive language)
4. Change **Status** to "Approved"
5. Click **"Save"**

### Rejecting a Review

1. Click on the review
2. Change **Status** to "Rejected"
3. Click **"Save"**
4. Review won't appear on website

### Responding to Reviews (as Provider)

1. Find the review
2. Scroll to "Review Response" section
3. Click **"Add Review Response"**
4. Write your response
5. Click **"Save"**

### Handling Reported Reviews

If users report fake reviews:

1. Click **"Reviews"** → **"Review reports"**
2. Click on the report to see details
3. Check the review
4. Take action:
   - If fake: Reject the review
   - If real: Ignore the report
5. Mark report as **"Resolved"**

---

## 👥 Managing Users

### View All Users

1. Click **"Accounts"** → **"Users"**
2. You'll see all registered users

### View User Profile

1. Click on a username
2. See user details:
   - Email, Phone
   - Bookings history
   - Reviews written

### Verify User Identity

1. Click **"Accounts"** → **"User Profiles"**
2. Find the user
3. Check verification boxes:
   - **Email verified:** Email confirmed
   - **Phone verified:** Phone confirmed
   - **Identity verified:** Passport/ID checked

### Making Someone an Admin

⚠️ **Be careful!** Admins have full access.

1. Click **"Accounts"** → **"Users"**
2. Click on the user
3. Scroll to "Permissions"
4. Check these boxes:
   - ✅ **Staff status** (can access admin)
   - ✅ **Superuser status** (full permissions)
5. Click **"Save"**

### Blocking a User

1. Click on the user
2. Uncheck **"Active"** box
3. Click **"Save"**
4. User can't log in anymore

---

## 💳 Managing Payments

### View All Payments

1. Click **"Payments"** → **"Payments"**
2. See all transactions

### Payment Statuses

- **Pending:** Waiting for payment
- **Processing:** Payment in progress
- **Completed:** Successfully paid
- **Failed:** Payment failed
- **Refunded:** Money returned

### Confirming a Payment Manually

1. Click on the payment
2. Change **Status** to "Completed"
3. Fill in **Transaction ID** (from payment gateway)
4. Click **"Save"**

### Processing a Refund

1. Click **"Payments"** → **"Refunds"**
2. Click **"Add Refund"**
3. Select the original payment
4. Enter:
   - **Refund Amount:** How much to refund
   - **Reason:** Why refunding
   - **Status:** Processing or Completed
5. Click **"Save"**

### Downloading Invoices

1. Find the payment
2. Scroll to "Invoice" section
3. Click on invoice number
4. Click **"Download PDF"** (if available)

---

## 📝 Writing Blog Posts

### Creating a New Blog Post

1. Click **"Blog"** → **"Blog posts"**
2. Click **"Add Blog Post"**
3. Fill in:

**Content:**
- **Title:** e.g., "Top 10 Things to Do in Cairo"
- **Slug:** URL-friendly version (auto-generated)
- **Content:** Full article text
- **Excerpt:** Short summary

**Settings:**
- **Category:** Select or create category
- **Author:** Select author
- **Featured Image:** Upload main image
- **Published:** Check to make live
- **Published Date:** When to publish

4. Click **"Save"**

### Editing a Blog Post

1. Click **"Blog"** → **"Blog posts"**
2. Click on the post title
3. Make changes
4. Click **"Save"**

### Managing Comments

1. Click **"Blog"** → **"Blog comments"**
2. See all comments
3. Check **"Is Approved"** to show comment
4. Uncheck to hide spam

---

## ✅ Common Tasks

### Daily Tasks

**Check New Bookings**
1. Go to **"Bookings"**
2. Filter by status: **"Pending"**
3. Confirm or contact customer

**Moderate Reviews**
1. Go to **"Reviews"**
2. Filter by status: **"Pending"**
3. Approve or reject

**Check Payments**
1. Go to **"Payments"**
2. Check for failed payments
3. Follow up if needed

### Weekly Tasks

**Update Availability**
- Check accommodation availability
- Update tour schedules
- Block unavailable dates

**Review Analytics**
- Check most popular tours
- Check most viewed accommodations
- Review booking trends

**Content Updates**
- Publish new blog posts
- Update travel guides
- Add new photos

### Monthly Tasks

**Financial Reports**
- Total bookings
- Total revenue
- Refunds processed
- Outstanding payments

**User Engagement**
- New user registrations
- Active users
- Review activity

---

## 🆘 Troubleshooting

### "I can't log in to admin panel"

**Solution:**
1. Check you're using correct URL: `/admin/`
2. Verify username and password
3. Make sure **"Staff status"** is checked on your account
4. Contact your developer if still stuck

### "Changes I made aren't showing on website"

**Solutions:**
1. Did you click **"Save"**?
2. Check **"Is Active"** box is checked
3. Clear your browser cache (Ctrl+F5)
4. Wait 5 minutes (caching may be enabled)

### "I can't upload images"

**Solutions:**
1. Check file size (max 5MB per image)
2. Use JPG or PNG format
3. Check image dimensions (max 4000x4000)
4. Contact developer if problem persists

### "Booking confirmation emails not sending"

**Solutions:**
1. Check email settings in admin
2. Verify customer email address is correct
3. Check spam folder
4. Contact developer to check email configuration

### "Payment showing as pending but customer paid"

**Solutions:**
1. Check payment gateway dashboard (Stripe, etc.)
2. Manually confirm payment if verified
3. Update payment status to "Completed"
4. Send manual confirmation email to customer

---

## 🔒 Security Best Practices

### Password Safety
- ✅ Use a strong password (12+ characters)
- ✅ Mix uppercase, lowercase, numbers, symbols
- ✅ Never share your admin password
- ✅ Change password every 90 days

### Account Safety
- ✅ Log out when done
- ✅ Don't save password in public computers
- ✅ Only access admin from secure networks
- ✅ Report suspicious activity immediately

### Data Privacy
- ✅ Keep customer data confidential
- ✅ Never share customer personal information
- ✅ Follow data protection regulations
- ✅ Delete old data when no longer needed

---

## 📞 Getting Help

### Quick Reference

**Website:** https://yourdomain.com
**Admin Panel:** https://yourdomain.com/admin/
**API Docs:** https://yourdomain.com/api/docs/

### Support Contacts

**Technical Issues:** Contact your developer
**Payment Issues:** Check payment gateway support
**Content Questions:** Review this manual

---

## 📚 Additional Resources

- **Video Tutorials:** Coming soon
- **FAQ:** See website FAQ section
- **Technical Docs:** For developers only

---

**Last Updated:** November 15, 2025
**Version:** 1.0.0

**Need more help?** This manual covers the basics. For advanced features, consult the technical documentation or contact your developer.
