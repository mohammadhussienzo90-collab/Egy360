# FILE: tours/test_simple.py
# ============================================================
"""
Tests for Tours App

These tests cover:
- Tour categories and operators
- Tour packages and activities
- Tour schedules and availability
- Serializer validation
- Viewset CRUD operations
- Filtering, search, and ordering
- Admin verification endpoints
- Permission and authentication
"""

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser
from destinations.models import City, Attraction
from .models import (
    TourCategory,
    TourOperator,
    Tour,
    TourImage,
    TourSchedule,
)


class TourModelTest(TestCase):
    """
    Tests for Tour models
    """

    def setUp(self):
        """Set up test data"""
        # Create users
        self.tourist = CustomUser.objects.create_user(
            username='tourist',
            email='tourist@example.com',
            password='TouristPass123!',
            user_type='tourist'
        )

        self.operator_user = CustomUser.objects.create_user(
            username='operator',
            email='operator@example.com',
            password='OperatorPass123!',
            user_type='provider'
        )

        # Create destination
        self.city = City.objects.create(
            name='Cairo',
            slug='cairo',
            description='Capital of Egypt'
        )

        self.attraction = Attraction.objects.create(
            name='Pyramids of Giza',
            city=self.city,
            description='Ancient pyramids'
        )

        # Create tour category
        self.category = TourCategory.objects.create(
            name='Cultural',
            description='Cultural tours',
            icon='🏛️'
        )

        # Create tour operator
        self.operator = TourOperator.objects.create(
            name='Cairo Tours',
            user=self.operator_user,
            description='Professional tour company',
            phone_number='+201001234567',
            email='info@cairotours.com',
            license_number='TOUR12345',
            years_of_experience=5,
            is_verified=True,
            is_safe=True
        )

        # Create tour
        self.tour = Tour.objects.create(
            title='Pyramids and Sphinx Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Full day tour of ancient wonders',
            duration_value=8,
            duration_unit='hours',
            difficulty_level='easy',
            min_group_size=1,
            max_group_size=15,
            price_per_person=500.00,
            start_date='2024-01-15',
            available_slots=20,
            language='en',
            guide_name='Ahmed Mohamed',
            is_active=True
        )
        self.tour.attractions.add(self.attraction)

    def test_tour_category_creation(self):
        """Test tour category creation"""
        self.assertEqual(self.category.name, 'Cultural')
        self.assertEqual(self.category.description, 'Cultural tours')
        self.assertEqual(str(self.category), 'Cultural')

    def test_tour_operator_creation(self):
        """Test tour operator creation"""
        self.assertEqual(self.operator.name, 'Cairo Tours')
        self.assertEqual(self.operator.user.username, 'operator')
        self.assertEqual(self.operator.phone_number, '+201001234567')
        self.assertTrue(self.operator.is_verified)
        self.assertTrue(self.operator.is_safe)
        self.assertEqual(self.operator.years_of_experience, 5)

        # Test slug generation
        self.assertEqual(self.operator.slug, 'cairo-tours')

    def test_tour_creation(self):
        """Test tour creation and basic properties"""
        self.assertEqual(self.tour.title, 'Pyramids and Sphinx Tour')
        self.assertEqual(self.tour.operator.name, 'Cairo Tours')
        self.assertEqual(self.tour.category.name, 'Cultural')
        self.assertEqual(self.tour.city.name, 'Cairo')
        self.assertEqual(self.tour.duration_value, 8)
        self.assertEqual(self.tour.duration_unit, 'hours')
        self.assertEqual(self.tour.difficulty_level, 'easy')
        self.assertEqual(self.tour.price_per_person, 500.00)
        self.assertEqual(self.tour.available_slots, 20)
        self.assertTrue(self.tour.is_active)

        # Test attractions relationship
        self.assertEqual(self.tour.attractions.count(), 1)
        self.assertEqual(self.tour.attractions.first().name, 'Pyramids of Giza')

        # Test slug generation
        self.assertEqual(self.tour.slug, 'pyramids-and-sphinx-tour-cairo')

    def test_tour_str_representation(self):
        """Test string representation"""
        self.assertEqual(
            str(self.tour),
            'Pyramids and Sphinx Tour - Cairo'
        )

    def test_tour_operator_str_representation(self):
        """Test operator string representation"""
        self.assertEqual(str(self.operator), 'Cairo Tours')


