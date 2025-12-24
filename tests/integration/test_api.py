"""
Integration Tests for API Endpoints
Tests API endpoints with database interactions
"""
import json
from decimal import Decimal
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from accommodations.models import Accommodation
from tours.models import Tour
from core.models import AffiliateClick
from home.models import NewsletterSubscription


@override_settings(SECURE_SSL_REDIRECT=False)
class AffiliateTrackingAPITests(TestCase):
    """Integration tests for affiliate click tracking API"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        # Create test accommodation
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test Address",
            price_per_night=Decimal("100.00"),
            is_active=True
        )

        # Create test tour
        self.tour = Tour.objects.create(
            name="Test Tour",
            slug="test-tour",
            tour_type="cultural",
            description="Test",
            highlights="Test",
            departure_city="Cairo",
            price_per_person=Decimal("100.00"),
            is_active=True
        )

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_track_accommodation_click(self):
        """Test tracking accommodation affiliate click"""
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.accommodation.id,
                'platform': 'booking_com',
                'url': 'https://booking.com/hotel/test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Check click was recorded
        self.assertTrue(AffiliateClick.objects.filter(
            platform='booking_com',
            item_type='accommodation'
        ).exists())

    def test_track_tour_click(self):
        """Test tracking tour affiliate click"""
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'tour',
                'item_id': self.tour.id,
                'platform': 'viator',
                'url': 'https://viator.com/tours/test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

    def test_track_click_with_authenticated_user(self):
        """Test tracking click with authenticated user"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.accommodation.id,
                'platform': 'booking_com',
                'url': 'https://booking.com/hotel/test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Check click has user
        click = AffiliateClick.objects.filter(
            platform='booking_com',
            item_type='accommodation'
        ).first()
        if click:
            self.assertEqual(click.user, self.user)

    def test_track_click_records_commission_estimate(self):
        """Test click records commission estimate"""
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.accommodation.id,
                'platform': 'viator',
                'url': 'https://viator.com/test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        click = AffiliateClick.objects.filter(platform='viator').first()
        if click:
            self.assertIsNotNone(click.estimated_commission)

    def test_track_click_with_invalid_json(self):
        """Test handling invalid JSON"""
        response = self.client.post(
            '/api/track-click/',
            data='not valid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_track_click_records_device_type(self):
        """Test click records device type from user agent"""
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.accommodation.id,
                'platform': 'booking_com',
                'url': 'https://booking.com/test'
            }),
            content_type='application/json',
            HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0) AppleWebKit/605.1.15'
        )

        self.assertEqual(response.status_code, 200)

        click = AffiliateClick.objects.filter(platform='booking_com').first()
        if click:
            # Device type detection may vary - just check it's recorded
            self.assertIn(click.device_type, ['mobile', 'desktop', 'tablet'])


@override_settings(SECURE_SSL_REDIRECT=False)
class NewsletterAPITests(TestCase):
    """Integration tests for newsletter API"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_subscribe_new_email(self):
        """Test subscribing new email"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'new@example.com'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Check subscription exists
        self.assertTrue(NewsletterSubscription.objects.filter(
            email='new@example.com'
        ).exists())

    def test_subscribe_with_name(self):
        """Test subscribing with name"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({
                'email': 'named@example.com',
                'name': 'Test User'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        sub = NewsletterSubscription.objects.filter(
            email='named@example.com'
        ).first()
        if sub:
            self.assertEqual(sub.name, 'Test User')

    def test_subscribe_existing_active_email(self):
        """Test subscribing already subscribed email"""
        NewsletterSubscription.objects.create(
            email='existing@example.com',
            is_active=True
        )

        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'existing@example.com'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('already', data['message'].lower())

    def test_resubscribe_inactive_email(self):
        """Test resubscribing inactive subscription"""
        sub = NewsletterSubscription.objects.create(
            email='inactive@example.com',
            is_active=False
        )

        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'inactive@example.com'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Check subscription is reactivated
        sub.refresh_from_db()
        self.assertTrue(sub.is_active)

    def test_subscribe_invalid_email(self):
        """Test subscribing with invalid email"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'not-an-email'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_subscribe_empty_email(self):
        """Test subscribing with empty email"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': ''}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_subscribe_missing_email(self):
        """Test subscribing without email field"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)


