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
    return JsonResponse({'status': 'ok', 'version': 'v7-hotels-search', 'branch': 'main'})

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
    """Simple debug endpoint"""
    return JsonResponse({'status': 'ok', 'version': 'v9-egypt-articles', 'branch': 'main', 'features': ['hotels-search', 'privacy', 'terms', 'paymob-ready', 'egypt-history-articles']})

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

urlpatterns = [
    path('favicon.svg', favicon, name='favicon'),
    path('favicon.ico', favicon, name='favicon_ico'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('health/', health_check, name='health'),
    path('seed/', seed_articles, name='seed'),
    path('seed2026/', seed_2026_articles, name='seed2026'),
    path('seed-egypt/', seed_egypt_history_articles, name='seed_egypt'),
    path('debug/', debug_check, name='debug'),
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
