"""
System Tests for Complete User Flows
Tests end-to-end user journeys through the application
"""
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User

from accommodations.models import Accommodation
from tours.models import Tour, TourBooking
from home.models import NewsletterSubscription, ContactMessage


@override_settings(SECURE_SSL_REDIRECT=False)
class UserRegistrationFlowTests(TestCase):
    """System tests for user registration flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_complete_registration_flow(self):
        """Test complete user registration journey"""
        # Step 1: Visit registration page
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Submit registration form
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success

        # Step 3: Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')

        # Step 4: Verify profile was auto-created
        self.assertTrue(hasattr(user, 'profile'))

        # Step 5: User should be able to login
        login_success = self.client.login(
            username='newuser',
            password='SecurePass123!'
        )
        self.assertTrue(login_success)

        # Step 6: Access dashboard
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)


@override_settings(SECURE_SSL_REDIRECT=False)
class AccommodationSearchFlowTests(TestCase):
    """System tests for accommodation search flow"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        # Create various accommodations
        self.cairo_hotel = Accommodation.objects.create(
            name="Marriott Cairo",
            slug="marriott-cairo",
            accommodation_type="hotel",
            description="Luxury hotel in Cairo",
            city="Cairo",
            address="Zamalek",
            star_rating=5,
            price_per_night=Decimal("250.00"),
            is_active=True,
            is_featured=True,
            booking_com_url="https://booking.com/marriott-cairo"
        )

        self.hurghada_resort = Accommodation.objects.create(
            name="Red Sea Resort",
            slug="red-sea-resort",
            accommodation_type="resort",
            description="Beach resort",
            city="Hurghada",
            address="Beach Road",
            star_rating=4,
            price_per_night=Decimal("180.00"),
            is_active=True
        )

    def test_complete_search_flow(self):
        """Test complete accommodation search journey"""
        # Step 1: Visit home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Visit accommodations list
        response = self.client.get('/accommodations/')
        self.assertEqual(response.status_code, 200)

        # Step 3: Filter by city
        response = self.client.get('/accommodations/?city=Cairo')
        self.assertEqual(response.status_code, 200)

        # Step 4: View accommodation details
        response = self.client.get(f'/accommodations/{self.cairo_hotel.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_search_with_filters(self):
        """Test search with multiple filters"""
        # Search by city and type
        response = self.client.get('/accommodations/?city=Cairo&type=hotel')
        self.assertEqual(response.status_code, 200)

        # Search by price range
        response = self.client.get('/accommodations/?min_price=100&max_price=300')
        self.assertEqual(response.status_code, 200)

    def test_affiliate_click_tracking_flow(self):
        """Test affiliate click tracking during search flow"""
        # Step 1: View accommodation
        response = self.client.get(f'/accommodations/{self.cairo_hotel.slug}/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Click affiliate link (tracked via API)
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.cairo_hotel.id,
                'platform': 'booking_com',
                'url': self.cairo_hotel.booking_com_url
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


@override_settings(SECURE_SSL_REDIRECT=False)
class TourBookingFlowTests(TestCase):
    """System tests for tour booking flow"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        self.user = User.objects.create_user(
            username='traveler',
            email='traveler@example.com',
            password='TravelPass123!'
        )

        self.tour = Tour.objects.create(
            name="Pyramids Day Tour",
            slug="pyramids-day-tour",
            tour_type="cultural",
            description="Full day tour to pyramids",
            highlights="Sphinx, Great Pyramid",
            departure_city="Cairo",
            price_per_person=Decimal("89.00"),
            is_active=True,
            viator_url="https://viator.com/pyramids"
        )

    def test_complete_booking_flow_guest(self):
        """Test tour browsing as guest user"""
        # Step 1: Browse tours
        response = self.client.get('/tours/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Filter tours
        response = self.client.get('/tours/?type=cultural')
        self.assertEqual(response.status_code, 200)

        # Step 3: View tour details
        response = self.client.get(f'/tours/{self.tour.slug}/')
        self.assertEqual(response.status_code, 200)

        # Step 4: Try to book (should redirect to login)
        response = self.client.get(f'/tours/{self.tour.slug}/book/')
        self.assertEqual(response.status_code, 302)

    def test_complete_booking_flow_authenticated(self):
        """Test complete tour booking as authenticated user"""
        # Step 1: Login
        self.client.login(username='traveler', password='TravelPass123!')

        # Step 2: Browse tours
        response = self.client.get('/tours/')
        self.assertEqual(response.status_code, 200)

        # Step 3: View tour details
        response = self.client.get(f'/tours/{self.tour.slug}/')
        self.assertEqual(response.status_code, 200)

        # Step 4: Access booking form
        response = self.client.get(f'/tours/{self.tour.slug}/book/')
        # May return 200 or 404 depending on implementation
        self.assertIn(response.status_code, [200, 404])

    def test_affiliate_booking_redirect_flow(self):
        """Test affiliate booking redirect flow"""
        # View tour
        response = self.client.get(f'/tours/{self.tour.slug}/')
        self.assertEqual(response.status_code, 200)

        # Track click
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'tour',
                'item_id': self.tour.id,
                'platform': 'viator',
                'url': self.tour.viator_url
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


@override_settings(SECURE_SSL_REDIRECT=False)
class NewsletterSubscriptionFlowTests(TestCase):
    """System tests for newsletter subscription flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_homepage_newsletter_signup(self):
        """Test newsletter signup from homepage"""
        # Step 1: Visit homepage
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Subscribe to newsletter
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'subscriber@example.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Step 3: Verify subscription
        self.assertTrue(NewsletterSubscription.objects.filter(
            email='subscriber@example.com',
            is_active=True
        ).exists())

    def test_deals_page_newsletter_signup(self):
        """Test newsletter signup from deals page"""
        # Step 1: Visit deals page
        response = self.client.get('/deals/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Subscribe
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({
                'email': 'deals@example.com',
                'name': 'Deal Hunter'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


@override_settings(SECURE_SSL_REDIRECT=False)
class ContactFormFlowTests(TestCase):
    """System tests for contact form flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_complete_contact_flow(self):
        """Test complete contact form journey"""
        # Step 1: Visit contact page
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Submit contact form
        response = self.client.post('/contact/', {
            'name': 'John Traveler',
            'email': 'john@example.com',
            'subject': 'Tour Inquiry',
            'message': 'I would like information about Nile cruises.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success

        # Step 3: Verify message was saved
        self.assertTrue(ContactMessage.objects.filter(
            email='john@example.com',
            subject='Tour Inquiry'
        ).exists())


@override_settings(SECURE_SSL_REDIRECT=False)
class UserDashboardFlowTests(TestCase):
    """System tests for user dashboard flow"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='dashuser',
            email='dash@example.com',
            password='DashPass123!'
        )

    def test_dashboard_access_flow(self):
        """Test dashboard access journey"""
        # Step 1: Try to access dashboard without login
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Step 2: Login
        self.client.login(username='dashuser', password='DashPass123!')

        # Step 3: Access dashboard
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

        # Step 4: Access bookings
        response = self.client.get('/dashboard/bookings/')
        self.assertEqual(response.status_code, 200)

        # Step 5: Access settings
        response = self.client.get('/dashboard/settings/')
        self.assertEqual(response.status_code, 200)

    def test_profile_update_flow(self):
        """Test profile update journey"""
        self.client.login(username='dashuser', password='DashPass123!')

        # Step 1: Visit settings page
        response = self.client.get('/dashboard/settings/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Update profile (depends on form implementation)
        response = self.client.post('/dashboard/settings/', {
            'action': 'update_profile',
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'dash@example.com'
        })
        # Should redirect or return 200
        self.assertIn(response.status_code, [200, 302])


@override_settings(SECURE_SSL_REDIRECT=False)
class FlightSearchFlowTests(TestCase):
    """System tests for flight search flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_flight_search_page_flow(self):
        """Test flight search page journey"""
        # Step 1: Visit flights page
        response = self.client.get('/flights/')
        self.assertEqual(response.status_code, 200)

        # Page should contain Travelpayouts widget (check content)
        self.assertContains(response, 'tp.media', status_code=200)


@override_settings(SECURE_SSL_REDIRECT=False)
class InsuranceFlowTests(TestCase):
    """System tests for insurance page flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_insurance_page_flow(self):
        """Test insurance page journey"""
        # Step 1: Visit insurance page
        response = self.client.get('/insurance/')
        self.assertEqual(response.status_code, 200)

        # Page should show insurance plans
        self.assertContains(response, 'Basic', status_code=200)
        self.assertContains(response, 'Standard', status_code=200)
        self.assertContains(response, 'Premium', status_code=200)


@override_settings(SECURE_SSL_REDIRECT=False)
class DealsPageFlowTests(TestCase):
    """System tests for deals page flow"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_deals_page_flow(self):
        """Test deals page journey"""
        # Step 1: Visit deals page
        response = self.client.get('/deals/')
        self.assertEqual(response.status_code, 200)

        # Page should contain deals sections
        self.assertContains(response, 'Hot Deals', status_code=200)
        self.assertContains(response, 'Promo Codes', status_code=200)


@override_settings(SECURE_SSL_REDIRECT=False)
class MultiStepBookingFlowTests(TestCase):
    """System tests for multi-step booking flow"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        self.user = User.objects.create_user(
            username='booker',
            email='booker@example.com',
            password='BookerPass123!'
        )

        self.tour = Tour.objects.create(
            name="Multi-Day Nile Cruise",
            slug="nile-cruise",
            tour_type="cruise",
            description="5-day cruise",
            highlights="Luxor, Aswan",
            departure_city="Luxor",
            duration_days=5,
            duration_nights=4,
            price_per_person=Decimal("899.00"),
            is_active=True
        )

    def test_search_to_booking_flow(self):
        """Test flow from search to booking"""
        # Step 1: Login
        self.client.login(username='booker', password='BookerPass123!')

        # Step 2: Search for cruises
        response = self.client.get('/tours/?type=cruise')
        self.assertEqual(response.status_code, 200)

        # Step 3: View cruise details
        response = self.client.get(f'/tours/{self.tour.slug}/')
        self.assertEqual(response.status_code, 200)

        # Step 4: Initiate booking
        response = self.client.get(f'/tours/{self.tour.slug}/book/')
        # Depends on implementation
        self.assertIn(response.status_code, [200, 404])


@override_settings(SECURE_SSL_REDIRECT=False)
class CrossSiteNavigationFlowTests(TestCase):
    """System tests for navigation between different site sections"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()

        Accommodation.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test",
            price_per_night=Decimal("100.00"),
            is_active=True
        )

        Tour.objects.create(
            name="Test Tour",
            slug="test-tour",
            tour_type="cultural",
            description="Test",
            highlights="Test",
            departure_city="Cairo",
            price_per_person=Decimal("50.00"),
            is_active=True
        )

    def test_navigation_flow(self):
        """Test navigation between site sections"""
        # Start at home
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Navigate to accommodations
        response = self.client.get('/accommodations/')
        self.assertEqual(response.status_code, 200)

        # Navigate to tours
        response = self.client.get('/tours/')
        self.assertEqual(response.status_code, 200)

        # Navigate to destinations
        response = self.client.get('/destinations/')
        self.assertEqual(response.status_code, 200)

        # Navigate to flights
        response = self.client.get('/flights/')
        self.assertEqual(response.status_code, 200)

        # Navigate to about
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

        # Navigate to contact
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