class TourImageViewTest(TestCase):
    """
    Tests for TourImage model
    """

    def setUp(self):
        """Set up test data"""
        self.city = City.objects.create(name='Luxor')
        self.category = TourCategory.objects.create(name='Historical')

        self.operator_user = CustomUser.objects.create_user(
            username='luxor_guide',
            email='guide@luxor.com',
            password='pass123'
        )

        self.operator = TourOperator.objects.create(
            name='Luxor Guides',
            user=self.operator_user,
            phone_number='+201009876543',
            email='info@luxorguides.com'
        )

        self.tour = Tour.objects.create(
            title='Valley of the Kings Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Ancient tombs exploration',
            duration_value=4,
            duration_unit='hours',
            price_per_person=300.00,
            start_date='2024-01-20',
            available_slots=10
        )

        self.tour_image = TourImage.objects.create(
            tour=self.tour,
            caption='Tomb entrance',
            order=1
        )

    def test_tour_image_creation(self):
        """Test tour image creation"""
        self.assertEqual(self.tour_image.tour.title, 'Valley of the Kings Tour')
        self.assertEqual(self.tour_image.caption, 'Tomb entrance')
        self.assertEqual(self.tour_image.order, 1)

    def test_tour_image_str_representation(self):
        """Test string representation"""
        self.assertEqual(
            str(self.tour_image),
            'Image for Valley of the Kings Tour'
        )


class TourScheduleModelTest(TestCase):
    """
    Tests for TourSchedule model
    """

    def setUp(self):
        """Set up test data"""
        self.city = City.objects.create(name='Aswan')
        self.category = TourCategory.objects.create(name='River')

        self.operator_user = CustomUser.objects.create_user(
            username='aswan_tours',
            email='tours@aswan.com',
            password='pass123'
        )

        self.operator = TourOperator.objects.create(
            name='Aswan River Tours',
            user=self.operator_user,
            phone_number='+201005551234',
            email='info@aswantours.com'
        )

        self.tour = Tour.objects.create(
            title='Nile Felucca Ride',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Traditional boat ride',
            duration_value=2,
            duration_unit='hours',
            price_per_person=150.00,
            start_date='2024-01-25',
            available_slots=8
        )

        self.schedule = TourSchedule.objects.create(
            tour=self.tour,
            start_date='2024-01-25',
            start_time='09:00',
            available_slots=8,
            booked_slots=2,
            price=150.00,
            is_available=True
        )

    def test_tour_schedule_creation(self):
        """Test tour schedule creation"""
        self.assertEqual(self.schedule.tour.title, 'Nile Felucca Ride')
        self.assertEqual(str(self.schedule.start_date), '2024-01-25')
        self.assertEqual(str(self.schedule.start_time), '09:00:00')
        self.assertEqual(self.schedule.available_slots, 8)
        self.assertEqual(self.schedule.booked_slots, 2)
        self.assertEqual(self.schedule.price, 150.00)
        self.assertTrue(self.schedule.is_available)

    def test_tour_schedule_str_representation(self):
        """Test string representation"""
        self.assertEqual(
            str(self.schedule),
            'Nile Felucca Ride - 2024-01-25'
        )


