"""
Model Tests for Egy360

Tests all database models to ensure they work correctly.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal


class AccommodationModelTests(TestCase):
    """Test Accommodation model"""

    def setUp(self):
        from accommodations.models import Accommodation, Amenity

        self.amenity = Amenity.objects.create(
            name='WiFi',
            icon='fas fa-wifi'
        )

        self.accommodation = Accommodation.objects.create(
            name='Test Hotel',
            slug='test-hotel',
            accommodation_type='hotel',
            description='A test hotel for testing',
            city='Cairo',
            address='123 Test Street',
            star_rating=4,
            price_per_night=Decimal('150.00'),
            is_active=True,
            is_featured=True
        )
        self.accommodation.amenities.add(self.amenity)

    def test_accommodation_creation(self):
        """Test accommodation is created correctly"""
        from accommodations.models import Accommodation
        self.assertEqual(Accommodation.objects.count(), 1)
        self.assertEqual(self.accommodation.name, 'Test Hotel')
        self.assertEqual(self.accommodation.city, 'Cairo')

    def test_accommodation_str(self):
        """Test accommodation string representation"""
        self.assertIn('Test Hotel', str(self.accommodation))

    def test_accommodation_slug(self):
        """Test accommodation slug is set correctly"""
        self.assertEqual(self.accommodation.slug, 'test-hotel')

    def test_accommodation_amenities(self):
        """Test accommodation amenities relationship"""
        self.assertEqual(self.accommodation.amenities.count(), 1)
        self.assertEqual(self.accommodation.amenities.first().name, 'WiFi')

    def test_accommodation_type_choices(self):
        """Test accommodation type is valid"""
        from accommodations.models import Accommodation
        valid_types = [t[0] for t in Accommodation.ACCOMMODATION_TYPES]
        self.assertIn(self.accommodation.accommodation_type, valid_types)

    def test_accommodation_booking_options(self):
        """Test get_all_booking_options method"""
        options = self.accommodation.get_all_booking_options()
        self.assertIsInstance(options, list)


class TourModelTests(TestCase):
    """Test Tour model"""

    def setUp(self):
        from tours.models import Tour

        self.tour = Tour.objects.create(
            name='Pyramids Tour',
            slug='pyramids-tour',
            tour_type='cultural',
            description='Visit the great pyramids',
            duration_days=1,
            duration_nights=0,
            departure_city='Cairo',
            difficulty_level='easy',
            price_per_person=Decimal('100.00'),
            is_active=True,
            is_featured=True
        )

    def test_tour_creation(self):
        """Test tour is created correctly"""
        from tours.models import Tour
        self.assertEqual(Tour.objects.count(), 1)
        self.assertEqual(self.tour.name, 'Pyramids Tour')

    def test_tour_str(self):
        """Test tour string representation"""
        self.assertIn('Pyramids', str(self.tour))

    def test_tour_slug(self):
        """Test tour slug is set correctly"""
        self.assertEqual(self.tour.slug, 'pyramids-tour')

    def test_tour_type_choices(self):
        """Test tour type is valid"""
        from tours.models import Tour
        valid_types = [t[0] for t in Tour.TOUR_TYPES]
        self.assertIn(self.tour.tour_type, valid_types)

    def test_tour_difficulty_choices(self):
        """Test tour difficulty is valid"""
        from tours.models import Tour
        valid_difficulties = [d[0] for d in Tour.DIFFICULTY_LEVELS]
        self.assertIn(self.tour.difficulty_level, valid_difficulties)


class UserProfileModelTests(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_created_automatically(self):
        """Test user profile is created automatically via signal"""
        from accounts.models import UserProfile
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_user_profile_str(self):
        """Test user profile string representation"""
        from accounts.models import UserProfile
        profile = UserProfile.objects.get(user=self.user)
        self.assertIn('testuser', str(profile))


class ReviewModelTests(TestCase):
    """Test Review model"""

    def setUp(self):
        from accommodations.models import Accommodation
        from reviews.models import Review

        self.user = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='testpass123'
        )

        self.accommodation = Accommodation.objects.create(
            name='Reviewed Hotel',
            slug='reviewed-hotel',
            accommodation_type='hotel',
            description='A hotel to review',
            city='Luxor',
            price_per_night=Decimal('100.00'),
            is_active=True
        )

        content_type = ContentType.objects.get_for_model(Accommodation)

        self.review = Review.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.accommodation.id,
            title='Great Stay',
            comment='Really enjoyed my stay here',
            rating=5,
            status='approved'
        )

    def test_review_creation(self):
        """Test review is created correctly"""
        from reviews.models import Review
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.review.title, 'Great Stay')
        self.assertEqual(self.review.rating, 5)

    def test_review_user_relationship(self):
        """Test review user relationship"""
        self.assertEqual(self.review.user.username, 'reviewer')

    def test_review_content_object(self):
        """Test review content object relationship"""
        self.assertEqual(self.review.content_object, self.accommodation)


class BookingModelTests(TestCase):
    """Test Booking model"""

    def setUp(self):
        from accommodations.models import Accommodation
        from bookings.models import Booking
        import uuid

        self.user = User.objects.create_user(
            username='booker',
            email='booker@example.com',
            password='testpass123'
        )

        self.accommodation = Accommodation.objects.create(
            name='Booked Hotel',
            slug='booked-hotel',
            accommodation_type='hotel',
            description='A hotel to book',
            city='Aswan',
            price_per_night=Decimal('200.00'),
            is_active=True
        )

        content_type = ContentType.objects.get_for_model(Accommodation)

        # Generate unique booking reference
        booking_ref = f"EGY-{uuid.uuid4().hex[:8].upper()}"

        self.booking = Booking.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.accommodation.id,
            booking_type='accommodation',
            booking_reference=booking_ref,
            check_in_date='2024-06-01',
            check_out_date='2024-06-05',
            total_amount=Decimal('800.00'),
            contact_name='Test Booker',
            contact_email='booker@example.com',
            contact_phone='+1234567890',
            status='pending'
        )

    def test_booking_creation(self):
        """Test booking is created correctly"""
        from bookings.models import Booking
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.booking.total_amount, Decimal('800.00'))

    def test_booking_reference_exists(self):
        """Test booking reference is set"""
        self.assertIsNotNone(self.booking.booking_reference)
        self.assertTrue(len(self.booking.booking_reference) > 0)

    def test_booking_status_methods(self):
        """Test booking status change methods"""
        self.booking.confirm()
        self.assertEqual(self.booking.status, 'confirmed')

        self.booking.complete()
        self.assertEqual(self.booking.status, 'completed')


class CityModelTests(TestCase):
    """Test City model"""

    def setUp(self):
        from destinations.models import Country, City

        self.country = Country.objects.create(
            name='Egypt',
            code='EGY'
        )

        self.city = City.objects.create(
            country=self.country,
            name='Cairo',
            slug='cairo',
            description='Capital of Egypt',
            is_popular=True
        )

    def test_city_creation(self):
        """Test city is created correctly"""
        from destinations.models import City
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(self.city.name, 'Cairo')

    def test_city_country_relationship(self):
        """Test city country relationship"""
        self.assertEqual(self.city.country.name, 'Egypt')

    def test_city_str(self):
        """Test city string representation"""
        self.assertIn('Cairo', str(self.city))
        self.assertIn('Egypt', str(self.city))


class AmenityModelTests(TestCase):
    """Test Amenity model"""

    def setUp(self):
        from accommodations.models import Amenity

        self.amenity = Amenity.objects.create(
            name='Swimming Pool',
            icon='fas fa-swimming-pool'
        )

    def test_amenity_creation(self):
        """Test amenity is created correctly"""
        from accommodations.models import Amenity
        self.assertEqual(Amenity.objects.count(), 1)
        self.assertEqual(self.amenity.name, 'Swimming Pool')

    def test_amenity_str(self):
        """Test amenity string representation"""
        self.assertEqual(str(self.amenity), 'Swimming Pool')
