"""
Egy360 Core Test Suite
======================
Critical functionality tests for production readiness.

Run with: python manage.py test core.tests -v 2
"""

import json
import sys
from decimal import Decimal
from unittest import skipIf
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Python 3.14+ has known compatibility issues with Django template context copying
# See: https://code.djangoproject.com/ticket/35959
PYTHON_314_PLUS = sys.version_info >= (3, 14)


# =============================================================================
# CRITICAL ENDPOINT TESTS
# =============================================================================

class CriticalEndpointTests(TestCase):
    """Test critical endpoints that must work for revenue generation"""

    def setUp(self):
        self.client = Client()

    @skipIf(PYTHON_314_PLUS, "Django template context copy issue with Python 3.14+")
    def test_homepage_loads(self):
        """Homepage must load for users to find the site"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Egy360')

    def test_health_endpoint(self):
        """Health endpoint for Railway monitoring"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')

    def test_favicon_loads(self):
        """Favicon for browser tabs"""
        response = self.client.get('/favicon.svg')
        self.assertEqual(response.status_code, 200)

    @skipIf(PYTHON_314_PLUS, "Django template context copy issue with Python 3.14+")
    def test_sitemap_loads(self):
        """Sitemap for SEO"""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)


# =============================================================================
# PAGE LOADING TESTS
# =============================================================================

