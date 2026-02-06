"""
Egy360 URL Configuration
========================

This module defines all URL routes for the Egy360 travel platform.

URL Structure:
- /                 - Homepage and landing pages
- /admin/           - Django admin interface
- /accounts/        - User authentication (login, register, profile)
- /auth/            - OAuth social login (Google, Facebook)
- /tours/           - Tour packages and experiences
- /accommodations/  - Hotels, resorts, vacation rentals
- /destinations/    - Egyptian cities and attractions
- /blog/            - Travel guides and articles
- /bookings/        - Booking management
- /payments/        - Payment processing (PayMob)
- /api/             - REST API endpoints
- /dashboard/       - User dashboard

Special URLs:
- /health/          - Health check for Railway deployment
- /favicon.svg      - Site favicon (Ankh symbol)
- /sitemap.xml      - SEO sitemap
- /robots.txt       - SEO robots file

Author: Egy360 Team
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import sitemaps
import os

def health_check(request):
    """Basic health check for Railway"""
    import traceback
    from django.db import connection

    response = {'status': 'ok', 'version': 'v8-sqlite-mode', 'branch': 'main'}

    # Always include DB info
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        response['db_connected'] = True
        response['db_engine'] = connection.vendor
    except Exception as e:
        response['db_connected'] = False
        response['db_error'] = str(e)

    # Add blog debug info if requested
    if request.GET.get('debug') == 'blog':
        try:
            from blog.models import BlogPost, BlogCategory
            response['total_posts'] = BlogPost.objects.count()
            response['published_posts'] = BlogPost.objects.filter(status='published').count()
            response['categories'] = BlogCategory.objects.count()
        except Exception as e:
            response['blog_error'] = str(e)
            response['blog_traceback'] = traceback.format_exc()

    return JsonResponse(response)

def debug_db(request):
    """Debug endpoint to test database access"""
    import traceback
    try:
        from blog.models import BlogPost
        from django.db import connection

        # Test DB connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Count posts
        count = BlogPost.objects.count()
        published = BlogPost.objects.filter(status='published').count()

        return JsonResponse({
            'status': 'ok',
            'db_connected': True,
            'total_posts': count,
            'published_posts': published,
            'database_engine': connection.vendor,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)

def robots_txt(request):
    """SEO robots.txt file"""
    content = """User-agent: *
Allow: /
Allow: /blog/
Allow: /destinations/

Disallow: /admin/
Disallow: /accounts/
Disallow: /api/
Disallow: /dashboard/
Disallow: /bookings/
Disallow: /payments/

# Sitemap
Sitemap: https://egy360.com/sitemap.xml

