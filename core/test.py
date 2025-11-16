"""
Egy360 Core App Tests - UPDATED WITH BOOKING FLOW
Complete test suite for all views including booking

Run tests with:
    python manage.py test core
"""

from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTests(TestCase):
    """Test cases for the homepage view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('home')

    def test_home_page_status_code(self):
        """Test that homepage returns 200 status code"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Test that homepage uses the correct template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_contains_expected_content(self):
        """Test that homepage contains expected HTML elements"""
        response = self.client.get(self.url)
        self.assertContains(response, 'EGY')
        self.assertContains(response, '360')
        self.assertContains(response, 'Discover Egypt')

    def test_home_page_accessible_by_name(self):
        """Test that homepage is accessible via URL name"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class AccommodationSearchViewTests(TestCase):
    """Test cases for accommodation search view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('accommodation-search')

    def test_accommodation_search_status_code(self):
        """Test that search page returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_accommodation_search_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accommodation_search.html')

    def test_accommodation_search_with_parameters(self):
        """Test search with query parameters"""
        response = self.client.get(self.url, {
            'city': 'Cairo',
            'check_in': '2024-12-25',
            'check_out': '2024-12-28',
            'guests': '2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['city'], 'Cairo')
        self.assertEqual(response.context['check_in'], '2024-12-25')
        self.assertEqual(response.context['check_out'], '2024-12-28')
        self.assertEqual(response.context['guests'], '2')

    def test_accommodation_search_empty_parameters(self):
        """Test search without parameters uses defaults"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['city'], '')
        self.assertEqual(response.context['guests'], '2')

    def test_accommodation_search_contains_filters(self):
        """Test that search page contains filter elements"""
        response = self.client.get(self.url)
        self.assertContains(response, 'filter')
        self.assertContains(response, 'search')


class AccommodationDetailViewTests(TestCase):
    """Test cases for accommodation detail view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_accommodation_detail_status_code(self):
        """Test that detail page returns 200"""
        url = reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_accommodation_detail_uses_correct_template(self):
        """Test correct template is used"""
        url = reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'accommodation_detail.html')

    def test_accommodation_detail_with_different_ids(self):
        """Test detail page with different accommodation IDs"""
        for accommodation_id in [1, 2, 3, 10, 99]:
            url = reverse('accommodation-detail', kwargs={'accommodation_id': accommodation_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['accommodation_id'], accommodation_id)

    def test_accommodation_detail_contains_booking_form(self):
        """Test that detail page contains booking elements"""
        url = reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'booking')
        self.assertContains(response, 'Book')

    def test_accommodation_detail_contains_gallery(self):
        """Test that detail page contains gallery elements"""
        url = reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'gallery')


class TourListingViewTests(TestCase):
    """Test cases for tour listing view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('tour-listing')

    def test_tour_listing_status_code(self):
        """Test that tour listing returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_tour_listing_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'tour_listing.html')

    def test_tour_listing_with_parameters(self):
        """Test tour listing with query parameters"""
        response = self.client.get(self.url, {
            'city': 'Luxor',
            'date': '2024-12-25',
            'category': 'historical',
            'travelers': '2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['city'], 'Luxor')
        self.assertEqual(response.context['date'], '2024-12-25')
        self.assertEqual(response.context['category'], 'historical')
        self.assertEqual(response.context['travelers'], '2')

    def test_tour_listing_empty_parameters(self):
        """Test tour listing without parameters uses defaults"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['city'], '')
        self.assertEqual(response.context['travelers'], '2')

    def test_tour_listing_contains_filters(self):
        """Test that tour listing contains filter elements"""
        response = self.client.get(self.url)
        self.assertContains(response, 'filter')
        self.assertContains(response, 'category')
        self.assertContains(response, 'duration')


