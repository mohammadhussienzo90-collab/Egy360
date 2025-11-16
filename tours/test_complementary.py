"""
COMPLEMENTARY Tests for Tours App
Filling gaps in existing test coverage
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser
from destinations.models import City, Attraction
from .models import TourCategory, TourOperator, Tour, TourImage, TourSchedule


class ToursEdgeCaseTests(APITestCase):
    """
    Edge cases and error conditions not covered in main tests
    """

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.tourist = CustomUser.objects.create_user(
            username='edgetourist',
            email='edge@tourist.com',
            password='EdgePass123!',
            user_type='tourist'
        )

        self.provider = CustomUser.objects.create_user(
            username='edgeprovider',
            email='edge@provider.com',
            password='EdgePass123!',
            user_type='provider'
        )

        # Create basic data
        self.city = City.objects.create(name='Edge City', slug='edge-city')
        self.category = TourCategory.objects.create(name='Edge Category')

        self.operator = TourOperator.objects.create(
            name='Edge Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='edge@operator.com'
        )

        self.tour = Tour.objects.create(
            title='Edge Case Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Testing edge cases',
            duration_value=1,
            duration_unit='hours',
            price_per_person=100.00,
            start_date='2024-12-01',
            available_slots=5
        )

    def test_tour_duplicate_slug_prevention(self):
        """Test that duplicate slugs are handled gracefully"""
        # Create tour with same title and city (should generate same slug)
        duplicate_tour = Tour.objects.create(
            title='Edge Case Tour',  # Same title
            operator=self.operator,
            category=self.category,
            city=self.city,  # Same city
            description='Duplicate tour test',
            duration_value=2,
            duration_unit='hours',
            price_per_person=150.00,
            start_date='2024-12-02',
            available_slots=3
        )

        # Should have different slugs due to auto-append
        self.assertNotEqual(self.tour.slug, duplicate_tour.slug)
        self.assertIn('edge-case-tour-edge-city', duplicate_tour.slug)

    def test_tour_operator_unique_user_constraint(self):
        """Test that one user can only have one tour operator"""
        # Try to create another operator with same user
        with self.assertRaises(Exception):  # Should raise integrity error
            TourOperator.objects.create(
                name='Duplicate Operator',
                user=self.provider,  # Same user
                phone_number='+201000000001',
                email='duplicate@operator.com'
            )

    def test_tour_schedule_unique_date_constraint(self):
        """Test unique constraint on tour + start_date"""
        schedule1 = TourSchedule.objects.create(
            tour=self.tour,
            start_date='2024-12-01',
            available_slots=5,
            price=100.00
        )

        # Try to create duplicate schedule
        with self.assertRaises(Exception):
            TourSchedule.objects.create(
                tour=self.tour,
                start_date='2024-12-01',  # Same date
                available_slots=3,
                price=100.00
            )

    def test_tour_max_capacity_validation(self):
        """Test that booked slots don't exceed available slots"""
        schedule = TourSchedule.objects.create(
            tour=self.tour,
            start_date='2024-12-03',
            available_slots=5,
            booked_slots=0,
            price=100.00
        )

        # Try to set booked_slots > available_slots
        schedule.booked_slots = 10  # More than available
        with self.assertRaises(Exception):
            schedule.save()


