from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import BlogPost, BlogCategory, BlogComment
import traceback


def debug_blog(request):
    """Debug endpoint to test blog functionality"""
    try:
        total = BlogPost.objects.count()
        published = BlogPost.objects.filter(status='published').count()
        categories = BlogCategory.objects.count()
        version = 'v3-fixed'  # Version indicator for deployment verification
        posts = list(BlogPost.objects.filter(status='published').values('title', 'slug')[:5])
        return JsonResponse({
            'status': 'ok',
            'version': version,
            'total_posts': total,
            'published_posts': published,
            'categories': categories,
            'sample_posts': posts
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def seed_pyramid_articles(request):
    """
    Seed the 9 Great Pyramid articles.
    Access via: /blog/seed-pyramids/?key=egy360seed
    """
    # Simple security check
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User

    # Get or create category
    category, _ = BlogCategory.objects.get_or_create(
        slug='ancient-egypt',
        defaults={'name': 'Ancient Egypt', 'description': 'Explore the wonders of Ancient Egypt'}
    )

    # Get author
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users found'}, status=500)

    now = timezone.now()

    articles = [
        {
            'title': 'The Great Pyramid of Giza: 4,500 Years of Mystery and Marvel',
            'slug': 'great-pyramid-giza-introduction',
            'excerpt': 'Discover the mind-blowing facts about the Great Pyramid of Giza - the only surviving Wonder of the Ancient World.',
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': 'Building the Great Pyramid: Timeline, Workers, and the 20-Year Challenge',
            'slug': 'great-pyramid-history-timeline-workers',
            'excerpt': 'How long did it take to build the Great Pyramid? Who were the workers? Explore the complete timeline.',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': "The Architecture of the Great Pyramid: Precision That Shouldn't Exist",
            'slug': 'great-pyramid-architecture-precision',
            'excerpt': "The Great Pyramid's precision rivals modern engineering - 99.98% symmetrical, aligned to true north.",
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': "The King's Chamber: Heart of the Great Pyramid",
            'slug': 'great-pyramid-kings-chamber-secrets',
            'excerpt': "Deep inside the Great Pyramid lies the King's Chamber - built of granite from 800km away.",
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'How Was the Great Pyramid Built? Construction Methods Explained',
            'slug': 'great-pyramid-construction-methods',
            'excerpt': "No wheels, no cranes, no iron - how did ancient Egyptians build the Great Pyramid?",
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Cutting Pyramid Stones: How Did They Do It With Copper Tools?',
            'slug': 'great-pyramid-stone-cutting',
            'excerpt': "The Great Pyramid's stones are cut so precisely you can't fit paper between them.",
            'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Moving Pyramid Stones: Transporting 2.3 Million Blocks Without Wheels',
            'slug': 'great-pyramid-transporting-stones',
            'excerpt': "How did the Egyptians move 80-ton blocks 800 kilometers without trucks or cranes?",
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Great Pyramid Myths Debunked: Aliens, Slaves, and Misconceptions',
            'slug': 'great-pyramid-myths-debunked',
            'excerpt': "Aliens didn't build the pyramids. Slaves didn't either. Let's debunk the myths.",
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Why Was the Great Pyramid Built? Purpose, Meaning, and Mysteries',
            'slug': 'great-pyramid-purpose-meaning',
            'excerpt': "The Great Pyramid took 20 years and millions of blocks. But why?",
            'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200&q=80',
            'is_featured': False,
        },
    ]

    created = 0
    updated = 0

    for article in articles:
        content = f"""## {article['title']}

{article['excerpt']}

This is part of our comprehensive 9-part series on the Great Pyramid of Giza, exploring its history, construction, mysteries, and enduring legacy.

The Great Pyramid stands as humanity's greatest architectural achievement - built 4,500 years ago with precision that rivals modern engineering.

### Key Facts
- Built around 2560 BCE during Pharaoh Khufu's reign
- 2.3 million stone blocks, weighing 2.5 to 80 tons each
- Original height: 146.6 meters (481 feet)
- Base accuracy: 99.98% perfect symmetry
- Aligned to true north within 0.05 degrees

Visit 360egy.com for the complete article with full details, images, and interactive content.

---
*Part of the Great Pyramid Series on 360egy.com*
"""

        post, was_created = BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'excerpt': article['excerpt'],
                'content': content,
                'image_url': article['image_url'],
                'meta_description': article['excerpt'],
                'meta_keywords': 'great pyramid, giza, egypt, ancient egypt, pyramids',
                'tags': 'pyramids, giza, ancient egypt, history',
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': now,
            }
        )
        if was_created:
            created += 1
        else:
            updated += 1

    return JsonResponse({
        'success': True,
        'created': created,
        'updated': updated,
        'total': len(articles),
        'message': f'Created {created}, updated {updated} pyramid articles'
    })


