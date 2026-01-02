# Generated migration to seed city guide blog posts
from django.db import migrations
from django.utils import timezone


def create_city_guides(apps, schema_editor):
    """Create the 6 city guide blog posts."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    BlogCategory = apps.get_model('blog', 'BlogCategory')
    User = apps.get_model('auth', 'User')

    # Get or create category
    category, _ = BlogCategory.objects.get_or_create(
        slug='travel-guides',
        defaults={'name': 'Travel Guides', 'description': 'Comprehensive travel guides'}
    )

    # Get admin user
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    if not author:
        return  # No users, skip

    now = timezone.now()

    # Blog post data with unique relevant images for each city
    posts_data = [
        {
            'title': 'Dahab Travel Guide: Top Attractions, Best Time to Visit and Things to Do',
            'slug': 'dahab-travel-guide-attractions-activities',
            'excerpt': 'Discover Dahab, Egypt\'s laid-back Red Sea paradise. From world-class diving at the Blue Hole to desert adventures and beachfront relaxation.',
            'meta_description': 'Complete Dahab travel guide covering top attractions, best time to visit, diving spots, activities and travel tips.',
            'meta_keywords': 'dahab egypt, dahab travel guide, blue hole dahab, dahab diving',
            'tags': 'dahab, red sea, diving, sinai, beach',
            'image_url': 'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=1200&q=80',  # Underwater diving coral reef
        },
        {
            'title': 'Marsa Alam Travel Guide: Pristine Reefs, Dolphins and Desert Beauty',
            'slug': 'marsa-alam-travel-guide-diving-beaches',
            'excerpt': 'Explore Marsa Alam, Egypt\'s unspoiled Red Sea gem. Home to dugongs, dolphins and pristine coral reefs.',
            'meta_description': 'Complete Marsa Alam travel guide with top dive sites, dolphin encounters and beach activities.',
            'meta_keywords': 'marsa alam egypt, marsa alam diving, marsa alam dolphins',
            'tags': 'marsa alam, red sea, diving, dolphins, beach',
            'image_url': 'https://images.unsplash.com/photo-1607153333879-c174d265f1d2?w=1200&q=80',  # Dolphins swimming
        },
        {
            'title': 'Marsa Matrouh Travel Guide: Egypt\'s Mediterranean Paradise',
            'slug': 'marsa-matrouh-travel-guide-mediterranean-beaches',
            'excerpt': 'Discover Marsa Matrouh, home to Egypt\'s most beautiful Mediterranean beaches with crystal-clear turquoise waters.',
            'meta_description': 'Complete Marsa Matrouh guide covering the best beaches, attractions and travel tips.',
            'meta_keywords': 'marsa matrouh egypt, marsa matrouh beaches, agiba beach',
            'tags': 'marsa matrouh, mediterranean, beach, north coast',
            'image_url': 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1200&q=80',  # Turquoise Mediterranean beach
        },
        {
            'title': 'Siwa Oasis Travel Guide: Egypt\'s Desert Paradise',
            'slug': 'siwa-oasis-travel-guide-desert-paradise',
            'excerpt': 'Explore Siwa Oasis, Egypt\'s most remote and magical destination with ancient ruins, natural springs and endless sand dunes.',
            'meta_description': 'Complete Siwa Oasis travel guide covering top attractions, desert safaris and hot springs.',
            'meta_keywords': 'siwa oasis egypt, siwa travel guide, siwa desert safari',
            'tags': 'siwa, oasis, desert, sahara, adventure',
            'image_url': 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80',  # Desert oasis with palm trees
        },
        {
            'title': 'Saint Catherine Travel Guide: Mount Sinai, Monastery and Sinai Highlands',
            'slug': 'saint-catherine-mount-sinai-travel-guide',
            'excerpt': 'Discover Saint Catherine, home to Egypt\'s highest mountains and the ancient monastery at Mount Sinai.',
            'meta_description': 'Complete Saint Catherine travel guide covering Mount Sinai sunrise trek and the ancient monastery.',
            'meta_keywords': 'saint catherine egypt, mount sinai, sinai monastery',
            'tags': 'saint catherine, mount sinai, monastery, hiking',
            'image_url': 'https://images.unsplash.com/photo-1548786811-dd6e453ccca7?w=1200&q=80',  # Mountain sunrise
        },
        {
            'title': 'El Gouna Travel Guide: Egypt\'s Luxury Red Sea Resort Town',
            'slug': 'el-gouna-travel-guide-luxury-resort',
            'excerpt': 'Discover El Gouna, Egypt\'s most stylish Red Sea destination with beautiful lagoons and excellent dining.',
            'meta_description': 'Complete El Gouna travel guide covering beaches, water sports, dining and nightlife.',
            'meta_keywords': 'el gouna egypt, el gouna resort, el gouna hotels',
            'tags': 'el gouna, red sea, luxury resort, beach',
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80',  # Luxury resort pool
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
                'content': f'<p class="lead">{post_data["excerpt"]}</p><p>Full content available. Visit the site to read more.</p>',
                'tags': post_data['tags'],
                'image_url': post_data['image_url'],
                'meta_description': post_data['meta_description'],
                'meta_keywords': post_data['meta_keywords'],
                'status': 'published',
                'is_featured': False,
                'published_at': now,
            }
        )


def reverse_city_guides(apps, schema_editor):
    """Remove the seeded blog posts."""
    BlogPost = apps.get_model('blog', 'BlogPost')
    slugs = [
        'dahab-travel-guide-attractions-activities',
        'marsa-alam-travel-guide-diving-beaches',
        'marsa-matrouh-travel-guide-mediterranean-beaches',
        'siwa-oasis-travel-guide-desert-paradise',
        'saint-catherine-mount-sinai-travel-guide',
        'el-gouna-travel-guide-luxury-resort',
    ]
    BlogPost.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_seed_major_city_guides'),
    ]

    operations = [
        migrations.RunPython(create_city_guides, reverse_city_guides),
    ]