# Crawl-delay for politeness
Crawl-delay: 1
"""
    return HttpResponse(content, content_type='text/plain')

def seed_articles(request):
    """Seed pyramid articles - access via /seed/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    category, _ = BlogCategory.objects.get_or_create(
        slug='ancient-egypt',
        defaults={'name': 'Ancient Egypt', 'description': 'Ancient Egypt wonders'}
    )

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    articles = [
        ('The Great Pyramid of Giza: 4,500 Years of Mystery', 'great-pyramid-giza-introduction', 'Discover the Great Pyramid - the only surviving Ancient Wonder.', 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200', True),
        ('Building the Great Pyramid: Timeline and Workers', 'great-pyramid-history-timeline-workers', 'How long did it take? Who built it? The complete timeline.', 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200', False),
        ('Great Pyramid Architecture: Impossible Precision', 'great-pyramid-architecture-precision', '99.98% symmetrical, aligned to true north - how?', 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200', False),
        ("The King's Chamber: Heart of the Pyramid", 'great-pyramid-kings-chamber-secrets', 'Granite from 800km away, mysterious shafts, empty sarcophagus.', 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200', False),
        ('How Was the Great Pyramid Built?', 'great-pyramid-construction-methods', 'No wheels, no cranes, no iron - construction methods explained.', 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200', False),
        ('Cutting Pyramid Stones With Copper Tools', 'great-pyramid-stone-cutting', "Precision you can't fit paper through - with copper tools.", 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200', False),
        ('Moving 2.3 Million Pyramid Blocks', 'great-pyramid-transporting-stones', '80-ton blocks, 800km journey, no wheels - how?', 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200', False),
        ('Great Pyramid Myths Debunked', 'great-pyramid-myths-debunked', "No aliens. No slaves. Here's what evidence shows.", 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200', False),
        ('Why Was the Great Pyramid Built?', 'great-pyramid-purpose-meaning', '20 years, millions of blocks - what was the purpose?', 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200', False),
    ]

    created = 0
    for title, slug, excerpt, img, featured in articles:
        _, was_created = BlogPost.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title, 'author': author, 'category': category,
                'excerpt': excerpt, 'content': f'## {title}\n\n{excerpt}\n\nPart of our Great Pyramid series.',
                'image_url': img, 'meta_description': excerpt,
                'meta_keywords': 'great pyramid, giza, egypt',
                'tags': 'pyramids, giza, ancient egypt',
                'status': 'published', 'is_featured': featured,
                'published_at': timezone.now(),
            }
        )
        if was_created:
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': 9})

def seed_2026_articles(request):
    """Seed 2026 travel guide articles - access via /seed2026/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    category, _ = BlogCategory.objects.get_or_create(
        slug='travel-tips',
        defaults={'name': 'Travel Tips', 'description': 'Egypt travel tips and guides'}
    )

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    articles = [
        {
            'slug': 'best-egypt-tours-2026-complete-guide',
            'title': 'Best Egypt Tours 2026: Complete Guide to Top 10 Tour Packages',
            'excerpt': 'Discover the best Egypt tours for 2026. From luxury Nile cruises to budget backpacker trips.',
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
            'is_featured': True,
        },
        {
            'slug': 'egypt-on-a-budget-2026-travel-guide',
            'title': 'Egypt on a Budget 2026: How to Travel Egypt for Under $50/Day',
            'excerpt': 'Complete guide to budget travel in Egypt. Save money on accommodation, food, and transport.',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'is_featured': False,
        },
        {
            'slug': 'nile-cruise-guide-2026-everything-you-need-to-know',
            'title': 'Nile Cruise Guide 2026: Everything You Need to Know',
            'excerpt': 'Complete guide to Nile River cruises. Compare options, routes, prices and insider tips.',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'is_featured': True,
        },
        {
            'slug': 'egypt-visa-guide-2026-requirements-by-nationality',
            'title': 'Egypt Visa Guide 2026: Requirements, Costs & How to Apply',
            'excerpt': 'Complete Egypt visa guide. Learn about e-Visa, visa on arrival, and requirements by nationality.',
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
            'is_featured': False,
        },
    ]

    created = 0
    for article in articles:
        _, was_created = BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'excerpt': article['excerpt'],
                'content': f"## {article['title']}\n\n{article['excerpt']}\n\nFull content available in the blog.",
                'image_url': article['image_url'],
                'meta_description': article['excerpt'],
                'meta_keywords': 'egypt travel, egypt tours, egypt guide, 2026',
                'tags': 'egypt, travel, 2026, guide',
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': timezone.now(),
            }
        )
        if was_created:
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': len(articles)})

def debug_check(request):
    """Simple debug endpoint - updated v12"""
    return JsonResponse({'status': 'ok', 'version': 'v12-diagnose', 'branch': 'main', 'deploy_time': '2026-02-05-2200', 'features': ['blog-diagnose', 'hotels-search', 'privacy', 'terms']})

def blog_diagnose(request):
    """Diagnose blog app issues"""
    import traceback
    result = {'step': 'start', 'errors': []}

    # Step 1: Try importing blog models
    try:
        from blog.models import BlogPost, BlogCategory
        result['step'] = 'models_imported'
        result['models'] = True
    except Exception as e:
        result['errors'].append({'step': 'import_models', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    # Step 2: Try database query
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        result['step'] = 'db_connected'
        result['db'] = True
    except Exception as e:
        result['errors'].append({'step': 'db_connect', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    # Step 3: Count blog posts
    try:
        count = BlogPost.objects.count()
        result['step'] = 'query_success'
        result['post_count'] = count
    except Exception as e:
        result['errors'].append({'step': 'query_posts', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    # Step 4: Get published posts
    try:
        published = BlogPost.objects.filter(status='published').count()
        result['published_count'] = published
    except Exception as e:
        result['errors'].append({'step': 'filter_published', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    # Step 5: Try blog views import
    try:
        from blog import views as blog_views
        result['step'] = 'views_imported'
        result['views'] = True
    except Exception as e:
        result['errors'].append({'step': 'import_views', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    # Step 6: Try to instantiate BlogListView
    try:
        view = blog_views.BlogListView()
        result['step'] = 'view_instantiated'
        result['view_class'] = str(type(view))
    except Exception as e:
        result['errors'].append({'step': 'instantiate_view', 'error': str(e), 'trace': traceback.format_exc()})
        return JsonResponse(result, status=500)

    result['status'] = 'ok'
    result['step'] = 'complete'
    return JsonResponse(result)

def seed_luxury_articles(request):
    """Seed 5 luxury travel articles - access via /seed-luxury/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    category, _ = BlogCategory.objects.get_or_create(
        slug='luxury-travel',
        defaults={'name': 'Luxury Travel', 'description': 'Premium hotels, cruises, and VIP experiences in Egypt'}
    )

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    articles = [
        ('Best 5-Star Hotels in Egypt 2026: Ultimate Luxury Guide', 'best-5-star-hotels-egypt-2026',
         'Discover Egypt\'s most luxurious hotels from Four Seasons to Sofitel Legend Old Cataract.',
         'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200', True),
        ('Luxury Nile Cruises 2026: Complete Guide', 'luxury-nile-cruises-2026-complete-guide',
         'Experience the Nile on the most luxurious cruise ships. Oberoi, Sanctuary, AmaCerto reviewed.',
         'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200', True),
        ('Private Egypt Tours: VIP Experiences 2026', 'private-egypt-tours-vip-experiences-2026',
         'Private guides, helicopter tours, after-hours pyramid access - ultimate VIP Egypt.',
         'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200', False),
        ('Egypt Honeymoon Guide 2026: Romantic Luxury', 'egypt-honeymoon-guide-2026-romantic-luxury',
         'Plan the perfect Egypt honeymoon. Romantic hotels, private experiences, sunset moments.',
         'https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=1200', False),
        ('Grand Egyptian Museum VIP Guide 2026', 'grand-egyptian-museum-2026-vip-luxury-guide',
         'The world\'s largest archaeological museum. VIP tours, private viewings, luxury dining.',
         'https://images.unsplash.com/photo-1594322436404-5a0526db4d13?w=1200', False),
    ]

    created = 0
    for title, slug, excerpt, img, featured in articles:
        _, was_created = BlogPost.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title, 'author': author, 'category': category,
                'excerpt': excerpt,
                'content': f'## {title}\n\n{excerpt}\n\nPart of our Luxury Egypt Travel series.',
                'image_url': img, 'meta_description': excerpt[:157] + '...' if len(excerpt) > 160 else excerpt,
                'meta_keywords': 'luxury egypt, 5 star hotels, nile cruise, vip tours',
                'tags': 'luxury, egypt, hotels, cruises',
                'status': 'published', 'is_featured': featured,
                'published_at': timezone.now(),
            }
        )
        if was_created:
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': 5})

def seed_true_stories(request):
    """Seed 11 dramatic true stories - access via /seed-stories/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    category, _ = BlogCategory.objects.get_or_create(
        slug='true-stories',
        defaults={'name': 'True Stories', 'description': 'Captivating true stories from Egypt\'s dramatic history'}
    )

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    stories = [
        ('The Battle of Kadesh: When Egypt Faced Annihilation', 'battle-of-kadesh-egypt-hittites-ramses',
         'Ramses II walked into the greatest ambush in ancient history. What happened next became legend.', True),
        ('The Curse of the Pharaohs: Deaths That Defied Explanation', 'curse-of-the-pharaohs-tutankhamun-deaths',
         'Lord Carnarvon died 4 months after opening Tutankhamun\'s tomb. He wasn\'t the last.', True),
        ('Cleopatra\'s Last Night: The Death That Ended an Empire', 'cleopatra-death-last-pharaoh-true-story',
         'August 12, 30 BC. Alexandria. The last pharaoh made her final choice.', True),
        ('The Lost Army of Cambyses: 50,000 Soldiers Swallowed by the Desert', 'lost-army-cambyses-desert-mystery',
         'In 524 BC, an entire Persian army vanished in the Sahara. They\'ve never been found.', True),
        ('The Murder of Ramses III: A 3,000-Year-Old Cold Case', 'murder-ramses-iii-harem-conspiracy',
         'CT scans revealed what ancient texts concealed: Ramses III\'s throat was cut to the bone.', False),
        ('Moving Abu Simbel: The Engineering Marvel That Saved History', 'moving-abu-simbel-engineering-marvel',
         'They cut a temple into 1,036 pieces to save it from drowning. It worked.', False),
        ('The Exodus Mystery: Did Moses Really Part the Red Sea?', 'exodus-moses-red-sea-historical-evidence',
         'The most famous escape in history. But did it happen? Here\'s what evidence shows.', False),
        ('Hatshepsut: The Female King They Tried to Erase', 'hatshepsut-female-king-erased-history',
         'She wore the beard. She ruled as King. Then they tried to destroy every trace of her.', False),
        ('The Bent Pyramid: When Ancient Engineers Made a Mistake', 'bent-pyramid-dahshur-engineering-failure',
         'Halfway up, something went wrong. What they did next created Egypt\'s strangest monument.', False),
        ('Cracking the Code: The Rosetta Stone Story', 'rosetta-stone-deciphering-hieroglyphics',
         'For 1,400 years no one could read hieroglyphics. Then a broken stone changed everything.', False),
        ('The Sea Peoples: The Mystery Invaders Who Ended Civilizations', 'sea-peoples-bronze-age-collapse-mystery',
         'Around 1200 BC, mysterious warriors burned the ancient world. Only Egypt survived.', False),
    ]

    created = 0
    for title, slug, excerpt, featured in stories:
        _, was_created = BlogPost.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title, 'author': author, 'category': category,
                'excerpt': excerpt,
                'content': f'## {title}\n\n{excerpt}\n\nA captivating true story from Egypt\'s dramatic history.',
                'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
                'meta_description': excerpt[:157] + '...' if len(excerpt) > 160 else excerpt,
                'meta_keywords': 'egypt history, true story, ancient egypt, mystery',
                'tags': 'true stories, egypt, history, mystery',
                'status': 'published', 'is_featured': featured,
                'published_at': timezone.now(),
            }
        )
        if was_created:
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': 11})

def organize_all_articles(request):
    """Organize all articles into categories - access via /organize/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from blog.models import BlogPost, BlogCategory

    # Create categories
    CATEGORIES = [
        ('True Stories', 'true-stories', 'Captivating true stories from Egypt\'s dramatic history'),
        ('Ancient Egypt', 'ancient-egypt', 'Deep dives into ancient Egyptian civilization'),
        ('City Guides', 'city-guides', 'Complete travel guides to Egyptian cities'),
        ('Luxury Travel', 'luxury-travel', 'Premium hotels, cruises, and VIP experiences'),
        ('Travel Planning', 'travel-planning', 'Practical guides for planning your Egypt trip'),
        ('Culture & Food', 'culture-food', 'Egyptian culture, customs, cuisine'),
        ('Adventures', 'adventures', 'Desert safaris, diving, outdoor activities'),
    ]

    for name, slug, desc in CATEGORIES:
        BlogCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})

    # Article assignments
    ASSIGNMENTS = {
        'true-stories': ['battle-of-kadesh', 'curse-of-the-pharaohs', 'cleopatra-death', 'lost-army', 'murder-ramses', 'moving-abu-simbel', 'exodus', 'hatshepsut-female-king', 'bent-pyramid', 'rosetta-stone', 'sea-peoples'],
        'luxury-travel': ['5-star-hotels', 'luxury-nile', 'private-egypt-tours', 'honeymoon', 'grand-egyptian-museum-vip'],
        'ancient-egypt': ['great-pyramid', 'tutankhamun', 'ramses', 'cleopatra-last-pharaoh', 'queen-hatshepsut', 'mummies', 'valley-of-the-kings', 'karnak', 'abu-simbel', 'gods', 'hieroglyphics', 'daily-life'],
        'city-guides': ['cairo-travel', 'luxor-travel', 'aswan-travel', 'hurghada-travel', 'dahab-travel', 'marsa-alam', 'siwa', 'el-gouna', 'saint-catherine', 'marsa-matrouh', 'alexandria'],
        'travel-planning': ['best-egypt-tours', 'egypt-travel-cost', 'egypt-safe', 'best-time', 'egypt-visa', 'cairo-airport', 'packing-list', '7-day', 'solo-travel', 'kids-family'],
        'culture-food': ['egyptian-food', 'egyptian-culture', 'modern-cairo', 'nubian', 'ramadan', 'souvenirs'],
        'adventures': ['red-sea-diving', 'desert-safari', 'felucca', 'photography'],
    }

    assigned = 0
    for cat_slug, keywords in ASSIGNMENTS.items():
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
            for keyword in keywords:
                posts = BlogPost.objects.filter(slug__icontains=keyword)
                for post in posts:
                    if post.category != category:
                        post.category = category
                        post.save()
                        assigned += 1
        except BlogCategory.DoesNotExist:
            pass

    # Mark featured
    FEATURED = ['curse-of-the-pharaohs', 'cleopatra-death', 'battle-of-kadesh', 'lost-army', '5-star-hotels', 'luxury-nile']
    featured = 0
    BlogPost.objects.all().update(is_featured=False)
    for slug_part in FEATURED:
        posts = BlogPost.objects.filter(slug__icontains=slug_part)[:1]
        for post in posts:
            post.is_featured = True
            post.save()
            featured += 1

    total = BlogPost.objects.filter(status='published').count()
    categorized = BlogPost.objects.exclude(category__isnull=True).count()

    return JsonResponse({
        'success': True,
        'total_articles': total,
        'categorized': categorized,
        'assigned': assigned,
        'featured': featured,
        'categories': BlogCategory.objects.count()
    })

def seed_egypt_history_articles(request):
    """Seed 14 captivating Egypt history articles - access via /seed-egypt/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory
    from blog.egypt_articles_data import EGYPT_ARTICLES

    # Create or get the Ancient Egypt category
    category, _ = BlogCategory.objects.get_or_create(
        slug='ancient-egypt-history',
        defaults={'name': 'Ancient Egypt History', 'description': 'Fascinating articles about ancient Egyptian civilization, pharaohs, mysteries, and culture'}
    )

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users found'}, status=500)

    created = 0
    updated = 0
    for article in EGYPT_ARTICLES:
        # Truncate meta_description to 160 chars (database limit)
        meta_desc = article['meta_description'][:157] + '...' if len(article['meta_description']) > 160 else article['meta_description']

        _, was_created = BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'excerpt': article['excerpt'],
                'content': article['content'],
                'image_url': article['image_url'],
                'meta_description': meta_desc,
                'meta_keywords': article['meta_keywords'][:255],  # Also limit keywords
                'tags': article['tags'][:255],  # Also limit tags
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': timezone.now(),
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
        'total': len(EGYPT_ARTICLES),
        'category': 'Ancient Egypt History'
    })

@cache_control(max_age=3600)
def favicon(request):
    """Serve Ankh favicon directly - embedded SVG with white background"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFD700"/>
      <stop offset="50%" style="stop-color:#FFA500"/>
      <stop offset="100%" style="stop-color:#DAA520"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" fill="white"/>
  <ellipse cx="32" cy="16" rx="8" ry="10" fill="none" stroke="url(#goldGradient)" stroke-width="4"/>
  <line x1="20" y1="28" x2="44" y2="28" stroke="url(#goldGradient)" stroke-width="4" stroke-linecap="round"/>
  <line x1="32" y1="24" x2="32" y2="52" stroke="url(#goldGradient)" stroke-width="4" stroke-linecap="round"/>
  <circle cx="32" cy="56" r="2" fill="#FFD700" opacity="0.6"/>
</svg>'''
    return HttpResponse(svg_content, content_type='image/svg+xml')

def setup_all(request):
    """Setup user and seed ALL articles - access via /setup-all/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    # Create admin user if none exists
    if not User.objects.exists():
        admin = User.objects.create_user('admin', 'admin@egy360.com', 'egy360admin2026')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    author = User.objects.first()
    results = {'user': author.username, 'articles_created': 0}

    # Create categories
    categories = {}
    cat_data = [
        ('ancient-egypt', 'Ancient Egypt', 'Ancient Egypt wonders'),
        ('travel-guides', 'Travel Guides', 'Comprehensive travel guides'),
        ('egypt-history', 'Egypt History', 'Captivating Egypt history'),
        ('luxury-travel', 'Luxury Travel', 'Luxury travel experiences'),
        ('true-stories', 'True Stories', 'Dramatic true stories'),
    ]
    for slug, name, desc in cat_data:
        cat, _ = BlogCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
        categories[slug] = cat

    # All articles data
    all_articles = [
        # Pyramid articles
        ('The Great Pyramid of Giza: 4,500 Years of Mystery', 'great-pyramid-giza-introduction', 'Discover the Great Pyramid - the only surviving Ancient Wonder.', 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200', 'ancient-egypt', True),
        ('Building the Great Pyramid: Timeline and Workers', 'great-pyramid-history-timeline-workers', 'How long did it take? Who built it? The complete timeline.', 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200', 'ancient-egypt', False),
        ('Great Pyramid Architecture: Impossible Precision', 'great-pyramid-architecture-precision', '99.98% symmetrical, aligned to true north - how?', 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200', 'ancient-egypt', False),
        ("The King's Chamber: Heart of the Pyramid", 'great-pyramid-kings-chamber-secrets', 'Granite from 800km away, mysterious shafts, empty sarcophagus.', 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200', 'ancient-egypt', False),
        ('How Was the Great Pyramid Built?', 'great-pyramid-construction-methods', 'No wheels, no cranes, no iron - construction methods explained.', 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200', 'ancient-egypt', False),
        # Travel guides
        ('7-Day Egypt Itinerary: Cairo to Abu Simbel', '7-day-egypt-itinerary-cairo-abu-simbel', 'The perfect week in Egypt - pyramids, temples, and the Nile.', 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200', 'travel-guides', True),
        ('Best Time to Visit Egypt 2026', 'best-time-visit-egypt-2026', 'Month-by-month guide to Egypt weather and crowds.', 'https://images.unsplash.com/photo-1551634979-2b11f8c946fe?w=1200', 'travel-guides', False),
        ('Grand Egyptian Museum 2026 Complete Guide', 'grand-egyptian-museum-2026-guide', 'Everything about GEM - the largest archaeological museum.', 'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=1200', 'travel-guides', True),
        # Egypt history
        ('Cleopatra: The Last Pharaoh of Egypt', 'cleopatra-last-pharaoh-egypt', 'The fascinating story of Egypt most famous queen.', 'https://images.unsplash.com/photo-1608152142361-1d131f5e520e?w=1200', 'egypt-history', True),
        ('Tutankhamun: The Boy King', 'tutankhamun-boy-king-egypt', 'The discovery that changed archaeology forever.', 'https://images.unsplash.com/photo-1595981234058-a9302fb97229?w=1200', 'egypt-history', True),
        ('The Rosetta Stone: Key to Ancient Egypt', 'rosetta-stone-ancient-egypt', 'How a stone unlocked 3000 years of history.', 'https://images.unsplash.com/photo-1567354723472-d3e9f3f8c6b0?w=1200', 'egypt-history', False),
        ('Nefertiti: The Beautiful Queen', 'nefertiti-beautiful-queen-egypt', 'The mysterious queen whose bust captivated the world.', 'https://images.unsplash.com/photo-1599423423927-8f77f7c5b0c8?w=1200', 'egypt-history', False),
        ('Ramesses II: Egypt Greatest Pharaoh', 'ramesses-ii-greatest-pharaoh', 'The warrior king who built more monuments than any other.', 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200', 'egypt-history', True),
        # Luxury travel
        ('Luxury Nile Cruises 2026', 'luxury-nile-cruises-2026', 'The most exclusive Nile cruise experiences.', 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200', 'luxury-travel', True),
        ('Five-Star Hotels in Cairo', 'five-star-hotels-cairo-egypt', 'The best luxury accommodations in Egypt capital.', 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200', 'luxury-travel', False),
        ('Private Tours of the Pyramids', 'private-tours-pyramids-giza', 'Exclusive access to Egypt ancient wonders.', 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200', 'luxury-travel', False),
        # True stories
        ('Lost in the Desert: A Survival Story', 'lost-desert-egypt-survival', 'How a tourist survived 3 days in the Sahara.', 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200', 'true-stories', True),
        ('The Hidden Tomb Discovery', 'hidden-tomb-discovery-luxor', 'Amateur archaeologist finds untouched tomb.', 'https://images.unsplash.com/photo-1562679299-266d0a81c40f?w=1200', 'true-stories', True),
    ]

    for title, slug, excerpt, image, cat_slug, featured in all_articles:
        if not BlogPost.objects.filter(slug=slug).exists():
            content = f"<h2>{title}</h2><p>{excerpt}</p><p>This is a comprehensive article about {title.lower()}. Egypt offers incredible experiences for travelers seeking history, adventure, and culture.</p>"
            BlogPost.objects.create(
                title=title,
                slug=slug,
                excerpt=excerpt[:200],
                content=content,
                image_url=image,
                author=author,
                category=categories.get(cat_slug),
                is_featured=featured,
                status='published',
                published_at=timezone.now()
            )
            results['articles_created'] += 1

    results['total_articles'] = BlogPost.objects.count()
    return JsonResponse(results)

def seed_more_articles(request):
    """Seed 40+ more articles - access via /seed-more/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    created = 0

    # Get/create categories
    categories = {}
    for slug, name in [('ancient-egypt', 'Ancient Egypt'), ('travel-guides', 'Travel Guides'),
                       ('practical-tips', 'Practical Tips'), ('destinations', 'Destinations'),
                       ('culture', 'Egyptian Culture'), ('food-drink', 'Food & Drink')]:
        cat, _ = BlogCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'description': f'{name} articles'})
        categories[slug] = cat

    more_articles = [
        # Ancient Egypt batch
        ("King Tutankhamun: The Boy King Who Changed History", "king-tutankhamun-boy-king-guide", "Discover the fascinating story of King Tutankhamun, Egypt's famous boy pharaoh.", "https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200", "ancient-egypt"),
        ("Queen Nefertiti: The Beautiful One Has Come", "queen-nefertiti-complete-guide", "The mysterious queen whose iconic bust captivated the world.", "https://images.unsplash.com/photo-1599423423927-8f77f7c5b0c8?w=1200", "ancient-egypt"),
        ("Ramesses II: The Great Builder Pharaoh", "ramesses-ii-great-builder", "Egypt's longest-reigning pharaoh built more monuments than any other.", "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200", "ancient-egypt"),
        ("Karnak Temple: The Largest Religious Complex", "karnak-temple-complete-guide", "Explore Karnak Temple, the largest ancient religious site in the world.", "https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200", "ancient-egypt"),
        ("Valley of the Kings: Royal Tombs Guide", "valley-of-kings-complete-guide", "Everything you need to know about the royal burial ground of ancient Egypt.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "ancient-egypt"),
        # Travel guides
        ("Egypt Visa Guide 2026: Requirements & Application", "egypt-visa-guide-2026", "Complete guide to Egypt tourist visas - requirements, fees, and how to apply.", "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200", "practical-tips"),
        ("Egypt Currency & Money Guide 2026", "egypt-currency-money-guide", "Egyptian Pound exchange rates, ATMs, credit cards, and tipping culture.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "practical-tips"),
        ("What to Pack for Egypt: Complete List", "what-to-pack-egypt-checklist", "Essential packing list for Egypt - clothes, gadgets, and must-have items.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "practical-tips"),
        ("Egypt Safety Tips for Tourists 2026", "egypt-safety-tips-tourists", "Is Egypt safe? Your complete guide to staying safe while traveling in Egypt.", "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200", "practical-tips"),
        ("Cairo Metro Guide: Navigate Like a Local", "cairo-metro-guide-map", "How to use Cairo's metro system - lines, stations, tickets, and tips.", "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200", "practical-tips"),
        # Destinations
        ("Alexandria Egypt: Mediterranean Pearl Guide", "alexandria-egypt-travel-guide", "Explore Alexandria - Egypt's second city with Greek, Roman, and Egyptian heritage.", "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200", "destinations"),
        ("Aswan: Gateway to Nubia Complete Guide", "aswan-nubia-travel-guide", "Discover Aswan - feluccas, temples, and the gateway to Abu Simbel.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "destinations"),
        ("Dahab: Red Sea Diving Paradise Guide", "dahab-diving-guide", "Dahab guide: World-class diving, beaches, and laid-back Sinai vibes.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200", "destinations"),
        ("Siwa Oasis: Desert Paradise Guide", "siwa-oasis-complete-guide", "Explore Siwa Oasis - Egypt's most remote and magical desert destination.", "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200", "destinations"),
        ("Sharm El Sheikh: Red Sea Resort Guide", "sharm-el-sheikh-guide", "Complete guide to Sharm El Sheikh - beaches, diving, and nightlife.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200", "destinations"),
        # Culture
        ("Egyptian Food: 15 Dishes You Must Try", "egyptian-food-guide-dishes", "From koshari to ful medames - discover Egypt's delicious cuisine.", "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1200", "food-drink"),
        ("Ramadan in Egypt: Traveler's Guide", "ramadan-egypt-travel-guide", "What to expect traveling Egypt during Ramadan - tips and etiquette.", "https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200", "culture"),
        ("Egyptian Wedding Traditions Explained", "egyptian-wedding-traditions", "Discover the colorful customs of Egyptian weddings.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "culture"),
        ("Learn Egyptian Arabic: Essential Phrases", "egyptian-arabic-phrases-travelers", "50 essential Arabic phrases for your Egypt trip.", "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200", "culture"),
        ("Egyptian Handicrafts: Shopping Guide", "egyptian-handicrafts-shopping", "Where to buy authentic Egyptian crafts - papyrus, alabaster, and more.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "culture"),
        # More ancient
        ("Hatshepsut: Egypt's Female Pharaoh", "hatshepsut-female-pharaoh-guide", "The remarkable story of Egypt's most successful female ruler.", "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200", "ancient-egypt"),
        ("The Sphinx: Guardian of the Pyramids", "sphinx-giza-complete-guide", "Mysteries of the Great Sphinx - history, theories, and visiting tips.", "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200", "ancient-egypt"),
        ("Egyptian Mummies: Science & Mythology", "egyptian-mummies-guide", "How and why ancient Egyptians mummified their dead.", "https://images.unsplash.com/photo-1595981234058-a9302fb97229?w=1200", "ancient-egypt"),
        ("Hieroglyphics: Reading Ancient Egyptian", "hieroglyphics-guide-basics", "Introduction to ancient Egyptian writing - symbols and meanings.", "https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200", "ancient-egypt"),
        ("Egyptian Gods & Goddesses Guide", "egyptian-gods-goddesses-guide", "Meet the major deities of ancient Egypt - Ra, Isis, Osiris, and more.", "https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200", "ancient-egypt"),
        # More travel
        ("Nile River Cruise: Complete Guide 2026", "nile-cruise-guide-2026", "Everything about Nile cruises - best ships, routes, and what to expect.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "travel-guides"),
        ("Egypt With Kids: Family Travel Guide", "egypt-kids-family-guide", "Tips for traveling Egypt with children - kid-friendly attractions and safety.", "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200", "travel-guides"),
        ("Solo Female Travel in Egypt Guide", "solo-female-travel-egypt", "Complete guide for women traveling solo in Egypt - safety and tips.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "travel-guides"),
        ("Budget Egypt: Travel Under $50/Day", "budget-egypt-travel-guide", "How to experience Egypt on a tight budget without missing the highlights.", "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200", "travel-guides"),
        ("Egypt Photography Guide: Best Shots", "egypt-photography-guide-tips", "Photography tips for capturing Egypt's ancient wonders perfectly.", "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200", "travel-guides"),
        # Additional
        ("Abu Simbel: Sun Festival Guide", "abu-simbel-sun-festival-guide", "Witness the sun illuminate Ramesses II twice a year at Abu Simbel.", "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200", "ancient-egypt"),
        ("Luxor Temple: Night Visit Guide", "luxor-temple-night-visit", "Experience Luxor Temple illuminated at night - tips and what to see.", "https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200", "ancient-egypt"),
        ("Egyptian Museum Cairo: Complete Guide", "egyptian-museum-cairo-guide", "Navigate the treasures of the Egyptian Museum before GEM opens.", "https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=1200", "ancient-egypt"),
        ("Hot Air Balloon Luxor Guide", "hot-air-balloon-luxor-guide", "Float over ancient Thebes at sunrise - booking and what to expect.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "travel-guides"),
        ("Felucca Sailing on the Nile Guide", "felucca-sailing-nile-guide", "Traditional sailing on the Nile - routes, prices, and tips.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "travel-guides"),
        ("Egyptian Coffee Culture Guide", "egyptian-coffee-culture", "Discover Egypt's coffee traditions from ahwa to Turkish coffee.", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200", "food-drink"),
        ("Khan El Khalili Bazaar Guide", "khan-el-khalili-shopping-guide", "Navigate Cairo's famous medieval market - shopping tips and bargaining.", "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200", "destinations"),
        ("Coptic Cairo: Christian Heritage Tour", "coptic-cairo-christian-heritage", "Explore Cairo's ancient Christian quarter - churches, history, and tips.", "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200", "destinations"),
        ("Islamic Cairo Walking Tour Guide", "islamic-cairo-walking-tour", "Mosques, madrasas, and medieval architecture in Historic Cairo.", "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200", "destinations"),
        ("White Desert Egypt Camping Guide", "white-desert-camping-guide", "Camp among surreal chalk formations in Egypt's White Desert.", "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200", "destinations"),
    ]

    for title, slug, excerpt, image, cat_slug in more_articles:
        if not BlogPost.objects.filter(slug=slug).exists():
            content = f"<h2>{title}</h2><p>{excerpt}</p><p>Egypt offers incredible experiences for travelers. This comprehensive guide covers everything you need to know about {title.lower()}.</p><p>From ancient wonders to modern adventures, Egypt has something for every traveler. Plan your perfect trip with our expert insights.</p>"
            BlogPost.objects.create(
                title=title,
                slug=slug,
                excerpt=excerpt[:200],
                content=content,
                image_url=image,
                author=author,
                category=categories.get(cat_slug),
                is_featured=(created % 5 == 0),
                status='published',
                published_at=timezone.now()
            )
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': BlogPost.objects.count()})

def update_articles_content(request):
    """Update all articles with rich, engaging content - access via /update-content/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from blog.models import BlogPost
    updated = 0

    # Rich content templates for different article types
    article_contents = {
        # Ancient Egypt Articles
        'great-pyramid-giza-introduction': '''
<div class="article-hero" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">🏛️ The Great Pyramid: 4,500 Years of Wonder</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">The only surviving wonder of the ancient world stands as humanity's greatest architectural achievement</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">Standing on the Giza Plateau for over <strong>4,500 years</strong>, the Great Pyramid of Khufu isn't just Egypt's most iconic monument—it's a testament to human ambition that continues to baffle scientists, engineers, and visitors alike. Originally standing at <strong>146.6 meters</strong> (481 feet), it remained the tallest man-made structure on Earth for nearly 4,000 years.</p>

<h2>🔢 Mind-Blowing Statistics</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em; color: #e74c3c; font-weight: bold;">2.3M</div>
        <div style="color: #666;">Stone Blocks</div>
    </div>
    <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em; color: #3498db; font-weight: bold;">6.5M</div>
        <div style="color: #666;">Tons Total Weight</div>
    </div>
    <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em; color: #2ecc71; font-weight: bold;">20</div>
        <div style="color: #666;">Years to Build</div>
    </div>
    <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em; color: #9b59b6; font-weight: bold;">99.98%</div>
        <div style="color: #666;">Precision Accuracy</div>
    </div>
</div>

<h2>🏗️ Construction Mysteries That Still Puzzle Scientists</h2>
<p>How did ancient Egyptians, without wheels, iron tools, or modern machinery, create something so precisely aligned that modern engineers struggle to replicate it? The pyramid is aligned to true north with an accuracy of <strong>0.05 degrees</strong>—more precise than the Royal Greenwich Observatory!</p>

<h3>The Numbers Don't Add Up</h3>
<ul style="line-height: 2;">
    <li>🪨 Each block weighs an average of <strong>2.5 tons</strong>—some granite blocks weigh up to 80 tons</li>
    <li>⏱️ If built in 20 years, workers placed one block every <strong>2.5 minutes</strong>, 24/7</li>
    <li>📐 The base is level to within just <strong>2.1 centimeters</strong> across 230 meters</li>
    <li>🧭 Aligned to the cardinal directions with incredible precision</li>
</ul>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🎟️ Visit the Great Pyramid</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">Experience this wonder in person with our expert-guided tours</p>
    <a href="/tours/" style="background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Book Your Pyramid Tour</a>
</div>

<h2>👁️ Inside the Great Pyramid</h2>
<p>The interior contains three main chambers connected by narrow passages:</p>

<h3>The King's Chamber</h3>
<p>Located in the heart of the pyramid, this room contains an empty granite sarcophagus. The chamber is built entirely of <strong>Aswan granite</strong>, transported over 800 kilometers. Above it are five relieving chambers designed to distribute the immense weight.</p>

<h3>The Queen's Chamber</h3>
<p>Despite its name, this was likely never intended for a queen. Two mysterious shafts extend from this chamber—their purpose remains unknown.</p>

<h3>The Grand Gallery</h3>
<p>A magnificent corbelled hallway, 47 meters long and 8 meters high, leading to the King's Chamber. Its acoustics are so perfect that some researchers believe it had astronomical significance.</p>

<h2>🌟 2026 Visitor Tips</h2>
<ul style="line-height: 2;">
    <li>✅ <strong>Best time to visit:</strong> Early morning (8 AM) or late afternoon to avoid crowds and heat</li>
    <li>✅ <strong>Entry tickets:</strong> Pyramid complex entry ~$15, interior access ~$20 extra</li>
    <li>✅ <strong>What to wear:</strong> Comfortable shoes, modest clothing, sun protection</li>
    <li>✅ <strong>Pro tip:</strong> Book a sunrise tour for magical photos with fewer tourists</li>
</ul>

<blockquote style="background: #f8f9fa; border-left: 5px solid #e74c3c; padding: 25px; margin: 30px 0; font-style: italic; font-size: 1.2em;">
"Man fears Time, but Time fears the Pyramids." — Ancient Arab Proverb
</blockquote>
''',

        'king-tutankhamun-boy-king-guide': '''
<div class="article-hero" style="background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">👑 King Tutankhamun: The Boy Who Became Immortal</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">He died at 19, was forgotten for 3,000 years, then became the most famous pharaoh in history</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">On November 26, 1922, archaeologist Howard Carter peered through a small hole into a sealed chamber. When asked if he could see anything, he whispered the now-legendary words: <strong>"Yes, wonderful things."</strong> What he discovered would change our understanding of ancient Egypt forever.</p>

<h2>📜 The Short Life of a Boy King</h2>

<div style="background: #fff3e0; padding: 25px; border-radius: 15px; margin: 25px 0;">
    <h3 style="color: #e65100; margin-top: 0;">Timeline of Tutankhamun</h3>
    <ul style="line-height: 2.2;">
        <li><strong>c. 1341 BC:</strong> Born as Tutankhaten ("Living Image of Aten")</li>
        <li><strong>c. 1332 BC:</strong> Becomes pharaoh at age 9</li>
        <li><strong>c. 1330 BC:</strong> Changes name to Tutankhamun, restores old gods</li>
        <li><strong>c. 1323 BC:</strong> Dies mysteriously at age 19</li>
        <li><strong>1922 AD:</strong> Tomb discovered by Howard Carter</li>
    </ul>
</div>

<h2>🔍 The Discovery That Shook the World</h2>
<p>Lord Carnarvon had funded Carter's excavations for years with no major finds. He gave Carter one final season. With just days of funding left, a water boy stumbled upon a stone step hidden beneath ancient workmen's huts.</p>

<p>What they found inside was <strong>the most complete royal tomb ever discovered</strong>:</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 15px;">
        <h4 style="color: #c0392b;">🏺 5,398 Objects</h4>
        <p>Catalogued over 10 years</p>
    </div>
    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 25px; border-radius: 15px;">
        <h4 style="color: #8e44ad;">⚱️ 11 kg Gold Mask</h4>
        <p>Solid gold death mask</p>
    </div>
    <div style="background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); padding: 25px; border-radius: 15px;">
        <h4 style="color: #2980b9;">⚰️ 110 kg Gold Coffin</h4>
        <p>Innermost of three nested coffins</p>
    </div>
</div>

<h2>💀 The Mummy's Curse: Fact or Fiction?</h2>
<p>When Lord Carnarvon died just months after the tomb's opening, newspapers went wild with stories of an ancient curse. The truth?</p>

<ul style="line-height: 2;">
    <li>❌ Carter himself lived until 1939—17 years after the discovery</li>
    <li>❌ Most team members lived normal lifespans</li>
    <li>✅ Carnarvon died from an infected mosquito bite, worsened by a shaving cut</li>
    <li>📰 The "curse" was largely a media sensation—great for newspaper sales!</li>
</ul>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🏛️ See Tutankhamun's Treasures</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">The complete collection moves to the Grand Egyptian Museum in 2026</p>
    <a href="/tours/" style="background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Book GEM Tour</a>
</div>

<h2>🧬 Modern Science Reveals the Truth</h2>
<p>DNA analysis and CT scans have revealed fascinating details about Tut's life and death:</p>

<ul style="line-height: 2;">
    <li>🦴 He had a <strong>club foot</strong> and bone disease—over 130 walking canes were found in his tomb</li>
    <li>🦟 He suffered from <strong>malaria</strong>—multiple strains found in his DNA</li>
    <li>👨‍👩‍👦 His parents were <strong>siblings</strong>—inbreeding weakened his immune system</li>
    <li>🦵 A <strong>broken leg</strong> shortly before death may have led to fatal infection</li>
</ul>

<h2>🌟 Why Tutankhamun Matters</h2>
<p>Despite being a minor pharaoh who died young, Tut gave us an unparalleled window into ancient Egyptian life. His tomb contained everything a pharaoh needed for the afterlife—furniture, food, games, weapons, and even underwear!</p>

<blockquote style="background: #f8f9fa; border-left: 5px solid #f39c12; padding: 25px; margin: 30px 0; font-style: italic; font-size: 1.2em;">
"The treasures of Tutankhamun tell us more about daily life in ancient Egypt than any other discovery in history."
</blockquote>
''',

        'grand-egyptian-museum-2026-guide': '''
<div class="article-hero" style="background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">🏛️ Grand Egyptian Museum 2026: The Ultimate Guide</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">The world's largest archaeological museum opens its doors—here's everything you need to know</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">After nearly two decades of construction and a <strong>$1 billion investment</strong>, the Grand Egyptian Museum (GEM) is finally welcoming visitors. Located just 2 kilometers from the Pyramids of Giza, this architectural marvel houses over <strong>100,000 artifacts</strong>—including the complete Tutankhamun collection displayed together for the first time.</p>

<h2>🎯 GEM at a Glance</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em;">📏</div>
        <div style="font-size: 1.5em; font-weight: bold; color: #2e7d32;">490,000 m²</div>
        <div style="color: #666;">Total Area</div>
    </div>
    <div style="background: #e3f2fd; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em;">🏺</div>
        <div style="font-size: 1.5em; font-weight: bold; color: #1565c0;">100,000+</div>
        <div style="color: #666;">Artifacts</div>
    </div>
    <div style="background: #fff3e0; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em;">👑</div>
        <div style="font-size: 1.5em; font-weight: bold; color: #ef6c00;">5,000+</div>
        <div style="color: #666;">Tut Objects</div>
    </div>
    <div style="background: #fce4ec; padding: 25px; border-radius: 15px; text-align: center;">
        <div style="font-size: 2.5em;">👥</div>
        <div style="font-size: 1.5em; font-weight: bold; color: #c2185b;">5 Million</div>
        <div style="color: #666;">Annual Visitors Expected</div>
    </div>
</div>

<h2>✨ What Makes GEM Special</h2>

<h3>1. The Grand Staircase & Ramesses II</h3>
<p>As you enter, you're greeted by the colossal <strong>12-meter statue of Ramesses II</strong>, weighing 83 tons. Behind it, the Grand Staircase displays massive artifacts chronologically as you ascend.</p>

<h3>2. Complete Tutankhamun Collection</h3>
<p>For the first time ever, all <strong>5,398 objects</strong> from Tutankhamun's tomb will be displayed together. The Egyptian Museum could only show about 1,500—now you'll see chariots, beds, thrones, and items never before exhibited.</p>

<h3>3. Pyramid Views</h3>
<p>The museum's glass walls offer stunning views of the Giza Pyramids. The rooftop restaurant and café let you dine while gazing at the ancient wonders.</p>

<h3>4. Conservation Center</h3>
<p>Watch conservators restore ancient artifacts through glass windows in the state-of-the-art conservation labs.</p>

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🎟️ Book Your GEM Experience</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">Skip-the-line tickets with expert Egyptologist guides</p>
    <a href="/tours/" style="background: white; color: #11998e; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Reserve Tickets Now</a>
</div>

<h2>🗺️ Visitor Information 2026</h2>

<h3>📍 Location</h3>
<p>Pyramids Road, Giza—just 2 km from the Great Pyramid. New metro line connects directly to the museum.</p>

<h3>⏰ Hours</h3>
<ul>
    <li><strong>Sunday-Thursday:</strong> 9 AM - 5 PM</li>
    <li><strong>Friday-Saturday:</strong> 9 AM - 9 PM (extended hours)</li>
</ul>

<h3>💰 Tickets (Estimated 2026)</h3>
<ul>
    <li><strong>General Entry:</strong> ~$25-30</li>
    <li><strong>Tutankhamun Galleries:</strong> ~$15 additional</li>
    <li><strong>Combined Pyramid + GEM:</strong> ~$50</li>
</ul>

<h3>⏱️ How Long to Visit</h3>
<p>Plan for <strong>3-5 hours minimum</strong>. Serious history enthusiasts could easily spend a full day.</p>

<h2>💡 Pro Tips for 2026</h2>
<ul style="line-height: 2;">
    <li>🌅 <strong>Go early:</strong> Arrive at opening for smaller crowds</li>
    <li>📱 <strong>Download the app:</strong> GEM has an interactive guide app</li>
    <li>👟 <strong>Wear comfortable shoes:</strong> The museum is massive</li>
    <li>📸 <strong>Photography:</strong> Allowed in most areas (no flash)</li>
    <li>🍽️ <strong>Plan for lunch:</strong> Multiple restaurants with pyramid views</li>
</ul>
''',

        'cleopatra-last-pharaoh-egypt': '''
<div class="article-hero" style="background: linear-gradient(135deg, #8e44ad 0%, #3498db 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">👸 Cleopatra VII: The Queen Who Shook Rome</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">Seductress? Victim? Genius politician? The truth about history's most famous queen</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">Forget what Hollywood told you. Cleopatra VII wasn't just beautiful—she was a <strong>brilliant strategist, polyglot scholar, and political genius</strong> who held the Roman Empire at bay for two decades. She spoke nine languages, wrote scientific treatises, and nearly created an empire spanning the Mediterranean.</p>

<h2>🔥 Busting the Myths</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: #ffebee; padding: 25px; border-radius: 15px;">
        <h4 style="color: #c62828;">❌ MYTH</h4>
        <p>Cleopatra was Egyptian</p>
        <h4 style="color: #2e7d32; margin-top: 15px;">✅ FACT</h4>
        <p>She was Macedonian Greek, descended from Ptolemy I, one of Alexander the Great's generals. However, she was the first Ptolemaic ruler to learn Egyptian!</p>
    </div>
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px;">
        <h4 style="color: #c62828;">❌ MYTH</h4>
        <p>Her beauty was legendary</p>
        <h4 style="color: #2e7d32; margin-top: 15px;">✅ FACT</h4>
        <p>Ancient sources describe her charm, wit, and voice as captivating—but never mention extraordinary beauty. Her power was in her intellect.</p>
    </div>
</div>

<h2>📚 The Educated Queen</h2>
<p>Cleopatra was one of the most educated women of the ancient world:</p>
<ul style="line-height: 2;">
    <li>📖 Spoke <strong>9 languages</strong> including Egyptian, Greek, Latin, Hebrew, and Arabic</li>
    <li>🔬 Wrote treatises on <strong>medicine, cosmetics, and science</strong></li>
    <li>🏛️ Trained at the <strong>Library of Alexandria</strong>—the greatest library of antiquity</li>
    <li>💰 Personally managed Egypt's economy, making it Rome's wealthiest client state</li>
</ul>

<h2>❤️ Cleopatra & Her Romans</h2>

<h3>Julius Caesar (48-44 BC)</h3>
<p>When Caesar arrived in Alexandria to settle a civil war between Cleopatra and her brother, she famously had herself smuggled into his presence <strong>rolled in a carpet</strong>. She was 21; he was 52. Their son, Caesarion, would be proclaimed the last pharaoh of Egypt.</p>

<h3>Mark Antony (41-30 BC)</h3>
<p>After Caesar's assassination, Cleopatra allied with Mark Antony. Their legendary romance produced three children and nearly reshaped the ancient world. At the Battle of Actium in 31 BC, their combined fleet lost to Octavian (future Augustus Caesar).</p>

<h2>💀 The Death of a Dynasty</h2>
<p>Rather than be paraded through Rome as a trophy, Cleopatra chose death on her own terms. The famous asp bite may be legend—modern scholars suggest she likely used a quick-acting poison she had researched herself.</p>

<blockquote style="background: #f8f9fa; border-left: 5px solid #8e44ad; padding: 25px; margin: 30px 0; font-style: italic; font-size: 1.2em;">
"Age cannot wither her, nor custom stale her infinite variety." — Shakespeare, Antony and Cleopatra
</blockquote>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🏛️ Walk in Cleopatra's Footsteps</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">Explore Alexandria, her legendary capital, with expert guides</p>
    <a href="/tours/" style="background: white; color: #667eea; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Alexandria Tours</a>
</div>
''',

        'valley-of-kings-complete-guide': '''
<div class="article-hero" style="background: linear-gradient(135deg, #b8860b 0%, #8b4513 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">⚰️ Valley of the Kings: Complete Visitor Guide 2026</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">Navigate the ancient royal necropolis like an Egyptologist</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">Hidden in the barren hills of Luxor's West Bank, the <strong>Valley of the Kings</strong> contains 65 discovered tombs of Egypt's New Kingdom pharaohs. For 500 years (1539-1075 BC), this desolate valley was ancient Egypt's most sacred site—and possibly its best-kept secret.</p>

<h2>🎫 2026 Visitor Essentials</h2>

<div style="background: #fff8e1; padding: 30px; border-radius: 15px; margin: 25px 0;">
    <h3 style="color: #f57f17; margin-top: 0;">Quick Facts</h3>
    <ul style="line-height: 2.2;">
        <li>💰 <strong>Standard ticket:</strong> ~$20 (includes 3 tombs)</li>
        <li>👑 <strong>Tutankhamun's tomb:</strong> ~$25 extra</li>
        <li>🏛️ <strong>Seti I or Ramesses VI:</strong> ~$20-30 extra each</li>
        <li>⏰ <strong>Hours:</strong> 6 AM - 5 PM (winter), 6 AM - 6 PM (summer)</li>
        <li>📸 <strong>Photography:</strong> Not allowed inside tombs</li>
    </ul>
</div>

<h2>🏆 Top 5 Tombs to Visit</h2>

<h3>1. KV62 - Tutankhamun (Extra Ticket)</h3>
<p>The famous tomb is small but historically significant. The mummy remains inside. Worth the extra fee for the experience, though decorations are minimal compared to others.</p>

<h3>2. KV17 - Seti I (Extra Ticket)</h3>
<p>The <strong>longest and most decorated tomb</strong> in the valley. Stunning astronomical ceiling in the burial chamber. Many consider this the most beautiful tomb in Egypt.</p>

<h3>3. KV9 - Ramesses VI</h3>
<p>Incredible astronomical ceiling with the Book of Night and Book of Day. The colors remain remarkably vibrant after 3,000 years.</p>

<h3>4. KV2 - Ramesses IV</h3>
<p>One of the most accessible tombs with well-preserved hieroglyphics. Great for first-time visitors—spacious corridors and vivid wall paintings.</p>

<h3>5. KV34 - Thutmose III</h3>
<p>Climb steep stairs to reach this unique oval-shaped burial chamber with amazing painted decorations in a distinctive style.</p>

<div style="background: linear-gradient(135deg, #b8860b 0%, #daa520 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🎟️ Skip-the-Line Valley of Kings Tours</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">Expert guides + priority access to the best tombs</p>
    <a href="/tours/" style="background: white; color: #b8860b; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Book Luxor Tour</a>
</div>

<h2>💡 Expert Tips</h2>
<ul style="line-height: 2;">
    <li>🌅 <strong>Go at opening (6 AM):</strong> Fewer crowds, cooler temperatures</li>
    <li>🚗 <strong>Take the electric tram:</strong> Saves energy for tomb exploration</li>
    <li>💧 <strong>Bring water:</strong> It gets extremely hot (40°C+ in summer)</li>
    <li>👟 <strong>Wear sturdy shoes:</strong> Some tombs have steep stairs</li>
    <li>🔦 <strong>Bring a small flashlight:</strong> Helpful for seeing details</li>
    <li>📖 <strong>Get a guide:</strong> The stories bring the tombs to life</li>
</ul>

<h2>🔍 Why Were Pharaohs Buried Here?</h2>
<p>After tomb robbing became rampant, pharaohs abandoned the obvious pyramids for this hidden valley. The peak above resembles a natural pyramid (the Theban Peak), and the dry climate helped preserve mummies and artifacts.</p>

<blockquote style="background: #f8f9fa; border-left: 5px solid #b8860b; padding: 25px; margin: 30px 0; font-style: italic; font-size: 1.2em;">
"I found riches in the tombs, but the real treasure was understanding how much the ancient Egyptians loved life—that's why they prepared so carefully for eternity."
</blockquote>
''',

        '7-day-egypt-itinerary-cairo-abu-simbel': '''
<div class="article-hero" style="background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">✈️ Perfect 7-Day Egypt Itinerary 2026</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">Cairo • Luxor • Aswan • Abu Simbel — The ultimate Egypt experience</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">One week is perfect for experiencing Egypt's greatest highlights. This carefully crafted itinerary takes you from the <strong>Pyramids of Giza</strong> to the <strong>temples of Abu Simbel</strong>, balancing iconic monuments with authentic experiences. No rushing—just perfectly paced exploration.</p>

<h2>📅 Day-by-Day Breakdown</h2>

<div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #2c3e50;">Day 1: Arrive Cairo</h3>
    <p>🛬 Arrive Cairo International Airport<br>
    🏨 Check into hotel in Giza (pyramid views!)<br>
    🌅 Evening: Light show at the Pyramids<br>
    🍽️ Dinner at Pyramids-view restaurant</p>
</div>

<div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #2c3e50;">Day 2: Pyramids & Sphinx</h3>
    <p>🌅 Sunrise at the Pyramids (beat the crowds!)<br>
    🐪 Camel ride through the desert<br>
    🦁 Great Sphinx and Valley Temple<br>
    🏛️ Afternoon: Grand Egyptian Museum (GEM)<br>
    🌃 Evening: Khan El Khalili Bazaar</p>
</div>

<div style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #2c3e50;">Day 3: Cairo Exploration</h3>
    <p>🕌 Islamic Cairo: Al-Azhar Mosque, Citadel<br>
    ⛪ Coptic Cairo: Hanging Church, Ben Ezra Synagogue<br>
    🍲 Lunch: Authentic koshari experience<br>
    ✈️ Evening flight to Luxor</p>
</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; border-radius: 20px; margin: 25px 0; color: white;">
    <h3>Day 4: Luxor East Bank</h3>
    <p>🎈 Optional: Hot air balloon at sunrise<br>
    🏛️ Karnak Temple (morning, cooler)<br>
    🏺 Luxor Museum (air-conditioned break)<br>
    🌙 Luxor Temple at sunset (magical lighting)</p>
</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 30px; border-radius: 20px; margin: 25px 0; color: white;">
    <h3>Day 5: Luxor West Bank</h3>
    <p>⚰️ Valley of the Kings (3 tombs + Tutankhamun)<br>
    👸 Temple of Hatshepsut (Deir el-Bahari)<br>
    🎭 Colossi of Memnon<br>
    🚂 Evening: Sleeper train to Aswan (or fly)</p>
</div>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; margin: 25px 0; color: white;">
    <h3>Day 6: Aswan & Abu Simbel</h3>
    <p>🌅 Early morning: Abu Simbel tour (3-hour drive)<br>
    🏛️ Two magnificent temples of Ramesses II<br>
    ⛵ Afternoon: Felucca sailing on the Nile<br>
    🏝️ Sunset: Elephantine Island<br>
    🍽️ Nubian dinner experience</p>
</div>

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; border-radius: 20px; margin: 25px 0; color: white;">
    <h3>Day 7: Aswan & Departure</h3>
    <p>🏛️ Morning: Philae Temple (island temple)<br>
    🌊 High Dam viewpoint<br>
    🛒 Aswan Souk shopping<br>
    ✈️ Flight back to Cairo → International departure</p>
</div>

<div style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">📦 Get This Exact Itinerary</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">All-inclusive packages with guides, hotels & internal flights</p>
    <a href="/tours/" style="background: white; color: #ee0979; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">View 7-Day Packages</a>
</div>

<h2>💰 Budget Breakdown (Per Person)</h2>
<div style="background: #f8f9fa; padding: 25px; border-radius: 15px;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 12px;"><strong>Category</strong></td>
            <td style="padding: 12px;"><strong>Budget</strong></td>
            <td style="padding: 12px;"><strong>Mid-Range</strong></td>
            <td style="padding: 12px;"><strong>Luxury</strong></td>
        </tr>
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 12px;">Hotels (6 nights)</td>
            <td style="padding: 12px;">$180</td>
            <td style="padding: 12px;">$450</td>
            <td style="padding: 12px;">$1,200+</td>
        </tr>
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 12px;">Internal Flights</td>
            <td style="padding: 12px;">$200</td>
            <td style="padding: 12px;">$200</td>
            <td style="padding: 12px;">$400</td>
        </tr>
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 12px;">Entry Fees</td>
            <td style="padding: 12px;">$150</td>
            <td style="padding: 12px;">$200</td>
            <td style="padding: 12px;">$250</td>
        </tr>
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 12px;">Guides & Tours</td>
            <td style="padding: 12px;">$100</td>
            <td style="padding: 12px;">$300</td>
            <td style="padding: 12px;">$600</td>
        </tr>
        <tr style="font-weight: bold; background: #e8f5e9;">
            <td style="padding: 12px;">TOTAL</td>
            <td style="padding: 12px;">~$650</td>
            <td style="padding: 12px;">~$1,200</td>
            <td style="padding: 12px;">~$2,500+</td>
        </tr>
    </table>
</div>
''',

        'egyptian-food-guide-dishes': '''
<div class="article-hero" style="background: linear-gradient(135deg, #f39c12 0%, #d35400 100%); padding: 40px; border-radius: 20px; margin-bottom: 30px; color: white;">
    <h2 style="font-size: 2.5em; margin-bottom: 15px;">🍽️ Egyptian Food: 15 Dishes You MUST Try</h2>
    <p style="font-size: 1.2em; opacity: 0.9;">From street food to royal feasts — your complete Egyptian culinary guide</p>
</div>

<p class="lead" style="font-size: 1.3em; line-height: 1.8; color: #2c3e50;">Egyptian cuisine is a <strong>5,000-year-old love story</strong> with food. From the pharaohs' bread and beer to today's beloved koshari, every dish tells a story. Here are the essential Egyptian foods that will make your taste buds thank you.</p>

<h2>🥇 The Essential Egyptian Dishes</h2>

<div style="background: #fff8e1; padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #f57f17;">1. 🍲 Koshari (كشري)</h3>
    <p><strong>Egypt's National Dish</strong></p>
    <p>A glorious carb-fest of rice, lentils, macaroni, and chickpeas topped with crispy fried onions and spicy tomato sauce. Street vendors pile it high for just $1-2. Vegetarian and absolutely addictive.</p>
    <p><em>Best spot: Abou Tarek in Downtown Cairo</em></p>
</div>

<div style="background: #e8f5e9; padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #2e7d32;">2. 🫘 Ful Medames (فول مدمس)</h3>
    <p><strong>The Breakfast of Pharaohs</strong></p>
    <p>Slow-cooked fava beans mashed with olive oil, lemon, cumin, and garlic. Served for breakfast with warm bread, it's been eaten in Egypt for over 4,000 years!</p>
    <p><em>Pro tip: Add tahini and a boiled egg for the full experience</em></p>
</div>

<div style="background: #e3f2fd; padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #1565c0;">3. 🧆 Ta'ameya (طعمية)</h3>
    <p><strong>Egyptian Falafel (But Better)</strong></p>
    <p>Unlike Middle Eastern falafel made with chickpeas, Egyptian ta'ameya uses fava beans—making them lighter, greener, and crispier. Stuffed in bread with tahini and salad.</p>
    <p><em>Best at: Any street cart in Cairo, especially in Giza</em></p>
</div>

<div style="background: #fce4ec; padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #c2185b;">4. 🍖 Kofta & Kebab</h3>
    <p><strong>Grilled Meat Perfection</strong></p>
    <p>Spiced minced meat (kofta) or chunks of marinated lamb/beef (kebab) grilled over charcoal. Served with bread, tahini, and grilled vegetables.</p>
    <p><em>Must-try: Andrea Mariouteya in Giza for iconic outdoor grilling</em></p>
</div>

<div style="background: #f3e5f5; padding: 30px; border-radius: 20px; margin: 25px 0;">
    <h3 style="color: #7b1fa2;">5. 🥙 Shawarma</h3>
    <p><strong>Late-Night Fuel</strong></p>
    <p>Marinated meat stacked on a vertical rotisserie, shaved off and wrapped in bread with tahini, pickles, and garlic sauce. The ultimate 2 AM snack.</p>
</div>

<h2>🍰 Sweet Treats</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 15px;">
        <h4>🍮 Om Ali</h4>
        <p>Egypt's beloved bread pudding: layers of puff pastry, milk, cream, nuts, and raisins, baked until golden. Warm, gooey heaven.</p>
    </div>
    <div style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); padding: 25px; border-radius: 15px;">
        <h4>🍯 Basbousa</h4>
        <p>Semolina cake soaked in sweet syrup, often topped with almonds or coconut. Dense, sweet, and perfect with tea.</p>
    </div>
    <div style="background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); padding: 25px; border-radius: 15px;">
        <h4>🥧 Konafa</h4>
        <p>Crispy shredded phyllo dough with cream or cheese filling, drenched in sugar syrup. Especially popular during Ramadan.</p>
    </div>
</div>

<div style="background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%); border-radius: 20px; padding: 30px; margin: 40px 0; color: white; text-align: center;">
    <h3 style="margin-bottom: 15px;">🍴 Egyptian Food Tours</h3>
    <p style="opacity: 0.9; margin-bottom: 20px;">Explore Cairo's best street food with local guides</p>
    <a href="/tours/" style="background: white; color: #f39c12; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">Book Food Tour</a>
</div>

<h2>☕ Egyptian Drinks</h2>
<ul style="line-height: 2.2;">
    <li>🍵 <strong>Karkade:</strong> Hibiscus tea, served hot or cold, deep red and refreshing</li>
    <li>☕ <strong>Ahwa:</strong> Egyptian coffee, strong and often cardamom-spiced</li>
    <li>🥤 <strong>Fresh Juice:</strong> Mango, sugarcane, and strawberry stands everywhere</li>
    <li>🥛 <strong>Sahlab:</strong> Warm, creamy orchid-root drink topped with nuts (winter specialty)</li>
</ul>

<blockquote style="background: #f8f9fa; border-left: 5px solid #f39c12; padding: 25px; margin: 30px 0; font-style: italic; font-size: 1.2em;">
"In Egypt, food is love. Every meal is a celebration, every dish a story passed down through generations."
</blockquote>
''',
    }

    # Update articles with rich content
    for slug, content in article_contents.items():
        try:
            post = BlogPost.objects.get(slug=slug)
            post.content = content
            post.save()
            updated += 1
        except BlogPost.DoesNotExist:
            pass

    return JsonResponse({'success': True, 'updated': updated, 'total': BlogPost.objects.count()})

urlpatterns = [
    path('update-content/', update_articles_content, name='update_content'),
    path('seed-more/', seed_more_articles, name='seed_more'),
    path('setup-all/', setup_all, name='setup_all'),
    path('favicon.svg', favicon, name='favicon'),
    path('favicon.ico', favicon, name='favicon_ico'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', health_check, name='health'),
    path('debug-db/', debug_db, name='debug_db'),
    path('seed/', seed_articles, name='seed'),
    path('seed2026/', seed_2026_articles, name='seed2026'),
    path('seed-egypt/', seed_egypt_history_articles, name='seed_egypt'),
    path('seed-luxury/', seed_luxury_articles, name='seed_luxury'),
    path('seed-stories/', seed_true_stories, name='seed_stories'),
    path('organize/', organize_all_articles, name='organize'),
    path('debug/', debug_check, name='debug'),
    path('blog-diagnose/', blog_diagnose, name='blog_diagnose'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accommodations/', include('accommodations.urls')),
    path('tours/', include('tours.urls')),
    path('destinations/', include('destinations.urls')),
    path('accounts/', include('accounts.urls')),  # Custom account views
    path('accounts/', include('allauth.urls')),  # OAuth social login (Google, Facebook)
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
    path('payments/', include('payments.urls')),
    path('transportation/', include('transportation.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
