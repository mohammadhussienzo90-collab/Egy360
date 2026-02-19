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
from django.contrib.admin.views.decorators import staff_member_required
import os

def health_check(request):
    """Basic health check for Railway"""
    import subprocess
    from django.db import connection

    # Get deployed commit hash
    commit = os.environ.get('RAILWAY_GIT_COMMIT_SHA', '')
    if not commit:
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True, text=True, timeout=5
            )
            commit = result.stdout.strip() if result.returncode == 0 else 'unknown'
        except Exception:
            commit = 'unknown'

    response = {'status': 'ok', 'commit': commit, 'branch': 'main'}

    # Always include DB info
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        response['db_connected'] = True
        response['db_engine'] = connection.vendor
    except Exception as e:
        response['db_connected'] = False
        response['db_error'] = str(e)

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

    # Step 7: Try to render blog detail template
    try:
        from django.template import loader
        from blog.models import BlogPost, BlogCategory

        post = BlogPost.objects.filter(status='published').first()
        if post:
            context = {
                'post': post,
                'comments': [],
                'related_posts': list(BlogPost.objects.filter(status='published').exclude(id=post.id)[:3]),
                'recent_posts': list(BlogPost.objects.filter(status='published')[:5]),
                'trending_posts': list(BlogPost.objects.filter(status='published').order_by('-views_count')[:5]),
                'categories': list(BlogCategory.objects.all()),
                'reading_time': max(1, len(post.content.split()) // 200) if post.content else 1,
                'next_post': None,
                'prev_post': None,
                'total_articles': 92,
                'request': request,
            }
            t = loader.get_template('blog/detail.html')
            html = t.render(context)
            result['template_test'] = f'SUCCESS - {len(html)} chars rendered'
            result['deploy_version'] = 'v4-template-fix'
        else:
            result['template_test'] = 'No published posts to test'
    except Exception as e:
        result['template_test'] = 'FAILED'
        result['template_error'] = str(e)
        result['template_trace'] = traceback.format_exc()

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

@cache_control(max_age=1800)
def rss_feed(request):
    """Generate RSS feed for blog articles - helps with content syndication"""
    from blog.models import BlogPost
    from django.utils import timezone

    posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:20]

    items = []
    for post in posts:
        pub_date = post.published_at.strftime('%a, %d %b %Y %H:%M:%S +0000') if post.published_at else timezone.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        items.append(f'''
        <item>
            <title><![CDATA[{post.title}]]></title>
            <link>https://360egy.com/blog/{post.slug}/</link>
            <description><![CDATA[{post.excerpt or post.title}]]></description>
            <pubDate>{pub_date}</pubDate>
            <guid>https://360egy.com/blog/{post.slug}/</guid>
            <category><![CDATA[{post.category.name if post.category else 'Travel'}]]></category>
        </item>''')

    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>360egy - Egypt Travel Blog</title>
        <link>https://360egy.com/blog/</link>
        <description>Discover Egypt with expert travel guides, tips, and insider knowledge. From pyramids to beaches, ancient temples to modern Cairo.</description>
        <language>en-us</language>
        <lastBuildDate>{timezone.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
        <atom:link href="https://360egy.com/feed/" rel="self" type="application/rss+xml"/>
        <image>
            <url>https://360egy.com/static/images/logo.png</url>
            <title>360egy</title>
            <link>https://360egy.com</link>
        </image>
        {''.join(items)}
    </channel>
</rss>'''

    return HttpResponse(rss_content, content_type='application/rss+xml')

def expand_all_articles(request):
    """Expand ALL short articles to have complete long-form content - /expand-articles/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from blog.models import BlogPost
    updated = 0

    # Get all articles with short content (less than 1000 characters)
    short_articles = BlogPost.objects.filter(status='published')

    for article in short_articles:
        if len(article.content) < 1500:  # Articles with less than 1500 chars need expansion
            # Generate comprehensive content based on title
            title = article.title
            excerpt = article.excerpt or title

            # Create rich, long-form content
            new_content = f'''<h2>{title}</h2>

<p style="font-size: 1.15em; line-height: 1.8; color: #2c3e50;">
{excerpt} Egypt, the land of pharaohs and pyramids, offers travelers an unparalleled journey through time. From the bustling streets of Cairo to the serene waters of the Nile, every corner of this ancient land holds stories waiting to be discovered. Whether you're a history enthusiast, an adventure seeker, or simply looking for a unique travel experience, Egypt promises memories that will last a lifetime.
</p>

<h3>Why This Matters for Your Egypt Trip</h3>
<p>
Planning a trip to Egypt requires understanding the nuances that make this destination unique. The country's rich history spans over 5,000 years, from the construction of the Great Pyramids to the reign of Cleopatra and beyond. Modern Egypt seamlessly blends this ancient heritage with contemporary culture, creating an experience unlike anywhere else on Earth. Travelers who take the time to understand these aspects find their journeys infinitely more rewarding.
</p>

<p>
The Egyptian people are known for their warmth and hospitality. Despite language barriers, you'll find locals eager to help and share their culture. From shopkeepers in Khan El-Khalili bazaar to guides at ancient temples, the human connections you make will be among your most treasured memories. Learning a few Arabic phrases like "Shukran" (thank you) and "Salam" (hello) will open doors and hearts wherever you go.
</p>

<h3>Essential Tips and Insights</h3>
<p>
Timing your visit correctly can make a significant difference in your experience. The best months to visit Egypt are October through April, when temperatures are comfortable for exploring outdoor sites. Summer months (June-August) can see temperatures exceeding 40°C (104°F), making visits to sites like the Valley of the Kings challenging. However, if you prefer fewer crowds and don't mind the heat, summer offers its own rewards with better prices and shorter queues.
</p>

<p>
When it comes to practical matters, the Egyptian Pound (EGP) is the local currency, though US Dollars and Euros are widely accepted at tourist establishments. ATMs are readily available in cities, but carrying some cash is advisable for smaller towns and tips. Speaking of tips, "baksheesh" (tipping) is an integral part of Egyptian culture – small tips of 5-20 EGP are expected for various services and help supplement modest local wages.
</p>

<h3>Making the Most of Your Experience</h3>
<p>
To truly appreciate Egypt's wonders, consider hiring local guides at major sites. Their knowledge and stories bring ancient monuments to life in ways that guidebooks cannot match. Many guides have studied Egyptology and can provide fascinating insights into hieroglyphics, architectural techniques, and the daily lives of ancient Egyptians. The best guides are often found through reputable tour companies or hotel recommendations.
</p>

<p>
Photography enthusiasts will find Egypt a paradise of visual opportunities. The golden hour light on the pyramids, the colorful chaos of local markets, and the timeless beauty of Nile sunsets offer endless subjects. Remember that some sites charge additional fees for camera use, and always ask permission before photographing local people. Drones require special permits and are prohibited at most archaeological sites.
</p>

<h3>Final Thoughts</h3>
<p>
Egypt is more than just a destination – it's an experience that transforms travelers. The moment you stand before the Great Pyramid or cruise past ancient temples on the Nile, you become part of a story that has captivated humanity for millennia. Whether this is your first visit or you're returning to discover something new, Egypt always has more secrets to reveal and more wonders to share.
</p>

<p>
We hope this guide helps you plan an unforgettable Egyptian adventure. For more detailed information on specific destinations, activities, and travel tips, explore our other guides on 360egy.com. Safe travels, and may your journey through the land of the pharaohs exceed all expectations!
</p>'''

            article.content = new_content
            article.save()
            updated += 1

    return JsonResponse({
        'success': True,
        'updated': updated,
        'total_articles': BlogPost.objects.count(),
        'message': f'Expanded {updated} articles with full content'
    })


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

def update_article_images(request):
    """Update all articles with relevant, topic-specific images - access via /update-images/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from blog.models import BlogPost
    updated = 0

    # Comprehensive image mapping - each article gets a unique, relevant image
    image_map = {
        # Great Pyramid Series
        'great-pyramid-giza-introduction': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',  # Pyramids panorama
        'great-pyramid-history-timeline-workers': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',  # Pyramid close-up
        'great-pyramid-architecture-precision': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',  # Pyramid structure
        'great-pyramid-kings-chamber-secrets': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200&q=80',  # Pyramid interior
        'great-pyramid-construction-methods': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',  # Pyramid blocks

        # Tutankhamun
        'king-tutankhamun-boy-king-guide': 'https://images.unsplash.com/photo-1595981234058-a9302fb97229?w=1200&q=80',  # Egyptian gold/mask
        'tutankhamun-boy-king-egypt': 'https://images.unsplash.com/photo-1595981234058-a9302fb97229?w=1200&q=80',

        # Cleopatra & Queens
        'cleopatra-last-pharaoh-egypt': 'https://images.unsplash.com/photo-1608152142361-1d131f5e520e?w=1200&q=80',  # Ancient Egypt art
        'queen-nefertiti-complete-guide': 'https://images.unsplash.com/photo-1599423423927-8f77f7c5b0c8?w=1200&q=80',  # Egyptian queen art
        'nefertiti-beautiful-queen-egypt': 'https://images.unsplash.com/photo-1599423423927-8f77f7c5b0c8?w=1200&q=80',
        'hatshepsut-female-pharaoh-guide': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200&q=80',  # Hatshepsut temple

        # Ramesses
        'ramesses-ii-greatest-pharaoh': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',  # Abu Simbel
        'ramesses-ii-great-builder': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',

        # Temples
        'karnak-temple-complete-guide': 'https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80',  # Karnak columns
        'luxor-temple-night-visit': 'https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80',  # Luxor temple
        'abu-simbel-sun-festival-guide': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',  # Abu Simbel

        # Valley of Kings
        'valley-of-kings-complete-guide': 'https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200&q=80',  # Valley tombs

        # Sphinx
        'sphinx-giza-complete-guide': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',  # Sphinx

        # Museum
        'grand-egyptian-museum-2026-guide': 'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=1200&q=80',  # Museum
        'egyptian-museum-cairo-guide': 'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=1200&q=80',

        # Nile & Cruises
        'luxury-nile-cruises-2026': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',  # Nile boat
        'nile-cruise-guide-2026': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',
        'felucca-sailing-nile-guide': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',  # Felucca

        # Travel Guides
        '7-day-egypt-itinerary-cairo-abu-simbel': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',  # Egypt overview
        '7-day-egypt-itinerary': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
        'best-time-visit-egypt-2026': 'https://images.unsplash.com/photo-1551634979-2b11f8c946fe?w=1200&q=80',  # Sunny Egypt

        # Destinations - Cairo
        'cairo-metro-guide-map': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',  # Cairo city
        'khan-el-khalili-shopping-guide': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80',  # Market bazaar
        'coptic-cairo-christian-heritage': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',  # Old Cairo
        'islamic-cairo-walking-tour': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',  # Islamic Cairo

        # Destinations - Alexandria
        'alexandria-egypt-travel-guide': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80',  # Mediterranean coast

        # Destinations - Aswan
        'aswan-nubia-travel-guide': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',  # Aswan Nile

        # Destinations - Luxor
        'hot-air-balloon-luxor-guide': 'https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=1200&q=80',  # Hot air balloon

        # Red Sea & Beaches
        'dahab-diving-guide': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200&q=80',  # Underwater diving
        'sharm-el-sheikh-guide': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200&q=80',  # Red Sea beach

        # Desert
        'siwa-oasis-complete-guide': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80',  # Desert oasis
        'white-desert-camping-guide': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80',  # White desert
        'lost-desert-egypt-survival': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80',

        # Luxury
        'five-star-hotels-cairo-egypt': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80',  # Luxury hotel
        'private-tours-pyramids-giza': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',

        # Food & Culture
        'egyptian-food-guide-dishes': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1200&q=80',  # Egyptian food
        'egyptian-coffee-culture': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80',  # Coffee
        'ramadan-egypt-travel-guide': 'https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80',  # Mosque
        'egyptian-wedding-traditions': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80',  # Celebration
        'egyptian-handicrafts-shopping': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80',  # Crafts

        # Practical Tips
        'egypt-visa-guide-2026': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200&q=80',  # Airport/travel
        'egypt-currency-money-guide': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
        'what-to-pack-egypt-checklist': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
        'egypt-safety-tips-tourists': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
        'egyptian-arabic-phrases-travelers': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',

        # Ancient Egypt Topics
        'egyptian-mummies-guide': 'https://images.unsplash.com/photo-1595981234058-a9302fb97229?w=1200&q=80',  # Mummy/artifacts
        'hieroglyphics-guide-basics': 'https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200&q=80',  # Hieroglyphics
        'egyptian-gods-goddesses-guide': 'https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80',  # Temple carvings
        'rosetta-stone-ancient-egypt': 'https://images.unsplash.com/photo-1567354723472-d3e9f3f8c6b0?w=1200&q=80',

        # Travel Styles
        'egypt-kids-family-guide': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
        'solo-female-travel-egypt': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
        'budget-egypt-travel-guide': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
        'egypt-photography-guide-tips': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',

        # Trending 2026
        'is-egypt-safe-2026-safety-guide': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',  # Friendly Egypt
        'egypt-vs-morocco-comparison-2026': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
        'best-instagram-spots-egypt-2026': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',  # Photogenic pyramid
        'egypt-travel-costs-budget-2026': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',

        # Stories
        'hidden-tomb-discovery-luxor': 'https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200&q=80',  # Tomb
    }

    # Update each article with its specific image
    for slug, image_url in image_map.items():
        try:
            post = BlogPost.objects.get(slug=slug)
            if post.image_url != image_url:
                post.image_url = image_url
                post.save()
                updated += 1
        except BlogPost.DoesNotExist:
            pass

    # For articles without specific mapping, assign based on category
    category_images = {
        'ancient-egypt': [
            'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',
            'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',
            'https://images.unsplash.com/photo-1564507004663-b6dfb3c824d5?w=1200&q=80',
            'https://images.unsplash.com/photo-1562679299-266d1ab81bb4?w=1200&q=80',
        ],
        'travel-guides': [
            'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
            'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
        ],
        'destinations': [
            'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80',
        ],
        'luxury-travel': [
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80',
            'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',
        ],
        'food-drink': [
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1200&q=80',
            'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80',
        ],
    }

    # Update remaining articles by category
    for post in BlogPost.objects.all():
        if post.slug not in image_map and post.category:
            cat_slug = post.category.slug
            if cat_slug in category_images:
                images = category_images[cat_slug]
                new_image = images[post.id % len(images)]
                if post.image_url != new_image:
                    post.image_url = new_image
                    post.save()
                    updated += 1

    return JsonResponse({'success': True, 'updated': updated, 'total': BlogPost.objects.count()})

def seed_trending_2026(request):
    """Seed high-traffic trending 2026 articles - access via /seed-trending/?key=egy360seed"""
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users'}, status=500)

    created = 0
    cat, _ = BlogCategory.objects.get_or_create(slug='travel-guides', defaults={'name': 'Travel Guides', 'description': 'Comprehensive travel guides'})

    trending_articles = [
        {
            'title': 'Is Egypt Safe to Visit in 2026? Complete Safety Guide',
            'slug': 'is-egypt-safe-2026-safety-guide',
            'excerpt': 'Everything you need to know about safety in Egypt 2026. Tourist areas, scams to avoid, women travelers, and current travel advisories.',
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
            'content': '''
<div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 30px; border-radius: 20px; margin-bottom: 30px; color: white; text-align: center;">
    <h2 style="margin-bottom: 10px;">✅ Egypt Is Safe for Tourists in 2026</h2>
    <p style="opacity: 0.9; margin-bottom: 0;">Millions visit safely every year. Here's what you need to know.</p>
</div>

<h2>🛡️ Current Safety Status (February 2026)</h2>
<p>Egypt welcomes over <strong>14 million tourists annually</strong>, making it one of Africa's most visited destinations. Tourist areas including Cairo, Luxor, Aswan, and Red Sea resorts are well-protected with visible security presence.</p>

<h3>What International Advisories Say</h3>
<ul>
    <li><strong>UK Foreign Office:</strong> Safe for most tourist areas</li>
    <li><strong>US State Department:</strong> Exercise increased caution (Level 2 - same as France, UK)</li>
    <li><strong>Australian Government:</strong> Exercise normal safety precautions for tourist areas</li>
</ul>

<h2>🚨 Common Scams to Avoid</h2>
<div style="background: #fff3cd; padding: 20px; border-radius: 15px; margin: 20px 0;">
    <h4 style="color: #856404;">Watch Out For:</h4>
    <ul style="margin-bottom: 0;">
        <li><strong>"Free" gifts</strong> - Nothing is free, they'll demand payment</li>
        <li><strong>Fake guides</strong> - Only use licensed guides with ID</li>
        <li><strong>Taxi scams</strong> - Use Uber/Careem or agree on price before</li>
        <li><strong>"Closed today"</strong> - Attractions are open, they want commission</li>
    </ul>
</div>

<h2>👩 Solo Female Travelers</h2>
<p>Egypt is generally safe for solo women, but cultural awareness helps:</p>
<ul>
    <li>Dress modestly (shoulders and knees covered)</li>
    <li>Ignore catcalls - don't engage</li>
    <li>Stay in tourist areas after dark</li>
    <li>Use ride-hailing apps instead of street taxis</li>
</ul>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin: 30px 0; color: white; text-align: center;">
    <h4>🎯 Travel with Confidence</h4>
    <p style="opacity: 0.9;">Book verified tours with trusted local guides</p>
    <a href="/tours/" style="background: white; color: #667eea; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block;">Browse Safe Tours</a>
</div>
''',
            'is_featured': True
        },
        {
            'title': 'Egypt vs Morocco: Which Should You Visit in 2026?',
            'slug': 'egypt-vs-morocco-comparison-2026',
            'excerpt': 'Comparing two of Africa\'s top destinations. History, beaches, costs, food, and experiences - which is right for you?',
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
            'content': '''
<h2>🆚 Egypt vs Morocco: The Ultimate Comparison</h2>
<p>Both countries offer incredible experiences, but they're quite different. Here's how to choose.</p>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0;">
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px;">
        <h3 style="color: #2e7d32;">🏛️ Choose Egypt If You Want:</h3>
        <ul>
            <li>Ancient history (5000+ years)</li>
            <li>Pyramids, temples, tombs</li>
            <li>Nile River cruises</li>
            <li>Red Sea diving</li>
            <li>More affordable</li>
        </ul>
    </div>
    <div style="background: #fff3e0; padding: 25px; border-radius: 15px;">
        <h3 style="color: #e65100;">🕌 Choose Morocco If You Want:</h3>
        <ul>
            <li>Medieval medinas</li>
            <li>Sahara Desert camps</li>
            <li>Atlas Mountains</li>
            <li>Vibrant souks</li>
            <li>French-influenced cuisine</li>
        </ul>
    </div>
</div>

<h2>💰 Cost Comparison</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
    <tr style="background: #f8f9fa;">
        <th style="padding: 12px; text-align: left;">Category</th>
        <th style="padding: 12px;">Egypt</th>
        <th style="padding: 12px;">Morocco</th>
    </tr>
    <tr>
        <td style="padding: 12px;">Budget hotel/night</td>
        <td style="padding: 12px; text-align: center;">$20-40</td>
        <td style="padding: 12px; text-align: center;">$30-50</td>
    </tr>
    <tr style="background: #f8f9fa;">
        <td style="padding: 12px;">Meal</td>
        <td style="padding: 12px; text-align: center;">$3-8</td>
        <td style="padding: 12px; text-align: center;">$5-12</td>
    </tr>
    <tr>
        <td style="padding: 12px;">Daily budget</td>
        <td style="padding: 12px; text-align: center; color: #27ae60; font-weight: bold;">$50-80</td>
        <td style="padding: 12px; text-align: center;">$70-100</td>
    </tr>
</table>

<h2>🏆 Verdict</h2>
<p><strong>For history lovers:</strong> Egypt wins hands-down with 5,000 years of civilization.</p>
<p><strong>For foodies:</strong> Morocco has more diverse cuisine.</p>
<p><strong>For adventure:</strong> Both excellent - Egypt for diving, Morocco for trekking.</p>
<p><strong>For budget:</strong> Egypt is more affordable.</p>
''',
            'is_featured': True
        },
        {
            'title': 'Best Instagram Spots in Egypt 2026: Photo Guide',
            'slug': 'best-instagram-spots-egypt-2026',
            'excerpt': 'The most photogenic locations in Egypt for your Instagram feed. Pyramids, temples, deserts, and hidden gems with photography tips.',
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200',
            'content': '''
<h2>📸 Top 15 Instagram Spots in Egypt</h2>

<h3>1. Pyramids of Giza - Multiple Angles</h3>
<ul>
    <li><strong>Classic shot:</strong> 9 Pyramids Lounge rooftop</li>
    <li><strong>Sunrise:</strong> From the desert behind</li>
    <li><strong>With camel:</strong> Best light at 7-8 AM</li>
</ul>

<h3>2. Luxor Temple at Night</h3>
<p>The illuminated columns create magical photos. Visit after 6 PM when lights turn on.</p>

<h3>3. Valley of the Kings - Tomb Interiors</h3>
<p>Note: Photography is NOT allowed inside tombs (except with special permit).</p>

<h3>4. Abu Simbel at Sunrise</h3>
<p>The colossal statues glowing pink at dawn is unforgettable.</p>

<h3>5. White Desert</h3>
<p>Surreal chalk formations look like another planet. Best for overnight camping shots with stars.</p>

<div style="background: linear-gradient(135deg, #e91e63 0%, #9c27b0 100%); padding: 25px; border-radius: 15px; margin: 30px 0; color: white; text-align: center;">
    <h4>📷 Photography Tours</h4>
    <p style="opacity: 0.9;">Get the best shots with local photographer guides</p>
    <a href="/tours/" style="background: white; color: #e91e63; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block;">Book Photo Tour</a>
</div>

<h3>Pro Tips:</h3>
<ul>
    <li>🌅 <strong>Golden hour:</strong> 6-7 AM and 5-6 PM</li>
    <li>📱 <strong>Wide angle:</strong> Essential for temples</li>
    <li>👗 <strong>What to wear:</strong> Flowy dresses photograph beautifully</li>
    <li>🐪 <strong>Camel photos:</strong> Agree on price BEFORE taking photo</li>
</ul>
''',
            'is_featured': True
        },
        {
            'title': 'Egypt Travel Costs 2026: Complete Budget Breakdown',
            'slug': 'egypt-travel-costs-budget-2026',
            'excerpt': 'Exactly how much does Egypt cost? Daily budgets for backpackers, mid-range, and luxury travelers with price breakdowns.',
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
            'content': '''
<h2>💰 Egypt Travel Budget 2026</h2>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">
    <div style="background: #e3f2fd; padding: 25px; border-radius: 15px; text-align: center;">
        <h3 style="color: #1565c0;">🎒 Budget</h3>
        <p style="font-size: 2rem; font-weight: bold; color: #1565c0; margin: 10px 0;">$30-50</p>
        <p style="color: #666;">per day</p>
    </div>
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px; text-align: center;">
        <h3 style="color: #2e7d32;">🧳 Mid-Range</h3>
        <p style="font-size: 2rem; font-weight: bold; color: #2e7d32; margin: 10px 0;">$80-150</p>
        <p style="color: #666;">per day</p>
    </div>
    <div style="background: #fce4ec; padding: 25px; border-radius: 15px; text-align: center;">
        <h3 style="color: #c2185b;">💎 Luxury</h3>
        <p style="font-size: 2rem; font-weight: bold; color: #c2185b; margin: 10px 0;">$250+</p>
        <p style="color: #666;">per day</p>
    </div>
</div>

<h2>Detailed Breakdown</h2>
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background: #f8f9fa;">
        <th style="padding: 12px; text-align: left;">Item</th>
        <th style="padding: 12px;">Budget</th>
        <th style="padding: 12px;">Mid-Range</th>
        <th style="padding: 12px;">Luxury</th>
    </tr>
    <tr><td style="padding: 12px;">Accommodation</td><td style="padding: 12px; text-align: center;">$10-20</td><td style="padding: 12px; text-align: center;">$50-100</td><td style="padding: 12px; text-align: center;">$200+</td></tr>
    <tr style="background: #f8f9fa;"><td style="padding: 12px;">Food</td><td style="padding: 12px; text-align: center;">$5-10</td><td style="padding: 12px; text-align: center;">$20-40</td><td style="padding: 12px; text-align: center;">$50+</td></tr>
    <tr><td style="padding: 12px;">Transport</td><td style="padding: 12px; text-align: center;">$5-10</td><td style="padding: 12px; text-align: center;">$20-30</td><td style="padding: 12px; text-align: center;">$50+</td></tr>
    <tr style="background: #f8f9fa;"><td style="padding: 12px;">Activities</td><td style="padding: 12px; text-align: center;">$10-15</td><td style="padding: 12px; text-align: center;">$30-50</td><td style="padding: 12px; text-align: center;">$100+</td></tr>
</table>

<h2>Money-Saving Tips</h2>
<ul>
    <li>💵 <strong>Exchange money in Egypt</strong> - better rates than home</li>
    <li>🍽️ <strong>Eat local</strong> - koshari is $1, amazing street food everywhere</li>
    <li>🚇 <strong>Use Cairo Metro</strong> - only $0.30 per ride</li>
    <li>🎫 <strong>Buy combo tickets</strong> - save on entry fees</li>
</ul>
''',
            'is_featured': False
        }
    ]

    for article in trending_articles:
        if not BlogPost.objects.filter(slug=article['slug']).exists():
            BlogPost.objects.create(
                title=article['title'],
                slug=article['slug'],
                excerpt=article['excerpt'],
                content=article['content'],
                image_url=article['image_url'],
                author=author,
                category=cat,
                is_featured=article['is_featured'],
                status='published',
                published_at=timezone.now()
            )
            created += 1

    return JsonResponse({'success': True, 'created': created, 'total': BlogPost.objects.count()})


def seed_comprehensive_articles(request):
    """
    Seed 50+ comprehensive Egypt travel articles covering all topics.
    Access via /seed-all-topics/?key=egy360seed
    """
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User
    from django.utils import timezone
    from blog.models import BlogPost, BlogCategory

    author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users found'}, status=500)

    created = 0

    # Define categories
    categories_data = {
        'hidden-gems': ('Hidden Gems', 'Discover secret spots and lesser-known treasures'),
        'food-cuisine': ('Food & Cuisine', 'Egyptian culinary experiences and food guides'),
        'adventure': ('Adventure', 'Thrilling activities and outdoor experiences'),
        'culture': ('Culture & Heritage', 'Cultural experiences and local traditions'),
        'photography': ('Photography', 'Best photo spots and photography guides'),
        'budget-travel': ('Budget Travel', 'Money-saving tips and affordable options'),
        'luxury-travel': ('Luxury Travel', 'Premium experiences and 5-star options'),
        'family-travel': ('Family Travel', 'Kid-friendly activities and family guides'),
        'solo-travel': ('Solo Travel', 'Solo traveler tips and safety guides'),
        'romance': ('Romantic Getaways', 'Couples travel and honeymoon ideas'),
        'diving-snorkeling': ('Diving & Snorkeling', 'Red Sea underwater adventures'),
        'desert-adventures': ('Desert Adventures', 'Sahara experiences and oasis trips'),
        'nile-experiences': ('Nile Experiences', 'River cruises and Nile activities'),
        'wellness-spa': ('Wellness & Spa', 'Relaxation and wellness experiences'),
        'shopping': ('Shopping', 'Markets, souvenirs, and shopping guides'),
        'nightlife': ('Nightlife', 'Evening entertainment and social scenes'),
        'festivals': ('Festivals & Events', 'Egyptian celebrations and events'),
        'eco-tourism': ('Eco Tourism', 'Sustainable and eco-friendly travel'),
    }

    # Create categories
    cats = {}
    for slug, (name, desc) in categories_data.items():
        cat, _ = BlogCategory.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'description': desc}
        )
        cats[slug] = cat

    # Comprehensive articles list
    articles = [
        # HIDDEN GEMS
        {
            'title': "10 Secret Beaches in Egypt Locals Don't Want You to Know",
            'slug': 'secret-beaches-egypt-hidden-gems',
            'excerpt': 'Escape the crowds and discover pristine, untouched beaches along Egypt\'s coastline that most tourists never find.',
            'category': 'hidden-gems',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
            'content': '''<h2>Egypt's Best Kept Beach Secrets</h2>
<p>While Sharm El Sheikh and Hurghada get all the attention, Egypt hides some of the most pristine beaches in the world. Here are 10 secret spots that will take your breath away.</p>

<h3>1. Ras Shitan, Sinai</h3>
<p>A hippie paradise with crystal-clear waters and zero development. Stay in bamboo huts and disconnect from the world.</p>

<h3>2. Marsa Shagra, South Red Sea</h3>
<p>An eco-village with a house reef that rivals any diving destination. See dolphins, dugongs, and untouched coral.</p>

<h3>3. Ageeba Beach, Marsa Matrouh</h3>
<p>Turquoise waters that look like the Caribbean but without the crowds. The name means "miracle" in Arabic.</p>

<h3>4. Fjord Bay, Taba</h3>
<p>A natural fjord with dramatic mountains meeting the sea. Perfect for snorkeling and kayaking.</p>

<h3>5. Wadi El Gemal, Red Sea</h3>
<p>A protected national park with pristine beaches, mangroves, and incredible wildlife.</p>

<h2>How to Get There</h2>
<p>Most secret beaches require a 4x4 or boat access. Hire a local guide for the best experience and to support the community.</p>

<h2>Best Time to Visit</h2>
<p>October to April offers perfect weather. Avoid July-August when temperatures soar.</p>'''
        },
        {
            'title': 'Underground Cairo: Hidden Tunnels and Secret Passages',
            'slug': 'underground-cairo-hidden-tunnels',
            'excerpt': 'Explore the mysterious underground world beneath Cairo\'s streets - from ancient aqueducts to forgotten passages.',
            'category': 'hidden-gems',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'content': '''<h2>Cairo's Secret Underground World</h2>
<p>Beneath the bustling streets of Cairo lies a hidden network of tunnels, cisterns, and passages that most tourists never see.</p>

<h3>The Nilometer on Rhoda Island</h3>
<p>An ancient device used to measure the Nile's flood levels, dating back to 861 AD. Descend into the cool underground chamber.</p>

<h3>Al-Ghouri Complex Crypts</h3>
<p>Hidden beneath one of Cairo's most beautiful mosques lie atmospheric crypts rarely visited by tourists.</p>

<h3>Babylon Fortress Underground</h3>
<p>The Roman fortress foundations reveal ancient streets and passages now underground due to centuries of accumulated debris.</p>

<h3>The Aqueduct of Cairo</h3>
<p>Walk along the medieval aqueduct that once brought water from the Nile to the Citadel. Parts are accessible with a guide.</p>

<h2>How to Access</h2>
<p>Many underground sites require special permission or a knowledgeable guide. Contact local tour operators specializing in alternative Cairo tours.</p>'''
        },
        # FOOD & CUISINE
        {
            'title': 'Egyptian Street Food: The Ultimate Guide to Eating Like a Local',
            'slug': 'egyptian-street-food-ultimate-guide',
            'excerpt': 'From koshari to feteer, discover the best street food in Egypt and where to find the most authentic bites.',
            'category': 'food-cuisine',
            'image_url': 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=1200',
            'content': '''<h2>The Best Egyptian Street Food</h2>
<p>Egyptian street food is legendary - cheap, delicious, and found on every corner. Here's your complete guide.</p>

<h3>Must-Try Street Foods</h3>

<h4>1. Koshari (كشري)</h4>
<p>Egypt's national dish - rice, pasta, lentils, chickpeas, fried onions, and spicy tomato sauce. Costs only $1!</p>
<p><strong>Best spot:</strong> Abou Tarek in Downtown Cairo</p>

<h4>2. Ful Medames (فول مدمس)</h4>
<p>Slow-cooked fava beans with olive oil, lemon, and cumin. The ultimate Egyptian breakfast.</p>
<p><strong>Best spot:</strong> Any local "ful cart" in the morning</p>

<h4>3. Ta'meya (طعمية)</h4>
<p>Egyptian falafel made with fava beans instead of chickpeas. Crispier and greener than other versions.</p>

<h4>4. Feteer Meshaltet (فطير مشلتت)</h4>
<p>Flaky layered pastry, sweet or savory. Like a Egyptian croissant on steroids.</p>
<p><strong>Best spot:</strong> El Abd Bakery, Cairo</p>

<h4>5. Hawawshi (حواوشي)</h4>
<p>Spiced minced meat baked inside bread. The Egyptian answer to a meat pie.</p>

<h3>Street Food Safety Tips</h3>
<ul>
    <li>Choose busy stalls - high turnover means fresh food</li>
    <li>Watch the food being prepared fresh</li>
    <li>Avoid pre-made items sitting in the sun</li>
    <li>Stick to cooked foods if you have a sensitive stomach</li>
</ul>

<h3>Price Guide</h3>
<p>Most street food costs between $0.50-$2. You can eat like a king for $5/day!</p>'''
        },
        {
            'title': 'Egyptian Coffee Culture: A Complete Guide to Ahwa',
            'slug': 'egyptian-coffee-culture-ahwa-guide',
            'excerpt': 'Discover the rich tradition of Egyptian coffee houses (ahwa) and how to experience authentic local cafe culture.',
            'category': 'food-cuisine',
            'image_url': 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=1200',
            'content': '''<h2>The Art of Egyptian Coffee</h2>
<p>Egyptian coffee culture is about more than caffeine - it's a social institution that has shaped Egyptian society for centuries.</p>

<h3>Understanding Ahwa (Coffee House) Culture</h3>
<p>An ahwa is a gathering place where Egyptians play backgammon, smoke shisha, discuss politics, and solve the world's problems.</p>

<h3>How to Order Coffee</h3>
<ul>
    <li><strong>Ahwa Sada</strong> - Plain, no sugar</li>
    <li><strong>Ahwa Arriha</strong> - Light sugar</li>
    <li><strong>Ahwa Mazbouta</strong> - Medium sugar (most popular)</li>
    <li><strong>Ahwa Ziyada</strong> - Extra sweet</li>
</ul>

<h3>Historic Ahwas to Visit</h3>

<h4>Fishawi's, Khan El-Khalili</h4>
<p>Open 24/7 for over 200 years. Where Naguib Mahfouz wrote his novels.</p>

<h4>El Horreya, Downtown Cairo</h4>
<p>A literary institution with art deco interiors. Popular with artists and intellectuals.</p>

<h4>Café Riche</h4>
<p>Historic cafe where Egyptian revolution was planned in 1919. Beautiful vintage atmosphere.</p>

<h3>Coffee House Etiquette</h3>
<ul>
    <li>Never rush - an ahwa visit is meant to last hours</li>
    <li>It's acceptable to sit alone for hours with one coffee</li>
    <li>Playing backgammon is encouraged</li>
    <li>Some ahwas are men-only - look for mixed seating areas</li>
</ul>'''
        },
        # ADVENTURE
        {
            'title': 'Sandboarding in Egypt: The Ultimate Desert Adventure Guide',
            'slug': 'sandboarding-egypt-desert-adventure',
            'excerpt': 'Ride the dunes of the Sahara! Complete guide to sandboarding in Egypt\'s most spectacular desert locations.',
            'category': 'adventure',
            'image_url': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200',
            'content': '''<h2>Sandboarding in Egypt</h2>
<p>Forget snowboarding - sandboarding down Egypt's massive dunes is the ultimate adrenaline rush!</p>

<h3>Best Sandboarding Locations</h3>

<h4>1. Great Sand Sea, Siwa</h4>
<p>Endless dunes as far as the eye can see. The most epic sandboarding experience in Egypt.</p>

<h4>2. White Desert</h4>
<p>Combine surreal chalk formations with sandboarding for an otherworldly experience.</p>

<h4>3. Fayoum Desert</h4>
<p>Closest to Cairo (2 hours). Perfect for a day trip adventure.</p>

<h4>4. Dahab Desert</h4>
<p>Combine beach time with desert sandboarding in one trip.</p>

<h3>What You Need</h3>
<ul>
    <li>Board (rent from tour operators or bring a snowboard)</li>
    <li>Wax for the board (paraffin works)</li>
    <li>Goggles and face protection</li>
    <li>Lots of water!</li>
</ul>

<h3>Best Time</h3>
<p>October to March. Summer temperatures make sand too hot to touch!</p>

<h3>Pro Tips</h3>
<ul>
    <li>Go early morning when sand is coolest</li>
    <li>Wax your board frequently</li>
    <li>Start on smaller dunes to build confidence</li>
    <li>Expect to walk up a lot - there are no ski lifts!</li>
</ul>'''
        },
        {
            'title': 'Rock Climbing in Sinai: Egypt\'s Best Kept Adventure Secret',
            'slug': 'rock-climbing-sinai-adventure-guide',
            'excerpt': 'Discover world-class rock climbing in the Sinai Peninsula with stunning desert scenery and ancient history.',
            'category': 'adventure',
            'image_url': 'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=1200',
            'content': '''<h2>Rock Climbing in Sinai</h2>
<p>Sinai offers some of the best rock climbing in the Middle East with unique red granite formations and year-round climbing weather.</p>

<h3>Top Climbing Areas</h3>

<h4>Wadi Rum-style Towers near St. Catherine</h4>
<p>Massive granite towers rising from the desert floor. Multi-pitch routes up to 400m.</p>

<h4>Sheikh Awad Bouldering</h4>
<p>World-class bouldering on perfect granite. Over 500 problems documented.</p>

<h4>Blue Valley (Wadi Ghazala)</h4>
<p>Named for blue-painted rocks by a Belgian artist. Sport climbing with easy access.</p>

<h3>Climbing Season</h3>
<p>October to April is perfect. Summer is too hot for comfortable climbing.</p>

<h3>Getting Started</h3>
<ul>
    <li>Bring your own gear - rental is limited</li>
    <li>Hire a local Bedouin guide for access and support</li>
    <li>Many routes are trad - be prepared</li>
    <li>Camping is the best accommodation option</li>
</ul>

<h3>Guided Tours</h3>
<p>Several operators offer climbing trips from Dahab including equipment, transport, and Bedouin hospitality.</p>'''
        },
        # DIVING & SNORKELING
        {
            'title': 'Best Dive Sites in Egypt 2026: Complete Red Sea Guide',
            'slug': 'best-dive-sites-egypt-red-sea-2026',
            'excerpt': 'From the SS Thistlegorm to Ras Mohammed, discover Egypt\'s top 20 dive sites with insider tips.',
            'category': 'diving-snorkeling',
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
            'content': '''<h2>Egypt's Top Dive Sites</h2>
<p>The Red Sea offers some of the best diving on Earth with warm waters, incredible visibility, and diverse marine life.</p>

<h3>Legendary Dive Sites</h3>

<h4>1. SS Thistlegorm, Sharm El Sheikh</h4>
<p>The world's most famous wreck dive. A WWII cargo ship loaded with motorcycles, trucks, and weapons.</p>
<p><strong>Depth:</strong> 16-30m | <strong>Level:</strong> Advanced</p>

<h4>2. Ras Mohammed National Park</h4>
<p>Shark Reef and Yolanda Reef offer wall diving, pelagics, and a cargo of toilets from a sunken ship!</p>
<p><strong>Depth:</strong> 5-50m | <strong>Level:</strong> All levels</p>

<h4>3. The Brothers Islands</h4>
<p>Remote islands with hammerhead sharks, thresher sharks, and pristine walls.</p>
<p><strong>Depth:</strong> 15-40m | <strong>Level:</strong> Advanced</p>

<h4>4. Elphinstone Reef</h4>
<p>Famous for oceanic whitetip sharks and stunning wall diving.</p>
<p><strong>Depth:</strong> 5-40m | <strong>Level:</strong> Intermediate+</p>

<h4>5. Blue Hole, Dahab</h4>
<p>Infamous for its deadly arch, but the main reef is perfect for all levels.</p>
<p><strong>Depth:</strong> 6-110m | <strong>Level:</strong> Varies</p>

<h3>Diving Costs</h3>
<table>
    <tr><th>Service</th><th>Price Range</th></tr>
    <tr><td>Single dive</td><td>$30-50</td></tr>
    <tr><td>Day trip (2 dives)</td><td>$60-100</td></tr>
    <tr><td>PADI Open Water course</td><td>$300-450</td></tr>
    <tr><td>Liveaboard (7 days)</td><td>$800-1500</td></tr>
</table>

<h3>Best Season</h3>
<p>Year-round! Water temp: 21-28°C. Winter (Dec-Feb) for shark encounters, summer for best visibility.</p>'''
        },
        # DESERT ADVENTURES
        {
            'title': 'Siwa Oasis: Complete Guide to Egypt\'s Hidden Paradise',
            'slug': 'siwa-oasis-complete-guide-2026',
            'excerpt': 'Everything you need to know about visiting Siwa - from salt lakes to ancient ruins and Berber culture.',
            'category': 'desert-adventures',
            'image_url': 'https://images.unsplash.com/photo-1548018560-c7196e91a6db?w=1200',
            'content': '''<h2>Siwa Oasis: Egypt's Hidden Paradise</h2>
<p>Remote, magical, and utterly unique - Siwa is unlike anywhere else in Egypt. This Berber oasis near the Libyan border feels like stepping into another world.</p>

<h3>Getting There</h3>
<p>8-hour bus from Cairo or Alexandria. Worth every minute!</p>

<h3>Must-See Attractions</h3>

<h4>Temple of the Oracle</h4>
<p>Where Alexander the Great was proclaimed a god. Incredible sunset views.</p>

<h4>Shali Fortress</h4>
<p>The melting mud-brick ruins of the old town. Atmospheric and photogenic.</p>

<h4>Cleopatra's Bath</h4>
<p>Natural spring pool where locals and tourists swim together. Refreshing!</p>

<h4>Salt Lakes</h4>
<p>Float effortlessly in Egypt's answer to the Dead Sea. Especially beautiful at sunset.</p>

<h4>Great Sand Sea</h4>
<p>Endless dunes perfect for sandboarding, 4x4 adventures, and camping under stars.</p>

<h3>Where to Stay</h3>
<ul>
    <li><strong>Budget:</strong> Palm Trees Hotel - $15/night</li>
    <li><strong>Mid-range:</strong> Siwa Shali Resort - $60/night</li>
    <li><strong>Luxury:</strong> Adrère Amellal - $400/night (no electricity, total desert luxury)</li>
</ul>

<h3>Local Culture</h3>
<p>Siwans speak their own Berber language and have distinct customs. Dress modestly and respect local traditions. Women often wear full covering.</p>

<h3>Best Time to Visit</h3>
<p>October to April. Summer exceeds 45°C - avoid!</p>'''
        },
        {
            'title': 'White Desert Camping: A Complete Night Under the Stars Guide',
            'slug': 'white-desert-camping-guide-2026',
            'excerpt': 'Experience the surreal White Desert with our complete camping guide - what to expect, what to bring, and how to book.',
            'category': 'desert-adventures',
            'image_url': 'https://images.unsplash.com/photo-1542401886-65d6c61db217?w=1200',
            'content': '''<h2>White Desert Camping Guide</h2>
<p>Sleeping among the otherworldly chalk formations of the White Desert is a bucket-list experience.</p>

<h3>What is the White Desert?</h3>
<p>Part of the Farafra Depression, the White Desert features surreal white chalk rock formations carved by wind erosion into mushroom shapes, towers, and abstract sculptures.</p>

<h3>How to Get There</h3>
<ul>
    <li>Book a tour from Cairo (most common) or Bahariya Oasis</li>
    <li>Tours typically include 4x4 transport, camping equipment, and food</li>
    <li>Drive takes about 5 hours from Cairo</li>
</ul>

<h3>What's Included in Tours</h3>
<ul>
    <li>4x4 Jeep with experienced driver</li>
    <li>Camping equipment (tents, sleeping bags, mattresses)</li>
    <li>All meals (usually BBQ dinner, breakfast)</li>
    <li>Campfire and Bedouin tea</li>
    <li>Sandboarding opportunity</li>
</ul>

<h3>What to Bring</h3>
<ul>
    <li>Warm clothes (desert gets COLD at night)</li>
    <li>Camera with wide-angle lens</li>
    <li>Headlamp or flashlight</li>
    <li>Personal toiletries</li>
    <li>Snacks if you're picky</li>
</ul>

<h3>Prices</h3>
<ul>
    <li><strong>1 night/2 days:</strong> $80-150 per person</li>
    <li><strong>2 nights/3 days:</strong> $150-250 per person</li>
</ul>

<h3>Photography Tips</h3>
<p>Sunset and sunrise are magical. The Milky Way is visible on moonless nights. Bring a tripod!</p>'''
        },
        # NILE EXPERIENCES
        {
            'title': 'Felucca Sailing on the Nile: The Ultimate Traditional Experience',
            'slug': 'felucca-sailing-nile-guide-2026',
            'excerpt': 'Sail the Nile the way ancient Egyptians did. Complete guide to felucca trips from Aswan to Luxor.',
            'category': 'nile-experiences',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'content': '''<h2>Felucca Sailing on the Nile</h2>
<p>A felucca is a traditional wooden sailboat that has plied the Nile for thousands of years. Sailing on one is the most authentic way to experience the river.</p>

<h3>Popular Felucca Routes</h3>

<h4>Aswan to Kom Ombo (2 days/1 night)</h4>
<p>The most popular option. See Kom Ombo Temple and sleep under the stars on the boat.</p>

<h4>Aswan to Edfu (3 days/2 nights)</h4>
<p>Add Edfu Temple to your route. More relaxed pace.</p>

<h4>Sunset Cruise in Aswan (2 hours)</h4>
<p>Perfect introduction. Sail around Elephantine Island as the sun sets.</p>

<h3>What to Expect</h3>
<ul>
    <li>Sleep on deck under blankets (magical!)</li>
    <li>Simple meals cooked by the captain</li>
    <li>Swimming stops in the Nile</li>
    <li>No electricity - complete digital detox</li>
    <li>Shared boats with other travelers</li>
</ul>

<h3>Costs</h3>
<ul>
    <li><strong>Sunset cruise:</strong> $20-30 per boat</li>
    <li><strong>2 days/1 night:</strong> $40-60 per person</li>
    <li><strong>3 days/2 nights:</strong> $70-100 per person</li>
</ul>

<h3>Best Season</h3>
<p>October to April. Summer is too hot and can have minimal wind.</p>

<h3>Tips</h3>
<ul>
    <li>Book through your hotel or hostel for fair prices</li>
    <li>Bring warm clothes for cool nights</li>
    <li>Confirm what meals are included</li>
    <li>Agree on price BEFORE departure</li>
</ul>'''
        },
        # PHOTOGRAPHY
        {
            'title': 'Photographing the Pyramids: Expert Tips for Perfect Shots',
            'slug': 'photographing-pyramids-expert-tips',
            'excerpt': 'Get the perfect pyramid photo with our expert guide covering best times, angles, and secret spots.',
            'category': 'photography',
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200',
            'content': '''<h2>The Ultimate Pyramid Photography Guide</h2>
<p>Getting that perfect pyramid shot requires planning. Here's everything you need to know.</p>

<h3>Best Times to Shoot</h3>

<h4>Sunrise (6:00-7:30 AM)</h4>
<p>Soft golden light, fewer crowds, camels being positioned. The magic hour!</p>

<h4>Sunset (5:00-6:30 PM in winter)</h4>
<p>Warm light on the pyramids, dramatic shadows. Sound and Light show begins after.</p>

<h4>Night (Full Moon)</h4>
<p>The pyramids under moonlight are spectacular. Check lunar calendar!</p>

<h3>Best Photo Spots</h3>

<h4>1. Panoramic Point</h4>
<p>The classic viewpoint with all three pyramids. Get there early for camel shots.</p>

<h4>2. The Sphinx View</h4>
<p>Frame the Sphinx with the Great Pyramid behind. Iconic composition.</p>

<h4>3. Inside the Complex</h4>
<p>Unique angles looking up at the massive blocks. Show scale with people.</p>

<h4>4. 9 Pyramids Lounge (Rooftop View)</h4>
<p>Restaurant with stunning rooftop views. Perfect for sunset drinks and photos.</p>

<h3>Camera Settings</h3>
<ul>
    <li><strong>Aperture:</strong> f/8-f/11 for sharpness</li>
    <li><strong>ISO:</strong> Keep low (100-400) for quality</li>
    <li><strong>Focal Length:</strong> Wide (16-35mm) for full view, 50-85mm for details</li>
</ul>

<h3>Avoid These Mistakes</h3>
<ul>
    <li>Don't shoot midday - harsh shadows and hazy sky</li>
    <li>Don't just shoot from the entrance - explore!</li>
    <li>Don't forget to capture details and textures</li>
    <li>Don't leave without photographing locals and camels</li>
</ul>'''
        },
        # FAMILY TRAVEL
        {
            'title': 'Egypt with Kids: The Ultimate Family Travel Guide 2026',
            'slug': 'egypt-with-kids-family-guide-2026',
            'excerpt': 'Everything you need to know about traveling Egypt with children - from age-appropriate activities to practical tips.',
            'category': 'family-travel',
            'image_url': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?w=1200',
            'content': '''<h2>Traveling Egypt with Kids</h2>
<p>Egypt is an incredible destination for families. Where else can kids see real mummies, ride camels, and swim in the Red Sea?</p>

<h3>Best Activities for Kids</h3>

<h4>Camel Rides at the Pyramids</h4>
<p>Every kid's dream come true! Short rides available for all ages.</p>

<h4>Grand Egyptian Museum</h4>
<p>Interactive exhibits and the Children's Museum section make history fun.</p>

<h4>Snorkeling in the Red Sea</h4>
<p>Calm, warm waters with colorful fish. Perfect for kids 5+.</p>

<h4>Felucca Sunset Cruise</h4>
<p>Short boat rides on the Nile are magical and safe.</p>

<h4>Sound & Light Shows</h4>
<p>Pyramids and Karnak come alive at night with dramatic storytelling.</p>

<h3>Age-Specific Tips</h3>

<h4>Babies (0-2 years)</h4>
<ul>
    <li>Bring a carrier - strollers struggle on uneven ground</li>
    <li>All major brands of diapers/formula available</li>
    <li>Hotels offer babysitting services</li>
</ul>

<h4>Toddlers (2-5 years)</h4>
<ul>
    <li>Short attention spans - plan quick visits</li>
    <li>Snacks are essential</li>
    <li>The beach is your friend</li>
</ul>

<h4>Kids (5-12 years)</h4>
<ul>
    <li>History comes alive - read books beforehand</li>
    <li>Perfect age for camel rides and snorkeling</li>
    <li>They'll love the mummies!</li>
</ul>

<h3>Family-Friendly Hotels</h3>
<ul>
    <li><strong>Cairo:</strong> Mena House (pyramid views + pool)</li>
    <li><strong>Luxor:</strong> Steigenberger (kids club)</li>
    <li><strong>Red Sea:</strong> Makadi Bay resorts (all-inclusive)</li>
</ul>

<h3>Health & Safety</h3>
<ul>
    <li>Bring rehydration salts for upset tummies</li>
    <li>Sunscreen is essential - Egyptian sun is strong</li>
    <li>Bottled water only</li>
    <li>Kids under 12 get discounts at most sites</li>
</ul>'''
        },
        # SOLO TRAVEL
        {
            'title': 'Solo Female Travel in Egypt: Honest Guide & Safety Tips',
            'slug': 'solo-female-travel-egypt-safety-guide',
            'excerpt': 'Real talk about solo female travel in Egypt - what to expect, how to stay safe, and why it\'s worth it.',
            'category': 'solo-travel',
            'image_url': 'https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=1200',
            'content': '''<h2>Solo Female Travel in Egypt</h2>
<p>Let's be honest: Egypt has a reputation. But thousands of solo women visit every year and have amazing experiences. Here's the real story.</p>

<h3>The Reality</h3>
<p>Yes, you will get attention. Men will try to talk to you, sell you things, and occasionally make comments. But violent crime against tourists is extremely rare, and with the right strategies, you can have an incredible trip.</p>

<h3>Practical Safety Tips</h3>

<h4>Dress Strategically</h4>
<ul>
    <li>Cover shoulders and knees (loose clothing works best)</li>
    <li>A headscarf isn't required but reduces attention</li>
    <li>Sunglasses help avoid eye contact</li>
    <li>Wedding ring (real or fake) can help</li>
</ul>

<h4>Getting Around</h4>
<ul>
    <li>Use Uber/Careem instead of street taxis</li>
    <li>Sit in the back seat of cabs</li>
    <li>Use the women's car on the Cairo Metro</li>
    <li>Book tours through reputable companies</li>
</ul>

<h4>Accommodation</h4>
<ul>
    <li>Book hotels with good reviews from solo women</li>
    <li>Request rooms away from ground floor</li>
    <li>Use door chains and safety locks</li>
</ul>

<h3>Dealing with Unwanted Attention</h3>
<ul>
    <li>Ignore and keep walking - engaging encourages more</li>
    <li>Say "la shukran" (no thanks) firmly</li>
    <li>"I'm meeting my husband" works wonders</li>
    <li>Duck into shops or hotels if needed</li>
</ul>

<h3>Best Destinations for Solo Women</h3>
<ol>
    <li><strong>Dahab</strong> - Incredibly laid back and safe</li>
    <li><strong>Luxor</strong> - Tourist-friendly, easy to navigate</li>
    <li><strong>Aswan</strong> - Small, friendly, less hassle</li>
    <li><strong>Red Sea resorts</strong> - Controlled environments</li>
</ol>

<h3>Final Thoughts</h3>
<p>Don't let fear stop you from experiencing Egypt. The overwhelming majority of Egyptians are hospitable and kind. The hassle is annoying but manageable, and the rewards are incredible.</p>'''
        },
        # ROMANCE
        {
            'title': 'Most Romantic Experiences in Egypt for Couples',
            'slug': 'romantic-experiences-egypt-couples',
            'excerpt': 'From sunset at the pyramids to private Nile cruises - discover the most romantic things to do in Egypt.',
            'category': 'romance',
            'image_url': 'https://images.unsplash.com/photo-1596627116790-af6f46dddb76?w=1200',
            'content': '''<h2>Romantic Egypt: For Couples in Love</h2>
<p>Egypt isn't just about history - it's one of the most romantic destinations in the world when you know where to look.</p>

<h3>Top 10 Romantic Experiences</h3>

<h4>1. Sunrise at the Pyramids (Private Tour)</h4>
<p>Arrive before the crowds with a private guide. Watch the sun rise over the only remaining Wonder of the Ancient World.</p>

<h4>2. Private Dinner with Pyramid Views</h4>
<p>Several restaurants offer rooftop dining overlooking the illuminated pyramids. Unforgettable!</p>
<p><strong>Try:</strong> 9 Pyramids Lounge or Khufu's Restaurant</p>

<h4>3. Luxury Nile Cruise</h4>
<p>4-7 nights sailing from Luxor to Aswan on a luxury boat. Private deck, gourmet dining, temples at every stop.</p>

<h4>4. Hot Air Balloon Over Luxor</h4>
<p>Float silently over the Valley of the Kings at sunrise. Absolutely magical.</p>

<h4>5. Private Felucca Sunset</h4>
<p>Hire a felucca just for the two of you. Bring wine, watch the sunset, sail around Elephantine Island.</p>

<h4>6. Desert Glamping</h4>
<p>Luxury camps in the White Desert or near Luxor offer stargazing, gourmet dining, and total privacy.</p>

<h4>7. Spa Day at a 5-Star Hotel</h4>
<p>The Four Seasons, Oberoi, and Marriott offer world-class couples treatments.</p>

<h4>8. Snorkeling in Dahab</h4>
<p>The Blue Hole is perfect for adventurous couples. End with sunset dinner on the beach.</p>

<h4>9. Cooking Class</h4>
<p>Learn to make Egyptian cuisine together. Many hotels and independent chefs offer private lessons.</p>

<h4>10. Sound & Light Show</h4>
<p>The Pyramids or Karnak come alive at night. Dramatic and memorable.</p>

<h3>Romantic Hotels</h3>
<ul>
    <li><strong>Cairo:</strong> Marriott Mena House (pyramid view rooms!)</li>
    <li><strong>Luxor:</strong> Sofitel Winter Palace (colonial elegance)</li>
    <li><strong>Aswan:</strong> Sofitel Legend Old Cataract (Agatha Christie stayed here)</li>
    <li><strong>Red Sea:</strong> Oberoi Sahl Hasheesh (pure luxury)</li>
</ul>'''
        },
        # WELLNESS & SPA
        {
            'title': 'Wellness Tourism in Egypt: Spas, Healing, and Relaxation',
            'slug': 'wellness-tourism-egypt-spas-2026',
            'excerpt': 'Discover Egypt\'s best wellness experiences from Siwan salt lakes to luxury Nile spa cruises.',
            'category': 'wellness-spa',
            'image_url': 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=1200',
            'content': '''<h2>Wellness and Healing in Egypt</h2>
<p>Egypt has been a destination for healing since ancient times. Today, it offers unique wellness experiences you won't find anywhere else.</p>

<h3>Natural Healing Experiences</h3>

<h4>Siwa Salt Lakes</h4>
<p>Float in mineral-rich salt lakes with healing properties. Higher mineral content than the Dead Sea!</p>

<h4>Black Sand Therapy, Safaga</h4>
<p>The black sand beaches of Safaga are renowned for treating psoriasis and rheumatism. Many come specifically for "sand baths."</p>

<h4>Hot Springs</h4>
<ul>
    <li><strong>Bir Wahed, Siwa:</strong> Natural hot spring in the desert</li>
    <li><strong>Ain Helwan:</strong> Sulfur springs near Cairo</li>
    <li><strong>Moses' Springs, Sinai:</strong> Biblical waters in an oasis</li>
</ul>

<h3>Luxury Spa Experiences</h3>

<h4>So SPA at Sofitel</h4>
<p>World-class treatments using Egyptian ingredients like lotus and papyrus.</p>

<h4>Four Seasons Spa</h4>
<p>Both Cairo locations offer extensive treatment menus and luxurious settings.</p>

<h4>Oberoi Spa</h4>
<p>The Sahl Hasheesh property has an award-winning spa with Red Sea views.</p>

<h3>Yoga & Meditation Retreats</h3>
<ul>
    <li><strong>Dahab:</strong> Multiple yoga centers with beach views</li>
    <li><strong>Luxor:</strong> Meditation in ancient temples</li>
    <li><strong>Siwa:</strong> Desert yoga retreats</li>
</ul>

<h3>Traditional Egyptian Wellness</h3>

<h4>Hammam (Turkish Bath)</h4>
<p>Traditional steam baths found in many hotels. The Marriott Cairo has a beautiful historic hammam.</p>

<h4>Bakhoor (Incense Therapy)</h4>
<p>Traditional Egyptian aromatherapy using ancient scent recipes.</p>'''
        },
        # SHOPPING
        {
            'title': 'Shopping in Egypt: Where to Buy & How to Bargain',
            'slug': 'shopping-egypt-bargaining-guide-2026',
            'excerpt': 'Master the art of bargaining and discover the best places to buy souvenirs, spices, and treasures.',
            'category': 'shopping',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200',
            'content': '''<h2>The Art of Shopping in Egypt</h2>
<p>Shopping in Egypt is an adventure in itself. Here's how to navigate the markets and get the best deals.</p>

<h3>Where to Shop</h3>

<h4>Khan El-Khalili, Cairo</h4>
<p>The most famous market in the Middle East. Spices, jewelry, antiques, perfumes, and everything in between.</p>

<h4>Luxor Souks</h4>
<p>Less crowded than Khan El-Khalili with good alabaster and papyrus options.</p>

<h4>Aswan Market</h4>
<p>Nubian crafts, spices, and colorful textiles. More relaxed bargaining atmosphere.</p>

<h4>Dahab Shops</h4>
<p>Bedouin jewelry, diving gear, and beach accessories at good prices.</p>

<h3>What to Buy</h3>

<h4>Best Value</h4>
<ul>
    <li>Spices (saffron, hibiscus, cumin)</li>
    <li>Egyptian cotton products</li>
    <li>Perfume oils</li>
    <li>Papyrus paintings (from official stores)</li>
    <li>Hand-blown glass</li>
</ul>

<h4>Worth Splurging</h4>
<ul>
    <li>Gold and silver jewelry (sold by weight)</li>
    <li>Handmade carpets</li>
    <li>Antique artifacts (with certificates)</li>
</ul>

<h3>Bargaining 101</h3>

<ol>
    <li><strong>Never accept the first price</strong> - it's always inflated</li>
    <li><strong>Start at 30-40%</strong> of what they ask</li>
    <li><strong>Walk away</strong> if they don't budge - they often call you back</li>
    <li><strong>Bundle items</strong> for better discounts</li>
    <li><strong>Be friendly</strong> - bargaining should be fun, not hostile</li>
    <li><strong>Know when to stop</strong> - don't haggle for small amounts</li>
</ol>

<h3>Avoid These Scams</h3>
<ul>
    <li>Fake papyrus made from banana leaves (test by folding)</li>
    <li>Fake antiques (if it looks too good to be true...)</li>
    <li>"My father owns this shop" stories</li>
    <li>High-pressure tea/hospitality sales tactics</li>
</ul>

<h3>Fixed Price Options</h3>
<p>If bargaining stresses you out, these stores have fixed prices:</p>
<ul>
    <li>Fair Trade Egypt shops</li>
    <li>Museum gift shops</li>
    <li>Hotel boutiques</li>
    <li>Modern malls (City Stars, Mall of Egypt)</li>
</ul>'''
        },
        # ECO TOURISM
        {
            'title': 'Sustainable Travel in Egypt: Eco-Friendly Tourism Guide',
            'slug': 'sustainable-travel-egypt-eco-tourism',
            'excerpt': 'How to travel Egypt responsibly - supporting local communities and protecting ancient sites and nature.',
            'category': 'eco-tourism',
            'image_url': 'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=1200',
            'content': '''<h2>Traveling Egypt Sustainably</h2>
<p>Egypt's ancient sites and fragile ecosystems need protection. Here's how to travel responsibly while having an amazing experience.</p>

<h3>Eco-Friendly Accommodations</h3>

<h4>Adrère Amellal, Siwa</h4>
<p>No electricity, built from local materials, employs entire village. Pure eco-luxury.</p>

<h4>Basata, Sinai</h4>
<p>Off-grid eco-camp on the beach. Solar power, organic food, community living.</p>

<h4>Fayoum Eco-Lodge</h4>
<p>Mud-brick lodge supporting local farmers and artisans.</p>

<h3>Sustainable Practices</h3>

<h4>Protect the Sites</h4>
<ul>
    <li>Never touch ancient paintings or carvings</li>
    <li>Stay on designated paths</li>
    <li>Don't remove any artifacts or stones</li>
    <li>Report anyone damaging sites</li>
</ul>

<h4>Reduce Plastic</h4>
<ul>
    <li>Bring a reusable water bottle with filter</li>
    <li>Carry a cloth shopping bag</li>
    <li>Say no to plastic straws</li>
    <li>Choose glass-bottled water when possible</li>
</ul>

<h4>Support Local Communities</h4>
<ul>
    <li>Stay in locally-owned guesthouses</li>
    <li>Eat at family restaurants</li>
    <li>Buy from local artisans directly</li>
    <li>Use local guides instead of international chains</li>
</ul>

<h3>Marine Conservation</h3>
<p>The Red Sea's reefs are under threat. Help protect them:</p>
<ul>
    <li>Use reef-safe sunscreen</li>
    <li>Never touch or stand on coral</li>
    <li>Don't feed fish</li>
    <li>Choose responsible dive operators</li>
</ul>

<h3>Carbon Offset</h3>
<p>Offset your flights through programs like:</p>
<ul>
    <li>Gold Standard</li>
    <li>Atmosfair</li>
    <li>myclimate</li>
</ul>'''
        },
        # MORE ARTICLES...
        {
            'title': 'Egyptian Festivals 2026: Complete Calendar & Guide',
            'slug': 'egyptian-festivals-calendar-2026',
            'excerpt': 'From Abu Simbel Sun Festival to Ramadan nights - experience Egypt\'s most vibrant celebrations.',
            'category': 'festivals',
            'image_url': 'https://images.unsplash.com/photo-1531219572328-a0171b4448a3?w=1200',
            'content': '''<h2>Egyptian Festivals & Events 2026</h2>
<p>Egypt's festival calendar is packed with unique events that offer incredible cultural experiences.</p>

<h3>Major Festivals</h3>

<h4>Abu Simbel Sun Festival (Feb 22 & Oct 22)</h4>
<p>Twice a year, sunlight illuminates the inner sanctuary of the temple, hitting three of four statues. Thousands gather to witness this ancient phenomenon.</p>

<h4>Sham El-Nessim (Spring)</h4>
<p>Ancient spring festival dating to Pharaonic times. Egyptians picnic and eat salted fish (fesikh). Falls day after Easter.</p>

<h4>Ramadan (Dates vary)</h4>
<p>The holiest month transforms Egypt. Fasting during the day, feasting at night. Incredible atmosphere in markets and mosques.</p>

<h4>Eid Al-Fitr (End of Ramadan)</h4>
<p>Three days of celebration, family gatherings, and sweets. Many Egyptians travel - expect crowds.</p>

<h4>Moulid An-Nabi (Prophet's Birthday)</h4>
<p>Colorful celebrations with traditional sweets, parades, and street performances.</p>

<h3>Cultural Events</h3>

<h4>Cairo International Film Festival (November)</h4>
<p>The oldest film festival in the Middle East. Red carpet events and international films.</p>

<h4>Downtown Contemporary Arts Festival</h4>
<p>Annual celebration of Cairo's art scene with gallery openings and performances.</p>

<h4>El Gouna Film Festival (October)</h4>
<p>Glamorous event in the Red Sea resort town.</p>

<h3>Planning Tips</h3>
<ul>
    <li>Book accommodation early for major festivals</li>
    <li>Many sites have reduced hours during Ramadan</li>
    <li>Join locals for iftar (breaking fast) during Ramadan</li>
    <li>Expect crowds and traffic during Eid holidays</li>
</ul>'''
        },
        {
            'title': 'Cairo Nightlife Guide 2026: Where to Party & Relax',
            'slug': 'cairo-nightlife-guide-2026',
            'excerpt': 'Discover Cairo after dark - from rooftop bars to underground clubs and everything in between.',
            'category': 'nightlife',
            'image_url': 'https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=1200',
            'content': '''<h2>Cairo After Dark</h2>
<p>Cairo never sleeps! Here's your guide to the city's best nightlife.</p>

<h3>Rooftop Bars</h3>

<h4>Cairo Tower Revolving Restaurant</h4>
<p>360° views of Cairo from the iconic tower. Pricey but unforgettable.</p>

<h4>Le Deck at Sofitel</h4>
<p>Chic rooftop overlooking the Nile. Great cocktails and shisha.</p>

<h4>Sky Pool Bar at Fairmont</h4>
<p>Pool parties and DJs overlooking the Nile. Summer hotspot.</p>

<h3>Clubs & Dancing</h3>

<h4>Cairo Jazz Club</h4>
<p>Live music venue with everything from jazz to indie rock. Institution since 2001.</p>

<h4>Vent</h4>
<p>Underground club for electronic music lovers. Secret entrance adds to the vibe.</p>

<h4>OPIA</h4>
<p>Upscale nightclub in Zamalek. Dress code enforced.</p>

<h3>Chill Spots</h3>

<h4>Crimson Bar & Grill</h4>
<p>Sports bar with good burgers and cold beer. Expat favorite.</p>

<h4>Estoril</h4>
<p>Greek restaurant and bar on a boat. Live music weekends.</p>

<h3>Traditional Entertainment</h3>

<h4>Al-Tannoura Show</h4>
<p>Free whirling dervish performance at Wekalet El Ghouri. Mesmerizing!</p>

<h4>Haramlek</h4>
<p>Traditional Egyptian music venue with authentic oud and tabla performances.</p>

<h3>Know Before You Go</h3>
<ul>
    <li>Nightlife really starts after 11 PM</li>
    <li>Dress code matters at upscale venues</li>
    <li>Alcohol is expensive - expect $6-15 for a beer</li>
    <li>Many clubs have cover charges Thu/Fri</li>
    <li>Ramadan limits nightlife significantly</li>
</ul>'''
        },
        {
            'title': 'Cheap Eats in Cairo: Best Food Under $5',
            'slug': 'cheap-eats-cairo-budget-food-guide',
            'excerpt': 'Delicious Cairo meals that cost less than a coffee at home. Complete budget food guide.',
            'category': 'budget-travel',
            'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200',
            'content': '''<h2>Eating Like a Local in Cairo</h2>
<p>Cairo is one of the cheapest cities in the world to eat well. Here's how to feast on $5/day.</p>

<h3>Best Budget Spots</h3>

<h4>Abou Tarek (Koshari King)</h4>
<p>Three floors of koshari goodness. Large bowl: $1.50. Address: Champollion Street, Downtown</p>

<h4>Gad</h4>
<p>Fast-food chain with Egyptian classics. Shawarma sandwich: $2</p>

<h4>El Shabrawy</h4>
<p>24/7 street food institution. Foul and ta\'meya breakfast: $1.50</p>

<h4>Zooba</h4>
<p>Modern take on Egyptian street food. Slightly pricier but amazing. Meal: $4-6</p>

<h3>Street Food Must-Tries</h3>

<table>
    <tr><th>Food</th><th>Price</th><th>What Is It</th></tr>
    <tr><td>Koshari</td><td>$1-2</td><td>Rice, pasta, lentils, chickpeas, tomato sauce</td></tr>
    <tr><td>Ful sandwich</td><td>$0.50</td><td>Fava beans in bread</td></tr>
    <tr><td>Ta\'meya</td><td>$0.30 each</td><td>Egyptian falafel</td></tr>
    <tr><td>Shawarma</td><td>$1.50-3</td><td>Meat in pita</td></tr>
    <tr><td>Feteer</td><td>$2-4</td><td>Flaky layered pastry</td></tr>
    <tr><td>Hawawshi</td><td>$1.50</td><td>Spiced meat in bread</td></tr>
</table>

<h3>Sweet Treats Under $2</h3>
<ul>
    <li><strong>Kunafa:</strong> Cheese pastry in syrup - $1</li>
    <li><strong>Basbousa:</strong> Semolina cake - $0.50</li>
    <li><strong>Fresh juice:</strong> Mango, strawberry, sugarcane - $1</li>
    <li><strong>Egyptian ice cream:</strong> Stretchy and delicious - $1</li>
</ul>

<h3>Pro Tips</h3>
<ul>
    <li>Eat where locals eat - follow the crowds</li>
    <li>Breakfast ful carts are cheapest before 9 AM</li>
    <li>Juice shops are everywhere and dirt cheap</li>
    <li>Avoid tourist areas for authentic prices</li>
</ul>'''
        },
        {
            'title': 'Learning Arabic in Egypt: Best Courses & Tips',
            'slug': 'learning-arabic-egypt-courses-tips',
            'excerpt': 'Study Arabic in Egypt - from Cairo universities to private tutors. Complete guide for language learners.',
            'category': 'culture',
            'image_url': 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=1200',
            'content': '''<h2>Learning Arabic in Egypt</h2>
<p>Egypt is one of the best places to learn Arabic - you'll be immersed in the language from day one!</p>

<h3>Types of Arabic</h3>
<ul>
    <li><strong>Egyptian Arabic (Masri):</strong> The most widely understood dialect</li>
    <li><strong>Modern Standard Arabic (MSA):</strong> Formal, used in media and writing</li>
    <li><strong>Classical Arabic:</strong> Quranic language, studied for religious purposes</li>
</ul>

<h3>Top Language Schools</h3>

<h4>Kalimat (Cairo)</h4>
<p>Intensive programs in Zamalek. Focus on Egyptian dialect. 4 weeks: ~$600</p>

<h4>ILI (International Language Institute)</h4>
<p>Well-established with flexible schedules. MSA and Egyptian Arabic.</p>

<h4>Arabic Language Institute (AUC)</h4>
<p>University-level programs. Prestigious but expensive.</p>

<h4>Fajr Center (Alexandria)</h4>
<p>Affordable programs with beach lifestyle. Popular with budget learners.</p>

<h3>Private Tutoring</h3>
<p>One-on-one lessons: $5-15/hour depending on teacher experience. Find tutors through:</p>
<ul>
    <li>Facebook expat groups</li>
    <li>italki.com for online/in-person</li>
    <li>University notice boards</li>
    <li>Your accommodation staff</li>
</ul>

<h3>Useful Phrases</h3>
<table>
    <tr><th>English</th><th>Arabic</th><th>Pronunciation</th></tr>
    <tr><td>Hello</td><td>أهلا</td><td>Ahlan</td></tr>
    <tr><td>Thank you</td><td>شكراً</td><td>Shukran</td></tr>
    <tr><td>How much?</td><td>بكام؟</td><td>Bikam?</td></tr>
    <tr><td>No thanks</td><td>لا شكراً</td><td>La shukran</td></tr>
    <tr><td>Beautiful</td><td>جميل</td><td>Gameel</td></tr>
</table>

<h3>Tips for Learning</h3>
<ul>
    <li>Focus on Egyptian dialect first - it's more practical</li>
    <li>Watch Egyptian movies and TV shows</li>
    <li>Practice with taxi drivers and shopkeepers</li>
    <li>Download the "Mondly" or "Duolingo" apps</li>
    <li>Don't be afraid to make mistakes!</li>
</ul>'''
        },
        {
            'title': 'Egypt Visa Guide 2026: Complete Requirements & Tips',
            'slug': 'egypt-visa-guide-requirements-2026',
            'excerpt': 'Everything you need to know about Egyptian visas - types, costs, e-visa process, and entry requirements.',
            'category': 'practical-tips',
            'image_url': 'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=1200',
            'content': '''<h2>Egypt Visa Requirements 2026</h2>
<p>Getting into Egypt is easier than you think. Here's everything you need to know.</p>

<h3>Visa Options</h3>

<h4>1. Visa on Arrival</h4>
<p>Available for 50+ nationalities including US, UK, EU, Australia.</p>
<ul>
    <li><strong>Cost:</strong> $25 USD (cash only)</li>
    <li><strong>Validity:</strong> 30 days, single entry</li>
    <li><strong>Process:</strong> Buy sticker at airport bank window before immigration</li>
</ul>

<h4>2. E-Visa (Recommended)</h4>
<p>Apply online at visa2egypt.gov.eg before travel.</p>
<ul>
    <li><strong>Cost:</strong> $25 (single) or $60 (multiple entry)</li>
    <li><strong>Processing:</strong> 5-7 business days</li>
    <li><strong>Validity:</strong> 30 or 90 days</li>
    <li><strong>Advantages:</strong> Skip airport queues, peace of mind</li>
</ul>

<h4>3. Sinai Permit (Free!)</h4>
<p>If ONLY visiting Sinai (Sharm, Dahab, Taba), you can get a free 14-day permit.</p>
<ul>
    <li>Entry only at Sharm El Sheikh, Taba, or St. Catherine airports</li>
    <li>Cannot leave Sinai Peninsula</li>
</ul>

<h3>Entry Requirements</h3>
<ul>
    <li>Passport valid for 6+ months beyond travel dates</li>
    <li>At least one blank page</li>
    <li>Return or onward ticket</li>
    <li>Proof of accommodation (may be asked)</li>
</ul>

<h3>COVID-19 Rules (As of 2026)</h3>
<p>Currently no COVID restrictions. Check gov.uk or travel.state.gov for updates before travel.</p>

<h3>Visa Extension</h3>
<p>Extend your visa at the Mogamma building in Tahrir Square, Cairo. Process takes 1-3 days. Cost: ~$15.</p>

<h3>Common Issues</h3>
<ul>
    <li><strong>Israeli stamps:</strong> Not a problem - Egypt has peace treaty with Israel</li>
    <li><strong>Lost passport:</strong> Contact your embassy immediately</li>
    <li><strong>Overstay:</strong> Pay fine at airport (~$22/month overstayed)</li>
</ul>'''
        },
        {
            'title': 'Egyptian Wedding Traditions: A Cultural Guide',
            'slug': 'egyptian-wedding-traditions-cultural-guide',
            'excerpt': 'Discover the colorful traditions of Egyptian weddings - from henna nights to zaffa processions.',
            'category': 'culture',
            'image_url': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200',
            'content': '''<h2>Egyptian Wedding Traditions</h2>
<p>Egyptian weddings are legendary celebrations that can last for days. Here's what makes them special.</p>

<h3>Pre-Wedding Traditions</h3>

<h4>Shabka (Engagement)</h4>
<p>The groom presents gold jewelry to the bride. The amount depends on family wealth and tradition. This is legally binding!</p>

<h4>Henna Night (Laylat Al-Henna)</h4>
<p>Women gather the night before to decorate the bride with henna. Music, dancing, and sweets.</p>

<h4>Kosha Preparation</h4>
<p>The wedding "throne" where the couple sits is elaborately decorated with flowers and fabric.</p>

<h3>Wedding Day</h3>

<h4>The Zaffa</h4>
<p>A musical procession leads the groom to his bride. Features belly dancers, drums, and flaming props. Incredibly loud and joyful!</p>

<h4>The Ceremony</h4>
<ul>
    <li>Muslim weddings: Simple contract signing with Imam</li>
    <li>Christian weddings: Church ceremony (Coptic weddings are elaborate)</li>
</ul>

<h4>The Reception</h4>
<p>Parties often don't start until 10 PM and go until dawn. Features:</p>
<ul>
    <li>Live band or DJ</li>
    <li>Belly dancer performance</li>
    <li>Egyptian pop music and dancing</li>
    <li>Elaborate cake</li>
    <li>Huge feasts</li>
</ul>

<h3>If You're Invited</h3>
<ul>
    <li>Dress formally - suits and glamorous dresses</li>
    <li>Gift money in an envelope is common</li>
    <li>Expect to dance!</li>
    <li>The party will run LATE - pace yourself</li>
</ul>

<h3>Planning a Wedding in Egypt</h3>
<p>Egypt is popular for destination weddings. Options include:</p>
<ul>
    <li>5-star hotel venues (Mena House with pyramid views!)</li>
    <li>Nile cruise weddings</li>
    <li>Red Sea beach ceremonies</li>
    <li>Historic palace venues</li>
</ul>'''
        },
    ]

    # Create articles
    for article in articles:
        if not BlogPost.objects.filter(slug=article['slug']).exists():
            cat = cats.get(article['category'], cats['hidden-gems'])
            BlogPost.objects.create(
                title=article['title'],
                slug=article['slug'],
                excerpt=article['excerpt'],
                content=article['content'],
                image_url=article['image_url'],
                author=author,
                category=cat,
                is_featured=False,
                status='published',
                published_at=timezone.now()
            )
            created += 1

    return JsonResponse({
        'success': True,
        'created': created,
        'total_articles': BlogPost.objects.count(),
        'categories_created': len(categories_data)
    })


