# FILE: destinations/test_simple.py
# ============================================================
"""
Tests for Destinations App

These tests cover:
- Countries listing
- Cities listing, filtering, and search
- Attractions listing, filtering, and search
- Travel guides listing and filtering
- Detail views for all models
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Country, City, Attraction, TravelGuide


class DestinationsTestCase(TestCase):
    """Test suite for Destinations app"""

    def setUp(self):
        """Set up test client and sample data"""
        self.client = APIClient()

        # Create test country
        self.egypt = Country.objects.create(
            name='Egypt',
            code='EG',
            flag_emoji='🇪🇬',
            description='Land of Pharaohs'
        )

        # Create test cities
        self.cairo = City.objects.create(
            name='Cairo',
            country=self.egypt,
            description='Capital city of Egypt',
            is_popular=True,
            population=20000000,
            best_time_to_visit='October to April'
        )

        self.luxor = City.objects.create(
            name='Luxor',
            country=self.egypt,
            description='Ancient city with temples',
            is_popular=True,
            population=500000,
            best_time_to_visit='October to April'
        )

        self.aswan = City.objects.create(
            name='Aswan',
            country=self.egypt,
            description='Southern city on the Nile',
            is_popular=False,
            population=300000
        )

        # Create test attractions
        self.pyramids = Attraction.objects.create(
            name='Pyramids of Giza',
            city=self.cairo,
            category='monument',
            description='Ancient pyramids',
            entry_fee=200.00,
            is_safe=True,
            opening_hours='8 AM - 5 PM'
        )

        self.karnak = Attraction.objects.create(
            name='Karnak Temple',
            city=self.luxor,
            category='temple',
            description='Ancient temple complex',
            entry_fee=150.00,
            is_safe=True,
            opening_hours='6 AM - 6 PM'
        )

        # Create test travel guide
        self.safety_guide = TravelGuide.objects.create(
            title='Safety Tips for Egypt',
            city=self.cairo,
            content='Important safety information for tourists',
            category='safety',
            is_published=True,
            author='Admin'
        )

        self.unpublished_guide = TravelGuide.objects.create(
            title='Draft Guide',
            city=self.cairo,
            content='This is not published yet',
            category='other',
            is_published=False,
            author='Admin'
        )

    # ================================================================
    # COUNTRY TESTS
    # ================================================================

    def test_list_countries(self):
        """Test listing all countries"""
        url = reverse('country-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Egypt')

    def test_retrieve_country_detail(self):
        """Test retrieving specific country"""
        url = reverse('country-detail', kwargs={'pk': self.egypt.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Egypt')
        self.assertEqual(response.data['code'], 'EG')

    # ================================================================
    # CITY TESTS
    # ================================================================

    def test_list_cities(self):
        """Test listing all cities"""
        url = reverse('city-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_cities_by_country(self):
        """Test filtering cities by country"""
        url = reverse('city-list')
        response = self.client.get(url, {'country': self.egypt.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_cities_by_popularity(self):
        """Test filtering cities by popularity"""
        url = reverse('city-list')
        response = self.client.get(url, {'is_popular': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_cities(self):
        """Test searching cities by name"""
        url = reverse('city-list')
        response = self.client.get(url, {'search': 'Cairo'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Cairo')

    def test_retrieve_city_detail(self):
        """Test retrieving specific city with nested country"""
        url = reverse('city-detail', kwargs={'pk': self.cairo.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cairo')
        self.assertIn('country', response.data)
        self.assertEqual(response.data['country']['name'], 'Egypt')

    def test_order_cities_by_name(self):
        """Test ordering cities by name"""
        url = reverse('city-list')
        response = self.client.get(url, {'ordering': 'name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cities = response.data['results']
        self.assertEqual(cities[0]['name'], 'Aswan')
        self.assertEqual(cities[1]['name'], 'Cairo')
        self.assertEqual(cities[2]['name'], 'Luxor')

    # ================================================================
    # ATTRACTION TESTS
    # ================================================================

    def test_list_attractions(self):
        """Test listing all attractions"""
        url = reverse('attraction-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_attractions_by_city(self):
        """Test filtering attractions by city"""
        url = reverse('attraction-list')
        response = self.client.get(url, {'city': self.cairo.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Pyramids of Giza')

    def test_filter_attractions_by_category(self):
        """Test filtering attractions by category"""
        url = reverse('attraction-list')
        response = self.client.get(url, {'category': 'temple'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Karnak Temple')

    def test_filter_attractions_by_safety(self):
        """Test filtering attractions by safety"""
        url = reverse('attraction-list')
        response = self.client.get(url, {'is_safe': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_attractions(self):
        """Test searching attractions by name"""
        url = reverse('attraction-list')
        response = self.client.get(url, {'search': 'Pyramids'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Pyramids of Giza')

    def test_retrieve_attraction_detail(self):
        """Test retrieving specific attraction"""
        url = reverse('attraction-detail', kwargs={'pk': self.pyramids.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Pyramids of Giza')
        self.assertEqual(response.data['entry_fee'], '200.00')
        self.assertEqual(response.data['opening_hours'], '8 AM - 5 PM')

    def test_order_attractions_by_rating(self):
        """Test ordering attractions by rating"""
        url = reverse('attraction-list')
        response = self.client.get(url, {'ordering': '-average_rating'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    # ================================================================
    # TRAVEL GUIDE TESTS
    # ================================================================

    def test_list_travel_guides(self):
        """Test listing published travel guides"""
        url = reverse('guide-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only published guides should be visible
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Safety Tips for Egypt')

    def test_filter_guides_by_city(self):
        """Test filtering guides by city"""
        url = reverse('guide-list')
        response = self.client.get(url, {'city': self.cairo.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_guides_by_category(self):
        """Test filtering guides by category"""
        url = reverse('guide-list')
        response = self.client.get(url, {'category': 'safety'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], 'safety')

    def test_search_travel_guides(self):
        """Test searching guides by title"""
        url = reverse('guide-list')
        response = self.client.get(url, {'search': 'Safety'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_guide_detail(self):
        """Test retrieving specific travel guide"""
        url = reverse('guide-detail', kwargs={'pk': self.safety_guide.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Safety Tips for Egypt')
        self.assertEqual(response.data['category'], 'safety')

    def test_unpublished_guides_not_visible(self):
        """Test unpublished guides are not returned"""
        url = reverse('guide-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should not include unpublished guide
        guide_titles = [guide['title'] for guide in response.data['results']]
        self.assertNotIn('Draft Guide', guide_titles)


# ============================================================
# HOW TO RUN THESE TESTS
# ============================================================
"""
Run all destinations tests:
    python manage.py test destinations

Run specific test class:
    python manage.py test destinations.tests.DestinationsTestCase

Run specific test method:
    python manage.py test destinations.tests.DestinationsTestCase.test_list_cities

Run with verbose output:
    python manage.py test destinations --verbosity=2
"""