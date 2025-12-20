"""
Sitemap configuration for Egy360
Generates XML sitemaps for SEO optimization
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from accommodations.models import Accommodation
from tours.models import Tour
from blog.models import BlogPost
from destinations.models import City


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['homepage', 'home:about', 'home:contact', 'home:faq']

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
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:detail', kwargs={'slug': obj.slug})


class CitySitemap(Sitemap):
    """Sitemap for destination cities"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return City.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        return reverse('destinations:city-detail', kwargs={'slug': obj.slug})


# Dictionary of all sitemaps for use in urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'accommodations': AccommodationSitemap,
    'tours': TourSitemap,
    'blog': BlogSitemap,
    'cities': CitySitemap,
}
