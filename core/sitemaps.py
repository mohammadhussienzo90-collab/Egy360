"""
Sitemap configuration for Egy360
Generates XML sitemaps for SEO optimization
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from accommodations.models import Accommodation
from tours.models import Tour


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


# Dictionary of all sitemaps for use in urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'accommodations': AccommodationSitemap,
    'tours': TourSitemap,
}