class ToursIntegrationTests(APITestCase):
    """
    Integration tests with other apps
    """

    def setUp(self):
        self.client = APIClient()

        self.provider = CustomUser.objects.create_user(
            username='integration',
            email='integration@test.com',
            password='Integration123!',
            user_type='provider'
        )

        self.city = City.objects.create(name='Integration City')
        self.category = TourCategory.objects.create(name='Integration')

        self.operator = TourOperator.objects.create(
            name='Integration Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='integration@operator.com'
        )

    def test_tour_with_multiple_attractions(self):
        """Test tour with multiple attractions integration"""
        attraction1 = Attraction.objects.create(
            name='Integration Attraction 1',
            city=self.city
        )
        attraction2 = Attraction.objects.create(
            name='Integration Attraction 2',
            city=self.city
        )

        tour = Tour.objects.create(
            title='Multi-Attraction Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Tour with multiple attractions',
            duration_value=6,
            duration_unit='hours',
            price_per_person=300.00,
            start_date='2024-12-01',
            available_slots=10
        )

        tour.attractions.add(attraction1, attraction2)

        self.assertEqual(tour.attractions.count(), 2)
        self.assertIn(attraction1, tour.attractions.all())
        self.assertIn(attraction2, tour.attractions.all())

    def test_tour_operator_reviews_integration(self):
        """Test integration with reviews system"""
        # Simulate review impact on operator ratings
        self.operator.average_rating = 4.5
        self.operator.total_reviews = 10
        self.operator.save()

        # Verify rating affects operator visibility
        highly_rated_operator = TourOperator.objects.create(
            name='Highly Rated Operator',
            user=self.provider,
            phone_number='+201000000001',
            email='rated@operator.com',
            average_rating=4.8,
            total_reviews=15
        )

        # Higher rated operator should appear first in default ordering
        operators = TourOperator.objects.all()
        self.assertEqual(operators.first(), highly_rated_operator)


class ToursPerformanceTests(TestCase):
    """
    Performance and scalability tests
    """

    def setUp(self):
        self.city = City.objects.create(name='Performance City')
        self.category = TourCategory.objects.create(name='Performance')

        self.provider = CustomUser.objects.create_user(
            username='performance',
            email='performance@test.com',
            password='Performance123!',
            user_type='provider'
        )

        self.operator = TourOperator.objects.create(
            name='Performance Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='performance@operator.com'
        )

    def test_bulk_tour_creation_performance(self):
        """Test performance of creating multiple tours"""
        import time

        start_time = time.time()

        # Create 100 tours
        for i in range(100):
            Tour.objects.create(
                title=f'Performance Tour {i}',
                operator=self.operator,
                category=self.category,
                city=self.city,
                description=f'Performance test tour {i}',
                duration_value=2,
                duration_unit='hours',
                price_per_person=100.00 + i,
                start_date='2024-12-01',
                available_slots=10
            )

        end_time = time.time()
        creation_time = end_time - start_time

        # Should create 100 tours in reasonable time (adjust threshold as needed)
        self.assertLess(creation_time, 5.0)  # 5 seconds threshold
        self.assertEqual(Tour.objects.count(), 100)

    def test_tour_query_performance(self):
        """Test performance of complex tour queries"""
        # Create test data
        for i in range(50):
            Tour.objects.create(
                title=f'Query Tour {i}',
                operator=self.operator,
                category=self.category,
                city=self.city,
                description=f'Query test tour {i}',
                duration_value=2,
                duration_unit='hours',
                price_per_person=200.00,
                start_date='2024-12-01',
                available_slots=10,
                is_active=(i % 2 == 0),  # Half active
                is_featured=(i % 5 == 0)  # Some featured
            )

        import time
        start_time = time.time()

        # Complex query with multiple filters
        featured_tours = Tour.objects.filter(
            city=self.city,
            is_active=True,
            is_featured=True,
            price_per_person__lte=300.00
        ).select_related('operator', 'category', 'city')

        count = featured_tours.count()
        end_time = time.time()
        query_time = end_time - start_time

        self.assertLess(query_time, 1.0)  # Should be fast
        self.assertGreater(count, 0)


