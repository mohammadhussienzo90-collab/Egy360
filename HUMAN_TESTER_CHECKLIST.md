# Egy360 Human Tester Checklist

**Production URL**: https://360egy.com
**Test Date**: ___________
**Tester Name**: ___________

---

## 1. CRITICAL PAGES (Must Work 100%)

### Homepage
- [ ] Homepage loads without errors
- [ ] Logo and branding visible
- [ ] Navigation menu works
- [ ] Search widget functional
- [ ] Featured accommodations display
- [ ] Featured tours display
- [ ] Footer links work

### Health & Technical
- [ ] /health/ returns `{"status": "ok"}`
- [ ] /favicon.svg displays golden Ankh on white background
- [ ] /sitemap.xml loads XML content
- [ ] No console JavaScript errors on any page

---

## 2. ACCOMMODATIONS

### Listing Page (/accommodations/)
- [ ] Page loads without errors
- [ ] Accommodation cards display correctly
- [ ] Images load properly
- [ ] Prices displayed in correct format
- [ ] Star ratings visible
- [ ] Pagination works (if applicable)
- [ ] Filters work (city, type, price)

### Detail Page (click any accommodation)
- [ ] Page loads without errors
- [ ] All accommodation details visible
- [ ] Image gallery works
- [ ] "Book Now" button visible and clickable
- [ ] Clicking "Book Now" opens affiliate link in new tab
- [ ] Affiliate URL contains `marker=477897`
- [ ] Room types listed (if any)
- [ ] Amenities displayed
- [ ] Location/map shown

### Affiliate Tracking Test
1. [ ] Open browser DevTools > Network tab
2. [ ] Click "Book Now" on any accommodation
3. [ ] Verify POST request sent to `/api/track-click/`
4. [ ] Verify response is `{"success": true}`

---

## 3. TOURS

### Listing Page (/tours/)
- [ ] Page loads without errors
- [ ] Tour cards display correctly
- [ ] Images load properly
- [ ] Prices displayed correctly
- [ ] Duration shown
- [ ] Pagination works

### Detail Page (click any tour)
- [ ] Page loads without errors
- [ ] All tour details visible
- [ ] Image gallery works
- [ ] "Book This Tour" button visible
- [ ] Clicking "Book" opens affiliate link in new tab
- [ ] Affiliate URL contains `shmarker=477897`
- [ ] Itinerary displayed
- [ ] Inclusions/exclusions listed
- [ ] Departure city shown

---

## 4. DESTINATIONS

### Country/City Listing (/destinations/)
- [ ] Page loads without errors
- [ ] Countries displayed
- [ ] Cities within countries visible
- [ ] Images load properly
- [ ] Links to city pages work

### City Detail Page
- [ ] Page loads without errors
- [ ] City description displayed
- [ ] Accommodations in city shown
- [ ] Tours in city shown
- [ ] Attractions listed

---

## 5. BLOG

### Blog Listing (/blog/)
- [ ] Page loads without errors
- [ ] Blog posts displayed
- [ ] Featured images load
- [ ] Categories visible
- [ ] Pagination works

### Blog Detail Page
- [ ] Page loads without errors
- [ ] Content renders correctly (no raw markdown)
- [ ] Author shown
- [ ] Date displayed
- [ ] Images within content load
- [ ] No escaped characters (\\#, \\*, etc.)

---

## 6. STATIC PAGES

- [ ] About page loads (/about/)
- [ ] Contact page loads (/contact/)
- [ ] Terms of Service loads (/terms/)
- [ ] Privacy Policy loads (/privacy/)
- [ ] FAQ page loads (/faq/)

---

## 7. AUTHENTICATION

### Login
- [ ] Login page loads (/accounts/login/)
- [ ] Can enter email/password
- [ ] Login works with valid credentials
- [ ] Error message for invalid credentials
- [ ] Redirect to dashboard after login

### Registration
- [ ] Register page loads (/accounts/register/)
- [ ] Form validation works
- [ ] Password requirements enforced
- [ ] Email validation works
- [ ] Account creation successful

### Protected Pages
- [ ] /accounts/profile/ redirects to login if not logged in
- [ ] /dashboard/ redirects to login if not logged in
- [ ] After login, can access profile
- [ ] After login, can access dashboard

---

## 8. NEWSLETTER & CONTACT

### Newsletter
- [ ] Newsletter form visible on homepage
- [ ] Can submit email
- [ ] Success message shown
- [ ] Email validation works (rejects invalid emails)

### Contact Form
- [ ] Contact form loads
- [ ] All fields work
- [ ] Form validation works
- [ ] Submission successful
- [ ] Confirmation message shown

---

## 9. MOBILE RESPONSIVENESS

Test on mobile device or browser DevTools mobile mode:

- [ ] Homepage displays correctly on mobile
- [ ] Navigation menu collapses to hamburger
- [ ] Search works on mobile
- [ ] Accommodation cards stack vertically
- [ ] Tour cards stack vertically
- [ ] Detail pages readable on mobile
- [ ] Buttons are tap-friendly (44px minimum)
- [ ] Text is readable without zooming
- [ ] Images scale properly

---

## 10. AFFILIATE REVENUE TRACKING

### Verification Steps
1. Open DevTools Console
2. Navigate to an accommodation detail page
3. Click "Book Now" button
4. Check Console for tracking confirmation

### Expected Behavior
- [ ] Click tracked before redirect
- [ ] Affiliate link opens in new tab
- [ ] Original page stays open
- [ ] No JavaScript errors

### Affiliate Link Format Verification
- [ ] Hotellook links: `search.hotellook.com/hotels?...marker=477897`
- [ ] Viator links: `tp.media/click?shmarker=477897...`
- [ ] Marker ID matches: 477897

---

## 11. PERFORMANCE

- [ ] Homepage loads in < 3 seconds
- [ ] Images are optimized/lazy-loaded
- [ ] No broken images (404s)
- [ ] No console errors
- [ ] Pages feel responsive

---

## 12. SEO VERIFICATION

- [ ] Each page has unique title
- [ ] Meta descriptions present
- [ ] Proper heading hierarchy (H1 > H2 > H3)
- [ ] Images have alt text
- [ ] Sitemap accessible at /sitemap.xml
- [ ] Robots.txt accessible (if applicable)

---

## ISSUES FOUND

| # | Page/Feature | Issue Description | Severity |
|---|--------------|-------------------|----------|
| 1 | | | High/Med/Low |
| 2 | | | High/Med/Low |
| 3 | | | High/Med/Low |
| 4 | | | High/Med/Low |
| 5 | | | High/Med/Low |

---

## SIGN-OFF

**All critical features working**: [ ] Yes [ ] No

**Site ready for production traffic**: [ ] Yes [ ] No

**Notes**:
___________________________________________
___________________________________________
___________________________________________

**Tester Signature**: ___________
**Date**: ___________