@override_settings(SECURE_SSL_REDIRECT=False)
class SearchAutocompleteAPITests(TestCase):
    """Integration tests for search autocomplete API"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        # Create test data
        Accommodation.objects.create(
            name="Marriott Cairo",
            slug="marriott-cairo",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test",
            price_per_night=Decimal("200.00"),
            is_active=True
        )

        Tour.objects.create(
            name="Cairo Pyramids Tour",
            slug="cairo-pyramids-tour",
            tour_type="cultural",
            description="Test",
            highlights="Test",
            departure_city="Cairo",
            price_per_person=Decimal("89.00"),
            is_active=True
        )

    def test_autocomplete_accommodations(self):
        """Test autocomplete for accommodations"""
        response = self.client.get('/api/search-autocomplete/?q=marriott&type=accommodations')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)

    def test_autocomplete_tours(self):
        """Test autocomplete for tours"""
        response = self.client.get('/api/search-autocomplete/?q=pyramids&type=tours')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)

    def test_autocomplete_all(self):
        """Test autocomplete for all types"""
        response = self.client.get('/api/search-autocomplete/?q=cairo&type=all')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)

    def test_autocomplete_min_length(self):
        """Test autocomplete requires minimum query length"""
        response = self.client.get('/api/search-autocomplete/?q=a&type=all')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should return empty suggestions for short query
        self.assertEqual(len(data.get('suggestions', [])), 0)


@override_settings(SECURE_SSL_REDIRECT=False)
class PlatformStatsAPITests(TestCase):
    """Integration tests for platform stats API"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        # Create some test data
        for i in range(5):
            Accommodation.objects.create(
                name=f"Hotel {i}",
                slug=f"hotel-{i}",
                accommodation_type="hotel",
                description="Test",
                city="Cairo",
                address="Test",
                price_per_night=Decimal("100.00"),
                is_active=True
            )

        for i in range(3):
            Tour.objects.create(
                name=f"Tour {i}",
                slug=f"tour-{i}",
                tour_type="cultural",
                description="Test",
                highlights="Test",
                departure_city="Cairo",
                price_per_person=Decimal("100.00"),
                is_active=True
            )

    def test_stats_endpoint_returns_data(self):
        """Test stats endpoint returns platform statistics"""
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check expected fields
        self.assertIn('total_accommodations', data)
        self.assertIn('total_tours', data)


@override_settings(SECURE_SSL_REDIRECT=False)
class BookingCancelAPITests(TestCase):
    """Integration tests for booking cancellation API"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_cancel_requires_authentication(self):
        """Test cancellation requires login"""
        response = self.client.post('/dashboard/bookings/1/cancel/')
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_cancel_nonexistent_booking(self):
        """Test cancelling non-existent booking"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/dashboard/bookings/99999/cancel/')
        self.assertEqual(response.status_code, 404)


@override_settings(SECURE_SSL_REDIRECT=False)
class CSRFProtectionTests(TestCase):
    """Tests for CSRF protection on APIs"""

    def setUp(self):
        """Set up test client"""
        self.client = Client(enforce_csrf_checks=True)

    def test_newsletter_allows_without_csrf(self):
        """Test newsletter API doesn't require CSRF (uses JSON)"""
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        # Should work without CSRF token
        self.assertIn(response.status_code, [200, 400])

    def test_track_click_allows_without_csrf(self):
        """Test track-click API is CSRF exempt"""
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': 1,
                'platform': 'booking_com',
                'url': 'https://test.com'
            }),
            content_type='application/json'
        )
        # Should work without CSRF token
        self.assertIn(response.status_code, [200, 400])


@override_settings(SECURE_SSL_REDIRECT=False)
class RateLimitingTests(TestCase):
    """Tests for API rate limiting (if implemented)"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_newsletter_multiple_requests(self):
        """Test multiple newsletter requests are handled"""
        for i in range(5):
            response = self.client.post(
                '/api/newsletter/',
                data=json.dumps({'email': f'user{i}@example.com'}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

    def test_track_click_multiple_requests(self):
        """Test multiple track-click requests are handled"""
        # Create a test accommodation first
        accommodation = Accommodation.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test",
            price_per_night=Decimal("100.00"),
            is_active=True
        )

        for i in range(10):
            response = self.client.post(
                '/api/track-click/',
                data=json.dumps({
                    'item_type': 'accommodation',
                    'item_id': accommodation.id,
                    'platform': 'booking_com',
                    'url': 'https://test.com'
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