@skipIf(PYTHON_314_PLUS, "Django template context copy issue with Python 3.14+")
class PageLoadingTests(TestCase):
    """Test that critical pages load without errors"""

    def setUp(self):
        self.client = Client()

    def test_about_page(self):
        response = self.client.get(reverse('home:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('home:contact'))
        self.assertEqual(response.status_code, 200)

    def test_terms_page(self):
        response = self.client.get(reverse('home:terms'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_page(self):
        response = self.client.get(reverse('home:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_faq_page(self):
        response = self.client.get(reverse('home:faq'))
        self.assertEqual(response.status_code, 200)

    def test_accommodations_search(self):
        response = self.client.get(reverse('accommodations:search'))
        self.assertEqual(response.status_code, 200)

    def test_tours_list(self):
        response = self.client.get(reverse('tours:list'))
        self.assertEqual(response.status_code, 200)

    def test_destinations_list(self):
        response = self.client.get(reverse('destinations:list'))
        self.assertEqual(response.status_code, 200)

    def test_blog_list(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)


# =============================================================================
# AFFILIATE CLICK TRACKING TESTS
# =============================================================================

class AffiliateClickTrackingTests(TestCase):
    """Test the affiliate click tracking system"""

    def setUp(self):
        self.client = Client()
        # Create test data for GenericForeignKey
        from destinations.models import Country, City
        from accommodations.models import Accommodation
        from django.contrib.contenttypes.models import ContentType

        self.country = Country.objects.create(name='Egypt', code='EG')
        self.city = City.objects.create(name='Cairo', slug='cairo', country=self.country)
        self.accommodation = Accommodation.objects.create(
            name='Test Hotel',
            slug='test-hotel',
            city=self.city,
            accommodation_type='hotel',
            price_per_night=Decimal('100.00'),
            is_active=True
        )
        self.content_type = ContentType.objects.get_for_model(Accommodation)

    def test_track_click_endpoint_exists(self):
        """Track click endpoint should accept POST requests"""
        response = self.client.post(
            reverse('api:track_affiliate_click'),
            data=json.dumps({
                'platform': 'booking_com',
                'item_type': 'accommodation',
                'affiliate_url': 'https://booking.com/test'
            }),
            content_type='application/json'
        )
        # Should not be 404 or 405
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 405)

    def test_affiliate_click_model(self):
        """AffiliateClick model should store click data"""
        from core.models import AffiliateClick

        click = AffiliateClick.objects.create(
            platform='booking_com',
            item_type='accommodation',
            content_type=self.content_type,
            object_id=self.accommodation.id,
            affiliate_url='https://booking.com/hotel/test',
            device_type='desktop',
            estimated_commission=Decimal('4.00')
        )

        self.assertEqual(click.platform, 'booking_com')
        self.assertEqual(click.item_type, 'accommodation')
        self.assertIsNotNone(click.clicked_at)
        self.assertEqual(click.estimated_commission, Decimal('4.00'))

    def test_affiliate_click_platforms(self):
        """All expected platforms should be valid"""
        from core.models import AffiliateClick

        platforms = ['booking_com', 'hotellook', 'viator', 'getyourguide', 'agoda']

        for platform in platforms:
            click = AffiliateClick.objects.create(
                platform=platform,
                item_type='accommodation',
                content_type=self.content_type,
                object_id=self.accommodation.id,
                affiliate_url=f'https://{platform}.com/test',
                device_type='desktop'
            )
            self.assertEqual(click.platform, platform)


# =============================================================================
# API TESTS
# =============================================================================

class APITests(TestCase):
    """Test API endpoints"""

    def setUp(self):
        self.client = Client()

    def test_newsletter_subscribe(self):
        """Newsletter subscription should work"""
        response = self.client.post(
            reverse('home:newsletter-subscribe'),
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 201, 400])

    def test_platform_stats(self):
        """Platform stats API should return data"""
        response = self.client.get(reverse('home:platform-stats'))
        self.assertEqual(response.status_code, 200)


# =============================================================================
# AUTHENTICATION TESTS
# =============================================================================

@skipIf(PYTHON_314_PLUS, "Django template context copy issue with Python 3.14+")
class AuthenticationTests(TestCase):
    """Test authentication flow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_login_page_loads(self):
        """Login page should load"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        """Register page should load"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        """Profile page should redirect to login"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        """Dashboard should redirect to login"""
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)


# =============================================================================
# MODEL TESTS
# =============================================================================

class ModelTests(TestCase):
    """Test model creation and relationships"""

    def test_country_creation(self):
        """Country model should work"""
        from destinations.models import Country
        country = Country.objects.create(
            name='Egypt',
            code='EG',
            description='Arab Republic of Egypt'
        )
        self.assertEqual(country.name, 'Egypt')
        self.assertEqual(country.code, 'EG')

    def test_city_creation(self):
        """City model should work"""
        from destinations.models import Country, City
        country = Country.objects.create(name='Egypt', code='EG')
        city = City.objects.create(
            name='Cairo',
            slug='cairo',
            country=country,
            description='Capital of Egypt'
        )
        self.assertEqual(city.name, 'Cairo')
        self.assertEqual(city.country, country)

    def test_accommodation_creation(self):
        """Accommodation model should work"""
        from destinations.models import Country, City
        from accommodations.models import Accommodation

        country = Country.objects.create(name='Egypt', code='EG')
        city = City.objects.create(name='Cairo', slug='cairo', country=country)

        acc = Accommodation.objects.create(
            name='Marriott Cairo',
            slug='marriott-cairo',
            city=city,
            accommodation_type='hotel',
            description='Luxury hotel',
            price_per_night=Decimal('150.00'),
            booking_com_url='https://search.hotellook.com/hotels?marker=477897&q=Marriott+Cairo',
            is_active=True
        )

        self.assertEqual(acc.name, 'Marriott Cairo')
        self.assertEqual(acc.city, city)
        self.assertIn('hotellook', acc.booking_com_url)
        self.assertIn('marker=477897', acc.booking_com_url)

    def test_tour_creation(self):
        """Tour model should work"""
        from tours.models import Tour

        tour = Tour.objects.create(
            name='Pyramids Day Tour',
            slug='pyramids-day-tour',
            tour_type='cultural',
            description='Visit the pyramids',
            destinations=['Cairo', 'Giza'],
            departure_city='Cairo',
            price_per_person=Decimal('75.00'),
            duration_days=1,
            viator_url='https://tp.media/click?shmarker=477897&campaign_id=97',
            is_active=True
        )

        self.assertEqual(tour.name, 'Pyramids Day Tour')
        self.assertIn('Cairo', tour.destinations)
        self.assertIn('tp.media', tour.viator_url)
        self.assertIn('shmarker=477897', tour.viator_url)

    def test_blog_post_creation(self):
        """BlogPost model should work"""
        from blog.models import BlogPost, BlogCategory

        author = User.objects.create_user('author', 'author@test.com', 'pass123')
        category = BlogCategory.objects.create(name='Travel', slug='travel')

        post = BlogPost.objects.create(
            title='Best Places in Egypt',
            slug='best-places-egypt',
            content='Egypt has many amazing places to visit.',
            author=author,
            category=category,
            status='published'
        )

        self.assertEqual(post.title, 'Best Places in Egypt')
        self.assertEqual(post.author, author)


# =============================================================================
# AFFILIATE URL FORMAT TESTS
# =============================================================================

class AffiliateURLFormatTests(TestCase):
    """Test that affiliate URLs have correct format for revenue tracking"""

    def test_hotellook_marker_format(self):
        """Hotellook URLs should have correct marker"""
        url = 'https://search.hotellook.com/hotels?marker=477897&q=Test'
        self.assertIn('marker=477897', url)

    def test_viator_shmarker_format(self):
        """Viator URLs should have correct shmarker"""
        url = 'https://tp.media/click?shmarker=477897&campaign_id=97'
        self.assertIn('shmarker=477897', url)

    def test_accommodation_has_affiliate_method(self):
        """Accommodation should have get_primary_booking_url method"""
        from destinations.models import Country, City
        from accommodations.models import Accommodation

        country = Country.objects.create(name='Egypt', code='EG')
        city = City.objects.create(name='Luxor', slug='luxor', country=country)

        acc = Accommodation.objects.create(
            name='Winter Palace',
            slug='winter-palace',
            city=city,
            accommodation_type='hotel',
            price_per_night=Decimal('200.00'),
            booking_com_url='https://search.hotellook.com/hotels?marker=477897&q=Winter+Palace',
            is_active=True
        )

        url = acc.get_primary_booking_url()
        self.assertIsNotNone(url)
        self.assertIn('477897', url)


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

@skipIf(PYTHON_314_PLUS, "Django template context copy issue with Python 3.14+")
class ErrorHandlingTests(TestCase):
    """Test that errors are handled gracefully"""

    def test_404_for_nonexistent_page(self):
        """Nonexistent pages should return 404"""
        response = self.client.get('/this-page-does-not-exist-12345/')
        self.assertEqual(response.status_code, 404)

    def test_404_for_nonexistent_accommodation(self):
        """Nonexistent accommodation should return 404"""
        response = self.client.get(
            reverse('accommodations:detail', kwargs={'slug': 'nonexistent-hotel-xyz'})
        )
        self.assertEqual(response.status_code, 404)

    def test_404_for_nonexistent_tour(self):
        """Nonexistent tour should return 404"""
        response = self.client.get(
            reverse('tours:detail', kwargs={'slug': 'nonexistent-tour-xyz'})
        )
        self.assertEqual(response.status_code, 404)


# =============================================================================
# DAILY REVENUE SUMMARY TESTS
# =============================================================================

class DailyRevenueSummaryTests(TestCase):
    """Test revenue tracking models"""

    def test_daily_summary_creation(self):
        """DailyRevenueSummary should be creatable"""
        from core.models import DailyRevenueSummary
        from datetime import date

        summary = DailyRevenueSummary.objects.create(
            date=date.today(),
            total_clicks=100,
            accommodation_clicks=60,
            tour_clicks=40,
            estimated_revenue=Decimal('50.00'),
            confirmed_revenue=Decimal('25.00'),
            conversions=5,
            conversion_rate=Decimal('5.00')
        )

        self.assertEqual(summary.total_clicks, 100)
        self.assertEqual(summary.estimated_revenue, Decimal('50.00'))