def blog_list_test(request):
    """Temporary test view - returns JSON to debug"""
    try:
        posts = list(BlogPost.objects.filter(status='published').order_by('-published_at')[:5].values('title', 'slug'))
        categories = list(BlogCategory.objects.values('name', 'slug')[:5])
        return JsonResponse({
            'status': 'ok',
            'posts': posts,
            'categories': categories,
            'total_posts': BlogPost.objects.count(),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        import sys
        # Auto-seed if no articles exist (Railway ephemeral storage fix)
        try:
            if BlogPost.objects.count() == 0:
                print("AUTO-SEED: No articles found, seeding now...", file=sys.stderr)
                self._auto_seed_articles()
                print(f"AUTO-SEED: Completed. Total articles: {BlogPost.objects.count()}", file=sys.stderr)
        except Exception as e:
            print(f"AUTO-SEED ERROR: {str(e)}", file=sys.stderr)
            # Continue even if seeding fails

        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Print to stdout for gunicorn capture
            print(f"BLOG_ERROR: {str(e)}", file=sys.stderr)
            print(f"BLOG_TRACE: {traceback.format_exc()}", file=sys.stderr)
            # Return error as JSON for debugging
            from django.http import JsonResponse
            return JsonResponse({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'view': 'BlogListView'
            }, status=500)

    def _auto_seed_articles(self):
        """Auto-seed articles when database is empty (Railway ephemeral fix)"""
        from django.contrib.auth.models import User
        from django.utils import timezone

        # Create admin user if needed
        if not User.objects.exists():
            User.objects.create_superuser('admin', 'admin@360egy.com', 'admin360egy')

        author = User.objects.first()

        # Create categories
        categories_data = [
            ('ancient-egypt', 'Ancient Egypt', 'Explore pyramids, temples, and pharaohs'),
            ('travel-guides', 'Travel Guides', 'Complete Egypt travel guides'),
            ('destinations', 'Destinations', 'Egyptian cities and attractions'),
            ('tips-advice', 'Tips & Advice', 'Travel tips for Egypt'),
            ('food-culture', 'Food & Culture', 'Egyptian cuisine and traditions'),
            ('red-sea', 'Red Sea', 'Beaches, diving, and resorts'),
        ]

        for slug, name, desc in categories_data:
            BlogCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})

        # Articles with rich, detailed content (200+ words each)
        articles_data = self._get_rich_articles_data()

        now = timezone.now()
        for article in articles_data:
            category = BlogCategory.objects.filter(slug=article['category']).first()
            BlogPost.objects.get_or_create(
                slug=article['slug'],
                defaults={
                    'title': article['title'],
                    'author': author,
                    'category': category,
                    'excerpt': article['excerpt'],
                    'content': article['content'],
                    'image_url': article['image'],
                    'meta_description': article['excerpt'][:155],
                    'status': 'published',
                    'is_featured': article['featured'],
                    'published_at': now,
                }
            )

    def _get_rich_articles_data(self):
        """Return articles with rich, detailed content (200+ words each)"""
        return [
            {
                'title': 'The Great Pyramid of Giza: Complete Visitor Guide 2026',
                'slug': 'great-pyramid-giza-guide',
                'category': 'ancient-egypt',
                'excerpt': 'Discover everything about the Great Pyramid - the last surviving Wonder of the Ancient World.',
                'image': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200',
                'featured': True,
                'content': """## The Great Pyramid of Giza: Complete Visitor Guide 2026

The Great Pyramid of Giza is the oldest and largest of the three pyramids on the Giza plateau. Built around 2560 BCE for Pharaoh Khufu, it stood as the tallest man-made structure in the world for over 3,800 years. Today, it remains one of the most visited monuments on Earth and the only surviving Wonder of the Ancient World.

![The Great Pyramid at sunset](https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800)

### Why Visit the Great Pyramid?

Standing before the Great Pyramid is a life-changing experience. The sheer size is overwhelming - it covers 13 acres and contains over 2.3 million stone blocks. Each block weighs between 2.5 to 15 tons. The precision of construction is remarkable, with the base being level to within just 2.1 centimeters across its entire length.

![Close-up view of pyramid stones](https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800)

### Key Facts You Should Know

- **Height**: Originally 146.6 meters (481 feet), now 138.8 meters due to erosion
- **Base**: Each side measures 230.4 meters (756 feet)
- **Weight**: Estimated 6 million tons total
- **Construction Time**: Approximately 20 years
- **Workers**: Around 20,000-30,000 skilled workers (not slaves)

### Best Time to Visit

The best months to visit are October through April when temperatures are comfortable. Arrive early in the morning, ideally at 8 AM when the site opens, to avoid crowds and the midday heat. The site gets very busy between 10 AM and 2 PM.

![Camels near the pyramids](https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800)

### Ticket Prices 2026

- **Giza Plateau Entry**: 200 EGP (approximately $6.50 USD)
- **Great Pyramid Interior**: 400 EGP additional
- **Solar Boat Museum**: 100 EGP

### Tips for Your Visit

- Wear comfortable walking shoes - the terrain is uneven and sandy
- Bring plenty of water and sunscreen
- Hire an official guide for deeper historical context
- Watch out for unofficial "helpers" who may demand tips
- Photography is allowed outside but not inside the pyramid
- The interior passage is narrow and steep - not suitable for claustrophobic visitors

### What to See Nearby

![The Sphinx with pyramids in background](https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800)

While at Giza, don't miss the Sphinx, the Pyramid of Khafre, the Pyramid of Menkaure, and the Solar Boat Museum. The Sound and Light Show in the evening is also spectacular.

The Great Pyramid continues to inspire wonder and mystery. Whether you're a history enthusiast, a photographer, or simply a curious traveler, this ancient monument will leave you speechless."""
            },
            {
                'title': 'Best Time to Visit Egypt in 2026',
                'slug': 'best-time-visit-egypt-2026',
                'category': 'travel-guides',
                'excerpt': 'Planning your Egypt trip? Learn the best months to visit, weather patterns, and how to avoid crowds.',
                'image': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
                'featured': True,
                'content': """## Best Time to Visit Egypt in 2026

Egypt is a year-round destination, but choosing the right time to visit can make a huge difference in your experience. The weather, crowd levels, and prices vary significantly throughout the year. This guide will help you plan the perfect Egypt trip.

![Beautiful Egyptian temple at golden hour](https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800)

### Understanding Egypt's Climate

Egypt has a desert climate with hot, dry summers and mild winters. The country experiences very little rainfall, with most areas receiving less than 80mm per year. However, temperatures can vary dramatically between regions.

![Luxor Temple illuminated at night](https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800)

### Season-by-Season Breakdown

**Winter (December - February)**
- Temperature: 15-25°C (59-77°F)
- Best for: Sightseeing in Cairo, Luxor, and Aswan
- Crowds: High season - expect more tourists
- Prices: Peak rates for hotels and tours

**Spring (March - May)**
- Temperature: 20-35°C (68-95°F)
- Best for: All activities, beaches starting to warm up
- Crowds: Moderate
- Prices: Shoulder season rates
- Note: Occasional sandstorms (khamsin) in March-April

**Summer (June - August)**
- Temperature: 30-45°C (86-113°F)
- Best for: Red Sea beaches and diving
- Crowds: Low at ancient sites, high at resorts
- Prices: Great deals on Cairo and Luxor hotels

**Fall (September - November)**
- Temperature: 25-35°C (77-95°F)
- Best for: All activities - ideal balance
- Crowds: Building up towards winter
- Prices: Shoulder season - good value

### Our Top Recommendation

The absolute best time to visit Egypt is **October through April**. During these months, you'll enjoy:

- Comfortable temperatures for exploring ancient sites
- Perfect weather for desert adventures
- Great diving conditions in the Red Sea
- Beautiful Nile cruise weather

### Important Dates to Consider

- **Ramadan**: The Islamic holy month affects opening hours and restaurant availability. Dates change yearly.
- **Egyptian Holidays**: Eid celebrations can mean crowded sites
- **European School Holidays**: Christmas and Easter bring more tourists
- **Abu Simbel Sun Festival**: February 22 and October 22 - book months ahead

### Regional Considerations

- **Cairo & Pyramids**: Best October-April, avoid July-August
- **Luxor & Aswan**: Best November-March (summer is extremely hot)
- **Red Sea Resorts**: Year-round, but March-May and September-November are ideal
- **Sinai & Desert**: Best October-April, cool nights in winter

### Money-Saving Tips

Visit during shoulder season (March-May or September-November) for the best combination of good weather, fewer crowds, and reasonable prices. Book major sites early in the morning to beat both the heat and the tour groups."""
            },
            {
                'title': 'Cairo Travel Guide: Top 20 Things to Do',
                'slug': 'cairo-travel-guide-things-to-do',
                'category': 'destinations',
                'excerpt': 'Explore Cairo like a local! From the Egyptian Museum to Khan El Khalili bazaar, discover the best attractions.',
                'image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
                'featured': True,
                'content': """## Cairo Travel Guide: Top 20 Things to Do

Cairo, the capital of Egypt, is a city of contrasts where ancient history meets modern life. With over 20 million people, it's the largest city in Africa and the Arab world. This bustling metropolis offers endless things to see and do.

![Cairo cityscape with mosques and minarets](https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800)

### Top 20 Must-Do Experiences in Cairo

![Khan El-Khalili bazaar](https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800)

**1. Visit the Pyramids of Giza**
The iconic pyramids are just outside Cairo. Start early to beat the crowds and heat. Don't miss the Sphinx and the Sound and Light Show.

**2. Explore the Egyptian Museum**
Home to over 120,000 artifacts including Tutankhamun's treasures. Plan for at least 3-4 hours. The new Grand Egyptian Museum near Giza is also now open.

**3. Wander Through Khan El-Khalili Bazaar**
Cairo's famous market dates back to the 14th century. Shop for spices, jewelry, souvenirs, and traditional crafts. Bargaining is expected!

**4. Visit Islamic Cairo**
Explore historic mosques, madrasas, and medieval streets. Key sites include Al-Azhar Mosque, Sultan Hassan Mosque, and the Citadel of Saladin.

**5. See the Citadel of Saladin**
This medieval fortress offers panoramic city views and houses the beautiful Muhammad Ali Mosque.

**6. Take a Felucca Ride on the Nile**
A traditional sailboat ride at sunset is magical. Negotiate the price before boarding - about 200 EGP for an hour is fair.

**7. Explore Coptic Cairo**
Visit the Hanging Church, Ben Ezra Synagogue, and the Coptic Museum. This area has been a Christian center for nearly 2,000 years.

**8. Climb the Cairo Tower**
Get 360-degree views of the city from this 187-meter tower in Zamalek.

**9. Walk Along Al-Muizz Street**
One of the oldest streets in Cairo, lined with stunning Islamic architecture and historic monuments.

**10. Visit the Al-Azhar Park**
A beautiful green oasis in the heart of the city. Perfect for escaping the chaos and enjoying views of Islamic Cairo.

### More Amazing Experiences

**11. Eat Koshari**
Try Egypt's national dish - a delicious mix of pasta, rice, lentils, and crispy onions with spicy tomato sauce.

**12. Visit the Mosque of Ibn Tulun**
One of Cairo's oldest and largest mosques with a unique spiral minaret.

**13. Explore the City of the Dead**
A vast historic cemetery where people live among the tombs. Fascinating but respectful visits recommended.

**14. Shop at Cairo Festival City**
Modern mall with international brands, great restaurants, and entertainment.

**15. Take a Food Tour**
Discover local eateries, street food stalls, and traditional Egyptian cuisine with a knowledgeable guide.

**16. Visit the Gayer-Anderson Museum**
Two restored Ottoman houses filled with Islamic art and antiques.

**17. Watch the Whirling Dervishes**
Free performance at the Wekalet El-Ghouri every Saturday, Monday, and Wednesday evening.

**18. Explore Memphis and Saqqara**
Day trip to see the Step Pyramid and ancient capital. Just 30km south of Cairo.

**19. Visit the Manial Palace**
Beautiful royal palace on Rhoda Island with stunning architecture and gardens.

**20. Experience Cairo's Nightlife**
From rooftop bars to traditional ahwas (coffeehouses), Cairo comes alive at night.

### Practical Tips for Cairo

- Traffic is chaotic - use Uber or Careem apps for safe, fair-priced rides
- Friday is the Muslim holy day - some sites may have limited hours
- Dress modestly, especially when visiting mosques
- Learn a few Arabic phrases - locals appreciate the effort
- Carry small bills for tips and purchases
- Stay hydrated and take breaks in air-conditioned spaces"""
            },
            {
                'title': 'Luxor Temple: Ancient Thebes Guide',
                'slug': 'luxor-temple-ancient-thebes-guide',
                'category': 'ancient-egypt',
                'excerpt': 'Walk through 3,400 years of history at Luxor Temple. Complete guide to this magnificent ancient Egyptian temple.',
                'image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
                'featured': False,
                'content': """## Luxor Temple: Ancient Thebes Guide

Luxor Temple is one of the most beautiful and well-preserved ancient monuments in Egypt. Located on the east bank of the Nile in the heart of modern Luxor, this temple has been a place of worship for over 3,400 years - from ancient Egyptian times through Roman rule to Islamic and even Christian periods.

![Luxor Temple columns at night](https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800)

### History of Luxor Temple

![Ancient hieroglyphics on temple walls](https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800)

The temple was primarily built by two pharaohs: Amenhotep III (who built the inner temple around 1390 BCE) and Ramesses II (who added the outer court, entrance pylons, and obelisks around 1250 BCE). Unlike other temples dedicated to gods, Luxor Temple was dedicated to the rejuvenation of kingship.

### What Makes Luxor Temple Special

- **Avenue of Sphinxes**: A 3km road lined with sphinx statues once connected Luxor Temple to Karnak Temple. Much of this avenue has been excavated and restored.

- **The Massive Entrance Pylon**: Ramesses II built the 24-meter-high entrance with scenes of his military victories. Originally, two obelisks stood here - one now stands in Place de la Concorde, Paris.

- **Colossal Statues**: Giant seated statues of Ramesses II guard the entrance.

- **The Great Colonnade**: Built by Amenhotep III, this impressive hall features 14 massive papyrus columns, each 16 meters tall.

- **The Mosque of Abu Haggag**: Built in the 13th century on top of the ancient ruins, this mosque is still in use today. It shows how the temple was buried under centuries of sand and debris.

### Key Features to See

1. **First Pylon**: Decorated with scenes of Ramesses II at the Battle of Kadesh
2. **Court of Ramesses II**: Surrounded by 74 papyrus columns
3. **Colonnade of Amenhotep III**: The processional colonnade with beautiful reliefs
4. **Court of Amenhotep III**: The inner courtyard with double rows of columns
5. **Hypostyle Hall**: Leading to the inner sanctuaries
6. **Birth Room**: Reliefs showing Amenhotep III's divine birth
7. **Sanctuary of Alexander the Great**: Yes, Alexander was here!

### Best Time to Visit

The temple is magical at any time, but visiting during sunset or at night is especially beautiful. The temple is illuminated after dark, creating a stunning atmosphere.

**Opening Hours**: 6 AM - 9 PM (10 PM in summer)
**Ticket Price**: 200 EGP (approximately $6.50 USD)

### Tips for Your Visit

- Visit in the late afternoon to see the temple in golden light and then illuminated at night
- Hire a guide to understand the complex history and symbolism
- Combine with a visit to Karnak Temple (2.5km north)
- Photography is allowed throughout
- Wear comfortable shoes - there's a lot of walking
- Allow at least 1.5-2 hours for a thorough visit

### Nearby Attractions

- Karnak Temple (2.5km via the Avenue of Sphinxes)
- Luxor Museum (excellent collection in modern building)
- Mummification Museum
- Valley of the Kings (West Bank)
- Temple of Hatshepsut (West Bank)

Luxor Temple remains one of Egypt's most impressive monuments. Standing among these ancient columns as the sun sets over the Nile is an unforgettable experience."""
            },
            {
                'title': 'Red Sea Diving: Best Sites in Egypt',
                'slug': 'red-sea-diving-best-sites-egypt',
                'category': 'red-sea',
                'excerpt': 'Discover world-class diving in the Red Sea. From the SS Thistlegorm wreck to Ras Mohammed, explore Egypt underwater paradise.',
                'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
                'featured': True,
                'content': """## Red Sea Diving: Best Sites in Egypt

The Red Sea is one of the world's top diving destinations, famous for crystal-clear waters, vibrant coral reefs, and incredible marine life. With visibility often exceeding 30 meters and water temperatures between 21-28°C year-round, Egypt offers perfect diving conditions for beginners and experts alike.

![Colorful coral reef in the Red Sea](https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800)

### Why the Red Sea is Special

![Tropical fish swimming near coral](https://images.unsplash.com/photo-1559825481-12a05cc00344?w=800)

The Red Sea is a unique body of water. It has:
- No rivers flowing into it (keeping water clear)
- High salinity (more buoyant for divers)
- Over 1,200 species of fish (10% found nowhere else)
- 200+ species of soft and hard coral
- Warm water year-round

### Top 10 Dive Sites in Egypt

**1. SS Thistlegorm (Sharm El Sheikh)**
The world's most famous wreck dive. This WWII British supply ship sunk in 1941 still carries motorcycles, trucks, and military supplies. Suitable for Advanced divers.

**2. Ras Mohammed National Park (Sharm El Sheikh)**
Shark Reef and Yolanda Reef offer spectacular wall diving with sharks, turtles, and massive schools of fish. The famous "toilets" from the Yolanda cargo ship rest on the reef.

**3. The Blue Hole (Dahab)**
A 130-meter deep sinkhole famous (and infamous) for free diving. Recreational divers explore the shallow reef around the edges. Beautiful but demands respect.

**4. The Brothers Islands (Offshore)**
Remote islands with pristine reefs, hammerhead sharks, and thresher sharks. Accessed by liveaboard only. For experienced divers.

**5. Elphinstone Reef (Marsa Alam)**
One of the best sites for oceanic whitetip sharks. Dramatic walls covered in soft corals. Strong currents possible.

**6. Jackson Reef (Tiran Strait)**
Part of the Tiran Island group with strong currents bringing big fish. Excellent for shark sightings and coral gardens.

**7. Abu Nuhas (Red Sea)**
Known as the "Ship Graveyard" with four shipwrecks including the Giannis D and Carnatic. Great for wreck diving enthusiasts.

**8. Dolphin House (Marsa Alam)**
Sheltered bay where spinner dolphins rest. Amazing snorkeling and diving with wild dolphins.

**9. Rocky Island and Zabargad (Offshore)**
Remote southern sites accessed by liveaboard. Pristine reefs and pelagic action.

**10. Salem Express (Safaga)**
Controversial but stunning wreck of a ferry that sank in 1991. Now an artificial reef teeming with life.

### Best Diving Areas by Experience Level

**Beginners**: Hurghada, Sharm El Sheikh (protected bays), Dahab (shore diving)
**Intermediate**: Ras Mohammed, Marsa Alam, Tiran Strait
**Advanced**: Brothers Islands, Elphinstone, Daedalus Reef, St. John's

### When to Go

- **Best Overall**: March-May and September-November
- **Big Fish**: June-September (mantas and whale sharks)
- **Warm Water**: June-September (28°C)
- **Calm Seas**: April-May and September-October

### What You'll See

- Dolphins (spinner and bottlenose)
- Sea turtles (green and hawksbill)
- Sharks (whitetip reef, oceanic whitetip, hammerhead, whale shark)
- Manta rays and eagle rays
- Moray eels and octopus
- Napoleon wrasse and barracuda
- Colorful reef fish and nudibranchs

### Practical Information

- **Certification**: PADI, SSI, and NAUI courses available everywhere
- **Costs**: Expect $40-60 per boat dive, liveaboards from $150/day
- **Equipment**: Most centers have rental gear, bring your own mask
- **Tip**: The Red Sea is excellent for learning to dive - warm, clear, and calm"""
            },
            {
                'title': 'Egyptian Street Food: 15 Must-Try Dishes',
                'slug': 'egyptian-street-food-must-try',
                'category': 'food-culture',
                'excerpt': 'From koshari to ful medames, discover the authentic flavors of Egyptian street food. Where to find the best local eats.',
                'image': 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=1200',
                'featured': False,
                'content': """## Egyptian Street Food: 15 Must-Try Dishes

Egyptian street food is delicious, affordable, and found everywhere. From busy Cairo streets to small village stalls, the same beloved dishes have been feeding Egyptians for generations. Here are 15 dishes you absolutely must try.

![Delicious Egyptian koshari dish](https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=800)

### The Essential Egyptian Dishes

![Fresh Egyptian falafel (ta'ameya)](https://images.unsplash.com/photo-1593001874117-c99c800e3eb7?w=800)

**1. Koshari (Egypt's National Dish)**
A hearty mix of rice, macaroni, lentils, chickpeas, and crispy fried onions, topped with spicy tomato sauce and garlic vinegar. Filling, cheap, and completely vegan. Every Egyptian has their favorite koshari shop.
- **Price**: 15-40 EGP ($0.50-1.30)
- **Best in Cairo**: Abou Tarek, Koshary El Tahrir

**2. Ful Medames**
Slow-cooked fava beans mashed and served with olive oil, lemon, cumin, and garlic. Egypt's traditional breakfast, eaten with fresh baladi bread.
- **Variations**: With egg, tahini, or tomato
- **Price**: 10-25 EGP

**3. Ta'ameya (Egyptian Falafel)**
Unlike Middle Eastern falafel made from chickpeas, Egyptian ta'ameya uses fava beans, making it bright green inside and incredibly flavorful.
- **Best eaten**: Fresh and hot in an aish baladi sandwich
- **Price**: 5-15 EGP for a sandwich

**4. Feteer Meshaltet**
Flaky, buttery layered pastry similar to puff pastry. Can be sweet (with honey, sugar, cream) or savory (with cheese, meat, vegetables).
- **Price**: 30-80 EGP depending on toppings

**5. Shawarma**
Thinly sliced meat (chicken or beef) wrapped in bread with tahini, pickles, and vegetables. The Egyptian version is lighter than Lebanese style.
- **Price**: 25-50 EGP

### More Delicious Options

**6. Hawawshi**
Spiced minced meat stuffed inside bread and baked until crispy. Like a meat-stuffed pita pocket. Absolutely delicious.
- **Price**: 20-40 EGP

**7. Fiteer Baladi**
Simple village-style flatbread, perfect for scooping up ful or dipping in honey and cream.

**8. Molokhia**
Green soup made from jute leaves, served over rice with chicken or rabbit. The texture is unique but the flavor is amazing.

**9. Kofta**
Grilled ground meat on skewers, seasoned with onions and spices. Often served with bread and tahini.

**10. Kebda Iskandarani**
Alexandria-style liver, quickly fried with peppers and spices. A street food specialty.

### Sweet Treats

**11. Basbousa**
Semolina cake soaked in sweet syrup, often topped with almonds or coconut. Incredibly sweet and satisfying.

**12. Konafa**
Shredded phyllo pastry filled with cream or cheese, baked and soaked in syrup. Best eaten warm.

**13. Om Ali**
Egyptian bread pudding with milk, nuts, raisins, and coconut. Served warm and comforting.

**14. Balah El Sham**
Fried dough similar to churros, soaked in syrup. Crispy outside, soft inside.

**15. Roz Bel Laban**
Creamy rice pudding flavored with rose water and topped with pistachios.

### Where to Find the Best Street Food

- **Cairo**: Downtown, Khan El Khalili, Sayeda Zeinab
- **Alexandria**: Along the Corniche, Raml Station area
- **Luxor**: Near the train station, local souqs
- **Aswan**: The souq area, Nile-side stalls

### Tips for Eating Street Food

- Look for busy stalls - high turnover means fresh food
- Watch where locals eat - they know the best spots
- Start with cooked-to-order items if you have a sensitive stomach
- Carry hand sanitizer
- Don't be afraid to try new things!
- Learn basic Arabic food words for easier ordering"""
            },
            {
                'title': 'Hurghada Beach Resorts: Complete Guide',
                'slug': 'hurghada-beach-resorts-guide',
                'category': 'red-sea',
                'excerpt': 'Find the perfect beach resort in Hurghada. Compare prices, amenities, and locations for your Red Sea vacation.',
                'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
                'featured': False,
                'content': """## Hurghada Beach Resorts: Complete Guide

Hurghada is Egypt's most popular Red Sea resort town, offering beautiful beaches, world-class diving, and endless sunshine. With hundreds of resorts ranging from budget-friendly to ultra-luxury, finding the right one can be overwhelming. This guide will help you choose the perfect resort.

![Beautiful Hurghada beach with crystal clear water](https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800)

### Understanding Hurghada's Layout

![Luxury resort pool overlooking the Red Sea](https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=800)

Hurghada stretches about 40km along the coast and is divided into several areas:

**El Dahar (Downtown)**
- The original town center
- Authentic Egyptian atmosphere
- Budget hotels and local restaurants
- Best for: Budget travelers, cultural experience

**Sigala**
- Between downtown and resort strip
- Mix of hotels and local life
- Good restaurants and shops
- Best for: Mid-range travelers

**Resort Strip (Sakkala to Makadi Bay)**
- Main tourist area
- All-inclusive resorts
- Private beaches
- Best for: Beach vacations, families

**Makadi Bay & Soma Bay**
- South of Hurghada (20-45km)
- Newer, more upscale resorts
- Quieter, more exclusive
- Best for: Luxury seekers, couples

### Top Resort Recommendations by Budget

**Luxury (5-Star) - $150-400/night**
- Oberoi Sahl Hasheesh: Ultimate luxury, stunning architecture
- Kempinski Soma Bay: World-class spa, golf course
- Baron Palace Sahl Hasheesh: Moorish design, private beach
- The Cascades Golf Resort: Family-friendly luxury

**Mid-Range (4-Star) - $60-150/night**
- Steigenberger Al Dau Beach: Great beach, good food
- Hilton Hurghada Resort: Reliable quality, nice pools
- Sunrise Holidays Resort: Excellent value, lively atmosphere
- Jaz Aquamarine: Huge pools, family-friendly

**Budget (3-Star) - $30-60/night**
- Arabia Azur: Good beach, decent food
- Desert Rose: Great value all-inclusive
- Bella Vista: Simple but comfortable
- Royal Lagoons: Near airport, good pools

### What to Look for in a Resort

**Beach Quality**
- Sandy or rocky entry?
- Natural beach or man-made?
- How far is the reef for snorkeling?

**All-Inclusive Value**
- What's included? (drinks, activities, restaurants)
- Quality of food and variety
- Are there extra charges?

**Facilities**
- Number and size of pools
- Spa and fitness center
- Kids' clubs and activities
- Dive center on-site

**Location**
- Distance from airport (30min-1.5hrs)
- Access to town or shops
- Nearby attractions

### Best Activities in Hurghada

- Snorkeling and diving (world-class reefs)
- Glass-bottom boat tours
- Desert safari and quad biking
- Giftun Island day trips
- Dolphin watching
- Kitesurfing and windsurfing
- Day trips to Luxor

### When to Visit

- **Best Weather**: March-May, September-November
- **Warmest Water**: July-September
- **Cheapest Rates**: June-August (too hot for some)
- **Peak Season**: December-February, Easter

### Practical Tips

- Book all-inclusive for best value
- Check recent reviews for current quality
- Airport transfers are usually included
- Bring reef-safe sunscreen
- Tipping is expected (10-20 EGP per day for housekeeping)
- Learn a few Arabic phrases - staff appreciate it

Hurghada offers something for everyone. Whether you're seeking relaxation, adventure, or a family holiday, you'll find the perfect resort on the Red Sea coast."""
            },
            {
                'title': 'Valley of the Kings: Tomb Explorer Guide',
                'slug': 'valley-of-kings-tomb-guide',
                'category': 'ancient-egypt',
                'excerpt': 'Explore the burial place of pharaohs. Complete guide to visiting the Valley of the Kings.',
                'image': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
                'featured': True,
                'content': """## Valley of the Kings: Tomb Explorer Guide

The Valley of the Kings is one of the most famous archaeological sites in the world. Hidden in the desert hills on the west bank of the Nile near Luxor, this valley served as the royal burial ground for pharaohs and nobles of the New Kingdom (1550-1070 BCE). Over 60 tombs have been discovered here, including the legendary tomb of Tutankhamun.

![Valley of the Kings entrance](https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800)

### Why Was This Valley Chosen?

![Ancient tomb paintings](https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=800)

After centuries of pyramid building, pharaohs realized that obvious tombs attracted robbers. They chose this remote valley because:
- The pyramid-shaped mountain (al-Qurn) symbolized the primordial mound
- The location was hidden and easier to guard
- The soft limestone was ideal for carving elaborate tombs

Despite these precautions, all tombs except Tutankhamun's were robbed in ancient times.

### Must-See Tombs

**Tomb of Tutankhamun (KV62)**
The most famous tomb, discovered by Howard Carter in 1922 with treasures intact. The tomb itself is small and the paintings less impressive than others, but its historical significance is unmatched.
- **Extra ticket required**: 300 EGP

**Tomb of Ramesses VI (KV9)**
One of the most beautiful tombs with stunning astronomical ceiling paintings. The colors are incredibly well-preserved.
- **Included in general ticket**

**Tomb of Seti I (KV17)**
The longest and deepest tomb with the finest artwork in the valley. Recently reopened after restoration.
- **Extra ticket required**: 1000 EGP

**Tomb of Ramesses III (KV11)**
Known for its unusual secular scenes including foreign peoples and crafts.
- **Included in general ticket**

**Tomb of Thutmose III (KV34)**
Requires climbing steep stairs, but rewards with beautiful red and black painted walls.
- **Included in general ticket**

### Ticket Information

**General Ticket**: 300 EGP
- Allows entry to 3 tombs (not including Tutankhamun or Seti I)
- Different tombs rotate being open

**Special Tombs**:
- Tutankhamun: 300 EGP additional
- Seti I: 1000 EGP additional
- Ramesses V/VI photography: 300 EGP

**Opening Hours**: 6 AM - 5 PM (winter) / 6 AM - 6 PM (summer)

### Tips for Your Visit

- **Go Early**: Arrive when it opens at 6 AM to avoid crowds and heat
- **Wear Comfortable Shoes**: You'll be walking on uneven ground and climbing stairs
- **Bring Water**: There's no shade and it gets extremely hot
- **No Photography**: Photography is not allowed inside tombs (except with special ticket)
- **Hire a Guide**: The history and symbolism are complex - a good guide enhances the experience
- **Take the Tuf-Tuf**: Electric carts take you from the entrance to the tombs (included in ticket)

### Understanding the Tombs

Each tomb follows a similar pattern:
1. **Entrance Corridor**: Descending passages with guardian figures
2. **Well Chamber**: Originally designed as a trap for robbers
3. **Pillared Hall**: Decorated with scenes of the pharaoh with gods
4. **Burial Chamber**: Where the sarcophagus was placed
5. **Treasury**: Storage rooms for funerary items

### Combine with Other West Bank Sites

- Temple of Hatshepsut (10 minutes)
- Valley of the Queens
- Medinet Habu
- Colossi of Memnon
- Tombs of the Nobles

A full West Bank tour takes a full day and is best started at sunrise.

The Valley of the Kings offers an unforgettable glimpse into ancient Egyptian beliefs about death and the afterlife. Take your time, respect the sites, and let yourself be transported back 3,000 years."""
            },
            {
                'title': 'Egypt on a Budget: How to Travel for $50/Day',
                'slug': 'egypt-budget-travel-guide',
                'category': 'tips-advice',
                'excerpt': 'Yes, you can explore Egypt affordably! Budget tips for accommodation, food, transport, and attractions.',
                'image': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200',
                'featured': False,
                'content': """## Egypt on a Budget: How to Travel for $50/Day

Egypt is one of the best-value destinations in the world. With careful planning, you can see ancient wonders, enjoy delicious food, and have amazing experiences on a tight budget. Here's how to make your money go further.

![Budget-friendly street food in Egypt](https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800)

### Daily Budget Breakdown

![Affordable local transport in Cairo](https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800)

**Tight Budget ($30-40/day)**
- Accommodation: $8-15 (hostel or budget hotel)
- Food: $8-12 (street food and local restaurants)
- Transport: $5-8 (public transport, shared taxis)
- Attractions: $10-15 (1-2 sites per day)

**Comfortable Budget ($50-70/day)**
- Accommodation: $15-25 (private room, mid-range hotel)
- Food: $15-20 (mix of local and tourist restaurants)
- Transport: $8-12 (occasional Uber, trains)
- Attractions: $15-20 (more sites, occasional guide)

### Saving on Accommodation

**Best Budget Options**
- Hostels: $6-15/night for dorms, $15-25 for private rooms
- Budget hotels: $20-40/night for clean, basic rooms
- Airbnb: Often great value for longer stays

**Money-Saving Tips**
- Book in advance for better rates
- Stay near train stations to save on transport
- Negotiate for longer stays (3+ nights)
- Consider homestays for authentic experiences
- Downtown Cairo is cheaper than Zamalek or Maadi

**Top Budget Hostels**
- Wake Up! Cairo (Cairo): Great location, social atmosphere
- Bob Marley House (Luxor): Rooftop with temple views
- Bedouin Moon (Dahab): Beach vibes, cheap rooms

### Eating on a Budget

Egyptian food is delicious AND cheap. Here's what to spend:

**Street Food Prices (EGP)**
- Koshari: 15-40 ($0.50-1.30)
- Ful and ta'ameya sandwich: 10-20 ($0.30-0.65)
- Shawarma: 25-40 ($0.80-1.30)
- Feteer: 30-60 ($1-2)
- Fresh juice: 10-25 ($0.30-0.80)

**Restaurant Meals**
- Local Egyptian restaurant: 50-100 EGP ($1.60-3.25)
- Tourist restaurant: 150-300 EGP ($5-10)

**Budget Eating Tips**
- Eat where locals eat - follow the crowds
- Breakfast at your hotel (often included)
- Buy fruit from street vendors
- Carry water to refill (filter or bottled)
- Avoid tourist restaurants near major sites

### Transport Savings

**Cheapest Options**
- Cairo Metro: 8 EGP per ride (one of cheapest in world)
- Public buses: 5-10 EGP
- Microbuses: 5-15 EGP between towns
- Shared taxis: Negotiate, usually cheap
- Trains: 2nd class very affordable

**When to Splurge**
- Night trains save hotel costs
- Uber/Careem for safety and convenience
- Domestic flights if time is limited

### Saving on Attractions

**Student Discounts**
- 50% off with valid ISIC card
- Some sites accept any student ID
- Worth getting an ISIC before your trip

**Free or Cheap Activities**
- Walking through Islamic Cairo
- Sunset on the Nile Corniche
- Al-Azhar Park (minimal entry fee)
- Wandering Khan El Khalili bazaar
- Beach time in Dahab or Hurghada

**Bundle Tickets**
- Luxor Pass covers all West Bank sites
- Egypt Pass available for major sites
- Negotiate tours for groups

### Other Money-Saving Tips

- Exchange money at banks, not hotels
- Bargain for everything in markets
- Learn basic Arabic numbers
- Travel in shoulder season (March-May, Sept-Nov)
- Join free walking tours
- Use local SIM cards instead of roaming
- Carry small bills for tips and purchases

### Sample 2-Week Budget Itinerary ($700-900 total)

**Days 1-4: Cairo** - Pyramids, museum, Islamic Cairo
**Days 5-7: Luxor** - Temples, Valley of Kings
**Days 8-9: Aswan** - Nubian village, Philae Temple
**Days 10-14: Dahab or Hurghada** - Beach, snorkeling, relaxing

Egypt rewards budget travelers with incredible experiences at unbeatable prices. The less you spend on luxuries, the more authentic your experience becomes."""
            },
            {
                'title': 'Nile Cruise: Luxor to Aswan Journey',
                'slug': 'nile-cruise-luxor-aswan',
                'category': 'travel-guides',
                'excerpt': 'Experience the magic of a Nile cruise. Everything you need to know about cruising from Luxor to Aswan.',
                'image': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200',
                'featured': True,
                'content': """## Nile Cruise: Luxor to Aswan Journey

A Nile cruise is the most magical way to experience ancient Egypt. Drifting along the world's longest river, visiting temples and tombs, and watching timeless village life pass by - it's an experience unlike any other. This guide covers everything you need to plan your perfect cruise.

![Luxury Nile cruise ship at sunset](https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=800)

### Why Take a Nile Cruise?

![Traditional felucca sailboat on the Nile](https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800)

- **Convenience**: Your hotel moves with you between sites
- **Scenery**: Beautiful views of the Nile, farms, and villages
- **Relaxation**: Pool deck time between temple visits
- **History**: Access to temples along the riverbank
- **Romance**: Sunsets over the Nile are unforgettable

### Types of Nile Cruises

**Large Cruise Ships (100-200 passengers)**
- Most popular option
- Full amenities (pool, restaurants, entertainment)
- Fixed itineraries
- Price: $80-300 per night

**Dahabiyas (Traditional Sailing Boats, 10-20 passengers)**
- Authentic experience
- Intimate atmosphere
- Flexible schedules
- Price: $200-500 per night

**Feluccas (Small Sailboats, 6-12 passengers)**
- Budget option
- Basic facilities (sleep on deck)
- Adventure experience
- Price: $30-50 per night

### Standard Cruise Itinerary

**Day 1: Luxor (Embarkation)**
- Board ship, lunch on board
- Afternoon: Karnak Temple
- Evening: Luxor Temple
- Overnight: Luxor

**Day 2: Luxor West Bank**
- Morning: Valley of the Kings, Hatshepsut Temple
- Lunch on board while sailing
- Afternoon: Sailing to Esna
- Overnight: Esna

**Day 3: Edfu**
- Morning: Temple of Horus at Edfu
- Sailing to Kom Ombo
- Afternoon: Kom Ombo Temple
- Overnight: Sailing to Aswan

**Day 4: Aswan**
- Morning: High Dam, Philae Temple
- Afternoon: Free time or Nubian village visit
- Evening: Felucca ride
- Overnight: Aswan

**Day 5: Aswan (Disembarkation)**
- Optional: Abu Simbel excursion
- Breakfast, disembarkation

### What's Included

Most cruises include:
- Accommodation in private cabin
- All meals (breakfast, lunch, dinner)
- Tea and coffee
- Temple visits with Egyptologist guide
- Entertainment (folklore shows, belly dancing)

Usually NOT included:
- Drinks and alcohol
- Tips for crew and guides
- Optional excursions
- Travel insurance

### Choosing the Right Cruise

**Luxury Options**
- Oberoi Philae, Zahra
- Sonesta Star Goddess, Moon Goddess
- Sanctuary Retreats Sun Boat III

**Mid-Range Options**
- Steigenberger Minerva, Regency
- Mövenpick MS Royal Lily
- Amarco I, II

**Budget Options**
- Many 3-star and 4-star ships available
- Book through local agencies for best rates
- Check recent reviews carefully

### Best Time to Cruise

- **Peak Season**: October-April (best weather, highest prices)
- **Shoulder Season**: March, May, September (good value)
- **Low Season**: June-August (hot but cheapest)

### Tips for Your Cruise

- **Book Ahead**: Popular ships sell out months in advance
- **Check Cabin Location**: Avoid engine rooms, choose upper decks
- **Bring Cash**: For tips, drinks, and purchases
- **Pack Light Layers**: Air conditioning can be cold
- **Bring Sunscreen**: Pool deck time adds up
- **Wake Early**: Temple visits are best before the heat
- **Tip Appropriately**: $10-15/day per person for crew, extra for guides

### How to Book

**Options**:
1. Through a tour operator (most convenient)
2. Direct with cruise company
3. Through Egyptian travel agency (often cheapest)
4. Last-minute deals in Luxor (risky but cheap)

The Nile cruise is often the highlight of any Egypt trip. Watching the sunset over the river while ancient temples glow in the golden light is a memory you'll treasure forever."""
            },
            {
                'title': 'Abu Simbel Temples: Complete Visitor Guide',
                'slug': 'abu-simbel-temples-guide',
                'category': 'ancient-egypt',
                'excerpt': 'Marvel at Ramesses II greatest monument. How to visit Abu Simbel, including the famous sun festival dates.',
                'image': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200',
                'featured': False,
                'content': """## Abu Simbel Temples: Complete Visitor Guide

Abu Simbel is home to two of the most impressive temples in Egypt, carved directly into a mountainside by Ramesses II over 3,200 years ago. The four colossal statues guarding the entrance are among the most iconic images of ancient Egypt. This guide covers everything you need to plan your visit.

![Colossal statues at Abu Simbel temple](https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=800)

### The History of Abu Simbel

![Interior of Abu Simbel with ancient carvings](https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800)

Ramesses II built these temples around 1264 BCE to:
- Commemorate his victory at the Battle of Kadesh
- Impress Egypt's southern neighbors
- Honor himself and his beloved wife Nefertari
- Demonstrate Egypt's power and artistic achievement

In the 1960s, the temples faced destruction from the rising waters of Lake Nasser after the Aswan High Dam was built. In an incredible UNESCO operation, both temples were cut into blocks and relocated 65 meters higher - one of the greatest archaeological rescues in history.

### The Great Temple of Ramesses II

**The Facade**
Four colossal seated statues of Ramesses II, each 20 meters tall, guard the entrance. Smaller statues of family members stand between his legs. One statue's upper body fell during an earthquake in ancient times.

**Inside the Temple**
- **Great Hypostyle Hall**: Eight Osirid pillars showing Ramesses as Osiris
- **Second Hall**: Four pillars with beautiful reliefs
- **Sanctuary**: Four seated gods - the sun illuminates three of them twice a year

**The Sun Festival Phenomenon**
On February 22 and October 22, the rising sun illuminates the sanctuary, lighting up three of the four statues (Ptah, god of the underworld, remains in shadow). Thousands gather to witness this astronomical achievement.

### Temple of Hathor and Nefertari

The smaller temple is dedicated to goddess Hathor and Queen Nefertari. Six 10-meter statues (four of Ramesses, two of Nefertari) adorn the facade. This is the only temple in Egypt where a queen appears the same size as the pharaoh - a testament to Ramesses' love for Nefertari.

### How to Get There

**By Convoy from Aswan (Most Popular)**
- 3-hour drive each way
- Organized tours depart 4-5 AM
- Arrive for sunrise at the temples
- Cost: $50-100 per person

**By Flight from Aswan**
- 30-minute flight
- More expensive but comfortable
- Allows more time at temples
- EgyptAir operates daily flights

**By Cruise (Lake Nasser)**
- Multi-day cruises from Aswan
- Luxurious, relaxed experience
- Visit other lakeside temples
- Cost: $200-500 per night

### Visiting Information

**Opening Hours**: 5 AM - 6 PM (winter), 5 AM - 7 PM (summer)
**Ticket Price**: 240 EGP (approximately $8)
**Photography**: Allowed outside, not inside temples

### Tips for Your Visit

- **Book Accommodation in Aswan**: Most visitors stay in Aswan and day-trip to Abu Simbel
- **Join the Morning Convoy**: Arriving at sunrise is magical and less crowded
- **Spend 2-3 Hours**: Take your time exploring both temples
- **Visit the Exhibition**: Learn about the UNESCO relocation project
- **Bring Water and Snacks**: Limited food options on site
- **Sun Festival Dates**: February 22 and October 22 - book months ahead
- **Hire a Guide**: The history and details are fascinating with expert commentary

### What to Wear

- Comfortable walking shoes
- Light, breathable clothing
- Hat and sunglasses
- Sunscreen (the desert sun is intense)
- Modest dress for entering temples

### Nearby Attractions

If taking a Lake Nasser cruise, you can also visit:
- Temple of Kalabsha
- Temple of Wadi el-Sebua
- Temple of Amada

Abu Simbel is a long journey from anywhere, but the temples are absolutely worth the effort. Standing before these colossal statues, you'll understand why Ramesses II is remembered as one of Egypt's greatest pharaohs."""
            },
            {
                'title': 'Sharm El Sheikh: Ultimate Resort Guide',
                'slug': 'sharm-el-sheikh-resort-guide',
                'category': 'red-sea',
                'excerpt': 'Plan your perfect Sharm El Sheikh vacation. Best resorts, beaches, diving spots, and nightlife.',
                'image': 'https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1200',
                'featured': False,
                'content': """## Sharm El Sheikh: Ultimate Resort Guide

Sharm El Sheikh, located at the southern tip of the Sinai Peninsula, is Egypt's premier beach resort destination. Known for world-class diving, beautiful beaches, and year-round sunshine, "Sharm" attracts millions of visitors every year. This guide will help you plan the perfect vacation.

![Stunning Sharm El Sheikh beach and resort](https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=800)

### Understanding Sharm's Areas

![Crystal clear waters for diving](https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800)

**Naama Bay**
- The heart of Sharm
- Main pedestrian promenade
- Shops, restaurants, nightlife
- Beach clubs and water sports
- Best for: First-timers, nightlife lovers

**Sharks Bay**
- North of Naama
- Quieter, more upscale
- Great snorkeling from shore
- Luxury resorts
- Best for: Divers, relaxation seekers

**Nabq Bay**
- North end of resort area
- Newer developments
- Kite-surfing hub
- Family-friendly resorts
- Best for: Families, water sports enthusiasts

**Hadaba**
- Clifftop area above Naama
- Some older hotels
- Better views, less beach
- More affordable
- Best for: Budget travelers

**Ras Um Sid**
- Southern area
- Beautiful coral reefs
- Quieter atmosphere
- Good restaurants
- Best for: Divers, snorkelers

### Top Resort Recommendations

**Luxury (5-Star)**
- Four Seasons Sharm El Sheikh
- Rixos Premium Seagate
- Savoy Sharm El Sheikh
- Hyatt Regency Sharm El Sheikh

**Mid-Range (4-Star)**
- Coral Sea Sensatori
- Jaz Mirabel Beach
- Stella Di Mare Beach Hotel
- Royal Savoy

**Budget-Friendly**
- Tropitel Naama Bay
- Falcon Naama Star
- Sharm Cliff Resort

### Best Beaches

1. **Ras Um Sid Beach**: Excellent snorkeling, natural reef
2. **Naama Bay Beach**: Central location, water sports
3. **Sharks Bay**: Protected marine area, turtles
4. **White Knight Beach**: Secluded, beautiful views
5. **Farsha Beach**: Bohemian vibes, great for sunset

### Diving and Snorkeling

Sharm offers some of the world's best diving:

**Top Dive Sites**
- Ras Mohammed National Park (famous walls and schools of fish)
- Thistlegorm Wreck (WWII cargo ship)
- Jackson Reef (sharks and currents)
- Blue Hole (Dahab - day trip)
- The Gardens (beautiful coral gardens)

**Snorkeling Options**
- House reefs at most hotels
- Boat trips to offshore reefs
- Ras Mohammed day trip
- Tiran Island excursion

### Things to Do Beyond the Beach

- **Mount Sinai**: Overnight trek for sunrise
- **St. Catherine's Monastery**: UNESCO World Heritage site
- **Colored Canyon**: Stunning rock formations
- **Quad Biking**: Desert adventures
- **Glass-Bottom Boats**: See the reef without getting wet
- **Old Market**: Traditional Sharm, bargain for souvenirs
- **Soho Square**: Evening entertainment
- **SOHO Square**: Modern dining and nightlife

### Nightlife

Sharm has Egypt's liveliest nightlife:
- **Pacha Sharm**: Famous club
- **Little Buddha**: Asian-themed lounge
- **Hard Rock Cafe**: Live music
- **Camel Bar**: Classic Sharm spot
- **Bus Stop**: Local favorite

### Best Time to Visit

- **Peak Season**: December-February (Europeans escaping winter)
- **Best Weather**: March-May, September-November
- **Warmest Sea**: July-September
- **Cheapest**: June-August (very hot, but great deals)

### Practical Information

**Getting There**
- Sharm El Sheikh International Airport (SSH)
- Direct flights from many European cities
- 6-hour bus from Cairo

**Getting Around**
- Taxis (negotiate fare first)
- Hotel shuttles
- Uber is not available
- Walking in Naama Bay is pleasant

**Money**
- Egyptian Pounds (EGP)
- USD and EUR widely accepted
- ATMs throughout resort areas
- Most hotels and restaurants take cards

### Tips for Visitors

- Book all-inclusive for best value
- Bring reef-safe sunscreen
- The sun is intense - use SPF 50+
- Dress modestly outside resorts
- Learn basic Arabic greetings
- Bargain at the Old Market
- Tip 10-15% at restaurants

Sharm El Sheikh offers the perfect combination of relaxation, adventure, and natural beauty. Whether you're a diver seeking underwater thrills or a beach lover wanting to unwind, Sharm delivers an unforgettable Red Sea experience."""
            },
            {
                'title': 'Is Egypt Safe? 2026 Travel Safety Guide',
                'slug': 'is-egypt-safe-2026-guide',
                'category': 'tips-advice',
                'excerpt': 'Get the facts about traveling in Egypt. Safety tips, areas to visit, and what to expect as a tourist.',
                'image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
                'featured': True,
                'content': """## Is Egypt Safe? 2026 Travel Safety Guide

"Is Egypt safe?" is one of the most common questions travelers ask. The short answer is yes - millions of tourists visit Egypt every year without incident. However, like any destination, it pays to be informed and prepared. This guide provides honest, practical safety information.

![Tourists safely exploring the pyramids](https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800)

### Current Safety Situation

![Friendly local Egyptians](https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800)

Egypt has invested heavily in tourism security since 2011. Today, popular tourist areas have:
- Heavy police and security presence
- Metal detectors at major sites and hotels
- Tourist police dedicated to helping visitors
- Security checkpoints on major roads

The main tourist areas (Cairo, Luxor, Aswan, Red Sea resorts) are well-protected and regularly visited by millions of travelers.

### Safe Areas for Tourists

**Very Safe - Standard Precautions**
- Cairo (main tourist areas)
- Giza Pyramids
- Luxor and Aswan
- Hurghada
- Sharm El Sheikh
- Dahab
- Alexandria
- Nile cruise route

**Exercise Increased Caution**
- Remote desert areas (join tours)
- Border regions
- Northern Sinai (avoid)

### Common Safety Concerns Addressed

**Terrorism**
- Tourist areas have not seen incidents for years
- Security presence is very high
- Risk is comparable to major European cities

**Crime**
- Violent crime against tourists is rare
- Petty theft (pickpocketing) can occur in crowded areas
- Keep valuables secure, use hotel safes

**Scams**
- More common than crime
- Overcharging, pushy vendors, "helpful" strangers
- Stay firm, agree prices in advance, use licensed guides

**Traffic**
- Egyptian traffic is chaotic but you'll adapt
- Use Uber/Careem instead of flagging taxis
- Look both ways multiple times before crossing

**Health**
- "Pharaoh's revenge" (traveler's diarrhea) is common
- Stick to bottled water, cooked food initially
- Bring medications from home

### Safety Tips for All Travelers

**Before You Go**
- Register with your embassy
- Get travel insurance
- Check government travel advisories
- Share your itinerary with someone at home
- Download offline maps

**Money Safety**
- Use ATMs inside banks or hotels
- Don't carry large amounts of cash
- Split your money in different places
- Keep copies of important documents

**At Tourist Sites**
- Use licensed guides
- Agree prices before services
- Keep belongings close in crowded places
- Don't follow strangers offering "help"
- Trust your instincts

**On the Street**
- Dress modestly (especially women)
- Walk confidently, look like you know where you're going
- Avoid walking alone late at night
- Keep phone and valuables out of sight

### Safety Tips for Women

Egypt is generally safe for women, but harassment (verbal, occasionally physical) does occur. Tips:
- Dress conservatively (covered shoulders, knees)
- Wear a wedding ring (real or fake)
- Avoid eye contact with harassers
- Stay in well-lit, populated areas at night
- Consider joining group tours
- Don't hesitate to be firm with unwanted attention
- Seek help from police or other women if needed

### Safety Tips for Solo Travelers

- Stay in hostels or hotels with good reviews
- Join group tours for major sites
- Keep someone informed of your plans
- Be extra cautious at night
- Trust your instincts about people and situations

### What to Do If Something Goes Wrong

**Emergency Numbers**
- Tourist Police: 126
- Ambulance: 123
- Police: 122

**Embassy Contacts**
- Know your embassy's location and phone number
- They can help with lost passports, emergencies, legal issues

### The Reality

Millions of tourists visit Egypt safely every year. The vast majority have wonderful experiences without any safety issues. Egyptians are famously hospitable and will often go out of their way to help visitors.

Use common sense, stay informed, and don't let fear prevent you from experiencing one of the world's most incredible destinations. Egypt's ancient wonders, warm hospitality, and rich culture are absolutely worth experiencing."""
            },
            {
                'title': 'Egyptian Museum Cairo: Treasures Guide',
                'slug': 'egyptian-museum-cairo-treasures',
                'category': 'destinations',
                'excerpt': 'Home to Tutankhamun gold. Complete guide to the Egyptian Museum most important artifacts and galleries.',
                'image': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200',
                'featured': False,
                'content': """## Egyptian Museum Cairo: Treasures Guide

The Egyptian Museum in Tahrir Square is home to the world's largest collection of ancient Egyptian artifacts - over 120,000 items spanning 5,000 years of history. From Tutankhamun's golden treasures to royal mummies, this museum is an essential stop for anyone interested in ancient Egypt.

![The Egyptian Museum facade](https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800)

### Museum Overview

![Ancient Egyptian artifacts on display](https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800)

**Location**: Tahrir Square, Downtown Cairo
**Opening Hours**: 9 AM - 5 PM daily (until 9 PM on Fridays)
**Ticket Prices**:
- General admission: 300 EGP
- Mummy Room: 180 EGP additional
- Photography: 50 EGP

**Note**: The new Grand Egyptian Museum (GEM) near the Pyramids is now open and houses many treasures, including most of Tutankhamun's collection.

### Must-See Treasures

**Ground Floor Highlights**

**1. Narmer Palette**
One of the most important artifacts in Egyptology, this 5,000-year-old ceremonial palette shows the unification of Upper and Lower Egypt.

**2. Rahotep and Nofret Statues**
Stunningly preserved painted limestone statues from the Old Kingdom. The colors look like they were painted yesterday.

**3. Khafre Enthroned**
Magnificent diorite statue of the pyramid-building pharaoh, protected by the Horus falcon.

**4. Wooden Statue of Ka-Aper**
So lifelike that the workers who discovered it thought it was their village chief - they called him "Sheikh el-Balad."

**5. Meidum Geese**
Exquisite painting of geese from 4,600 years ago, often called the "Egyptian Mona Lisa."

### Upper Floor - Tutankhamun Galleries

The boy king's treasures dominated the upper floor for decades. While many items have moved to the GEM, you can still see:

**The Golden Death Mask** (if still present - check current location)
- 11 kg of solid gold
- Most famous artifact in the world
- Incredibly detailed craftsmanship

**Golden Throne**
- Covered in gold and silver
- Shows Tutankhamun with his wife Ankhesenamun
- Beautiful inlay work

**Canopic Shrine**
- Four miniature golden coffins
- Held the pharaoh's internal organs
- Protected by four goddesses

**Jewelry Collection**
- Pectorals, necklaces, rings, bracelets
- Incredible craftsmanship
- Precious stones and gold

### The Royal Mummy Room

**Extra ticket required (180 EGP)**

This hushed, dimly lit room contains mummified remains of Egypt's greatest pharaohs:
- Ramesses II (The Great)
- Seti I
- Thutmose III
- Hatshepsut
- And many others

Standing before these 3,000-year-old pharaohs is a profound experience.

### Tips for Your Visit

**Timing**
- Arrive when it opens (9 AM) to avoid crowds
- Allow 3-4 hours minimum
- Visit on weekday mornings for fewer tourists

**Navigation**
- Get a map at the entrance
- The museum is not well-labeled - a guide is helpful
- Ground floor roughly chronological, upper floor thematic

**What to Bring**
- Comfortable shoes
- Camera (if you buy photo ticket)
- Water (cafeteria inside)
- Patience - it gets crowded

**Guides**
- Official guides available at entrance
- Budget $20-40 for a 2-hour tour
- Book through your hotel for better quality

### What You Might Miss

Many visitors rush past these treasures:
- Akhenaten statues (revolutionary art style)
- Yuya and Tuya collection (Tutankhamun's great-grandparents)
- Middle Kingdom wooden models
- Greco-Roman mummy portraits
- The animal mummy room

### The Grand Egyptian Museum

The new GEM near the Pyramids is now the primary home for many treasures, including:
- Complete Tutankhamun collection (5,000+ items)
- Massive Ramesses II statue
- Solar Boat of Khufu
- Modern exhibition spaces

Consider visiting both museums for the complete experience.

### Practical Information

**Getting There**
- Located on Tahrir Square
- Walk from downtown hotels
- Metro: Sadat Station
- Uber/taxi drop-off at museum entrance

**Nearby**
- Islamic Cairo (15 minutes)
- Khan El Khalili (20 minutes)
- Nile Corniche (5 minute walk)

The Egyptian Museum remains one of the world's great museums. Despite aging facilities, the sheer quantity and quality of artifacts is overwhelming. Every mummy, every statue, every tiny amulet has a story spanning millennia."""
            },
            {
                'title': 'Aswan: Gateway to Nubia Guide',
                'slug': 'aswan-gateway-nubia-guide',
                'category': 'destinations',
                'excerpt': 'Discover Aswan temples, Nubian villages, and the beautiful Nile. Complete travel guide to southern Egypt.',
                'image': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
                'featured': False,
                'content': """## Aswan: Gateway to Nubia Guide

Aswan is Egypt's sunniest southern city, where the Nile flows through golden sand and granite islands. Less hectic than Cairo and more relaxed than Luxor, Aswan offers a unique blend of ancient temples, Nubian culture, and natural beauty. It's also the gateway to Abu Simbel and Lake Nasser.

![Beautiful Nile view in Aswan](https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800)

### Why Visit Aswan?

![Colorful Nubian village](https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800)

- **Beautiful Setting**: The Nile at its most scenic
- **Nubian Culture**: Vibrant, colorful heritage
- **Ancient Temples**: Philae, Kalabsha, Abu Simbel
- **Relaxed Atmosphere**: Slower pace than other cities
- **Winter Weather**: Perfect warmth from October-April
- **Gateway**: Abu Simbel, Lake Nasser cruises

### Top Attractions

**Philae Temple (Temple of Isis)**
Dedicated to goddess Isis, this beautiful temple was relocated to Agilika Island after the Aswan Dam flooded its original location. Take a boat across the lake and watch the temple glow in morning light.
- **Entry**: 300 EGP
- **Sound and Light Show**: Worth seeing

**Aswan High Dam**
This massive engineering project created Lake Nasser and changed Egypt forever. The views from the top are impressive, and there's a monument to Egyptian-Soviet cooperation.
- **Entry**: Free

**Unfinished Obelisk**
The largest ancient obelisk ever attempted - it cracked during construction and was abandoned in the quarry. Walking around it gives you a sense of ancient stone-working techniques.
- **Entry**: 150 EGP

**Nubian Villages**
Take a boat or camel ride to the colorful villages on Elephantine Island or the West Bank. The painted houses, friendly people, and traditional hospitality are highlights of any Aswan visit.
- **Tip**: Visit in late afternoon for best light and cooler temperatures

**Elephantine Island**
One of the oldest inhabited places in Egypt with ancient temples, a Nilometer, and lovely walks among palm trees.

### More Experiences

**Felucca Sailing**
A sunset felucca ride around Elephantine Island and Kitchener's Island is magical. Negotiate directly with captains at the Corniche.
- **Price**: 200-300 EGP for 1-2 hours

**Kitchener's Island (Aswan Botanical Garden)**
Lord Kitchener turned this island into a tropical garden. It's a peaceful escape with exotic plants from around the world.
- **Entry**: 55 EGP

**Tombs of the Nobles**
Carved into the hillside across the river, these tombs offer great views and interesting decorations dating back 4,000 years.

**Aswan Museum**
Small but excellent collection in a beautiful setting on Elephantine Island.

### Day Trips from Aswan

**Abu Simbel**
The famous temples of Ramesses II, 3 hours drive south. Most visitors join the 4 AM convoy for a day trip.

**Kalabsha Temple**
Relocated near the High Dam, this Nubian temple is impressive and less crowded than Philae.

**Wadi el-Sebua**
Lake Nasser cruise to remote temples rarely visited by tourists.

### Where to Stay

**Luxury**
- Sofitel Legend Old Cataract: Historic, gorgeous, where Agatha Christie wrote
- Mövenpick Resort: Island setting, great facilities

**Mid-Range**
- Basma Hotel: Great views, comfortable
- Pyramisa Isis Island: Island resort, good value
- Helnan Aswan: Overlooking the Nile

**Budget**
- Keylany Hotel: Rooftop restaurant, good location
- Nubian Oasis Hotel: Simple, clean, friendly
- Mango Guest House: Budget with character

### Best Restaurants

- 1902 Restaurant (Old Cataract): Fine dining, stunning views
- Nubian House: Traditional food, cultural show
- Al Makka: Local favorite, rooftop
- Panorama Restaurant: River views, good food
- Salah El Din: Authentic Egyptian

### Practical Information

**Getting There**
- Aswan Airport: Flights from Cairo, Luxor
- Train from Cairo (12-14 hours) or Luxor (3 hours)
- Nile cruise from Luxor

**Best Time to Visit**
- October-April: Perfect weather (20-30°C)
- May-September: Very hot (40°C+)

**Getting Around**
- Walking along Corniche is pleasant
- Taxis for longer distances
- Feluccas and boats for island hopping
- Horse carriages (negotiate prices)

### Nubian Culture

The Nubian people have lived in this region for thousands of years. Their culture features:
- Distinctive colorful art and architecture
- Unique language (still spoken)
- Traditional music and dance
- Famous hospitality
- Distinctive cuisine

Visiting a Nubian village and sharing tea with a family is a highlight of any Egypt trip.

### Tips for Your Visit

- Aswan is small - 2-3 days is enough
- Sunsets from the Corniche are spectacular
- Take a felucca ride - it's essential
- Visit Nubian villages for authentic culture
- Book Abu Simbel trip through your hotel
- Bring sun protection - it's Egypt's hottest city
- Learn a few Nubian greeting phrases

Aswan is many travelers' favorite Egyptian city - the combination of natural beauty, fascinating history, and warm Nubian hospitality creates an unforgettable experience."""
            },
            {
                'title': 'White Desert Egypt: Camping Adventure',
                'slug': 'white-desert-egypt-camping',
                'category': 'travel-guides',
                'excerpt': 'Experience the surreal White Desert. Guide to camping among chalk formations under starry skies.',
                'image': 'https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=1200',
                'featured': False,
                'content': """## White Desert Egypt: Camping Adventure

The White Desert is one of Egypt's most otherworldly landscapes - a surreal world of brilliant white chalk formations sculpted by wind into mushrooms, towers, and fantastical shapes. Camping under a blanket of stars among these ancient rock sculptures is an unforgettable experience.

![Surreal white chalk formations in the desert](https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=800)

### What is the White Desert?

![Desert camping under the stars](https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=800)

Located in the Western Desert about 500km southwest of Cairo, the White Desert (Sahara el-Beyda) is a national park protecting unique geological formations. Millions of years ago, this area was a seabed. The chalk and limestone deposits, eroded by wind over millennia, have created an alien landscape unlike anywhere else on Earth.

### Getting There

**From Cairo**
The White Desert is reached through Bahariya Oasis, approximately:
- 5-6 hours drive from Cairo to Bahariya
- 2-3 hours from Bahariya to White Desert

**Tour Options**
Almost all visitors join organized tours that include:
- 4x4 desert vehicles
- Camping equipment
- Food and water
- Experienced Bedouin guides
- National park fees

### What to Expect on a Typical Tour

**Day 1**
- Morning departure from Cairo or Bahariya
- Visit Black Desert (volcanic hills)
- Crystal Mountain (quartz formations)
- Lunch in the desert
- Enter White Desert at sunset
- Camp among the formations
- Bedouin dinner under stars
- Stargazing

**Day 2**
- Wake for sunrise photography
- Explore more formations
- Visit Agabat Valley (pristine white formations)
- Return via Bahariya
- Optional: Hot springs visit
- Return to Cairo

### The Magic of Desert Camping

**Sunset**
Watch the white formations turn golden, then pink, then purple as the sun sets. It's one of Egypt's most photogenic moments.

**Stargazing**
With zero light pollution, the Milky Way stretches overhead in breathtaking clarity. You'll see more stars than you thought existed.

**Silence**
The profound silence of the desert is meditative. No traffic, no phones, just wind and stars.

**Bedouin Hospitality**
Your guides cook traditional food over open fires. Tea is always brewing. Stories are shared under the stars.

### Formations to See

- **Mushroom Rocks**: The most iconic - balanced boulders on thin stems
- **The Chicken**: Famous formation resembling a giant chicken
- **Inselbergs**: Isolated hills rising from flat desert
- **Chalk Towers**: Pillars carved by wind erosion
- **Agabat Valley**: Pristine white formations, restricted access

### Practical Information

**Best Time to Visit**
- October to April: Comfortable temperatures
- December-February: Cold nights, warm days
- Avoid summer: Extreme heat (45°C+)

**What to Bring**
- Warm layers (desert nights are cold, even in winter)
- Sleeping bag liner (tours provide equipment)
- Camera and extra batteries
- Flashlight/headlamp
- Sunscreen and sunglasses
- Comfortable walking shoes
- Hat for sun protection
- Personal medications
- Cash for tipping guides

**Tour Costs**
- Budget tours: $60-80 per person (2 days/1 night)
- Mid-range tours: $100-150 per person
- Private tours: $200+ per person
- Price includes everything except tips

### Booking a Tour

**From Cairo**
Many hotels and travel agencies offer packages. Recommended operators:
- Western Desert Tours
- Egypt Western Desert
- Bahariya Safari

**From Bahariya Oasis**
More options and often cheaper if you arrange locally.

### Important Tips

- **Physical Condition**: Tours involve some walking on sand, but nothing strenuous
- **Photography**: Bring extra batteries (cold drains them fast)
- **Camping Comfort**: Sleeping pads and blankets are provided, but bring a liner
- **Water**: Tours provide water, but bring extra
- **Respect the Environment**: Leave no trace, take only photos
- **Wildlife**: Foxes may visit camp - don't feed them

### Combining with Other Destinations

The White Desert works well combined with:
- Bahariya Oasis hot springs and palm groves
- Black Desert volcanic landscape
- Siwa Oasis (longer trip)
- Cairo (entry/exit point)

### What Makes It Special

The White Desert isn't just about strange rocks - it's about experiencing:
- Complete disconnection from modern life
- Ancient landscapes unchanged for millennia
- Bedouin culture and hospitality
- The vastness of the Sahara
- Unforgettable sunrises and sunsets
- A sky full of stars

Camping in the White Desert is one of those travel experiences that stays with you forever. The combination of surreal landscape, profound silence, and brilliant stars creates memories you'll treasure for a lifetime."""
            },
            {
                'title': 'Alexandria: Mediterranean Egypt Guide',
                'slug': 'alexandria-mediterranean-egypt-guide',
                'category': 'destinations',
                'excerpt': 'Explore Egypt second city. From the new Library to seafood restaurants, discover Alexandria charms.',
                'image': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=1200',
                'featured': False,
                'content': """## Alexandria: Mediterranean Egypt Guide

Alexandria is Egypt's second-largest city and its window to the Mediterranean world. Founded by Alexander the Great in 331 BCE, this city was once the intellectual capital of the ancient world, home to the legendary Library and the Pharos Lighthouse. Today, Alexandria offers a different Egypt - breezy, cosmopolitan, and flavored with Greek, Italian, and French influences.

![Alexandria waterfront and Mediterranean Sea](https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800)

### Why Visit Alexandria?

![The new Bibliotheca Alexandrina](https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800)

- **Different Atmosphere**: Mediterranean vibes unlike anywhere else in Egypt
- **Ancient History**: Cleopatra's city, once rivaling Rome
- **The Library**: Stunning modern architecture honoring ancient scholarship
- **Seafood**: Egypt's best fish restaurants
- **Corniche**: Beautiful waterfront promenade
- **Day Trip**: Easy 3-hour train ride from Cairo

### Top Attractions

**Bibliotheca Alexandrina (New Library)**
The modern library, opened in 2002, honors the ancient Library of Alexandria. The stunning tilted disc architecture houses millions of books, museums, and exhibition spaces. Even non-bookworms are impressed.
- **Entry**: 70 EGP
- **Hours**: 10 AM - 7 PM (closed Friday morning)

**Citadel of Qaitbay**
This 15th-century fortress sits on the site of the ancient Pharos Lighthouse, one of the Seven Wonders. The views of the harbor are beautiful, and the interior has a small naval museum.
- **Entry**: 60 EGP

**Catacombs of Kom el-Shoqafa**
Fascinating underground tombs mixing Egyptian, Greek, and Roman styles. The descent into these 2nd-century chambers is eerie and memorable.
- **Entry**: 80 EGP

**Pompey's Pillar**
A 27-meter red granite column erected in honor of Emperor Diocletian. It's impressive but can be combined with the nearby Serapeum ruins.
- **Entry**: 80 EGP

**Roman Amphitheater**
Small but well-preserved Roman theater discovered accidentally in 1960. The marble seats and acoustics are still remarkable.
- **Entry**: 60 EGP

### The Corniche Experience

Alexandria's waterfront Corniche stretches for miles along the Mediterranean. Walking here is essential:
- Watch waves crash against the seawall
- See old-style cafes and new restaurants
- Observe locals fishing, walking, courting
- Catch sunset over the Mediterranean
- Find hidden beaches and swimming spots

### Where to Eat

**Seafood (Alexandria's Specialty)**
- **Fish Market Restaurant**: Choose your fish, choose your preparation
- **Kadoura**: Legendary, always packed
- **Seagull**: Upscale, waterfront views
- **Tikka Grill**: Modern Egyptian seafood

**Traditional Egyptian**
- **Mohammed Ahmed**: Famous ful and falafel since 1910
- **Hosny**: Historic restaurant, excellent Egyptian food

**Historic Cafes**
- **Trianon**: Belle époque elegance, pastries
- **Délices**: Greek-Egyptian sweets since 1922
- **Brazilian Coffee Store**: Atmospheric old cafe

### Day Trip Itinerary

If visiting from Cairo (3 hours by train), here's a suggested one-day itinerary:

**Morning**
- 7 AM train from Cairo Ramses Station
- Arrive Alexandria ~10 AM
- Visit Bibliotheca Alexandrina
- Coffee break nearby

**Midday**
- Walk along Corniche to Citadel
- Visit Qaitbay Citadel
- Seafood lunch at Fish Market

**Afternoon**
- Catacombs of Kom el-Shoqafa
- Pompey's Pillar (quick stop)
- Stroll through old Greek quarter

**Evening**
- Sunset on the Corniche
- Dinner at Kadoura
- 8 PM train back to Cairo

### Staying Overnight

**Luxury**
- Four Seasons San Stefano
- Hilton Alexandria Corniche
- Steigenberger Cecil Hotel (historic)

**Mid-Range**
- Paradise Inn Windsor Palace
- Romance Alexandria Corniche
- Cherry Maryski Hotel

**Budget**
- Union Hotel
- Triomphe Hostel
- Various Airbnbs downtown

### Practical Information

**Getting There**
- Train from Cairo: 3 hours, comfortable, cheap
- Bus from Cairo: 3 hours, frequent departures
- Car: 3 hours via desert road

**Getting Around**
- Yellow trams are charming but slow
- Uber and Careem work well
- Taxis (negotiate first)
- Walking along Corniche is pleasant

**Best Time to Visit**
- Year-round destination (Mediterranean climate)
- Summer: Egyptians crowd beaches
- Winter: Cooler, sometimes rainy, fewer crowds
- Spring/Fall: Ideal weather

### Historical Notes

Ancient Alexandria was:
- Capital of Ptolemaic Egypt
- Home of Cleopatra VII
- Location of the Great Library (tragically lost)
- Site of the Pharos Lighthouse (one of Seven Wonders)
- A center of learning (Euclid, Ptolemy, Hypatia taught here)

While little remains of ancient Alexandria (it's under the modern city and sea), the spirit of cosmopolitan learning continues.

### Tips for Visitors

- Alexandria is more liberal than Cairo - but still dress modestly
- Try the seafood - it's Egypt's best
- The Corniche is best at sunset
- Train is better than bus from Cairo
- Don't skip the Library even if you're not a reader
- Allow time just to wander and soak up the atmosphere

Alexandria offers a different side of Egypt - more Mediterranean, more cosmopolitan, more relaxed. It's worth at least a day trip, but staying overnight lets you fully appreciate this fascinating city's unique character."""
            },
            {
                'title': 'Egyptian Coffee Culture: A Local Experience',
                'slug': 'egyptian-coffee-culture-guide',
                'category': 'food-culture',
                'excerpt': 'Experience ahwa like a local. Guide to Egyptian coffee houses, traditions, and the best cafes.',
                'image': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=1200',
                'featured': False,
                'content': """## Egyptian Coffee Culture: A Local Experience

The ahwa (coffee house) is the heart of Egyptian social life. For centuries, men have gathered in these establishments to drink coffee and tea, smoke shisha, play backgammon, watch football, and discuss everything from politics to philosophy. Understanding Egyptian coffee culture gives you insight into the Egyptian soul.

![Traditional Egyptian coffee house](https://images.unsplash.com/photo-1511920170033-f8396924c348?w=800)

### History of Egyptian Coffee Houses

![Turkish coffee being poured](https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800)

Coffee arrived in Egypt from Yemen in the 16th century and quickly became central to social life. The traditional ahwa has changed little since then:
- Simple furniture (often plastic or wooden chairs)
- Small tables for games and drinks
- Television showing football or news
- Shisha pipes lined up
- Tea and coffee prepared the traditional way

### What to Drink

**Turkish Coffee (Ahwa)**
Egyptian coffee is prepared Turkish-style - finely ground beans boiled with water and sugar in a small pot called a kanaka.

Order by sweetness:
- **Sada**: No sugar (bitter)
- **Ariha**: Slightly sweet
- **Mazboot**: Medium sweet (most popular)
- **Ziyada**: Very sweet

The coffee comes in a small cup. Don't drink the grounds at the bottom!

**Tea (Shai)**
Equally popular, tea is served:
- **Shai Koshary**: Strong tea with lots of sugar
- **Shai bil-na'na'**: Tea with fresh mint
- **Shai bil-laban**: Tea with milk

**Other Drinks**
- **Karkade**: Hibiscus tea (hot or cold)
- **Sahlab**: Warm, milky drink with nuts
- **Tamarind**: Refreshing tamarind juice
- **Lemon with mint**: Fresh and cooling

### The Shisha Experience

No ahwa is complete without shisha (water pipe), called "shisha" or "hubbly bubbly":
- Tobacco comes in many flavors (apple, grape, mint, mixed)
- Usually shared with friends
- Takes 30-60 minutes to enjoy
- Costs 25-60 EGP depending on location

**Etiquette**
- Pass the pipe handle first, not the hose
- Don't blow smoke in others' faces
- It's okay to share with strangers if they offer
- Clean the mouthpiece before passing (disposable tips available)

### Games at the Ahwa

**Tawla (Backgammon)**
The most popular game - you'll hear dice clacking everywhere. It's taken very seriously.

**Dominoes**
Slapped down loudly on metal tables - the noise is part of the fun.

**Cards**
Various games played, often for small stakes.

Watching locals play is entertaining; joining in (if invited) is even better.

### Famous Historic Cafes

**Cairo**
- **Fishawi's** (Khan El Khalili): Tourist-famous but atmospheric, open 24 hours for 250 years
- **El Horreya** (Downtown): Intellectuals' hangout since 1940s, great people-watching
- **Café Riche** (Downtown): Historic literary cafe, revolutionaries met here
- **Naguib Mahfouz Cafe** (Khan El Khalili): Named for Nobel laureate, elegant setting

**Alexandria**
- **Trianon**: Belle époque elegance
- **Brazilian Coffee Store**: Historic downtown institution
- **Délices**: Greek-Egyptian patisserie tradition

### Modern Coffee Culture

Egypt now has a thriving modern cafe scene:
- **Costa, Starbucks**: International chains everywhere
- **Cilantro**: Local chain, excellent coffee
- **Beano's**: Good espresso, Western pastries
- **Left Bank**: Hipster cafes, specialty coffee
- **Harris Cafe**: Instagram-worthy spots

These offer espresso, cappuccino, and familiar Western drinks, but you'll miss the traditional experience.

### Coffee House Etiquette

- Men traditionally dominate ahwas, but tourist women are welcome in touristy areas
- Order when you arrive - service comes to your table
- Pay when you're ready to leave
- Tip 10-15% or round up
- Feel free to stay for hours - no one will rush you
- Striking up conversation is encouraged
- Taking photos is fine but ask first

### Finding Authentic Ahwas

The best ahwas are:
- On side streets, not main tourist roads
- Filled with locals, not tourists
- Simple in appearance
- Playing Arabic music or football
- Noisy with conversation and game sounds

### What Makes It Special

The ahwa is not just about coffee - it's about:
- Escaping daily stress
- Connecting with friends and strangers
- Watching the world go by
- Feeling the pulse of Egyptian life
- Time slowing down

In our rushed world, the Egyptian coffee house reminds us of the value of simply sitting, sipping, and being present.

### Tips for Visitors

- Try Turkish coffee at least once - it's an acquired taste
- Order shisha to extend your experience
- Don't rush - lingering is expected
- Learn a few Arabic phrases
- Be open to conversation with locals
- Early evening is the liveliest time
- Some ahwas are open 24 hours

Spending an evening at a traditional ahwa is one of the most authentic Egyptian experiences you can have. No monuments, no museums - just coffee, conversation, and connection."""
            },
        ]

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').order_by('-published_at', '-created_at')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(
            posts__status='published'
        ).distinct().order_by('name')
        context['featured_posts'] = BlogPost.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_at')[:6]
        context['recent_posts'] = BlogPost.objects.filter(status='published')[:5]

        # New context for enhanced blog list
        context['current_category'] = self.request.GET.get('category', '')
        context['featured_post'] = BlogPost.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_at').first()
        context['trending_posts'] = BlogPost.objects.filter(
            status='published'
        ).order_by('-views_count', '-published_at')[:5]
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        import sys
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(f"BLOG_DETAIL_ERROR: {str(e)}", file=sys.stderr)
            print(f"BLOG_DETAIL_TRACE: {traceback.format_exc()}", file=sys.stderr)
            return JsonResponse({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'view': 'BlogDetailView',
                'slug': kwargs.get('slug', 'unknown')
            }, status=500)

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Comments
        context['comments'] = post.comments.filter(status='approved')

        # Smart Related Articles Algorithm
        # Priority: Same category > Similar tags > Popular > Recent
        related_posts = []

        # 1. Same category articles
        if post.category:
            same_category = BlogPost.objects.filter(
                status='published',
                category=post.category
            ).exclude(id=post.id).order_by('-views_count')[:3]
            related_posts.extend(list(same_category))

        # 2. Fill with popular posts if needed
        if len(related_posts) < 5:
            popular = BlogPost.objects.filter(
                status='published'
            ).exclude(id=post.id).exclude(
                id__in=[p.id for p in related_posts]
            ).order_by('-views_count')[:5 - len(related_posts)]
            related_posts.extend(list(popular))

        context['related_posts'] = related_posts[:5]

        # Recent posts for sidebar
        context['recent_posts'] = BlogPost.objects.filter(
            status='published'
        ).exclude(id=post.id).order_by('-published_at')[:5]

        # Trending posts
        context['trending_posts'] = BlogPost.objects.filter(
            status='published'
        ).order_by('-views_count')[:5]

        # Categories for navigation
        context['categories'] = BlogCategory.objects.filter(
            posts__status='published'
        ).distinct()

        # Reading time calculation
        word_count = len(post.content.split()) if post.content else 0
        context['reading_time'] = max(1, word_count // 200)

        # Next/Previous articles
        context['next_post'] = BlogPost.objects.filter(
            status='published',
            published_at__gt=post.published_at
        ).order_by('published_at').first()

        context['prev_post'] = BlogPost.objects.filter(
            status='published',
            published_at__lt=post.published_at
        ).order_by('-published_at').first()

        # Total article count for social proof
        context['total_articles'] = BlogPost.objects.filter(status='published').count()

        return context


def pillar_egypt_guide(request):
    """
    SEO Pillar Page: Ultimate Egypt Travel Guide
    This comprehensive page targets high-volume keywords
    """
    context = {
        'page_title': 'Ultimate Egypt Travel Guide 2026: Everything You Need to Know',
        'meta_description': 'Complete Egypt travel guide covering visa, costs, best time to visit, top attractions, safety tips, and insider advice. Plan your perfect Egypt trip.',

        # Featured content by category
        'pyramid_articles': BlogPost.objects.filter(
            status='published',
            slug__icontains='pyramid'
        ).order_by('-views_count')[:4],

        'travel_tips': BlogPost.objects.filter(
            status='published',
            category__slug='travel-guides'
        ).order_by('-views_count')[:4],

        'destination_articles': BlogPost.objects.filter(
            status='published',
            category__slug='destinations'
        ).order_by('-views_count')[:4],

        'history_articles': BlogPost.objects.filter(
            status='published',
            category__slug='ancient-egypt'
        ).order_by('-views_count')[:4],

        # Stats for social proof
        'total_articles': BlogPost.objects.filter(status='published').count(),
        'total_views': BlogPost.objects.filter(status='published').aggregate(
            total=models.Sum('views_count')
        )['total'] or 0,
    }

    return render(request, 'blog/pillar_egypt_guide.html', context)