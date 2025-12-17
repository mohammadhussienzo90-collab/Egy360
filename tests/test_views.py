"""
Tests for Egy360 views
Tests for accommodations, tours, dashboard, and home views
"""

import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from accommodations.models import Accommodation
from tours.models import Tour, TourBooking
from home.models import NewsletterSubscription


class AccommodationViewsTest(TestCase):
    """Tests for accommodation views"""

    def setUp(self):
        self.client = Client()
        self.accommodation = Accommodation.objects.create(
            name='Test Hotel',
            slug='test-hotel',
            accommodation_type='hotel',
            description='A test hotel',
            city='Cairo',
            address='123 Test Street',
            price_per_night=Decimal('100.00'),
            star_rating=4,
            is_active=True,
            is_featured=True,
        )

    def test_accommodation_search_view(self):
        """Test accommodation search page loads"""
        response = self.client.get(reverse('accommodations:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    def test_accommodation_search_with_city_filter(self):
        """Test accommodation search with city filter"""
        response = self.client.get(
            reverse('accommodations:search'),
            {'city': 'Cairo'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    def test_accommodation_search_with_type_filter(self):
        """Test accommodation search with type filter"""
        response = self.client.get(
            reverse('accommodations:search'),
            {'type': 'hotel'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    def test_accommodation_detail_view(self):
        """Test accommodation detail page loads"""
        response = self.client.get(
            reverse('accommodations:detail', kwargs={'slug': 'test-hotel'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    def test_accommodation_by_city_view(self):
        """Test accommodation by city view"""
        response = self.client.get(
            reverse('accommodations:by-city', kwargs={'city': 'Cairo'})
        )
        self.assertEqual(response.status_code, 200)

    def test_accommodation_by_type_view(self):
        """Test accommodation by type view"""
        response = self.client.get(
            reverse('accommodations:by-type', kwargs={'acc_type': 'hotel'})
        )
        self.assertEqual(response.status_code, 200)


class TourViewsTest(TestCase):
    """Tests for tour views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.tour = Tour.objects.create(
            name='Test Tour',
            slug='test-tour',
            tour_type='cultural',
            description='A test tour',
            highlights='Test highlights',
            departure_city='Cairo',
            duration_days=3,
            duration_nights=2,
            price_per_person=Decimal('500.00'),
            is_active=True,
            is_featured=True,
        )

    def test_tour_list_view(self):
        """Test tour list page loads"""
        response = self.client.get(reverse('tours:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tour')

    def test_tour_list_with_type_filter(self):
        """Test tour list with type filter"""
        response = self.client.get(
            reverse('tours:list'),
            {'type': 'cultural'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tour')

    def test_tour_detail_view(self):
        """Test tour detail page loads"""
        response = self.client.get(
            reverse('tours:detail', kwargs={'slug': 'test-tour'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tour')

    def test_tour_by_type_view(self):
        """Test tour by type view"""
        response = self.client.get(
            reverse('tours:by-type', kwargs={'tour_type': 'cultural'})
        )
        self.assertEqual(response.status_code, 200)

    def test_tour_booking_requires_login(self):
        """Test tour booking requires authentication"""
        response = self.client.post(
            reverse('tours:book', kwargs={'slug': 'test-tour'}),
            data=json.dumps({'tour_date': '2025-01-15', 'adults': 2}),
            content_type='application/json'
        )
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_tour_booking_authenticated(self):
        """Test tour booking for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('tours:book', kwargs={'slug': 'test-tour'}),
            data=json.dumps({
                'tour_date': '2025-06-15',
                'adults': 2,
                'children': 0,
                'contact_name': 'Test User',
                'contact_email': 'test@example.com',
                'contact_phone': '+1234567890'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('booking_id', data)


class DashboardViewsTest(TestCase):
    """Tests for dashboard views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_authenticated(self):
        """Test dashboard loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_bookings_view(self):
        """Test bookings view loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:bookings'))
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        """Test settings view loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:settings'))
        self.assertEqual(response.status_code, 200)


class NewsletterViewsTest(TestCase):
    """Tests for newsletter subscription"""

    def setUp(self):
        self.client = Client()

    def test_newsletter_subscribe_success(self):
        """Test successful newsletter subscription"""
        response = self.client.post(
            reverse('home:newsletter-subscribe'),
            data=json.dumps({'email': 'test@example.com', 'name': 'Test User'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # Verify subscription was created
        self.assertTrue(
            NewsletterSubscription.objects.filter(email='test@example.com').exists()
        )

    def test_newsletter_subscribe_invalid_email(self):
        """Test newsletter subscription with invalid email"""
        response = self.client.post(
            reverse('home:newsletter-subscribe'),
            data=json.dumps({'email': 'invalid-email'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_newsletter_subscribe_duplicate(self):
        """Test newsletter subscription with duplicate email"""
        NewsletterSubscription.objects.create(email='test@example.com')

        response = self.client.post(
            reverse('home:newsletter-subscribe'),
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('already subscribed', data['message'])

    def test_newsletter_reactivation(self):
        """Test newsletter reactivation for unsubscribed user"""
        sub = NewsletterSubscription.objects.create(
            email='test@example.com',
            is_active=False
        )

        response = self.client.post(
            reverse('home:newsletter-subscribe'),
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('reactivated', data['message'])

        # Verify subscription was reactivated
        sub.refresh_from_db()
        self.assertTrue(sub.is_active)


class HomeViewsTest(TestCase):
    """Tests for home app views"""

    def setUp(self):
        self.client = Client()

    def test_homepage_loads(self):
        """Test homepage loads successfully"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        """Test about page loads"""
        response = self.client.get(reverse('home:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = self.client.get(reverse('home:contact'))
        self.assertEqual(response.status_code, 200)

    def test_faq_page_loads(self):
        """Test FAQ page loads"""
        response = self.client.get(reverse('home:faq'))
        self.assertEqual(response.status_code, 200)

    def test_search_autocomplete(self):
        """Test search autocomplete endpoint"""
        response = self.client.get(
            reverse('home:search-autocomplete'),
            {'q': 'cairo', 'type': 'all'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)

    def test_platform_stats(self):
        """Test platform stats endpoint"""
        response = self.client.get(reverse('home:platform-stats'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_accommodations', data)
        self.assertIn('total_tours', data)
