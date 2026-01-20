"""
Script to create new blog articles for Egy360
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

from blog.models import BlogPost, BlogCategory
from django.contrib.auth.models import User
from django.utils import timezone

def create_articles():
    # Get or create category
    category, _ = BlogCategory.objects.get_or_create(
        slug='travel-tips',
        defaults={'name': 'Travel Tips', 'description': 'Egypt travel tips and guides'}
    )

    author = User.objects.first()
    if not author:
        print("No users found!")
        return

    articles = [
        # Article 1: Best Egypt Tours 2026
        {
            'slug': 'best-egypt-tours-2026-complete-guide',
            'title': 'Best Egypt Tours 2026: Complete Guide to Top 10 Tour Packages',
            'excerpt': 'Discover the best Egypt tours for 2026. From luxury Nile cruises to budget backpacker trips, find the perfect tour package for your Egyptian adventure.',
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
            'meta_description': 'Best Egypt tours 2026: Compare top 10 tour packages including Nile cruises, Cairo trips, and adventure tours. Expert recommendations and booking tips.',
            'meta_keywords': 'egypt tours 2026, best egypt tour packages, nile cruise, cairo tour, egypt travel',
            'tags': 'tours, egypt travel, 2026, nile cruise, cairo',
            'is_featured': True,
            'content': '''## Why Book an Egypt Tour in 2026?

Egypt is experiencing a tourism renaissance, with new discoveries, restored monuments, and improved infrastructure making 2026 the perfect year to visit. Whether you're a history buff, adventure seeker, or luxury traveler, there's a tour package tailored for you.

### What Makes a Great Egypt Tour?

Before diving into our recommendations, here's what to look for:

- **Experienced Egyptologist guides** - Not just tour guides, but experts in ancient history
- **Small group sizes** - Ideally 12-16 people maximum
- **Quality accommodations** - 4-5 star hotels with Nile or pyramid views
- **Flexible itineraries** - Some free time for personal exploration
- **Transparent pricing** - No hidden fees or surprise charges

---

## Top 10 Egypt Tours for 2026

### 1. Classic Egypt: Cairo, Luxor & Aswan (8 Days)
**Best for:** First-time visitors | **Price:** From $1,299/person

This comprehensive tour covers all the highlights:
- Great Pyramids of Giza and the Sphinx
- Egyptian Museum (including King Tut's treasures)
- Luxor Temple and Karnak
- Valley of the Kings
- Aswan High Dam and Philae Temple

**Why we recommend it:** Perfect introduction to Egypt with the ideal balance of guided tours and free time.

[Book Classic Egypt Tour →](/tours/)

---

### 2. Luxury Nile Cruise Experience (5 Days)
**Best for:** Couples and luxury travelers | **Price:** From $1,899/person

Float down the Nile in style aboard a 5-star cruise ship:
- Luxor to Aswan route (or reverse)
- All meals included with Egyptian and international cuisine
- Stops at Edfu and Kom Ombo temples
- Onboard entertainment and spa services
- Private balcony cabins

[Browse Nile Cruises →](/tours/)

---

### 3. Cairo City Break (4 Days)
**Best for:** Weekend travelers | **Price:** From $599/person

Intensive Cairo experience covering Giza Pyramids, Egyptian Museum, Khan el-Khalili bazaar, Coptic Cairo, and Saqqara.

[Explore Cairo Tours →](/tours/)

---

### 4. Red Sea Beach & Desert Safari (7 Days)
**Best for:** Adventure seekers | **Price:** From $899/person

Combine relaxation with adventure - 4 nights at Hurghada or Sharm el-Sheikh, snorkeling, quad biking, and Bedouin dinner under the stars.

[View Beach Tours →](/tours/)

---

### 5. Budget Backpacker Egypt (10 Days)
**Best for:** Solo travelers | **Price:** From $499/person

See Egypt without breaking the bank with clean hostels, local transportation, street food tours, and flexible itineraries.

---

## How to Choose the Right Tour

### Consider Your Budget
- **Budget ($500-$1,000):** Backpacker tours, Cairo-only trips
- **Mid-range ($1,000-$2,000):** Classic tours with good hotels
- **Luxury ($2,000+):** Nile cruises, private guides, 5-star hotels

### Best Time to Visit Egypt in 2026

| Season | Months | Weather | Crowds | Prices |
|--------|--------|---------|--------|--------|
| Peak | Oct-Feb | Cool (15-25°C) | High | $$$ |
| Shoulder | Mar-Apr, Sep | Warm (25-30°C) | Medium | $$ |
| Low | May-Aug | Hot (35-45°C) | Low | $ |

**Our recommendation:** Book for October-November 2026 for ideal weather and reasonable prices.

---

## Book Your Egypt Tour Today

Ready to explore the land of the pharaohs? Browse our curated selection of tours:

- [All Egypt Tours](/tours/)
- [Find Accommodations](/accommodations/)
- [Contact Us](/contact/)

*Last updated: January 2026*'''
        },

        # Article 2: Egypt on a Budget
        {
            'slug': 'egypt-on-a-budget-2026-travel-guide',
            'title': 'Egypt on a Budget 2026: How to Travel Egypt for Under $50/Day',
            'excerpt': 'Complete guide to budget travel in Egypt. Save money on accommodation, food, transport, and attractions while experiencing the best of ancient Egypt.',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'meta_description': 'Egypt budget travel guide 2026: Tips for traveling Egypt under $50/day. Cheap hotels, free attractions, local food, and money-saving hacks.',
            'meta_keywords': 'egypt budget travel, cheap egypt trip, egypt backpacking, budget cairo, egypt travel costs',
            'tags': 'budget travel, backpacking, cheap egypt, money saving',
            'is_featured': False,
            'content': '''## Can You Really Travel Egypt on a Budget?

**Absolutely yes!** Egypt is one of the most affordable destinations in the world for travelers. While luxury options exist, you can easily explore this ancient land for $30-50 per day including accommodation, food, and attractions.

### Daily Budget Breakdown

| Category | Budget | Mid-Range | Luxury |
|----------|--------|-----------|--------|
| Accommodation | $10-20 | $40-80 | $150+ |
| Food | $5-10 | $15-30 | $50+ |
| Transport | $3-5 | $10-20 | $50+ |
| Attractions | $10-15 | $20-30 | $50+ |
| **Daily Total** | **$28-50** | **$85-160** | **$300+** |

---

## Cheap Accommodation in Egypt

### Hostels ($8-15/night)
- **Cairo:** Wake Up! Cairo, Meramees Hostel, Australian Hostel
- **Luxor:** Bob Marley House, Nefertiti Hotel
- **Aswan:** Keylany Hotel, Memnon Hotel

### Budget Hotels ($15-30/night)
Many 3-star hotels offer excellent value:
- Clean rooms with AC and private bathroom
- Often include breakfast
- Great locations near attractions

[Browse Budget Hotels →](/accommodations/)

### Money-Saving Tips
1. **Book in advance** - Prices drop 20-30% online
2. **Travel in low season** (May-September) - Up to 50% off
3. **Negotiate** - Always ask for discounts, especially for multiple nights
4. **Stay near train stations** - Convenient and affordable areas

---

## Cheap Food in Egypt

### Street Food (EGP 20-50 / $0.50-1.50)
- **Koshari** - Egypt's national dish (rice, pasta, lentils, chickpeas)
- **Ful Medames** - Fava bean stew with bread
- **Ta'ameya** - Egyptian falafel
- **Shawarma** - Meat wrap sandwiches

### Local Restaurants (EGP 50-100 / $1.50-3)
- Look for places where locals eat
- Order set meals for better value
- Drink tap water (safe in most tourist areas) or buy large bottles

### Where to Eat Cheap in Cairo
1. **Downtown Cairo** - Dozens of koshari shops
2. **Khan el-Khalili area** - Local eateries between tourist cafes
3. **Zamalek** - Good mid-range options

---

## Free & Cheap Attractions

### Completely Free
- Walking through Islamic Cairo's medieval streets
- Khan el-Khalili bazaar (window shopping!)
- Nile Corniche sunset walks
- Coptic Cairo churches
- Al-Azhar Park viewpoints

### Cheap Attractions (Under $5)
- Egyptian Museum: EGP 200 ($6) - Soon moving to Grand Egyptian Museum
- Pyramids of Giza: EGP 200 ($6)
- Valley of the Kings: EGP 240 ($7)
- Karnak Temple: EGP 200 ($6)

### Student Discounts
Bring an ISIC card for 50% off most attractions!

---

## Cheap Transportation

### Cairo Metro ($0.15-0.30)
The cheapest way to get around Cairo. Clean, fast, and covers major areas.

### Microbus ($0.10-0.50)
Local minivans - very cheap but confusing for tourists. Ask locals for help.

### Trains
- Cairo to Luxor: From EGP 100 ($3) in 2nd class
- Cairo to Aswan: From EGP 120 ($4) in 2nd class
- Book at the station for cheapest prices

### Uber/Careem
Surprisingly affordable in Egypt:
- Cairo airport to downtown: ~$5-8
- Short city trips: ~$1-3

---

## Budget Itinerary: 10 Days for Under $500

### Days 1-3: Cairo ($120)
- Hostel: $30 (3 nights)
- Pyramids + Museum: $15
- Food: $30
- Transport: $10
- Misc: $35

### Days 4-6: Luxor ($100)
- Train from Cairo: $5
- Budget hotel: $40 (3 nights)
- West Bank tour: $20
- Karnak + Luxor Temple: $15
- Food: $20

### Days 7-8: Aswan ($70)
- Train from Luxor: $3
- Hotel: $25 (2 nights)
- Philae Temple: $10
- Felucca ride: $10
- Food: $15
- Nubian village visit: $7

### Days 9-10: Return to Cairo ($60)
- Train: $5
- Hostel: $20
- Egyptian Museum: $7
- Shopping/souvenirs: $20
- Airport transfer: $8

**Total: ~$350-400** (leaving buffer for unexpected expenses)

---

## Money-Saving Hacks

1. **Exchange money at official exchange offices** - Better rates than hotels/airports
2. **Carry small bills** - Easier for tipping and bargaining
3. **Bargain everything** - Start at 30% of asking price
4. **Book Nile felucca, not cruise** - Same experience, 10% of the price
5. **Visit sites early morning** - Avoid tours and heat
6. **Use overnight trains** - Save on accommodation
7. **Join free walking tours** - Tip-based, usually excellent

---

## What NOT to Cheap Out On

- **Travel insurance** - Medical care can be expensive
- **Reputable guides** at the Pyramids - Avoid scams
- **Bottled water** in summer - Stay hydrated
- **Comfortable shoes** - You'll walk a lot

---

## Start Planning Your Budget Egypt Trip

[Browse Budget Accommodations →](/accommodations/)
[Find Affordable Tours →](/tours/)
[Contact Us for Tips →](/contact/)

*Prices updated January 2026. Exchange rate: 1 USD = ~30 EGP*'''
        },

        # Article 3: Nile Cruise Guide
        {
            'slug': 'nile-cruise-guide-2026-everything-you-need-to-know',
            'title': 'Nile Cruise Guide 2026: Everything You Need to Know',
            'excerpt': 'Complete guide to Nile River cruises in Egypt. Compare cruise options, routes, prices, and learn what to expect on this unforgettable journey.',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'meta_description': 'Nile cruise guide 2026: Compare luxury to budget cruises, routes from Luxor to Aswan, what to pack, and insider tips for the best experience.',
            'meta_keywords': 'nile cruise, egypt nile river cruise, luxor aswan cruise, nile cruise prices, best nile cruise',
            'tags': 'nile cruise, luxor, aswan, egypt cruise, river cruise',
            'is_featured': True,
            'content': '''## Why Take a Nile Cruise?

A Nile cruise is the quintessential Egypt experience. Floating down the same river that carried pharaohs and Cleopatra, you'll visit ancient temples while enjoying modern luxury. It's history, relaxation, and adventure combined.

### Quick Facts
- **Route:** Luxor ↔ Aswan (or reverse)
- **Duration:** 3-7 nights (4 nights most popular)
- **Distance:** ~230 km (143 miles)
- **Best time:** October to April
- **Price range:** $200-$500+/night depending on luxury level

---

## Types of Nile Cruises

### 1. Large Cruise Ships (100-150 passengers)
**Best for:** First-timers, families, social travelers

**Pros:**
- Most affordable option
- Full amenities (pool, spa, restaurants)
- Organized shore excursions
- Entertainment onboard

**Cons:**
- Less personal attention
- Fixed schedules
- Can feel crowded at sites

**Price:** $80-200/night

---

### 2. Boutique Cruise Ships (40-80 passengers)
**Best for:** Couples, discerning travelers

**Pros:**
- Better service-to-guest ratio
- Higher quality food and cabins
- More intimate atmosphere
- Often include Egyptologist guides

**Cons:**
- Higher price point
- Book up quickly

**Price:** $200-400/night

---

### 3. Luxury Dahabiyas (8-20 passengers)
**Best for:** Honeymooners, luxury seekers

**Pros:**
- Traditional sailing boats with modern comfort
- Extremely personalized service
- Flexible schedules
- Access to smaller sites others miss
- Romantic atmosphere

**Cons:**
- Most expensive option
- Limited availability
- Slower travel (relies on wind/motor)

**Price:** $400-800/night

---

### 4. Felucca Sailboats (2-8 passengers)
**Best for:** Budget travelers, adventurers

**Pros:**
- Authentic Egyptian experience
- Very affordable
- Sleeping under the stars
- Flexible and casual

**Cons:**
- Basic facilities (no bathroom, cold at night)
- Only Aswan area typically
- Weather dependent

**Price:** $20-50/night

---

## The Classic Route: Luxor to Aswan

### Day 1: Luxor
- Board ship and settle into cabin
- Lunch onboard
- Visit Karnak Temple (afternoon)
- Welcome dinner and briefing

### Day 2: Luxor West Bank
- Early morning hot air balloon ride (optional)
- Valley of the Kings
- Temple of Hatshepsut
- Colossi of Memnon
- Sail toward Esna

### Day 3: Edfu
- Pass through Esna Lock
- Temple of Horus at Edfu (best-preserved temple in Egypt)
- Afternoon sailing
- Onboard entertainment

### Day 4: Kom Ombo
- Kom Ombo Temple (unique double temple)
- Continue to Aswan
- Afternoon at leisure or optional felucca ride
- Nubian dinner show

### Day 5: Aswan
- Philae Temple (on an island)
- High Dam
- Optional: Abu Simbel day trip
- Disembark

---

## What's Included (Typically)

### Standard Inclusions:
- Cabin accommodation
- All meals (breakfast, lunch, dinner)
- Guided temple visits
- Entrance fees to sites on itinerary
- Onboard entertainment
- English-speaking guide

### Usually Extra:
- Drinks (alcoholic and soft drinks)
- Tips for crew and guides
- Optional excursions (Abu Simbel, hot air balloon)
- Spa treatments
- Laundry service

---

## How to Choose the Best Cruise

### 1. Check Recent Reviews
Look for reviews from the last 6 months on TripAdvisor. Ships change management/quality.

### 2. Compare Cabin Types
- **Standard:** Interior or small windows, basic amenities
- **Superior:** Larger windows, better location
- **Suite:** Private balcony, sitting area, premium location

### 3. Verify the Itinerary
Some cruises skip sites or rush through them. Compare included temples.

### 4. Ask About Guide Quality
The guide makes or breaks the experience. Ask if they're certified Egyptologists.

### 5. Check Food Options
If you have dietary restrictions, confirm in advance.

---

## Packing List for Nile Cruise

### Essentials
- Passport (needed at checkpoints)
- Comfortable walking shoes
- Sun hat and sunglasses
- Sunscreen (SPF 50+)
- Light layers (cold at night, hot during day)
- Modest clothing for temple visits

### Nice to Have
- Binoculars for bird watching
- Camera with zoom lens
- Portable charger
- Motion sickness medication
- Egyptian pounds for tips

### Dress Code
- Daytime: Casual, comfortable
- Dinner: Smart casual (no shorts/flip-flops)
- Gala night: Semi-formal (some ships)

---

## Tips for the Best Experience

1. **Book the top deck** - Best views and less engine noise
2. **Take the hot air balloon** - Sunrise over Luxor is magical
3. **Visit Abu Simbel** - Worth the early wake-up
4. **Bring binoculars** - Amazing bird life along the Nile
5. **Tip appropriately** - $5-10/day for cabin staff, $20-30 total for guide
6. **Stay hydrated** - The sun is intense
7. **Book directly or through reputable agent** - Avoid last-minute scams

---

## Book Your Nile Cruise

Ready to sail the Nile? We can help you find the perfect cruise:

[Browse Nile Cruises →](/tours/)
[Contact Our Travel Experts →](/contact/)
[Read More Egypt Guides →](/blog/)

*Updated January 2026*'''
        },

        # Article 4: Egypt Visa Guide
        {
            'slug': 'egypt-visa-guide-2026-requirements-by-nationality',
            'title': 'Egypt Visa Guide 2026: Requirements, Costs & How to Apply',
            'excerpt': 'Complete Egypt visa guide for 2026. Learn about visa requirements by nationality, e-Visa application, visa on arrival, and entry requirements.',
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
            'meta_description': 'Egypt visa requirements 2026: Complete guide to tourist visas, e-Visa application, visa on arrival, costs, and requirements by nationality.',
            'meta_keywords': 'egypt visa, egypt e-visa, egypt visa on arrival, egypt visa requirements, egypt entry requirements',
            'tags': 'visa, egypt visa, e-visa, travel documents, entry requirements',
            'is_featured': False,
            'content': '''## Egypt Visa Overview 2026

Good news: Egypt has made it easier than ever for tourists to visit. Most nationalities can get a visa on arrival or apply for an e-Visa online before traveling.

### Quick Summary

| Visa Type | Processing | Cost | Valid For |
|-----------|------------|------|-----------|
| Visa on Arrival | Immediate | $25 | 30 days |
| e-Visa | 5-7 days | $25-60 | 30-90 days |
| Embassy Visa | 1-2 weeks | $25-60 | 30-90 days |

---

## Who Needs a Visa for Egypt?

### Visa-Free Entry (No Visa Required)
Citizens of these countries can enter Egypt without a visa for short stays:
- Bahrain, Kuwait, Oman, Saudi Arabia, UAE (up to 6 months)
- Hong Kong, Macau (up to 14 days)

### Visa on Arrival Available
Most tourists can get a visa stamped in their passport at Egyptian airports:

**Eligible Countries Include:**
- United States
- United Kingdom
- Canada
- Australia
- All EU countries
- Japan, South Korea
- Malaysia
- And 40+ more countries

**Cost:** $25 USD (single entry, 30 days)

### e-Visa Recommended
While visa on arrival works, we recommend the e-Visa because:
- Skip the airport queue
- Pay online in advance
- Have documentation ready
- Peace of mind before travel

---

## How to Apply for Egypt e-Visa

### Step 1: Go to Official Website
Visit: **https://www.visa2egypt.gov.eg**

⚠️ **Warning:** Only use the official government website. Many scam sites charge excessive fees.

### Step 2: Create Account
- Enter email address
- Create password
- Verify email

### Step 3: Fill Application
Required information:
- Full name (as on passport)
- Date of birth
- Nationality
- Passport number and expiry
- Travel dates
- Accommodation address in Egypt
- Profession

### Step 4: Upload Documents
- Passport photo page (clear scan)
- Recent passport-style photo
- Return flight booking (sometimes required)

### Step 5: Pay Fee
- Single entry (30 days): $25
- Multiple entry (30 days each, 6 months validity): $60

### Step 6: Receive e-Visa
- Processing: 5-7 business days
- Sent to your email as PDF
- Print and carry with passport

---

## Visa on Arrival Process

### At the Airport
1. **Before immigration:** Find the bank kiosk
2. **Buy visa stamp:** $25 USD cash (exact change helps)
3. **Stick stamp in passport:** The bank gives you a sticker
4. **Go to immigration:** Officer stamps your visa

### Tips for Visa on Arrival
- Bring $25 in USD bills (cleanest method)
- Euros, GBP also accepted but USD preferred
- ATMs available if you forget cash
- Lines can be long in peak season (Oct-Feb)

---

## Entry Requirements (All Visitors)

### Passport Requirements
- Valid for at least 6 months from entry date
- At least 2 blank pages
- Good condition (no damage)

### Other Requirements
- Return or onward flight ticket
- Proof of accommodation (hotel booking)
- Sufficient funds for stay
- No Israeli stamps? **Not a problem** - Egypt has peace with Israel

### COVID-19 Requirements (As of 2026)
- **Vaccination:** Not currently required
- **Testing:** Not currently required
- **Health insurance:** Recommended but not mandatory

*Check latest requirements before travel as rules can change.*

---

## Special Visa Situations

### Sinai-Only Permit (Free)
If you're ONLY visiting the Sinai Peninsula (Sharm el-Sheikh, Dahab, Taba):
- Free entry permit at airport
- Valid for 14 days
- Cannot leave Sinai area

**Note:** If you plan to visit Cairo, Luxor, or anywhere outside Sinai, get a full visa.

### Extending Your Visa
Need more than 30 days?
1. Go to Mogamma building in Cairo or passport office in other cities
2. Bring: passport, photos, copy of passport, hotel booking
3. Pay extension fee (~$25)
4. Can extend up to 3-6 months total

### Overstaying Your Visa
- Fine at airport when leaving (~$50-150)
- Possible questioning/detention
- May affect future visa applications
- **Not recommended** - just extend legally

---

## Visa Requirements by Nationality

### United States
- e-Visa or visa on arrival
- Cost: $25
- Processing: Instant (arrival) or 5-7 days (e-Visa)

### United Kingdom
- e-Visa or visa on arrival
- Cost: $25
- Processing: Instant (arrival) or 5-7 days (e-Visa)

### Canada
- e-Visa or visa on arrival
- Cost: $25

### Australia/New Zealand
- e-Visa or visa on arrival
- Cost: $25

### European Union
- e-Visa or visa on arrival
- Cost: $25

### India
- Must apply at Egyptian Embassy before travel
- Cost: ~$50-80
- Processing: 5-10 business days

### China
- e-Visa or Embassy visa
- Cost: $25-60

### Philippines
- Embassy visa required
- Cost: ~$50

### Pakistan
- Embassy visa required
- Cost: ~$60
- Additional security checks may apply

---

## Frequently Asked Questions

### Can I get a visa at Cairo Airport?
Yes, visa on arrival is available at Cairo, Hurghada, Sharm el-Sheikh, Luxor, and Aswan airports.

### How long can I stay in Egypt?
Standard tourist visa: 30 days. Can extend up to 6 months.

### Do I need a visa for a layover?
If you stay in the airport transit area and leave within 24 hours, no visa needed. If you exit the airport, you need a visa.

### Can I work on a tourist visa?
No. Tourist visas are for tourism only. Working illegally can result in deportation and ban.

### Is Egypt safe to visit?
Yes, tourist areas are safe and well-policed. Follow normal travel precautions.

---

## Plan Your Egypt Trip

Now that you know about visas, start planning your adventure:

[Browse Egypt Tours →](/tours/)
[Find Hotels →](/accommodations/)
[Read Travel Guides →](/blog/)
[Contact Us →](/contact/)

*Information current as of January 2026. Always verify with official sources before travel.*'''
        },
    ]

    for article in articles:
        post, created = BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'content': article['content'],
                'excerpt': article['excerpt'],
                'image_url': article['image_url'],
                'meta_description': article['meta_description'],
                'meta_keywords': article['meta_keywords'],
                'tags': article['tags'],
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': timezone.now(),
            }
        )
        status = 'Created' if created else 'Updated'
        print(f"{status}: {article['title'][:50]}...")

if __name__ == '__main__':
    create_articles()
    print("\nAll articles created/updated successfully!")
