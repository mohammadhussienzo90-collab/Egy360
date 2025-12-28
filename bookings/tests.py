# bookings/tests.py
"""
Tests for Bookings App

Tests for booking creation, management, and checkout flow.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Booking, AccommodationBooking
from accommodations.models import Accommodation
from destinations.models import City


class BookingModelTest(TestCase):
    """Tests for Booking model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )

        # Create a city first
        self.city = City.objects.create(
            name='Cairo',
            slug='cairo',
            country='Egypt'
        )

        # Create an accommodation for testing
        self.accommodation = Accommodation.objects.create(
            name='Test Hotel',
            city=self.city,
            description='A test hotel',
            price_per_night=Decimal('100.00'),
            is_active=True
        )

        self.content_type = ContentType.objects.get_for_model(Accommodation)

    def test_booking_creation(self):
        """Test creating a booking"""
        booking = Booking.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.accommodation.id,
            booking_type='accommodation',
            booking_reference='EGY-TEST001',
            check_in_date=timezone.now().date() + timedelta(days=1),
            check_out_date=timezone.now().date() + timedelta(days=3),
            total_amount=Decimal('200.00'),
            contact_name='Test User',
            contact_email='test@example.com',
            contact_phone='+201234567890'
        )

        self.assertEqual(booking.booking_reference, 'EGY-TEST001')
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.payment_status, 'unpaid')

    def test_booking_str_representation(self):
        """Test booking string representation"""
        booking = Booking.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.accommodation.id,
            booking_type='accommodation',
            booking_reference='EGY-TEST002',
            total_amount=Decimal('200.00'),
            contact_name='Test User',
            contact_email='test@example.com',
            contact_phone='+201234567890'
        )

        expected = f"EGY-TEST002 - {self.user.username}"
        self.assertEqual(str(booking), expected)

    def test_booking_confirm(self):
        """Test confirming a booking"""
        booking = Booking.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.accommodation.id,
            booking_type='accommodation',
            booking_reference='EGY-TEST003',
            total_amount=Decimal('200.00'),
            contact_name='Test User',
            contact_email='test@example.com',
            contact_phone='+201234567890'
        )

        booking.confirm()

        self.assertEqual(booking.status, 'confirmed')

    def test_booking_cancel(self):
        """Test cancelling a booking"""
        booking = Booking.objects.create(
            user=self.user,
            content_type=self.content_type,
            object_id=self.accommodation.id,
            booking_type='accommodation',
            booking_reference='EGY-TEST004',
            total_amount=Decimal('200.00'),
            contact_name='Test User',
            contact_email='test@example.com',
            contact_phone='+201234567890'
        )

        booking.cancel()

        self.assertEqual(booking.status, 'cancelled')


class BookingViewTest(TestCase):
    """Tests for booking views"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )

        # Create test data
        self.city = City.objects.create(
            name='Cairo',
            slug='cairo',
            country='Egypt'
        )

        self.accommodation = Accommodation.objects.create(
            name='Test Hotel',
            city=self.city,
            description='A test hotel',
            price_per_night=Decimal('100.00'),
            is_active=True
        )

    def test_my_bookings_requires_login(self):
        """Test my bookings page requires authentication"""
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_my_bookings_accessible_when_logged_in(self):
        """Test my bookings page accessible when logged in"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_requires_login(self):
        """Test checkout page requires authentication"""
        response = self.client.get(
            reverse('bookings:checkout', kwargs={
                'booking_type': 'accommodation',
                'item_id': self.accommodation.id
            })
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_checkout_page_loads_for_valid_item(self):
        """Test checkout page loads for valid accommodation"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('bookings:checkout', kwargs={
                'booking_type': 'accommodation',
                'item_id': self.accommodation.id
            })
        )
        self.assertEqual(response.status_code, 200)

    def test_checkout_404_for_invalid_item(self):
        """Test checkout returns 404 for non-existent item"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('bookings:checkout', kwargs={
                'booking_type': 'accommodation',
                'item_id': 99999
            })
        )
        self.assertEqual(response.status_code, 404)