class ToursAdminTests(APITestCase):
    """
    Tests for admin-specific functionality
    """

    def setUp(self):
        self.client = APIClient()

        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='AdminPass123!'
        )

        self.provider = CustomUser.objects.create_user(
            username='adminprovider',
            email='adminprovider@test.com',
            password='ProviderPass123!',
            user_type='provider'
        )

        self.city = City.objects.create(name='Admin City')
        self.category = TourCategory.objects.create(name='Admin Category')

        self.operator = TourOperator.objects.create(
            name='Admin Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='admin@operator.com'
        )

        self.tour = Tour.objects.create(
            title='Admin Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Admin test tour',
            duration_value=3,
            duration_unit='hours',
            price_per_person=250.00,
            start_date='2024-12-01',
            available_slots=8
        )

        # Admin authentication
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_admin_tour_approval(self):
        """Test admin can approve/reject tours"""
        # Create unapproved tour
        unapproved_tour = Tour.objects.create(
            title='Unapproved Tour',
            operator=self.operator,
            category=self.category,
            city=self.city,
            description='Needs approval',
            duration_value=2,
            duration_unit='hours',
            price_per_person=150.00,
            start_date='2024-12-02',
            available_slots=5,
            is_active=False  # Not active initially
        )

        # Admin activates tour
        unapproved_tour.is_active = True
        unapproved_tour.save()

        unapproved_tour.refresh_from_db()
        self.assertTrue(unapproved_tour.is_active)

    def test_admin_operator_verification_workflow(self):
        """Test complete operator verification workflow"""
        pending_operator = TourOperator.objects.create(
            name='Pending Operator',
            user=self.provider,
            phone_number='+201000000001',
            email='pending@operator.com',
            verification_status='pending',
            is_verified=False
        )

        # Admin verifies operator
        pending_operator.verification_status = 'verified'
        pending_operator.is_verified = True
        pending_operator.save()

        pending_operator.refresh_from_db()
        self.assertEqual(pending_operator.verification_status, 'verified')
        self.assertTrue(pending_operator.is_verified)

    def test_admin_bulk_operations(self):
        """Test admin bulk operations on tours"""
        # Create multiple tours for bulk operations
        for i in range(10):
            Tour.objects.create(
                title=f'Bulk Tour {i}',
                operator=self.operator,
                category=self.category,
                city=self.city,
                description=f'Bulk test tour {i}',
                duration_value=2,
                duration_unit='hours',
                price_per_person=100.00 + (i * 10),
                start_date='2024-12-01',
                available_slots=5,
                is_featured=False
            )

        # Bulk feature tours
        featured_count = Tour.objects.filter(price_per_person__gte=150.00).update(is_featured=True)
        self.assertGreater(featured_count, 0)

        # Verify bulk update worked
        featured_tours = Tour.objects.filter(is_featured=True)
        self.assertEqual(featured_tours.count(), featured_count)


class ToursDataIntegrityTests(TestCase):
    """
    Data integrity and constraint tests
    """

    def test_tour_category_unique_name(self):
        """Test tour category name uniqueness"""
        TourCategory.objects.create(name='Unique Category')

        with self.assertRaises(Exception):
            TourCategory.objects.create(name='Unique Category')  # Duplicate

    def test_tour_operator_slug_uniqueness(self):
        """Test tour operator slug uniqueness"""
        provider1 = CustomUser.objects.create_user(
            username='provider1',
            email='provider1@test.com',
            password='pass123',
            user_type='provider'
        )

        provider2 = CustomUser.objects.create_user(
            username='provider2',
            email='provider2@test.com',
            password='pass123',
            user_type='provider'
        )

        TourOperator.objects.create(
            name='Same Name Operator',
            user=provider1,
            phone_number='+201000000001',
            email='operator1@test.com'
        )

        # Second operator with same name should have different slug
        operator2 = TourOperator.objects.create(
            name='Same Name Operator',
            user=provider2,
            phone_number='+201000000002',
            email='operator2@test.com'
        )

        self.assertIn('same-name-operator', operator2.slug)
        # Should be different due to auto-unique slug generation

    def test_tour_date_validation(self):
        """Test tour date validation constraints"""
        provider = CustomUser.objects.create_user(
            username='dateprovider',
            email='date@test.com',
            password='pass123',
            user_type='provider'
        )

        city = City.objects.create(name='Date City')
        category = TourCategory.objects.create(name='Date Category')

        operator = TourOperator.objects.create(
            name='Date Operator',
            user=provider,
            phone_number='+201000000000',
            email='date@operator.com'
        )

        # End date before start date should be prevented by validation
        # This would be caught by serializer validation in real usage
        tour = Tour.objects.create(
            title='Date Test Tour',
            operator=operator,
            category=category,
            city=city,
            description='Date validation test',
            duration_value=2,
            duration_unit='hours',
            price_per_person=100.00,
            start_date='2024-12-02',
            end_date='2024-12-01',  # End before start
            available_slots=5
        )

        # The model allows this, but business logic should prevent it
        # This tests that the database doesn't enforce this constraint
        self.assertIsNotNone(tour.id)