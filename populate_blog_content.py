#!/usr/bin/env python
"""
Populate Blog Content Script - Egy360
Adds comprehensive blog articles about Egyptian tourism
"""
import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import BlogCategory, BlogPost
from destinations.models import City

def create_blog_categories():
    """Create blog categories"""
    categories = [
        {
            'name': 'Travel Guides',
            'description': 'Comprehensive guides to Egyptian cities and attractions'
        },
        {
            'name': 'Safety & Scams',
            'description': 'Tips to avoid tourist scams and stay safe in Egypt'
        },
        {
            'name': 'Culture & History',
            'description': 'Learn about Egyptian culture, history, and traditions'
        },
        {
            'name': 'Travel Tips',
            'description': 'Practical advice for traveling in Egypt'
        },
        {
            'name': 'Food & Dining',
            'description': 'Egyptian cuisine and where to eat'
        },
        {
            'name': 'Budget Travel',
            'description': 'How to travel Egypt on a budget'
        }
    ]

    created_categories = {}
    for cat_data in categories:
        category, created = BlogCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories[cat_data['name']] = category
        print(f"{'Created' if created else 'Found'} category: {category.name}")

    return created_categories

def get_or_create_author():
    """Get or create blog author"""
    author, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@360egy.com',
            'first_name': 'Egy360',
            'last_name': 'Team',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        author.set_password('admin123')
        author.save()
        print(f"Created admin user")
    return author

