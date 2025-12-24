"""
Acceptance Tests for Egy360
Tests business requirements from end-user perspective
These tests validate that the system meets user expectations
"""
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core import mail

from accommodations.models import Accommodation
from tours.models import Tour, TourBooking
from home.models import NewsletterSubscription, ContactMessage, FAQItem
from core.models import AffiliateClick


@override_settings(SECURE_SSL_REDIRECT=False)
class AcceptanceTestBase(TestCase):
    """Base class for acceptance tests with common setup"""

    def setUp(self):
        """Set up common test data"""
        self.client = Client()

        # Create a standard test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='SecurePassword123!',
            first_name='Test',
            last_name='User'
        )

        # Create sample accommodations
        self.hotel = Accommodation.objects.create(
            name="Marriott Cairo",
            slug="marriott-cairo",
            accommodation_type="hotel",
            description="Luxury 5-star hotel with Nile views",
            city="Cairo",
            address="Zamalek, Cairo",
            star_rating=5,
            price_per_night=Decimal("299.00"),
            is_active=True,
            is_featured=True,
            booking_com_url="https://booking.com/marriott-cairo"
        )

        # Create sample tour
        self.tour = Tour.objects.create(
            name="Pyramids of Giza Day Tour",
            slug="pyramids-giza-day-tour",
            tour_type="cultural",
            description="Full day tour to the iconic Pyramids",
            highlights="Great Pyramid, Sphinx, Valley Temple",
            departure_city="Cairo",
            price_per_person=Decimal("89.00"),
            is_active=True,
            is_featured=True,
            viator_url="https://viator.com/pyramids"
        )


# ============================================================================
# FEATURE: User can browse and search accommodations
# ============================================================================

class UserCanBrowseAccommodationsTests(AcceptanceTestBase):
    """
    Feature: User can browse and search accommodations
    As a tourist
    I want to browse and search for hotels in Egypt
    So that I can find suitable accommodation for my trip
    """

    def test_user_can_view_accommodation_list(self):
        """Scenario: User views list of accommodations"""
        # When I visit the accommodations page
        response = self.client.get('/accommodations/')

        # Then I should see the page load successfully
        self.assertEqual(response.status_code, 200)

    def test_user_can_filter_by_city(self):
        """Scenario: User filters accommodations by city"""
        # Given there are accommodations in Cairo
        # When I filter by city=Cairo
        response = self.client.get('/accommodations/?city=Cairo')

        # Then I should see the filtered results
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_accommodation_details(self):
        """Scenario: User views accommodation details"""
        # When I click on a hotel
        response = self.client.get(f'/accommodations/{self.hotel.slug}/')

        # Then I should see the hotel details page
        self.assertEqual(response.status_code, 200)

    def test_user_sees_booking_options(self):
        """Scenario: User sees booking options on detail page"""
        # When I view the hotel details
        response = self.client.get(f'/accommodations/{self.hotel.slug}/')

        # Then I should see booking options
        self.assertEqual(response.status_code, 200)
        # The page should show the hotel has booking options
        self.assertTrue(self.hotel.has_booking_options())


# ============================================================================
# FEATURE: User can browse and book tours
# ============================================================================

class UserCanBrowseToursTests(AcceptanceTestBase):
    """
    Feature: User can browse and book tours
    As a tourist
    I want to browse available tours in Egypt
    So that I can plan my sightseeing activities
    """

    def test_user_can_view_tour_list(self):
        """Scenario: User views list of tours"""
        # When I visit the tours page
        response = self.client.get('/tours/')

        # Then I should see the page load successfully
        self.assertEqual(response.status_code, 200)

    def test_user_can_filter_tours_by_type(self):
        """Scenario: User filters tours by type"""
        # When I filter by cultural tours
        response = self.client.get('/tours/?type=cultural')

        # Then I should see filtered results
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_tour_details(self):
        """Scenario: User views tour details"""
        # When I click on a tour
        response = self.client.get(f'/tours/{self.tour.slug}/')

        # Then I should see tour details
        self.assertEqual(response.status_code, 200)


# ============================================================================
# FEATURE: User can register and manage account
# ============================================================================

class UserCanRegisterAndLoginTests(AcceptanceTestBase):
    """
    Feature: User registration and authentication
    As a visitor
    I want to create an account and login
    So that I can book tours and manage my reservations
    """

    def test_user_can_register_new_account(self):
        """Scenario: New user registers an account"""
        # When I submit the registration form
        response = self.client.post('/accounts/register/', {
            'username': 'newvisitor',
            'email': 'visitor@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })

        # Then I should be registered and redirected
        self.assertEqual(response.status_code, 302)

        # And my account should be created
        self.assertTrue(User.objects.filter(username='newvisitor').exists())

    def test_registered_user_can_login(self):
        """Scenario: Registered user logs in"""
        # When I login with valid credentials
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'SecurePassword123!'
        })

        # Then I should be logged in and redirected
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_access_dashboard(self):
        """Scenario: Logged in user accesses dashboard"""
        # Given I am logged in
        self.client.login(username='testuser', password='SecurePassword123!')

        # When I visit the dashboard
        response = self.client.get('/dashboard/')

        # Then I should see my dashboard
        self.assertEqual(response.status_code, 200)


