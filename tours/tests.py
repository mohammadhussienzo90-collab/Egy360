# tours/tests.py
"""
Tests for Tours App

Tests for tour listings, details, and affiliate link tracking.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Tour, TourBooking


class TourModelTest(TestCase):
    """Tests for Tour model"""

    def setUp(self):
        """Set up test data"""
        self.tour = Tour.objects.create(
            name='Pyramids Day Tour',
            slug='pyramids-day-tour',
            tour_type='cultural',
            description='Explore the ancient pyramids of Giza',
            highlights='Visit the Great Pyramid, Sphinx, and Valley Temple',
            duration_days=1,
            departure_city='Cairo',
            price_per_person=Decimal('75.00'),
            viator_url='https://www.viator.com/tours/pyramids',
            commission_rate=Decimal('8.0'),
            is_active=True
        )

    def test_tour_creation(self):
        """Test creating a tour"""
        self.assertEqual(self.tour.name, 'Pyramids Day Tour')
        self.assertEqual(self.tour.tour_type, 'cultural')
        self.assertTrue(self.tour.is_active)

    def test_tour_str_representation(self):
        """Test tour string representation"""
        self.assertEqual(str(self.tour), 'Pyramids Day Tour')

    def test_get_primary_affiliate_url(self):
        """Test getting primary affiliate URL"""
        url = self.tour.get_primary_affiliate_url()
        self.assertEqual(url, 'https://www.viator.com/tours/pyramids')

    def test_affiliate_url_priority(self):
        """Test affiliate URL priority (Viator > GetYourGuide)"""
        # Tour has Viator URL, should return that
        self.assertEqual(
            self.tour.get_primary_affiliate_url(),
            self.tour.viator_url
        )

        # Remove Viator, should fall back to GetYourGuide
        self.tour.viator_url = None
        self.tour.getyourguide_url = 'https://getyourguide.com/tour'
        self.tour.save()

        self.assertEqual(
            self.tour.get_primary_affiliate_url(),
            'https://getyourguide.com/tour'
        )


class TourViewTest(TestCase):
    """Tests for tour views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.tour = Tour.objects.create(
            name='Nile Cruise',
            slug='nile-cruise',
            tour_type='cruise',
            description='Luxury Nile cruise from Luxor to Aswan',
            highlights='Visit temples, tombs, and enjoy onboard dining',
            duration_days=4,
            duration_nights=3,
            departure_city='Luxor',
            price_per_person=Decimal('450.00'),
            is_active=True
        )

    def test_tour_list_loads(self):
        """Test tour list page loads"""
        response = self.client.get(reverse('tours:list'))
        self.assertEqual(response.status_code, 200)

    def test_tour_detail_loads(self):
        """Test tour detail page loads"""
        response = self.client.get(
            reverse('tours:detail', kwargs={'slug': self.tour.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_tour_detail_404_for_invalid_slug(self):
        """Test tour detail returns 404 for invalid slug"""
        response = self.client.get(
            reverse('tours:detail', kwargs={'slug': 'nonexistent-tour'})
        )
        self.assertEqual(response.status_code, 404)

    def test_tour_filter_by_type(self):
        """Test filtering tours by type"""
        response = self.client.get(
            reverse('tours:by-type', kwargs={'tour_type': 'cruise'})
        )
        self.assertEqual(response.status_code, 200)


class TourBookingTest(TestCase):
    """Tests for tour booking functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.tour = Tour.objects.create(
            name='Desert Safari',
            slug='desert-safari',
            tour_type='desert',
            description='Experience the Sahara desert',
            highlights='Camel ride, bedouin dinner, stargazing',
            duration_days=2,
            duration_nights=1,
            departure_city='Cairo',
            price_per_person=Decimal('150.00'),
            is_active=True
        )

    def test_tour_booking_requires_login(self):
        """Test tour booking requires authentication"""
        response = self.client.post(
            reverse('tours:book', kwargs={'slug': self.tour.slug}),
            data={}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_tour_booking_post_accessible_when_logged_in(self):
        """Test tour booking POST accessible when logged in"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('tours:book', kwargs={'slug': self.tour.slug}),
            data={'tour_date': '2025-02-01', 'participants': 2}
        )
        # Either 200 (form errors) or 302 (redirect on success)
        self.assertIn(response.status_code, [200, 302])