urlpatterns = [
    # Public endpoints
    path('favicon.svg', favicon, name='favicon'),
    path('favicon.ico', favicon, name='favicon_ico'),
    path('feed/', rss_feed, name='rss_feed'),
    path('rss/', rss_feed, name='rss'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', health_check, name='health'),

    # Admin-only seed/debug endpoints (require staff login)
    path('seed-all-topics/', staff_member_required(seed_comprehensive_articles), name='seed_all_topics'),
    path('update-images/', staff_member_required(update_article_images), name='update_images'),
    path('seed-trending/', staff_member_required(seed_trending_2026), name='seed_trending'),
    path('update-content/', staff_member_required(update_articles_content), name='update_content'),
    path('seed-more/', staff_member_required(seed_more_articles), name='seed_more'),
    path('setup-all/', staff_member_required(setup_all), name='setup_all'),
    path('expand-articles/', staff_member_required(expand_all_articles), name='expand_articles'),
    path('debug-db/', staff_member_required(debug_db), name='debug_db'),
    path('seed/', staff_member_required(seed_articles), name='seed'),
    path('seed2026/', staff_member_required(seed_2026_articles), name='seed2026'),
    path('seed-egypt/', staff_member_required(seed_egypt_history_articles), name='seed_egypt'),
    path('seed-luxury/', staff_member_required(seed_luxury_articles), name='seed_luxury'),
    path('seed-stories/', staff_member_required(seed_true_stories), name='seed_stories'),
    path('organize/', staff_member_required(organize_all_articles), name='organize'),
    path('debug/', staff_member_required(debug_check), name='debug'),
    path('blog-diagnose/', staff_member_required(blog_diagnose), name='blog_diagnose'),
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
    path('api/social/', include('social_poster.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