class TourDetailViewTests(TestCase):
    """Test cases for tour detail view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_tour_detail_status_code(self):
        """Test that tour detail returns 200"""
        url = reverse('tour-detail', kwargs={'tour_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tour_detail_uses_correct_template(self):
        """Test correct template is used"""
        url = reverse('tour-detail', kwargs={'tour_id': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'tour_detail.html')

    def test_tour_detail_with_different_ids(self):
        """Test detail page with different tour IDs"""
        for tour_id in [1, 2, 3, 10, 99]:
            url = reverse('tour-detail', kwargs={'tour_id': tour_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['tour_id'], tour_id)

    def test_tour_detail_contains_booking_form(self):
        """Test that tour detail contains booking elements"""
        url = reverse('tour-detail', kwargs={'tour_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'booking')
        self.assertContains(response, 'Book')

    def test_tour_detail_contains_itinerary(self):
        """Test that tour detail contains itinerary section"""
        url = reverse('tour-detail', kwargs={'tour_id': 1})
        response = self.client.get(url)
        self.assertContains(response, 'itinerary')


class UserDashboardViewTests(TestCase):
    """Test cases for user dashboard view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('user-dashboard')

    def test_user_dashboard_status_code(self):
        """Test that dashboard returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_dashboard_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user_dashboard.html')

    def test_user_dashboard_contains_navigation(self):
        """Test that dashboard contains navigation elements"""
        response = self.client.get(self.url)
        self.assertContains(response, 'dashboard')
        self.assertContains(response, 'overview-section')
        self.assertContains(response, 'bookings-section')

    def test_user_dashboard_contains_sections(self):
        """Test that dashboard contains all main sections"""
        response = self.client.get(self.url)
        self.assertContains(response, 'overview-section')
        self.assertContains(response, 'bookings-section')
        self.assertContains(response, 'favorites-section')
        self.assertContains(response, 'reviews-section')
        self.assertContains(response, 'profile-section')
        self.assertContains(response, 'settings-section')

    def test_user_dashboard_accessible_by_name(self):
        """Test that dashboard is accessible via URL name"""
        response = self.client.get(reverse('user-dashboard'))
        self.assertEqual(response.status_code, 200)


# ==================== NEW: BOOKING FLOW TESTS ====================

class BookingCheckoutViewTests(TestCase):
    """Test cases for booking checkout view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('booking-checkout')

    def test_booking_checkout_status_code(self):
        """Test that checkout page returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_booking_checkout_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'booking_checkout.html')

    def test_booking_checkout_accommodation_type(self):
        """Test checkout with accommodation type"""
        response = self.client.get(self.url, {
            'type': 'accommodation',
            'id': '1',
            'check_in': '2024-12-25',
            'check_out': '2024-12-28',
            'guests': '2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking_type'], 'accommodation')
        self.assertEqual(response.context['item_id'], '1')

    def test_booking_checkout_tour_type(self):
        """Test checkout with tour type"""
        response = self.client.get(self.url, {
            'type': 'tour',
            'id': '1',
            'tour_date': '2024-12-25',
            'guests': '2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking_type'], 'tour')

    def test_booking_checkout_contains_form_fields(self):
        """Test that checkout contains necessary form fields"""
        response = self.client.get(self.url)
        self.assertContains(response, 'firstName')
        self.assertContains(response, 'email')
        self.assertContains(response, 'phone')
        self.assertContains(response, 'Complete Booking')

    def test_booking_checkout_accessible_by_name(self):
        """Test that checkout is accessible via URL name"""
        response = self.client.get(reverse('booking-checkout'))
        self.assertEqual(response.status_code, 200)


class BookingConfirmationViewTests(TestCase):
    """Test cases for booking confirmation view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('booking-confirmation')

    def test_booking_confirmation_status_code(self):
        """Test that confirmation page returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_booking_confirmation_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'booking_confirmation.html')

    def test_booking_confirmation_with_booking_id(self):
        """Test confirmation with booking ID parameter"""
        response = self.client.get(self.url, {'id': 'BK12345678'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking_id'], 'BK12345678')

    def test_booking_confirmation_contains_success_elements(self):
        """Test that confirmation contains success elements"""
        response = self.client.get(self.url)
        self.assertContains(response, 'Confirmed')
        self.assertContains(response, 'Booking Reference')
        self.assertContains(response, 'bookingReference')

    def test_booking_confirmation_accessible_by_name(self):
        """Test that confirmation is accessible via URL name"""
        response = self.client.get(reverse('booking-confirmation'))
        self.assertEqual(response.status_code, 200)


class URLTests(TestCase):
    """Test URL patterns and routing"""

    def test_all_urls_resolve(self):
        """Test that all URLs resolve correctly"""
        urls = [
            ('home', {}),
            ('accommodation-search', {}),
            ('accommodation-detail', {'accommodation_id': 1}),
            ('tour-listing', {}),
            ('tour-detail', {'tour_id': 1}),
            ('user-dashboard', {}),
            ('booking-checkout', {}),
            ('booking-confirmation', {}),
        ]

        for url_name, kwargs in urls:
            url = reverse(url_name, kwargs=kwargs)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                f"URL '{url_name}' did not return 200"
            )

    def test_url_patterns_are_correct(self):
        """Test that URL patterns match expected paths"""
        test_cases = [
            ('home', {}, '/'),
            ('accommodation-search', {}, '/search/accommodations/'),
            ('accommodation-detail', {'accommodation_id': 1}, '/accommodations/1/'),
            ('tour-listing', {}, '/tours/'),
            ('tour-detail', {'tour_id': 1}, '/tours/1/'),
            ('user-dashboard', {}, '/dashboard/'),
            ('booking-checkout', {}, '/book/checkout/'),
            ('booking-confirmation', {}, '/booking/confirmation/'),
        ]

        for url_name, kwargs, expected_path in test_cases:
            url = reverse(url_name, kwargs=kwargs)
            self.assertEqual(
                url,
                expected_path,
                f"URL '{url_name}' does not match expected path"
            )


class StaticFilesTests(TestCase):
    """Test that static files are properly configured"""

    def test_css_files_load(self):
        """Test that CSS files are referenced in templates"""
        test_cases = [
            (reverse('home'), 'home_styles.css'),
            (reverse('accommodation-search'), 'accommodation_search.css'),
            (reverse('accommodation-detail', kwargs={'accommodation_id': 1}), 'accommodation_detail.css'),
            (reverse('tour-listing'), 'tour_listing.css'),
            (reverse('tour-detail', kwargs={'tour_id': 1}), 'tour_detail.css'),
            (reverse('user-dashboard'), 'user_dashboard.css'),
            (reverse('booking-checkout'), 'booking_checkout.css'),
            (reverse('booking-confirmation'), 'booking_confirmation.css'),
        ]

        for url, css_file in test_cases:
            response = self.client.get(url)
            self.assertContains(
                response,
                css_file,
                msg_prefix=f"CSS file '{css_file}' not found in template at {url}"
            )

    def test_js_files_load(self):
        """Test that JavaScript files are referenced in templates"""
        test_cases = [
            (reverse('home'), 'home_script.js'),
            (reverse('accommodation-search'), 'accommodation_search.js'),
            (reverse('accommodation-detail', kwargs={'accommodation_id': 1}), 'accommodation_detail.js'),
            (reverse('tour-listing'), 'tour_listing.js'),
            (reverse('tour-detail', kwargs={'tour_id': 1}), 'tour_detail.js'),
            (reverse('user-dashboard'), 'user_dashboard.js'),
            (reverse('booking-checkout'), 'booking_checkout.js'),
            (reverse('booking-confirmation'), 'booking_confirmation.js'),
        ]

        for url, js_file in test_cases:
            response = self.client.get(url)
            self.assertContains(
                response,
                js_file,
                msg_prefix=f"JavaScript file '{js_file}' not found in template at {url}"
            )


class IntegrationTests(TestCase):
    """Test integration between different views"""

    def test_navigation_between_pages(self):
        """Test that navigation links work between pages"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('accommodation-search'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('accommodation-detail', kwargs={'accommodation_id': 1}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('tour-listing'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('tour-detail', kwargs={'tour_id': 1}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('user-dashboard'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('booking-checkout'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('booking-confirmation'))
        self.assertEqual(response.status_code, 200)

    def test_search_to_detail_flow(self):
        """Test user flow from search to detail page"""
        search_response = self.client.get(
            reverse('accommodation-search'),
            {'city': 'Cairo', 'guests': '2'}
        )
        self.assertEqual(search_response.status_code, 200)

        detail_response = self.client.get(
            reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        )
        self.assertEqual(detail_response.status_code, 200)

    def test_tour_search_to_detail_flow(self):
        """Test user flow from tour listing to detail"""
        listing_response = self.client.get(
            reverse('tour-listing'),
            {'city': 'Luxor', 'category': 'historical'}
        )
        self.assertEqual(listing_response.status_code, 200)

        detail_response = self.client.get(
            reverse('tour-detail', kwargs={'tour_id': 1})
        )
        self.assertEqual(detail_response.status_code, 200)

    def test_booking_flow_integration(self):
        """Test complete booking flow from detail to confirmation"""
        # View accommodation detail
        detail_response = self.client.get(
            reverse('accommodation-detail', kwargs={'accommodation_id': 1})
        )
        self.assertEqual(detail_response.status_code, 200)

        # Go to checkout
        checkout_response = self.client.get(
            reverse('booking-checkout'),
            {
                'type': 'accommodation',
                'id': '1',
                'check_in': '2024-12-25',
                'check_out': '2024-12-28',
                'guests': '2'
            }
        )
        self.assertEqual(checkout_response.status_code, 200)

        # View confirmation
        confirmation_response = self.client.get(
            reverse('booking-confirmation'),
            {'id': 'BK12345678'}
        )
        self.assertEqual(confirmation_response.status_code, 200)


class ResponseContentTests(TestCase):
    """Test that responses contain expected content"""

    def test_all_pages_contain_navbar(self):
        """Test that all pages include navigation bar"""
        urls = [
            reverse('home'),
            reverse('accommodation-search'),
            reverse('accommodation-detail', kwargs={'accommodation_id': 1}),
            reverse('tour-listing'),
            reverse('tour-detail', kwargs={'tour_id': 1}),
            reverse('user-dashboard'),
            reverse('booking-checkout'),
            reverse('booking-confirmation'),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertContains(
                response,
                'navbar',
                msg_prefix=f"Navbar not found on {url}"
            )

    def test_home_page_contains_footer(self):
        """Test that homepage contains footer"""
        response = self.client.get(reverse('home'))
        self.assertContains(
            response,
            'footer',
            msg_prefix="Footer not found on home page"
        )


"""
Test Summary:
-------------
Total: 48 tests across 12 test classes (10 new booking tests added)

NEW TESTS:
- BookingCheckoutViewTests (6 tests)
- BookingConfirmationViewTests (5 tests)
- Updated IntegrationTests (1 new test for booking flow)
- Updated URL and Static Files tests

Run: python manage.py test core
Expected: Ran 48 tests ... OK ✅
"""