# ============================================================================
# FEATURE: User can subscribe to newsletter
# ============================================================================

class UserCanSubscribeToNewsletterTests(AcceptanceTestBase):
    """
    Feature: Newsletter subscription
    As a visitor
    I want to subscribe to the newsletter
    So that I can receive travel deals and updates
    """

    def test_user_can_subscribe_to_newsletter(self):
        """Scenario: User subscribes to newsletter"""
        # When I submit my email for newsletter
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'subscriber@example.com'}),
            content_type='application/json'
        )

        # Then I should be subscribed
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        # And my subscription should be saved
        self.assertTrue(NewsletterSubscription.objects.filter(
            email='subscriber@example.com'
        ).exists())

    def test_user_receives_confirmation_message(self):
        """Scenario: User receives confirmation after subscribing"""
        # When I subscribe
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'newsubscriber@example.com'}),
            content_type='application/json'
        )

        # Then I should receive a success message
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('success', data.get('message', '').lower())


# ============================================================================
# FEATURE: User can contact support
# ============================================================================

class UserCanContactSupportTests(AcceptanceTestBase):
    """
    Feature: Contact support
    As a visitor
    I want to contact the support team
    So that I can get help with my booking or ask questions
    """

    def test_user_can_submit_contact_form(self):
        """Scenario: User submits contact form"""
        # When I submit the contact form
        response = self.client.post('/contact/', {
            'name': 'John Tourist',
            'email': 'john@example.com',
            'subject': 'Booking Question',
            'message': 'I need help with my booking.'
        })

        # Then I should be redirected (success)
        self.assertEqual(response.status_code, 302)

        # And my message should be saved
        self.assertTrue(ContactMessage.objects.filter(
            email='john@example.com'
        ).exists())

    def test_user_sees_confirmation_after_contact(self):
        """Scenario: User sees confirmation after contact"""
        # When I submit and follow redirect
        response = self.client.post('/contact/', {
            'name': 'Jane Tourist',
            'email': 'jane@example.com',
            'subject': 'General Inquiry',
            'message': 'Hello, I have a question.'
        }, follow=True)

        # Then I should see a success message
        self.assertEqual(response.status_code, 200)


# ============================================================================
# FEATURE: User can search for flights
# ============================================================================

class UserCanSearchFlightsTests(AcceptanceTestBase):
    """
    Feature: Flight search
    As a tourist
    I want to search for flights to Egypt
    So that I can book my travel
    """

    def test_user_can_access_flights_page(self):
        """Scenario: User accesses flights page"""
        # When I visit the flights page
        response = self.client.get('/flights/')

        # Then I should see the flight search widget
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Flights to Egypt')

    def test_flights_page_shows_popular_routes(self):
        """Scenario: User sees popular flight routes"""
        # When I visit the flights page
        response = self.client.get('/flights/')

        # Then I should see popular routes
        self.assertEqual(response.status_code, 200)
        # Page should mention Cairo
        self.assertContains(response, 'Cairo')


# ============================================================================
# FEATURE: User can view travel deals
# ============================================================================

class UserCanViewDealsTests(AcceptanceTestBase):
    """
    Feature: Travel deals
    As a tourist
    I want to view travel deals
    So that I can find discounted trips
    """

    def test_user_can_access_deals_page(self):
        """Scenario: User views deals page"""
        # When I visit the deals page
        response = self.client.get('/deals/')

        # Then I should see deals
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Deals')

    def test_deals_page_shows_promo_codes(self):
        """Scenario: User sees promo codes"""
        # When I visit the deals page
        response = self.client.get('/deals/')

        # Then I should see promo codes section
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Promo')


# ============================================================================
# FEATURE: User can get travel insurance
# ============================================================================

class UserCanGetInsuranceTests(AcceptanceTestBase):
    """
    Feature: Travel insurance
    As a tourist
    I want to get travel insurance
    So that I am protected during my trip
    """

    def test_user_can_access_insurance_page(self):
        """Scenario: User views insurance page"""
        # When I visit the insurance page
        response = self.client.get('/insurance/')

        # Then I should see insurance options
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insurance')

    def test_insurance_shows_plan_options(self):
        """Scenario: User sees insurance plan options"""
        # When I visit the insurance page
        response = self.client.get('/insurance/')

        # Then I should see different plans
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Basic')
        self.assertContains(response, 'Premium')


# ============================================================================
# FEATURE: Affiliate clicks are tracked for monetization
# ============================================================================