class TourCategoryViewSetTest(APITestCase):
    """
    Tests for TourCategoryViewSet
    """

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create tour categories
        self.category1 = TourCategory.objects.create(
            name='Adventure',
            description='Adventure tours',
            icon='🧗'
        )

        self.category2 = TourCategory.objects.create(
            name='Food',
            description='Food and culinary tours',
            icon='🍲'
        )

        # URLs
        self.category_list_url = reverse('tour-category-list')
        self.category_detail_url = reverse(
            'tour-category-detail',
            kwargs={'pk': self.category1.id}
        )

    def test_category_list_unauthenticated(self):
        """Test category list without authentication"""
        response = self.client.get(self.category_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_category_detail_view(self):
        """Test category detail view"""
        response = self.client.get(self.category_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Adventure')
        self.assertEqual(response.data['description'], 'Adventure tours')


class TourOperatorViewSetTest(APITestCase):
    """
    Tests for TourOperatorViewSet
    """

    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()

        # Create users
        self.tourist = CustomUser.objects.create_user(
            username='tourist',
            email='tourist@example.com',
            password='TouristPass123!',
            user_type='tourist'
        )

        self.provider = CustomUser.objects.create_user(
            username='provider',
            email='provider@example.com',
            password='ProviderPass123!',
            user_type='provider'
        )

        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!'
        )

        # Create tour operators
        self.operator1 = TourOperator.objects.create(
            name='Verified Tours',
            user=self.provider,
            description='Verified tour company',
            phone_number='+201001234567',
            email='verified@tours.com',
            is_verified=True,
            is_safe=True,
            is_active=True
        )

        self.operator2 = TourOperator.objects.create(
            name='Unverified Tours',
            user=self.provider,
            description='Unverified company',
            phone_number='+201009876543',
            email='unverified@tours.com',
            is_verified=False,
            is_safe=True,
            is_active=True
        )

        # URLs
        self.operator_list_url = reverse('tour-operator-list')
        self.operator_detail_url = reverse(
            'tour-operator-detail',
            kwargs={'pk': self.operator1.id}
        )

    def test_operator_list_unauthenticated(self):
        """Test operator list without authentication"""
        response = self.client.get(self.operator_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_operator_list_filter_by_verified(self):
        """Test filtering operators by verification status"""
        response = self.client.get(
            self.operator_list_url,
            {'is_verified': 'true'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Verified Tours'
        )

    def test_operator_list_filter_by_safe(self):
        """Test filtering operators by safety status"""
        response = self.client.get(
            self.operator_list_url,
            {'is_safe': 'true'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_operator_list_search(self):
        """Test searching operators by name"""
        response = self.client.get(
            self.operator_list_url,
            {'search': 'Verified'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Verified Tours'
        )

    def test_operator_detail_view(self):
        """Test operator detail view"""
        response = self.client.get(self.operator_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Verified Tours')
        self.assertEqual(response.data['email'], 'verified@tours.com')
        self.assertTrue(response.data['is_verified'])

    def test_operator_create_authenticated(self):
        """Test creating operator when authenticated"""
        refresh = RefreshToken.for_user(self.provider)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        new_operator_data = {
            'name': 'New Tour Company',
            'description': 'A new tour company',
            'phone_number': '+201005551234',
            'email': 'new@company.com',
            'years_of_experience': 3,
            'has_insurance': True
        }

        response = self.client.post(
            self.operator_list_url,
            new_operator_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Tour Company')

        # Verify operator was created
        operator = TourOperator.objects.get(name='New Tour Company')
        self.assertEqual(operator.phone_number, '+201005551234')
        self.assertEqual(operator.years_of_experience, 3)

    def test_operator_create_unauthenticated(self):
        """Test creating operator without authentication"""
        new_operator_data = {
            'name': 'Unauthorized Operator',
            'description': 'Should not be created',
            'phone_number': '+201000000000',
            'email': 'unauthorized@example.com'
        }

        response = self.client.post(
            self.operator_list_url,
            new_operator_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_operator_verify_endpoint_admin(self):
        """Test operator verification endpoint as admin"""
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        verify_url = reverse(
            'tour-operator-verify',
            kwargs={'pk': self.operator2.id}  # Unverified operator
        )

        response = self.client.post(verify_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Tour operator verified')

        # Refresh operator and verify changes
        self.operator2.refresh_from_db()
        self.assertTrue(self.operator2.is_verified)
        self.assertEqual(self.operator2.verification_status, 'verified')

    def test_operator_verify_endpoint_non_admin(self):
        """Test operator verification endpoint as non-admin"""
        refresh = RefreshToken.for_user(self.provider)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        verify_url = reverse(
            'tour-operator-verify',
            kwargs={'pk': self.operator2.id}
        )

        response = self.client.post(verify_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TourViewSetTest(APITestCase):
    """
    Tests for TourViewSet
    """

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create users
        self.tourist = CustomUser.objects.create_user(
            username='tourist',
            email='tourist@example.com',
            password='TouristPass123!'
        )

        self.provider = CustomUser.objects.create_user(
            username='provider',
            email='provider@example.com',
            password='ProviderPass123!',
            user_type='provider'
        )

        # Create destination and category
        self.city = City.objects.create(name='Cairo', slug='cairo')
        self.category = TourCategory.objects.create(name='Cultural', icon='🏛️')

        # Create operator
        self.operator = TourOperator.objects.create(
            name='Cairo Tours',
            user=self.provider,
            phone_number='+201001234567',
            email='info@cairotours.com',
            is_verified=True
        )

        # Create tours
        self.tour1 = Tour.objects.create(
            title='Pyramids Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Visit ancient pyramids',
            duration_value=4,
            duration_unit='hours',
            difficulty_level='easy',
            price_per_person=400.00,
            start_date='2024-01-15',
            available_slots=15,
            is_active=True,
            is_featured=True
        )

        self.tour2 = Tour.objects.create(
            title='Cairo City Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Explore Cairo city',
            duration_value=6,
            duration_unit='hours',
            difficulty_level='moderate',
            price_per_person=300.00,
            start_date='2024-01-16',
            available_slots=10,
            is_active=True,
            is_featured=False
        )

        # URLs
        self.tour_list_url = reverse('tour-list')
        self.tour_detail_url = reverse(
            'tour-detail',
            kwargs={'pk': self.tour1.id}
        )

    def test_tour_list_unauthenticated(self):
        """Test tour list without authentication"""
        response = self.client.get(self.tour_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_tour_list_filter_by_city(self):
        """Test filtering tours by city"""
        response = self.client.get(
            self.tour_list_url,
            {'city': self.city.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_tour_list_filter_by_category(self):
        """Test filtering tours by category"""
        response = self.client.get(
            self.tour_list_url,
            {'category': self.category.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_tour_list_filter_by_difficulty(self):
        """Test filtering tours by difficulty level"""
        response = self.client.get(
            self.tour_list_url,
            {'difficulty_level': 'easy'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Pyramids Tour'
        )

    def test_tour_list_filter_by_featured(self):
        """Test filtering tours by featured status"""
        response = self.client.get(
            self.tour_list_url,
            {'is_featured': 'true'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Pyramids Tour'
        )

    def test_tour_list_search(self):
        """Test searching tours by title"""
        response = self.client.get(
            self.tour_list_url,
            {'search': 'Pyramids'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Pyramids Tour'
        )

    def test_tour_list_ordering_by_price(self):
        """Test ordering tours by price"""
        response = self.client.get(
            self.tour_list_url,
            {'ordering': 'price_per_person'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # Cheaper tour should come first when ordering by price ascending
        self.assertEqual(
            response.data['results'][0]['title'],
            'Cairo City Tour'
        )

    def test_tour_detail_view(self):
        """Test tour detail view"""
        response = self.client.get(self.tour_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pyramids Tour')
        self.assertEqual(response.data['operator']['name'], 'Cairo Tours')
        self.assertEqual(response.data['category']['name'], 'Cultural')
        self.assertEqual(response.data['price_per_person'], '400.00')
        self.assertEqual(response.data['difficulty_level'], 'easy')

    def test_tour_create_authenticated(self):
        """Test creating tour when authenticated"""
        refresh = RefreshToken.for_user(self.provider)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        new_tour_data = {
            'title': 'New Cairo Adventure',
            'operator': self.operator.id,
            'category': self.category.id,
            'city': self.city.id,
            'description': 'A new exciting tour',
            'duration_value': 5,
            'duration_unit': 'hours',
            'difficulty_level': 'moderate',
            'min_group_size': 2,
            'max_group_size': 12,
            'price_per_person': 350.00,
            'start_date': '2024-02-01',
            'available_slots': 8,
            'language': 'en',
            'guide_name': 'Tour Guide',
            'is_active': True
        }

        response = self.client.post(
            self.tour_list_url,
            new_tour_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Cairo Adventure')

        # Verify tour was created
        tour = Tour.objects.get(title='New Cairo Adventure')
        self.assertEqual(tour.price_per_person, 350.00)
        self.assertEqual(tour.difficulty_level, 'moderate')

    def test_tour_create_unauthenticated(self):
        """Test creating tour without authentication"""
        new_tour_data = {
            'title': 'Unauthorized Tour',
            'operator': self.operator.id,
            'category': self.category.id,
            'city': self.city.id,
            'description': 'Should not be created',
            'duration_value': 3,
            'duration_unit': 'hours',
            'price_per_person': 200.00,
            'start_date': '2024-02-01',
            'available_slots': 5
        }

        response = self.client.post(
            self.tour_list_url,
            new_tour_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TourScheduleViewSetTest(APITestCase):
    """
    Tests for TourScheduleViewSet
    """

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            user_type='provider'
        )

        # Create tour
        self.city = City.objects.create(name='Alexandria')
        self.category = TourCategory.objects.create(name='Coastal')

        self.operator = TourOperator.objects.create(
            name='Alexandria Tours',
            user=self.user,
            phone_number='+201001234567',
            email='info@alexandria.com'
        )

        self.tour = Tour.objects.create(
            title='Alexandria Beach Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Beach and city tour',
            duration_value=6,
            duration_unit='hours',
            price_per_person=250.00,
            start_date='2024-01-20',
            available_slots=12
        )

        # Create schedules
        self.schedule1 = TourSchedule.objects.create(
            tour=self.tour,
            start_date='2024-01-20',
            start_time='08:00',
            available_slots=12,
            booked_slots=3,
            price=250.00,
            is_available=True
        )

        self.schedule2 = TourSchedule.objects.create(
            tour=self.tour,
            start_date='2024-01-21',
            start_time='09:00',
            available_slots=8,
            booked_slots=0,
            price=250.00,
            is_available=False
        )

        # URLs
        self.schedule_list_url = reverse('tour-schedule-list')
        self.schedule_detail_url = reverse(
            'tour-schedule-detail',
            kwargs={'pk': self.schedule1.id}
        )

    def test_schedule_list_unauthenticated(self):
        """Test schedule list without authentication"""
        response = self.client.get(self.schedule_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only available schedules

    def test_schedule_list_filter_by_tour(self):
        """Test filtering schedules by tour"""
        response = self.client.get(
            self.schedule_list_url,
            {'tour': self.tour.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_schedule_list_filter_by_availability(self):
        """Test filtering schedules by availability"""
        response = self.client.get(
            self.schedule_list_url,
            {'is_available': 'true'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['start_date'],
            '2024-01-20'
        )

    def test_schedule_detail_view(self):
        """Test schedule detail view"""
        response = self.client.get(self.schedule_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['start_date'], '2024-01-20')
        self.assertEqual(response.data['available_slots'], 12)
        self.assertEqual(response.data['booked_slots'], 3)
        self.assertEqual(response.data['price'], '250.00')
        self.assertTrue(response.data['is_available'])

    def test_schedule_create_authenticated(self):
        """Test creating schedule when authenticated"""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        new_schedule_data = {
            'tour': self.tour.id,
            'start_date': '2024-01-22',
            'start_time': '10:00',
            'available_slots': 10,
            'booked_slots': 0,
            'price': 250.00,
            'is_available': True
        }

        response = self.client.post(
            self.schedule_list_url,
            new_schedule_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['start_date'], '2024-01-22')
        self.assertEqual(response.data['available_slots'], 10)

        # Verify schedule was created
        schedule = TourSchedule.objects.get(start_date='2024-01-22')
        self.assertEqual(schedule.available_slots, 10)
        self.assertEqual(schedule.price, 250.00)

    def test_schedule_create_unauthenticated(self):
        """Test creating schedule without authentication"""
        new_schedule_data = {
            'tour': self.tour.id,
            'start_date': '2024-01-23',
            'available_slots': 5,
            'booked_slots': 0,
            'price': 250.00
        }

        response = self.client.post(
            self.schedule_list_url,
            new_schedule_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TourSerializerValidationTest(APITestCase):
    """
    Tests for serializer validation
    """

    def setUp(self):
        """Set up test data"""
        self.city = City.objects.create(name='Giza')
        self.category = TourCategory.objects.create(name='Adventure')

        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            user_type='provider'
        )

        self.operator = TourOperator.objects.create(
            name='Test Operator',
            user=self.user,
            phone_number='+201001234567',
            email='test@operator.com'
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.tour_list_url = reverse('tour-list')

    def test_tour_price_validation(self):
        """Test tour price validation"""
        invalid_data = {
            'title': 'Invalid Price Tour',
            'operator': self.operator.id,
            'category': self.category.id,
            'city': self.city.id,
            'description': 'Tour with invalid price',
            'duration_value': 4,
            'duration_unit': 'hours',
            'price_per_person': -100.00,  # Invalid negative price
            'start_date': '2024-01-15',
            'available_slots': 10
        }

        response = self.client.post(
            self.tour_list_url,
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price_per_person', response.data)

    def test_tour_duration_validation(self):
        """Test tour duration validation"""
        invalid_data = {
            'title': 'Invalid Duration Tour',
            'operator': self.operator.id,
            'category': self.category.id,
            'city': self.city.id,
            'description': 'Tour with invalid duration',
            'duration_value': 0,  # Invalid duration
            'duration_unit': 'hours',
            'price_per_person': 200.00,
            'start_date': '2024-01-15',
            'available_slots': 10
        }

        response = self.client.post(
            self.tour_list_url,
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('duration_value', response.data)

    def test_tour_group_size_validation(self):
        """Test tour group size validation"""
        invalid_data = {
            'title': 'Invalid Group Tour',
            'operator': self.operator.id,
            'category': self.category.id,
            'city': self.city.id,
            'description': 'Tour with invalid group sizes',
            'duration_value': 4,
            'duration_unit': 'hours',
            'price_per_person': 200.00,
            'min_group_size': 10,
            'max_group_size': 5,  # Max < min
            'start_date': '2024-01-15',
            'available_slots': 10
        }

        response = self.client.post(
            self.tour_list_url,
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)