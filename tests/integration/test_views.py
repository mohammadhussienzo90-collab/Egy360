"""
Integration Tests for Views
Tests views with database interactions and template rendering
"""
from decimal import Decimal
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User

from accommodations.models import Accommodation
from tours.models import Tour, TourBooking
from home.models import NewsletterSubscription, ContactMessage, FAQItem
from datetime import date, timedelta


@override_settings(SECURE_SSL_REDIRECT=False)
class IntegrationTestBase(TestCase):
    """Base class for integration tests with helper methods"""

    def setUp(self):
        self.client = Client()

    def assertPageLoads(self, url, expected_status=200):
        """Helper to check page loads, following redirects"""
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, expected_status)
        return response


class HomeViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for home app views"""

    def setUp(self):
        super().setUp()

        # Create featured accommodations
        for i in range(3):
            Accommodation.objects.create(
                name=f"Featured Hotel {i}",
                slug=f"featured-hotel-{i}",
                accommodation_type="hotel",
                description="Test description",
                city="Cairo",
                address="Test Address",
                price_per_night=Decimal("100.00"),
                is_featured=True,
                is_active=True
            )

        # Create featured tours
        for i in range(3):
            Tour.objects.create(
                name=f"Featured Tour {i}",
                slug=f"featured-tour-{i}",
                tour_type="cultural",
                description="Test",
                highlights="Test",
                departure_city="Cairo",
                price_per_person=Decimal("100.00"),
                is_featured=True,
                is_active=True
            )

    def test_home_page_loads(self):
        """Test home page loads successfully"""
        self.assertPageLoads('/')

    def test_about_page_loads(self):
        """Test about page loads successfully"""
        self.assertPageLoads('/about/')

    def test_contact_page_loads(self):
        """Test contact page loads successfully"""
        self.assertPageLoads('/contact/')

    def test_flights_page_loads(self):
        """Test flights page loads successfully"""
        self.assertPageLoads('/flights/')

    def test_insurance_page_loads(self):
        """Test insurance page loads successfully"""
        self.assertPageLoads('/insurance/')

    def test_deals_page_loads(self):
        """Test deals page loads successfully"""
        self.assertPageLoads('/deals/')

    def test_faq_page_loads(self):
        """Test FAQ page loads successfully"""
        FAQItem.objects.create(
            question="What is Egy360?",
            answer="Egypt tourism platform",
            category="general",
            is_active=True
        )
        self.assertPageLoads('/faq/')

    def test_contact_form_submission(self):
        """Test contact form submission creates message"""
        response = self.client.post('/contact/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())


class AccommodationViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for accommodation views"""

    def setUp(self):
        super().setUp()
        self.hotel = Accommodation.objects.create(
            name="Test Hotel Cairo",
            slug="test-hotel-cairo",
            accommodation_type="hotel",
            description="A beautiful hotel in Cairo",
            city="Cairo",
            address="123 Test Street",
            star_rating=4,
            price_per_night=Decimal("150.00"),
            is_active=True
        )

    def test_accommodation_list_page_loads(self):
        """Test accommodation list page loads"""
        self.assertPageLoads('/accommodations/')

    def test_accommodation_detail_page_loads(self):
        """Test accommodation detail page loads"""
        self.assertPageLoads(f'/accommodations/{self.hotel.slug}/')

    def test_accommodation_filter_by_city(self):
        """Test filtering accommodations by city"""
        self.assertPageLoads('/accommodations/?city=Cairo')


class TourViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for tour views"""

    def setUp(self):
        super().setUp()
        self.tour = Tour.objects.create(
            name="Pyramids Day Tour",
            slug="pyramids-day-tour",
            tour_type="cultural",
            description="Visit the pyramids",
            highlights="See the Sphinx",
            departure_city="Cairo",
            price_per_person=Decimal("89.00"),
            is_active=True
        )

    def test_tour_list_page_loads(self):
        """Test tour list page loads"""
        self.assertPageLoads('/tours/')

    def test_tour_detail_page_loads(self):
        """Test tour detail page loads"""
        self.assertPageLoads(f'/tours/{self.tour.slug}/')

    def test_tour_filter_by_type(self):
        """Test filtering tours by type"""
        self.assertPageLoads('/tours/?type=cultural')


class AuthenticationViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for authentication views"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_page_loads(self):
        """Test login page loads"""
        self.assertPageLoads('/accounts/login/')

    def test_register_page_loads(self):
        """Test register page loads"""
        self.assertPageLoads('/accounts/register/')

    def test_successful_login(self):
        """Test successful login"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class DashboardViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for dashboard views"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_dashboard_loads_when_authenticated(self):
        """Test dashboard loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        self.assertPageLoads('/dashboard/')

    def test_revenue_dashboard_requires_staff(self):
        """Test revenue dashboard requires staff access"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/revenue/')
        self.assertEqual(response.status_code, 302)

    def test_revenue_dashboard_loads_for_staff(self):
        """Test revenue dashboard loads for staff user"""
        self.client.login(username='admin', password='adminpass123')
        self.assertPageLoads('/dashboard/revenue/')


class NewsletterIntegrationTests(IntegrationTestBase):
    """Integration tests for newsletter functionality"""

    def test_newsletter_subscription_api(self):
        """Test newsletter subscription via API"""
        import json
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'subscriber@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscription.objects.filter(
            email='subscriber@example.com'
        ).exists())

    def test_duplicate_subscription_handled(self):
        """Test duplicate subscription is handled gracefully"""
        import json
        NewsletterSubscription.objects.create(email='existing@example.com')
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'existing@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


class DestinationViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for destination views"""

    def test_destinations_page_loads(self):
        """Test destinations list page loads"""
        self.assertPageLoads('/destinations/')


class TransportationViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for transportation views"""

    def test_transportation_page_loads(self):
        """Test transportation list page loads"""
        self.assertPageLoads('/transportation/')


class BlogViewsIntegrationTests(IntegrationTestBase):
    """Integration tests for blog views"""

    def test_blog_page_loads(self):
        """Test blog list page loads"""
        self.assertPageLoads('/blog/')


class ErrorPageIntegrationTests(IntegrationTestBase):
    """Integration tests for error pages"""

    def test_404_page(self):
        """Test 404 page for non-existent URL"""
        response = self.client.get('/non-existent-page-12345/')
        self.assertEqual(response.status_code, 404)

    def test_non_existent_accommodation(self):
        """Test 404 for non-existent accommodation"""
        response = self.client.get('/accommodations/non-existent-hotel-xyz/')
        self.assertEqual(response.status_code, 404)

    def test_non_existent_tour(self):
        """Test 404 for non-existent tour"""
        response = self.client.get('/tours/non-existent-tour-xyz/')
        self.assertEqual(response.status_code, 404)