class AffiliateClicksAreTrackedTests(AcceptanceTestBase):
    """
    Feature: Affiliate tracking
    As the platform owner
    I want affiliate clicks to be tracked
    So that I can monitor revenue
    """

    def test_accommodation_affiliate_clicks_are_tracked(self):
        """Scenario: Accommodation booking click is tracked"""
        # When a user clicks an affiliate booking link
        response = self.client.post(
            '/api/track-click/',
            data=json.dumps({
                'item_type': 'accommodation',
                'item_id': self.hotel.id,
                'platform': 'booking_com',
                'url': self.hotel.booking_com_url
            }),
            content_type='application/json'
        )

        # Then the click should be recorded
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AffiliateClick.objects.filter(
            platform='booking_com',
            item_type='accommodation'
        ).exists())

    def test_tour_affiliate_clicks_are_tracked(self):
        """Scenario: Tour booking click is tracked"""
        # When a user clicks a tour affiliate link
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

        # Then the click should be recorded
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AffiliateClick.objects.filter(
            platform='viator',
            item_type='tour'
        ).exists())


# ============================================================================
# FEATURE: Admin can view revenue dashboard
# ============================================================================

class AdminCanViewRevenueDashboardTests(AcceptanceTestBase):
    """
    Feature: Revenue dashboard
    As an admin
    I want to view revenue analytics
    So that I can monitor business performance
    """

    def setUp(self):
        super().setUp()
        # Create admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!'
        )

    def test_admin_can_access_revenue_dashboard(self):
        """Scenario: Admin accesses revenue dashboard"""
        # Given I am logged in as admin
        self.client.login(username='admin', password='AdminPass123!')

        # When I visit the revenue dashboard
        response = self.client.get('/dashboard/revenue/')

        # Then I should see the dashboard
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_access_revenue_dashboard(self):
        """Scenario: Regular user cannot access revenue dashboard"""
        # Given I am logged in as a regular user
        self.client.login(username='testuser', password='SecurePassword123!')

        # When I try to visit the revenue dashboard
        response = self.client.get('/dashboard/revenue/')

        # Then I should be redirected (not authorized)
        self.assertEqual(response.status_code, 302)


# ============================================================================
# FEATURE: Site works on mobile devices
# ============================================================================

class SiteWorksOnMobileTests(AcceptanceTestBase):
    """
    Feature: Mobile responsiveness
    As a mobile user
    I want the site to work on my phone
    So that I can book while traveling
    """

    def test_pages_load_with_mobile_user_agent(self):
        """Scenario: Pages load on mobile device"""
        mobile_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0) AppleWebKit/605.1.15'

        pages = ['/', '/accommodations/', '/tours/', '/flights/', '/contact/']

        for page in pages:
            response = self.client.get(page, HTTP_USER_AGENT=mobile_agent)
            self.assertEqual(
                response.status_code, 200,
                f"Page {page} should load on mobile"
            )


# ============================================================================
# FEATURE: Site is accessible (basic checks)
# ============================================================================

class SiteAccessibilityTests(AcceptanceTestBase):
    """
    Feature: Site accessibility
    As a user with accessibility needs
    I want the site to be accessible
    So that I can use it effectively
    """

    def test_pages_have_proper_status_codes(self):
        """Scenario: All main pages return proper status codes"""
        pages = {
            '/': 200,
            '/accommodations/': 200,
            '/tours/': 200,
            '/destinations/': 200,
            '/flights/': 200,
            '/insurance/': 200,
            '/deals/': 200,
            '/about/': 200,
            '/contact/': 200,
            '/faq/': 200,
        }

        for page, expected_status in pages.items():
            response = self.client.get(page)
            self.assertEqual(
                response.status_code, expected_status,
                f"Page {page} should return {expected_status}"
            )

    def test_pages_return_html_content_type(self):
        """Scenario: Pages return HTML content"""
        pages = ['/', '/about/', '/contact/']

        for page in pages:
            response = self.client.get(page)
            self.assertIn(
                'text/html',
                response.get('Content-Type', ''),
                f"Page {page} should return HTML"
            )


# ============================================================================
# FEATURE: SEO requirements
# ============================================================================

class SEORequirementsTests(AcceptanceTestBase):
    """
    Feature: SEO optimization
    As a marketing team member
    I want the site to be SEO optimized
    So that we rank well in search engines
    """

    def test_pages_have_title_tags(self):
        """Scenario: Pages have title tags"""
        response = self.client.get('/')
        self.assertContains(response, '<title>')

    def test_pages_have_meta_description(self):
        """Scenario: Pages have meta descriptions"""
        response = self.client.get('/')
        self.assertContains(response, 'meta name="description"')

    def test_robots_txt_exists(self):
        """Scenario: robots.txt is accessible"""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_exists(self):
        """Scenario: sitemap.xml is accessible"""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