def create_blog_posts(author, categories):
    """Create comprehensive blog posts"""

    # Get cities for linking
    try:
        cairo = City.objects.get(name='Cairo')
    except City.DoesNotExist:
        cairo = None

    try:
        luxor = City.objects.get(name='Luxor')
    except City.DoesNotExist:
        luxor = None

    try:
        alexandria = City.objects.get(name='Alexandria')
    except City.DoesNotExist:
        alexandria = None

    try:
        aswan = City.objects.get(name='Aswan')
    except City.DoesNotExist:
        aswan = None

    posts = [
        {
            'title': 'Complete Guide to Visiting Cairo: Everything You Need to Know',
            'category': categories['Travel Guides'],
            'related_city': cairo,
            'excerpt': 'Planning your Cairo adventure? This comprehensive guide covers the best attractions, where to stay, how to get around, and essential tips for first-time visitors to Egypt\'s bustling capital.',
            'content': '''
# Complete Guide to Visiting Cairo

Cairo, the sprawling capital of Egypt, is a city where ancient history meets modern chaos. With over 20 million residents, it's one of the world's largest and most vibrant cities. Here's everything you need to know for an unforgettable visit.

## Must-See Attractions

### The Pyramids of Giza
No visit to Cairo is complete without seeing the last remaining Wonder of the Ancient World. The Pyramids of Giza stand just outside the city and are accessible via taxi or organized tour. Visit early morning (7-8 AM) to avoid crowds and heat.

**Tips:**
- Hire a licensed guide at the entrance (negotiate price beforehand)
- Bring water and sunscreen
- Budget 3-4 hours for the visit
- Don't accept "free" camel rides - they're never free!

### The Egyptian Museum
Home to the world's largest collection of ancient Egyptian artifacts, including Tutankhamun's treasures. Allow 2-3 hours minimum.

**Visitor Information:**
- Location: Tahrir Square
- Hours: 9 AM - 5 PM daily
- Price: Around 200 EGP for foreigners
- Photography fee: Extra 50 EGP

### Khan el-Khalili Bazaar
Cairo's famous souk (market) has been trading since the 14th century. Perfect for souvenirs, spices, jewelry, and experiencing local culture.

**Shopping Tips:**
- Bargain hard - start at 50% of asking price
- Visit El Fishawy Café for traditional mint tea
- Keep valuables secure in crowded areas

## Where to Stay

### Luxury ($$$$)
- **Four Seasons Cairo at Nile Plaza** - Stunning Nile views, excellent service
- **Marriott Mena House** - Historic hotel with pyramid views

### Mid-Range ($$$)
- **Steigenberger Hotel El Tahrir** - Central location near Egyptian Museum
- **Hilton Cairo Zamalek** - Quiet island neighborhood

### Budget ($-$$)
- **Wake Up! Cairo Hostel** - Downtown, social atmosphere
- **Australian Hostels Downtown** - Clean, friendly, rooftop terrace

## Getting Around

### Transportation Options
1. **Uber/Careem** - Cheapest and most reliable
2. **Metro** - Efficient for long distances, very cheap (5 EGP per ride)
3. **Taxi** - Negotiate price before entering (cash only)
4. **Walking** - Best for Downtown and Islamic Cairo areas

**Important:** Avoid unlicensed "black taxis" - use ride-hailing apps instead!

## Food & Dining

### Must-Try Egyptian Dishes
- **Koshari** - Egypt's national dish (lentils, rice, pasta, tomato sauce)
- **Ful Medames** - Slow-cooked fava beans (traditional breakfast)
- **Ta'ameya** - Egyptian falafel made from fava beans
- **Mahshi** - Stuffed vegetables
- **Om Ali** - Traditional Egyptian dessert

### Recommended Restaurants
- **Abou Tarek** - Famous for koshari (Downtown)
- **Felfela** - Authentic Egyptian food, tourist-friendly
- **Sequoia** - Upscale Nile-side dining in Zamalek
- **Street food** - Safe and delicious, try from busy vendors

## Safety Tips

1. **Dress modestly** - Especially when visiting mosques
2. **Avoid tap water** - Stick to bottled water
3. **Be firm with touts** - "La, shukran" (No, thank you)
4. **Keep small bills** - For tips and small purchases
5. **Register with embassy** - If staying long-term

## Best Time to Visit

- **October-April:** Perfect weather (20-25°C)
- **May-September:** Very hot (35-40°C) but fewer tourists
- **Ramadan:** Special atmosphere but shorter opening hours

## Budget Planning

### Daily Costs (Per Person)
- **Budget:** $20-30 (street food, hostels, public transport)
- **Mid-Range:** $50-80 (decent restaurants, mid-range hotels, tours)
- **Luxury:** $150+ (5-star hotels, private tours, fine dining)

## Essential Arabic Phrases

- **Salaam Alaikum** - Hello
- **Shukran** - Thank you
- **Bikam da?** - How much is this?
- **La** - No
- **Yalla** - Let's go/Come on
- **Mafeesh mushkila** - No problem

## Final Tips

1. Download offline maps (Google Maps works well)
2. Get a local SIM card at the airport (Vodafone or Orange)
3. Keep your passport safe - carry a copy
4. Bargain everywhere except in labeled-price stores
5. Be patient - "Egyptian time" is real!

Cairo is overwhelming, chaotic, and absolutely magical. Embrace the chaos, stay alert, and you'll have an incredible adventure in this ancient city!

**Need help planning your Cairo trip? Book verified tours and hotels through Egy360 - scam-free guaranteed!**
''',
            'tags': 'Cairo, Travel Guide, Egypt, Pyramids, Tourism',
            'meta_description': 'Complete guide to visiting Cairo: attractions, hotels, transport, safety tips, budget planning. Everything you need for your Cairo adventure.',
            'meta_keywords': 'Cairo travel guide, visiting Cairo, Egypt tourism, Pyramids of Giza, Egyptian Museum, Cairo tips',
            'is_featured': True,
            'views_count': 1250,
            'likes_count': 89
        },
        {
            'title': '10 Common Tourist Scams in Egypt and How to Avoid Them',
            'category': categories['Safety & Scams'],
            'related_city': cairo,
            'excerpt': 'Egypt is generally safe, but tourists can be targets for scams. Learn about the most common schemes and how to protect yourself while enjoying your Egyptian adventure.',
            'content': '''
# 10 Common Tourist Scams in Egypt and How to Avoid Them

Egypt is an incredible destination, but like any major tourist hotspot, scammers target unwary visitors. Here's how to protect yourself while still enjoying authentic Egyptian hospitality.

## 1. The "Free" Camel Ride

**The Scam:** At the Pyramids, someone offers you a "free" camel ride or photo opportunity. Once you're on the camel, they demand exorbitant payment (sometimes $100+) and refuse to let you down until you pay.

**How to Avoid:**
- Never accept "free" anything from strangers
- If you want a camel ride, arrange it with official tour guides
- Agree on price IN WRITING before getting on
- Keep your money hidden until service is complete

**Egy360 Tip:** Book pyramid tours through our verified partners for fixed, fair pricing!

## 2. Papyrus Shop "Detours"

**The Scam:** Your taxi driver or tour guide insists on stopping at a "government papyrus shop" or "perfume factory." These pay huge commissions to drivers, and prices are 5-10x market rate.

**How to Avoid:**
- Tell drivers firmly: NO STOPS
- Say you've already been to these shops
- Shop at Khan el-Khalili instead
- Use Uber/Careem to avoid this scam

**Fair Price:** Real papyrus bookmarks: 10-20 EGP, paintings: 50-150 EGP at Khan el-Khalili.

## 3. The Fake "Closed Today" Scam

**The Scam:** Someone (appearing official) tells you the attraction you're heading to is "closed today" but they can take you somewhere else (where they earn commission).

**How to Avoid:**
- Check official opening hours online beforehand
- Walk to the attraction entrance yourself
- Ignore people stopping you en route
- Ask at your hotel, not random people on the street

## 4. Taxi Meter "Broken"

**The Scam:** Taxi drivers claim their meter is broken and quote inflated flat rates (often 5-10x the real price).

**How to Avoid:**
- Use Uber or Careem ALWAYS
- If you must use taxi, agree on price before entering
- Learn reasonable prices (downtown to Pyramids: 50-70 EGP)
- Have exact change ready

**Best Solution:** Download Uber and Careem apps at the airport. Your trip will cost 50-70% less than street taxis!

## 5. The "Helpful" Photography Scam

**The Scam:** Someone offers to take your photo, then demands payment. Or they position you for a "better angle" with their camel/horse/shop in the background, then demand money.

**How to Avoid:**
- Politely decline photography help
- Use a selfie stick or tripod
- Only ask other tourists to take photos
- Say "La shukran" (No thank you) firmly

## 6. Overpriced "Tourist" Restaurants

**The Scam:** Restaurants near major attractions have no prices listed, then charge 10x normal rates. A tea that should cost 5 EGP becomes 50 EGP.

**How to Avoid:**
- Check prices BEFORE ordering
- Walk 2-3 blocks away from attractions
- Eat where locals eat
- Download a menu photo if prices aren't listed
- Use Egy360's verified restaurant recommendations

**Normal Prices:**
- Tea/coffee: 5-10 EGP
- Koshari: 20-30 EGP
- Full meal: 50-100 EGP

## 7. The Currency Confusion

**The Scam:** Vendors quote prices in dollars/euros but give change in Egyptian Pounds at terrible exchange rates. Or they claim you paid in pounds when you gave dollars.

**How to Avoid:**
- Use Egyptian Pounds for everything
- Clarify currency BEFORE transaction
- Keep different currencies in separate pockets
- Get change in the same currency you paid

**Exchange Rate (approx):** $1 USD = 30 EGP

## 8. Fake Entrance Fees

**The Scam:** Someone at pyramid/tomb entrances claims you need to pay them directly, or adds fake fees to the official price.

**How to Avoid:**
- Pay ONLY at official ticket booths
- Know the real prices beforehand
- Official tickets have security features
- Ignore people demanding "fees" before the entrance

**Real Entry Fees (2024):**
- Giza Pyramids: 200 EGP
- Egyptian Museum: 200 EGP
- Luxor temples: 200-300 EGP each

## 9. The Sob Story Scam

**The Scam:** Someone befriends you, shares a sad story (sick child, need medicine), then asks for money. Or they give you a "gift" then demand payment.

**How to Avoid:**
- Never accept unsolicited gifts
- Be friendly but firm with boundaries
- Give to registered charities, not individuals
- Learn the phrase: "Mafeesh fulus" (I have no money)

## 10. Baksheesh (Tip) Demands

**The Scam:** People demand tips for unwanted "services" - pointing at something, opening a door, taking a photo of you, or simply existing near you.

**How to Avoid:**
- Only tip for actual requested services
- Say "La, shukran" repeatedly
- Walk away confidently
- Tip appropriately when service is good (5-10 EGP for small services)

**When to Actually Tip:**
- Restaurant servers: 10-15%
- Hotel porters: 5-10 EGP per bag
- Tour guides: 50-100 EGP for good service
- Drivers: 10-20 EGP
- Bathroom attendants: 2-5 EGP

## General Anti-Scam Strategies

### DO:
✓ Research prices beforehand
✓ Use Uber/Careem exclusively
✓ Book tours through verified companies (like Egy360!)
✓ Keep small bills for legitimate expenses
✓ Trust your instincts
✓ Ask your hotel staff for price guidance

### DON'T:
✗ Accept "free" anything
✗ Stop at shops your driver suggests
✗ Pay for services you didn't request
✗ Believe "closed today" claims
✗ Flash large amounts of cash
✗ Let someone "hold" your money

## Stay Alert, Stay Safe

Most Egyptians are genuinely warm and hospitable. These scams are run by a small minority targeting tourists. By staying informed and vigilant, you can avoid these schemes while enjoying authentic Egyptian culture.

**Travel Smart:** Book your Egypt accommodations and tours through Egy360 - we verify every provider to protect you from scams!
''',
            'tags': 'Egypt, Scams, Safety, Tourist Scams, Travel Tips, Cairo',
            'meta_description': 'Learn the 10 most common tourist scams in Egypt and how to avoid them. Essential safety guide for travelers to Cairo, Luxor, and Egypt.',
            'meta_keywords': 'Egypt scams, tourist scams Egypt, Cairo scams, Egypt safety, avoid scams Egypt',
            'is_featured': True,
            'views_count': 2134,
            'likes_count': 156
        },
        {
            'title': 'Best Time to Visit Egypt: Month-by-Month Weather Guide',
            'category': categories['Travel Tips'],
            'related_city': None,
            'excerpt': 'Planning your Egypt trip? Our month-by-month guide covers weather, crowds, prices, and special events to help you choose the perfect time for your Egyptian adventure.',
            'content': '''
# Best Time to Visit Egypt: Month-by-Month Guide

Choosing when to visit Egypt can make or break your trip. Here's a comprehensive breakdown of what to expect each month.

## Quick Answer

**Best Overall:** October - April (peak season)
**Best Value:** May - September (hot but cheaper)
**Best for Nile Cruises:** October - November, February - April
**Best for Red Sea Diving:** March - May, September - November

## Month-by-Month Breakdown

### January ⭐⭐⭐⭐⭐

**Weather:** Cool and pleasant (15-23°C / 59-73°F)
**Crowds:** High
**Prices:** Expensive

Perfect weather for sightseeing! Comfortable temperatures at temples and pyramids. Pack layers for cool evenings.

**Pros:** Best weather for Upper Egypt (Luxor, Aswan)
**Cons:** High tourist numbers, elevated prices
**Best For:** First-time visitors, archaeological sites

### February ⭐⭐⭐⭐⭐

**Weather:** Mild (16-24°C / 61-75°F)
**Crowds:** High
**Prices:** High

Similar to January - excellent conditions for exploration.

**Pros:** Comfortable temperatures, blooming flowers in Alexandria
**Cons:** Still peak season pricing
**Best For:** Nile cruises, temple visits

### March ⭐⭐⭐⭐

**Weather:** Warming up (18-27°C / 64-81°F)
**Crowds:** Medium-High
**Prices:** Medium-High

Spring begins! Generally excellent, but occasional sandstorms (khamsin winds).

**Pros:** Good weather, slightly fewer crowds than Jan/Feb
**Cons:** Possible sandstorms
**Best For:** Red Sea resorts, balanced sightseeing

### April ⭐⭐⭐⭐

**Weather:** Warm (21-30°C / 70-86°F)
**Crowds:** Medium
**Prices:** Medium

Transition month - still comfortable but getting warmer.

**Pros:** Beautiful weather, Easter celebrations
**Cons:** Increasing temperatures in Upper Egypt
**Best For:** Cairo and Mediterranean coast

### May ⭐⭐⭐

**Weather:** Hot (24-35°C / 75-95°F)
**Crowds:** Low
**Prices:** Budget-friendly

Summer heat arrives. Start of low season.

**Pros:** Low prices, no crowds, great deals
**Cons:** Uncomfortably hot for long outdoor activities
**Best For:** Budget travelers, Red Sea beaches

### June ⭐⭐

**Weather:** Very hot (26-38°C / 79-100°F)
**Crowds:** Very low
**Prices:** Cheapest

Peak summer - sweltering temperatures.

**Pros:** Incredible deals, empty attractions
**Cons:** Dangerously hot midday
**Best For:** Beach resorts, early morning starts

### July ⭐⭐

**Weather:** Extremely hot (27-40°C / 81-104°F)
**Crowds:** Very low
**Prices:** Cheapest

Hottest month - not recommended for archaeological sites.

**Pros:** Massive discounts (50%+ off hotels)
**Cons:** Too hot for comfortable sightseeing
**Best For:** Air-conditioned museums, Red Sea diving

### August ⭐⭐

**Weather:** Extremely hot (27-40°C / 81-104°F)
**Crowds:** Very low
**Prices:** Cheapest

Similar to July - scorching temperatures.

**Pros:** Rock-bottom prices, no lines
**Cons:** Exhausting heat, some services reduced
**Best For:** Die-hard budget travelers

### September ⭐⭐⭐

**Weather:** Hot but cooling (25-36°C / 77-97°F)
**Crowds:** Low
**Prices:** Budget-friendly

Shoulder season begins - still hot but manageable.

**Pros:** Prices still low, fewer crowds, cooling down
**Cons:** Still quite hot during day
**Best For:** Good balance of price and comfort

### October ⭐⭐⭐⭐⭐

**Weather:** Perfect (22-32°C / 72-90°F)
**Crowds:** Increasing
**Prices:** Medium

Goldilocks month - not too hot, not too crowded!

**Pros:** Excellent weather, prices not yet peaked
**Cons:** Popularity means booking ahead essential
**Best For:** Everything! Best overall month

### November ⭐⭐⭐⭐⭐

**Weather:** Ideal (19-28°C / 66-82°F)
**Crowds:** High
**Prices:** Medium-High

Another perfect month for Egypt exploration.

**Pros:** Beautiful weather, minimal rain
**Cons:** Getting crowded and expensive
**Best For:** Nile cruises, full Egypt itineraries

### December ⭐⭐⭐⭐

**Weather:** Cool (16-24°C / 61-75°F)
**Crowds:** Very high (holiday season)
**Prices:** Expensive

Peak tourist season + holidays = busy!

**Pros:** Great weather, festive atmosphere
**Cons:** Highest crowds and prices of the year
**Best For:** Holiday vacations (book 3-6 months ahead!)

## Special Considerations

### Ramadan (Dates vary - Islamic calendar)

**Impact:**
- Restaurants closed during day
- Shorter opening hours for attractions
- Special evening atmosphere and food
- Can be challenging for non-Muslims

**Tips:** Still worth visiting! Embrace the cultural experience. Carry water/snacks. Special Iftar meals are amazing!

### School Holidays

**Egyptian holidays:** Mid-year break (Jan-Feb) and summer (Jun-Aug)
**European holidays:** July-August, Christmas, Easter
**Plan around:** Book early and expect domestic crowds

## Regional Differences

### Cairo & Giza
**Best:** October - April
**Avoid:** June - August (too hot)

### Luxor & Aswan (Upper Egypt)
**Best:** November - February (cooler than Cairo)
**Avoid:** May - September (extreme heat)

### Alexandria & Mediterranean Coast
**Best:** June - September (beach weather)
**Avoid:** December - February (surprisingly cool and wet)

### Red Sea (Hurghada, Sharm el-Sheikh)
**Best:** Year-round! Sea temperature stays warm
**Diving Best:** March - May, Sept - Nov (best visibility)

### Western Desert
**Best:** October - March
**Avoid:** April - September (dangerously hot)

## Budget Optimization

### Cheapest Times:
1. June - August: 50-60% discounts
2. May & September: 30-40% discounts
3. Mid-January: Post-holiday prices drop

### Most Expensive:
1. Christmas - New Year: 100-150% markup
2. Easter week: 50-75% premium
3. February - March: Peak pricing

## Our Recommendations

### First-Time Visitors
**Choose:** October, November, February, or March
**Why:** Perfect balance of weather, crowds, and prices

### Budget Travelers
**Choose:** May or September
**Why:** Shoulder season discounts, tolerable heat

### Beach Lovers
**Choose:** June - September (Red Sea)
**Why:** Perfect beach weather, less crowded than Cairo

### Photographers
**Choose:** November - February
**Why:** Best light, clear skies, golden hour perfection

### Cultural Immersion
**Choose:** Ramadan (any month)
**Why:** Unique experience, special atmosphere, authentic culture

## Final Verdict

**Best Overall Month:** October (weather + value)
**Best Value Month:** September (cooling down, still cheap)
**Best Experience:** November (perfect weather, not too crowded)

## Booking Tips

1. **Book 3-6 months ahead** for peak season (Oct - Apr)
2. **Book 1-2 months ahead** for summer (May - Sep)
3. **Use Egy360** for verified hotels and tours at fair prices
4. **Avoid** last-minute booking during holidays

No matter when you visit, Egypt's ancient wonders are waiting! Plan smart and enjoy your adventure.

**Ready to book?** Find verified accommodations and tours on Egy360 - scam-free, guaranteed!
''',
            'tags': 'Egypt, Weather, Best Time to Visit, Travel Planning, Egypt Weather',
            'meta_description': 'Month-by-month guide to visiting Egypt. Weather, crowds, prices, and special events to plan your perfect Egyptian vacation.',
            'meta_keywords': 'best time visit Egypt, Egypt weather, when to visit Egypt, Egypt travel seasons, Egypt climate',
            'is_featured': False,
            'views_count': 987,
            'likes_count': 72
        },
        {
            'title': 'Ultimate Guide to Egyptian Street Food: What to Eat and Where to Find It',
            'category': categories['Food & Dining'],
            'related_city': cairo,
            'excerpt': 'Discover Egypt\'s delicious street food scene! From koshari to ta\'ameya, learn what to eat, where to find it, and how much you should pay for authentic Egyptian flavors.',
            'content': '''
# Ultimate Guide to Egyptian Street Food

Egyptian street food is delicious, affordable, and safe - if you know what to order! Here's your complete guide to eating like a local.

## Must-Try Egyptian Street Foods

### 1. Koshari - Egypt's National Dish

**What it is:** Layers of rice, lentils, macaroni, chickpeas topped with spicy tomato sauce, crispy fried onions, and garlic vinegar.

**Taste:** Comfort food at its finest - filling, flavorful, and surprisingly satisfying.

**Price:** 15-30 EGP ($0.50-$1)

**Where to get it:**
- **Abou Tarek** (Cairo) - Most famous, 3 floors of koshari!
- **Koshari El Tahrir** (Cairo) - Local favorite
- Any koshari shop (they're everywhere!)

**Ordering tip:** Say "wahid koshari sagheer" (one small koshari) or "kabeer" for large.

### 2. Ta'ameya (Egyptian Falafel)

**What it is:** Fried balls made from fava beans (NOT chickpeas like Middle Eastern falafel), herbs, and spices.

**Taste:** Greener, more herbaceous than chickpea falafel. Crispy outside, fluffy inside.

**Price:** 3-5 EGP per sandwich ($0.10-$0.15!)

**Where to get it:**
- Street carts early morning
- Any "ful we ta'ameya" shop
- Breakfast spots

**Serving style:** Usually in baladi bread (Egyptian pita) with tahini, salad, and pickles.

### 3. Ful Medames - Traditional Breakfast

**What it is:** Slow-cooked fava beans mashed with cumin, garlic, lemon juice, and olive oil.

**Taste:** Hearty, earthy, perfect morning protein.

**Price:** 10-20 EGP with bread

**Where to get it:**
- Breakfast carts
- Small ful shops (open 6-11 AM)
- Hotel breakfasts

**Eating style:** Scoop with bread, add your own pickles/veggies.

### 4. Shawarma

**What it is:** Marinated meat (chicken or beef) roasted on a vertical spit, shaved off and wrapped in bread.

**Taste:** Juicy, well-spiced, often with tahini and pickles.

**Price:** 25-40 EGP ($0.80-$1.30)

**Where to get it:**
- **Shabrawy** (Cairo) - Upscale chain
- Street shawarma stands
- Late-night food streets

**Safety tip:** Eat where you see high turnover (meat doesn't sit long).

### 5. Hawawshi

**What it is:** Spiced minced meat stuffed inside baladi bread, then baked until crispy.

**Taste:** Like a meat pie - crispy bread, juicy spiced filling.

**Price:** 20-35 EGP

**Where to get it:**
- **El Prince** (Zamalek, Cairo) - Famous for hawawshi
- Local bakeries
- Late-night food spots

### 6. Feteer - Egyptian "Pizza"

**What it is:** Flaky layered pastry, can be savory (cheese, meat) or sweet (honey, sugar, nuts).

**Taste:** Like a cross between pizza and pastry - buttery, flaky, delicious.

**Price:** 30-70 EGP depending on filling

**Where to get it:**
- **Feteer El Tahrir** (Cairo)
- Traditional feteer shops
- Tourist areas

**Recommendation:** Try "feteer meshaltet" (plain with honey) first!

### 7. Baladi Bread

**What it is:** Traditional Egyptian flatbread - a staple with every meal.

**Taste:** Fresh and warm = heaven. Slightly sour, chewy.

**Price:** 0.05 EGP per loaf (yes, 5 piasters!)

**Where to get it:**
- Every neighborhood bakery
- Look for lines of locals

**Local secret:** Freshest around 6-7 AM and 4-5 PM

### 8. Fresh Juice (Aseer)

**Popular flavors:**
- **Mango** (summer) - 15-25 EGP
- **Sugarcane** - 5-10 EGP
- **Orange** - 10-20 EGP
- **Strawberry** (winter) - 15-25 EGP

**Safety:** Generally safe! High sugar content and acidity kill bacteria.

**Where:** Juice shops everywhere - look for fresh fruit piled high.

**Tip:** Say "min gheir sukkar" (without sugar) if you don't want added sugar.

### 9. Stuffed Vegetables (Mahshi)

**What it is:** Vegetables (peppers, zucchini, eggplant, grape leaves) stuffed with rice, herbs, and sometimes meat.

**Taste:** Comfort food - slightly tangy from lemon juice.

**Price:** 30-50 EGP for a mixed plate

**Where to get it:**
- Home-style restaurants
- "Mahshi" specialty shops
- Hotels (more expensive)

### 10. Molokhia

**What it is:** Green soup made from jute leaves, served with rice and meat.

**Taste:** Unique! Slightly slimy texture (like okra), garlicky flavor.

**Price:** 40-60 EGP

**Where to get it:**
- Traditional Egyptian restaurants
- Home-cooking style places
- Thursday lunch special at many restaurants

**Note:** Either love it or hate it - worth trying once!

## Sweet Treats

### Om Ali
Traditional Egyptian dessert - bread pudding with cream, nuts, and raisins. Heaven in a bowl!
**Price:** 25-40 EGP

### Basbousa
Semolina cake soaked in honey syrup. Sweet and crumbly.
**Price:** 15-25 EGP

### Konafa
Shredded pastry with cheese or cream filling, soaked in syrup. Best during Ramadan!
**Price:** 30-50 EGP per serving

## Safety Tips for Street Food

### DO:
✓ Eat where locals eat (long lines = good sign!)
✓ Choose vendors with high turnover
✓ Watch food being cooked fresh
✓ Eat freshly fried foods (high heat kills bacteria)
✓ Drink bottled water, not tap

### DON'T:
✗ Eat salads from street vendors (tap water risk)
✗ Have meat that's been sitting out
✗ Eat seafood from street carts (except coastal areas)
✗ Use tap water ice
✗ Eat cut fruit sitting out in hot weather

### General Rules:
1. **Hot food:** Safest - heat kills bacteria
2. **High turnover:** Popular spots = fresh food
3. **Observe locals:** If locals avoid it, you should too
4. **Trust your instincts:** If it smells off, walk away

## Budget Planning

### Daily Food Budget:

**Ultra-Budget ($3-5 per day):**
- Breakfast: Ful sandwich (10 EGP)
- Lunch: Koshari (20 EGP)
- Dinner: Ta'ameya sandwiches (15 EGP)
- Juice: Fresh sugarcane (10 EGP)

**Budget ($8-12 per day):**
- Breakfast: Ful with eggs (25 EGP)
- Lunch: Shawarma (35 EGP)
- Dinner: Hawawshi (40 EGP)
- Snacks/drinks: (20 EGP)

**Comfortable ($15-25 per day):**
- Breakfast: Hotel or café (50 EGP)
- Lunch: Restaurant meal (100 EGP)
- Dinner: Nice restaurant (150 EGP)
- Snacks/juice: (50 EGP)

## Where to Find the Best Street Food

### Cairo:

**Downtown Cairo:**
- Around Talaat Harb Square
- Mohamed Mahmoud Street
- Alfy Street

**Islamic Cairo:**
- Khan el-Khalili area
- Al-Muizz Street

**Late Night (midnight-5 AM):**
- Qasr el-Nil Street
- Tahrir Square area
- University districts

### Alexandria:

**Corniche Area:**
- Fresh seafood
- Alexandrian-style liver sandwiches

**Mansheya:**
- Traditional Alexandrian sweets

### Luxor:

**Around Luxor Temple:**
- Tourist-friendly street food
- Higher prices but convenient

**Local Markets:**
- Better prices, authentic experience

## Useful Arabic Phrases

- **Bikam da?** - How much is this?
- **Wahid** - One
- **Etnein** - Two
- **Min gheir...** - Without...
- **Harr** - Spicy
- **Mish harr** - Not spicy
- **Sahha!** - Bon appetit!
- **El hessab, low samaht** - The bill, please

## Pro Tips

1. **Eat breakfast like an Egyptian** - Ful and ta'ameya before 10 AM
2. **Late lunch** - Egyptians eat lunch 2-4 PM
3. **Late dinner** - Dinner is 9-11 PM or later
4. **Share and sample** - Order multiple items to share
5. **Small bills** - Keep 5, 10, 20 EGP notes for street food
6. **Point if needed** - Language barrier? Point at what others are eating!

## Final Thoughts

Egyptian street food is one of the country's greatest pleasures. It's delicious, ridiculously cheap, and genuinely safe when you follow basic precautions. Don't be afraid to dive in - some of your best Egypt memories will be around street food stalls!

**Hungry for more?** Check out Egy360's verified restaurant recommendations for both street food and sit-down dining across Egypt!
''',
            'tags': 'Egyptian Food, Street Food, Cairo Food, Koshari, Egyptian Cuisine',
            'meta_description': 'Guide to Egyptian street food: what to eat, where to find it, prices, safety tips. Koshari, ta\'ameya, ful, and more delicious dishes.',
            'meta_keywords': 'Egyptian street food, koshari, Egyptian food guide, Cairo food, ta\'ameya, ful medames',
            'is_featured': True,
            'views_count': 1567,
            'likes_count': 134
        }
    ]

    created_count = 0
    for post_data in posts:
        # Calculate publishing date (recent dates for each post)
        days_ago = created_count * 7  # Each post is 1 week apart
        published_at = timezone.now() - timedelta(days=days_ago)

        post, created = BlogPost.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'author': author,
                'category': post_data['category'],
                'related_city': post_data['related_city'],
                'excerpt': post_data['excerpt'],
                'content': post_data['content'],
                'tags': post_data['tags'],
                'meta_description': post_data['meta_description'],
                'meta_keywords': post_data['meta_keywords'],
                'status': 'published',
                'is_featured': post_data['is_featured'],
                'views_count': post_data['views_count'],
                'likes_count': post_data['likes_count'],
                'published_at': published_at
            }
        )

        if created:
            created_count += 1
            print(f"[OK] Created blog post: {post.title}")
        else:
            print(f"  Blog post already exists: {post.title}")

    return created_count

