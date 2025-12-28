"""
Sitemap configuration for Egy360
Generates XML sitemaps for SEO optimization

Includes:
- Static pages (home, about, contact, FAQ)
- Accommodations (hotels, resorts, etc.)
- Tours (day trips, multi-day tours)
- Blog posts (travel guides, tips)
- Destinations (cities, attractions)
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from accommodations.models import Accommodation
from tours.models import Tour
from blog.models import BlogPost
from destinations.models import City, Attraction


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home:home', 'home:about', 'home:contact', 'home:faq']

    def location(self, item):
        return reverse(item)


class AccommodationSitemap(Sitemap):
    """Sitemap for accommodation listings"""
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Accommodation.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('accommodations:detail', kwargs={'slug': obj.slug})


class TourSitemap(Sitemap):
    """Sitemap for tour listings"""
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Tour.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('tours:detail', kwargs={'slug': obj.slug})


class BlogSitemap(Sitemap):
    """Sitemap for blog posts - critical for SEO content strategy"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(status='published').order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.published_at

    def location(self, obj):
        return reverse('blog:detail', kwargs={'slug': obj.slug})


class CitySitemap(Sitemap):
    """Sitemap for destination cities (Cairo, Luxor, Aswan, etc.)"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return City.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', None)

    def location(self, obj):
        return reverse('destinations:city_detail', kwargs={'slug': obj.slug})


class AttractionSitemap(Sitemap):
    """Sitemap for attractions (Pyramids, Karnak Temple, etc.)"""
    changefreq = 'weekly'
    priority = 0.85

    def items(self):
        return Attraction.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', None)

    def location(self, obj):
        return reverse('destinations:attraction_detail', kwargs={'slug': obj.slug})


# Dictionary of all sitemaps for use in urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'accommodations': AccommodationSitemap,
    'tours': TourSitemap,
    'blog': BlogSitemap,
    'cities': CitySitemap,
    'attractions': AttractionSitemap,
}
