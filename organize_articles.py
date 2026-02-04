"""
Organize all articles into proper categories
Make the website professional and well-organized
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from blog.models import BlogPost, BlogCategory

# Create categories
CATEGORIES = [
    {
        'name': 'True Stories',
        'slug': 'true-stories',
        'description': 'Captivating true stories from Egypt\'s dramatic history - warfare, mystery, intrigue'
    },
    {
        'name': 'Ancient Egypt',
        'slug': 'ancient-egypt',
        'description': 'Deep dives into ancient Egyptian civilization, pharaohs, and monuments'
    },
    {
        'name': 'City Guides',
        'slug': 'city-guides',
        'description': 'Complete travel guides to Egyptian cities and destinations'
    },
    {
        'name': 'Luxury Travel',
        'slug': 'luxury-travel',
        'description': 'Premium hotels, cruises, and VIP experiences in Egypt'
    },
    {
        'name': 'Travel Planning',
        'slug': 'travel-planning',
        'description': 'Practical guides for planning your Egypt trip - visas, costs, safety'
    },
    {
        'name': 'Culture & Food',
        'slug': 'culture-food',
        'description': 'Egyptian culture, customs, cuisine, and modern life'
    },
    {
        'name': 'Adventures',
        'slug': 'adventures',
        'description': 'Desert safaris, diving, photography, and outdoor activities'
    },
]

# Article categorization
ARTICLE_CATEGORIES = {
    'true-stories': [
        'battle-of-kadesh-egypt-hittites-ramses',
        'curse-of-the-pharaohs-tutankhamun-deaths',
        'cleopatra-death-last-pharaoh-true-story',
        'lost-army-cambyses-desert-mystery',
        'murder-ramses-iii-harem-conspiracy',
        'moving-abu-simbel-engineering-marvel',
        'exodus-moses-red-sea-historical-evidence',
        'hatshepsut-female-king-erased-history',
        'bent-pyramid-dahshur-engineering-failure',
        'rosetta-stone-deciphering-hieroglyphics',
        'sea-peoples-bronze-age-collapse-mystery',
    ],
    'ancient-egypt': [
        'great-pyramid-giza-introduction',
        'great-pyramid-construction-methods',
        'great-pyramid-purpose-meaning',
        'great-pyramid-myths-debunked',
        'great-pyramid-kings-chamber-secrets',
        'great-pyramid-architecture-precision',
        'great-pyramid-transporting-stones',
        'great-pyramid-stone-cutting',
        'great-pyramid-history-timeline-workers',
        'king-tutankhamun-boy-king-guide',
        'ramses-ii-greatest-pharaoh',
        'cleopatra-last-pharaoh-egypt',
        'queen-hatshepsut-female-pharaoh',
        'ancient-egyptian-mummies-guide',
        'valley-of-the-kings-complete-guide',
        'karnak-temple-complete-guide',
        'abu-simbel-temples-guide',
        'ancient-egyptian-gods-mythology',
        'egyptian-hieroglyphics-explained',
        'daily-life-ancient-egypt',
    ],
    'city-guides': [
        'cairo-travel-guide-pyramids-museums',
        'luxor-travel-guide-temples-tombs',
        'aswan-travel-guide-nubia-temples',
        'hurghada-travel-guide-beaches-diving',
        'dahab-travel-guide-attractions-activities',
        'marsa-alam-travel-guide-diving-beaches',
        'siwa-oasis-travel-guide-desert-paradise',
        'el-gouna-travel-guide-luxury-resort',
        'saint-catherine-mount-sinai-travel-guide',
        'marsa-matrouh-travel-guide-mediterranean-beaches',
        'alexandria-travel-guide-2026',
    ],
    'luxury-travel': [
        'best-5-star-hotels-egypt-2026',
        'luxury-nile-cruises-2026-complete-guide',
        'private-egypt-tours-vip-experiences-2026',
        'egypt-honeymoon-guide-2026-romantic-luxury',
        'grand-egyptian-museum-2026-vip-luxury-guide',
        'egypt-honeymoon-guide',
        'nile-cruise-guide-2026',
    ],
    'travel-planning': [
        'best-egypt-tours-2026',
        'egypt-travel-cost-2026-budget',
        'is-egypt-safe-2026',
        'best-time-to-visit-egypt',
        'egypt-visa-requirements-2026',
        'cairo-airport-guide-2026',
        'egypt-packing-list-2026',
        '7-day-egypt-itinerary',
        'solo-travel-egypt-guide',
        'egypt-with-kids-family-guide',
    ],
    'culture-food': [
        'egyptian-food-guide',
        'egyptian-culture-customs-guide',
        'modern-cairo-beyond-pyramids',
        'nubian-culture-egypt-guide',
        'ramadan-egypt-visitor-guide',
        'grand-egyptian-museum-guide-2026',
        'egyptian-souvenirs-shopping-guide',
    ],
    'adventures': [
        'red-sea-diving-guide',
        'egypt-desert-safari-guide',
        'luxor-aswan-felucca-sailing',
        'egypt-photography-guide',
    ],
}

# Featured articles (will be marked as is_featured)
FEATURED_SLUGS = [
    'curse-of-the-pharaohs-tutankhamun-deaths',
    'cleopatra-death-last-pharaoh-true-story',
    'battle-of-kadesh-egypt-hittites-ramses',
    'lost-army-cambyses-desert-mystery',
    'best-5-star-hotels-egypt-2026',
    'luxury-nile-cruises-2026-complete-guide',
]

def organize_articles():
    print("\n" + "="*60)
    print("  ORGANIZING EGY360 ARTICLES")
    print("  Creating categories and assigning articles")
    print("="*60 + "\n")

    # Create categories
    print("Creating categories...")
    categories_created = 0
    for cat_data in CATEGORIES:
        cat, created = BlogCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        if created:
            categories_created += 1
            print(f"  CREATED: {cat_data['name']}")
        else:
            print(f"  EXISTS:  {cat_data['name']}")

    print(f"\nCategories: {categories_created} created, {len(CATEGORIES)} total\n")

    # Assign articles to categories
    print("Assigning articles to categories...")
    assigned = 0
    for cat_slug, article_slugs in ARTICLE_CATEGORIES.items():
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
            for article_slug in article_slugs:
                try:
                    article = BlogPost.objects.get(slug=article_slug)
                    if article.category != category:
                        article.category = category
                        article.save()
                        assigned += 1
                        print(f"  [{category.name}] {article.title[:40]}...")
                except BlogPost.DoesNotExist:
                    pass  # Article not found, skip
        except BlogCategory.DoesNotExist:
            print(f"  WARNING: Category {cat_slug} not found")

    print(f"\nAssigned {assigned} articles to categories\n")

    # Mark featured articles
    print("Marking featured articles...")
    featured_count = 0
    # First, unmark all
    BlogPost.objects.all().update(is_featured=False)

    for slug in FEATURED_SLUGS:
        try:
            article = BlogPost.objects.get(slug=slug)
            article.is_featured = True
            article.save()
            featured_count += 1
            print(f"  FEATURED: {article.title[:50]}...")
        except BlogPost.DoesNotExist:
            pass

    print(f"\n{featured_count} articles marked as featured")

    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    total = BlogPost.objects.count()
    categorized = BlogPost.objects.exclude(category__isnull=True).count()
    featured = BlogPost.objects.filter(is_featured=True).count()

    print(f"\n  Total articles:      {total}")
    print(f"  With categories:     {categorized}")
    print(f"  Featured articles:   {featured}")
    print(f"  Categories:          {BlogCategory.objects.count()}")

    # Articles per category
    print("\n  Articles by category:")
    for cat in BlogCategory.objects.all():
        count = BlogPost.objects.filter(category=cat).count()
        print(f"    {cat.name}: {count}")

    uncategorized = BlogPost.objects.filter(category__isnull=True).count()
    if uncategorized > 0:
        print(f"    (Uncategorized): {uncategorized}")

    print("\n" + "="*60)
    print("  Articles organized successfully!")
    print("="*60 + "\n")

if __name__ == '__main__':
    organize_articles()