def main():
    """Main execution function"""
    print("=" * 70)
    print("POPULATING EGY360 BLOG WITH CONTENT")
    print("=" * 70)
    print()

    # Create categories
    print("STEP 1: Creating blog categories...")
    categories = create_blog_categories()
    print(f"[OK] Created/found {len(categories)} categories")
    print()

    # Get author
    print("STEP 2: Setting up blog author...")
    author = get_or_create_author()
    print(f"[OK] Author ready: {author.username}")
    print()

    # Create blog posts
    print("STEP 3: Creating blog posts...")
    post_count = create_blog_posts(author, categories)
    print()

    # Summary
    print("=" * 70)
    print("BLOG POPULATION COMPLETE!")
    print("=" * 70)
    print(f"[OK] Total categories: {BlogCategory.objects.count()}")
    print(f"[OK] Total blog posts: {BlogPost.objects.filter(status='published').count()}")
    print(f"[OK] Featured posts: {BlogPost.objects.filter(is_featured=True).count()}")
    print()
    print("Blog is now ready! Visit https://360egy.com/blog/ to see the articles.")
    print()
    print("Next steps:")
    print("1. Review blog posts on the website")
    print("2. Add more articles as needed")
    print("3. Share blog posts on social media")
    print("4. Use blog content for SEO")
    print("=" * 70)

if __name__ == '__main__':
    main()
