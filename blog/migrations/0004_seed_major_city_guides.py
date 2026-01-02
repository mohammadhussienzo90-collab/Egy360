# Generated migration to seed major city guide blog posts
from django.db import migrations
from django.utils import timezone


def create_major_city_guides(apps, schema_editor):
    """Create Cairo, Luxor, Hurghada, Aswan blog posts."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    BlogCategory = apps.get_model('blog', 'BlogCategory')
    User = apps.get_model('auth', 'User')

    category, _ = BlogCategory.objects.get_or_create(
        slug='travel-guides',
        defaults={'name': 'Travel Guides', 'description': 'Comprehensive travel guides'}
    )

    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    if not author:
        return

    now = timezone.now()

    posts_data = [
        {
            'title': 'Cairo Travel Guide: Pyramids, Museums and the Heart of Egypt',
            'slug': 'cairo-travel-guide-pyramids-museums',
            'excerpt': 'Explore Cairo, the sprawling capital of Egypt where ancient wonders meet modern chaos. From the iconic Pyramids of Giza to the treasures of the Egyptian Museum.',
            'meta_description': 'Complete Cairo travel guide covering the Pyramids of Giza, Egyptian Museum, Khan el-Khalili, best areas to stay, and insider tips.',
            'meta_keywords': 'cairo egypt, cairo travel guide, pyramids of giza, egyptian museum, khan el khalili',
            'tags': 'cairo, pyramids, giza, egyptian museum, egypt capital',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
        },
        {
            'title': 'Luxor Travel Guide: The World\'s Greatest Open-Air Museum',
            'slug': 'luxor-travel-guide-temples-tombs',
            'excerpt': 'Discover Luxor, ancient Thebes, where more monuments survive than anywhere else on Earth. From the Valley of the Kings to Karnak Temple.',
            'meta_description': 'Complete Luxor travel guide covering Valley of the Kings, Karnak Temple, best tours, and Nile cruises.',
            'meta_keywords': 'luxor egypt, luxor travel guide, valley of the kings, karnak temple, luxor temple',
            'tags': 'luxor, valley of the kings, karnak, temples, ancient egypt',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',
        },
        {
            'title': 'Hurghada Travel Guide: Red Sea Beaches, Diving and Desert Adventures',
            'slug': 'hurghada-travel-guide-beaches-diving',
            'excerpt': 'Explore Hurghada, Egypt\'s original Red Sea resort destination. From world-class diving and pristine beaches to desert safaris and vibrant nightlife.',
            'meta_description': 'Complete Hurghada travel guide covering best beaches, diving sites, resorts, desert trips, and nightlife.',
            'meta_keywords': 'hurghada egypt, hurghada travel guide, hurghada diving, hurghada resorts, red sea',
            'tags': 'hurghada, red sea, diving, beach, resort, desert safari',
            'image_url': 'https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=1200&q=80',
        },
        {
            'title': 'Aswan Travel Guide: Nubian Culture, Nile Beauty and Ancient Temples',
            'slug': 'aswan-travel-guide-nubia-temples',
            'excerpt': 'Discover Aswan, Egypt\'s most relaxed and beautiful city where Nubian culture meets ancient temples. From sailing feluccas at sunset to the mighty Abu Simbel.',
            'meta_description': 'Complete Aswan travel guide covering Philae Temple, Abu Simbel, Nubian villages, and felucca sailing.',
            'meta_keywords': 'aswan egypt, aswan travel guide, abu simbel, philae temple, nubian village',
            'tags': 'aswan, abu simbel, philae, nubia, nile, felucca',
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0a9e9ef5e9b?w=1200&q=80',
        },
    ]

    for post_data in posts_data:
        BlogPost.objects.update_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'author': author,
                'category': category,
                'excerpt': post_data['excerpt'],
                'content': f'<p class="lead">{post_data["excerpt"]}</p><p>Full guide with attractions, best time to visit, activities, and practical tips. Visit the site to read the complete article.</p>',
                'tags': post_data['tags'],
                'image_url': post_data['image_url'],
                'meta_description': post_data['meta_description'],
                'meta_keywords': post_data['meta_keywords'],
                'status': 'published',
                'is_featured': True,
                'published_at': now,
            }
        )


def reverse_major_city_guides(apps, schema_editor):
    """Remove the seeded blog posts."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    slugs = [
        'cairo-travel-guide-pyramids-museums',
        'luxor-travel-guide-temples-tombs',
        'hurghada-travel-guide-beaches-diving',
        'aswan-travel-guide-nubia-temples',
    ]
    BlogPost.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_clean_blog_content_data'),
    ]

    operations = [
        migrations.RunPython(create_major_city_guides, reverse_major_city_guides),
    ]
