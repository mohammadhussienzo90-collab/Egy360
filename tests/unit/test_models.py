"""
Unit Tests for Models
Tests individual model methods, properties, validators, and business logic
"""
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from accommodations.models import Accommodation, Room, Amenity
from tours.models import Tour, TourItinerary, TourBooking
from accounts.models import UserProfile
from home.models import (
    NewsletterSubscription, ContactMessage, FAQItem,
    HomepageBanner, Testimonial, Partner
)
from core.models import AffiliateClick, DailyRevenueSummary
from django.contrib.contenttypes.models import ContentType


class AccommodationModelTests(TestCase):
    """Unit tests for Accommodation model"""

    def setUp(self):
        """Set up test data"""
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel Cairo",
            slug="test-hotel-cairo",
            accommodation_type="hotel",
            description="A test hotel in Cairo",
            city="Cairo",
            address="123 Test Street",
            star_rating=4,
            price_per_night=Decimal("150.00"),
            booking_com_url="https://booking.com/hotel/test",
            agoda_url="https://agoda.com/test",
            commission_rate=Decimal("4.00")
        )

    def test_accommodation_str_representation(self):
        """Test string representation of accommodation"""
        self.assertEqual(str(self.accommodation), "Test Hotel Cairo - Cairo")

    def test_accommodation_type_choices(self):
        """Test valid accommodation types"""
        valid_types = ['hotel', 'resort', 'hostel', 'apartment', 'villa', 'camp', 'cruise']
        for acc_type in valid_types:
            self.accommodation.accommodation_type = acc_type
            self.accommodation.full_clean()  # Should not raise

    def test_star_rating_validation(self):
        """Test star rating validators (1-5)"""
        # Valid ratings
        for rating in [1, 2, 3, 4, 5]:
            self.accommodation.star_rating = rating
            self.accommodation.full_clean()

        # Invalid rating (too low)
        self.accommodation.star_rating = 0
        with self.assertRaises(ValidationError):
            self.accommodation.full_clean()

        # Invalid rating (too high)
        self.accommodation.star_rating = 6
        with self.assertRaises(ValidationError):
            self.accommodation.full_clean()

    def test_get_primary_booking_url_prioritizes_booking_com(self):
        """Test that get_primary_booking_url returns Booking.com first"""
        url = self.accommodation.get_primary_booking_url()
        self.assertEqual(url, "https://booking.com/hotel/test")

    def test_get_primary_booking_url_fallback_to_agoda(self):
        """Test fallback to Agoda when Booking.com not available"""
        self.accommodation.booking_com_url = None
        self.accommodation.save()
        url = self.accommodation.get_primary_booking_url()
        self.assertEqual(url, "https://agoda.com/test")

    def test_get_primary_booking_url_returns_none_when_no_urls(self):
        """Test None returned when no booking URLs exist"""
        self.accommodation.booking_com_url = None
        self.accommodation.agoda_url = None
        self.accommodation.save()
        url = self.accommodation.get_primary_booking_url()
        self.assertIsNone(url)

    def test_has_booking_options_true_with_urls(self):
        """Test has_booking_options returns True when URLs exist"""
        self.assertTrue(self.accommodation.has_booking_options())

    def test_has_booking_options_false_without_urls(self):
        """Test has_booking_options returns False when no URLs"""
        self.accommodation.booking_com_url = None
        self.accommodation.agoda_url = None
        self.accommodation.hotels_com_url = None
        self.accommodation.direct_booking_url = None
        self.accommodation.save()
        self.assertFalse(self.accommodation.has_booking_options())

    def test_get_all_booking_options_returns_list(self):
        """Test get_all_booking_options returns correct structure"""
        options = self.accommodation.get_all_booking_options()
        self.assertIsInstance(options, list)
        self.assertEqual(len(options), 2)  # booking.com and agoda
        self.assertEqual(options[0][0], 'Booking.com')
        self.assertEqual(options[1][0], 'Agoda')

    def test_price_per_night_decimal_precision(self):
        """Test price maintains decimal precision"""
        self.accommodation.price_per_night = Decimal("199.99")
        self.accommodation.save()
        self.accommodation.refresh_from_db()
        self.assertEqual(self.accommodation.price_per_night, Decimal("199.99"))

    def test_default_values(self):
        """Test default values are set correctly"""
        acc = Accommodation.objects.create(
            name="Minimal Hotel",
            slug="minimal-hotel",
            accommodation_type="hotel",
            description="Minimal description",
            city="Luxor",
            address="Test Address",
            price_per_night=Decimal("100.00")
        )
        self.assertFalse(acc.is_featured)
        self.assertFalse(acc.is_verified)
        self.assertTrue(acc.is_active)
        self.assertEqual(acc.total_rooms, 1)
        self.assertEqual(acc.weekend_surcharge, Decimal("0"))
        self.assertEqual(acc.average_rating, Decimal("0"))


class RoomModelTests(TestCase):
    """Unit tests for Room model"""

    def setUp(self):
        """Set up test data"""
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test Address",
            price_per_night=Decimal("100.00")
        )
        self.room = Room.objects.create(
            accommodation=self.accommodation,
            room_type="double",
            name="Deluxe Double",
            description="Spacious double room",
            max_occupancy=2,
            beds="1 King Bed",
            base_price=Decimal("150.00")
        )

    def test_room_str_representation(self):
        """Test string representation of room"""
        self.assertEqual(str(self.room), "Deluxe Double - Test Hotel")

    def test_room_type_choices(self):
        """Test valid room types"""
        valid_types = ['single', 'double', 'twin', 'suite', 'family', 'deluxe']
        for room_type in valid_types:
            self.room.room_type = room_type
            self.room.full_clean()

    def test_room_default_features(self):
        """Test default feature values"""
        self.assertTrue(self.room.has_air_conditioning)
        self.assertTrue(self.room.has_wifi)
        self.assertTrue(self.room.has_tv)
        self.assertFalse(self.room.has_minibar)
        self.assertTrue(self.room.has_safe)
        self.assertFalse(self.room.has_balcony)


class TourModelTests(TestCase):
    """Unit tests for Tour model"""

    def setUp(self):
        """Set up test data"""
        self.tour = Tour.objects.create(
            name="Pyramids Day Tour",
            slug="pyramids-day-tour",
            tour_type="cultural",
            description="Explore the pyramids",
            highlights="See the Sphinx",
            departure_city="Cairo",
            price_per_person=Decimal("89.00"),
            viator_url="https://viator.com/tours/pyramids",
            getyourguide_url="https://getyourguide.com/pyramids",
            commission_rate=Decimal("8.00")
        )

    def test_tour_str_representation(self):
        """Test string representation of tour"""
        self.assertEqual(str(self.tour), "Pyramids Day Tour")

    def test_tour_type_choices(self):
        """Test valid tour types"""
        valid_types = ['cultural', 'adventure', 'desert', 'cruise', 'diving', 'religious', 'luxury', 'budget']
        for tour_type in valid_types:
            self.tour.tour_type = tour_type
            self.tour.full_clean(exclude=['destinations', 'includes', 'excludes', 'languages'])

    def test_difficulty_level_choices(self):
        """Test valid difficulty levels"""
        valid_levels = ['easy', 'moderate', 'challenging']
        for level in valid_levels:
            self.tour.difficulty_level = level
            self.tour.full_clean(exclude=['destinations', 'includes', 'excludes', 'languages'])

    def test_get_primary_affiliate_url_prioritizes_viator(self):
        """Test that Viator URL is prioritized"""
        url = self.tour.get_primary_affiliate_url()
        self.assertEqual(url, "https://viator.com/tours/pyramids")

    def test_get_primary_affiliate_url_fallback(self):
        """Test fallback to GetYourGuide"""
        self.tour.viator_url = None
        self.tour.save()
        url = self.tour.get_primary_affiliate_url()
        self.assertEqual(url, "https://getyourguide.com/pyramids")

    def test_has_affiliate_options(self):
        """Test affiliate options detection"""
        self.assertTrue(self.tour.has_affiliate_options())

        self.tour.viator_url = None
        self.tour.getyourguide_url = None
        self.tour.travelpayouts_url = None
        self.tour.save()
        self.assertFalse(self.tour.has_affiliate_options())

    def test_get_all_affiliate_options_structure(self):
        """Test affiliate options return correct structure"""
        options = self.tour.get_all_affiliate_options()
        self.assertIsInstance(options, list)
        self.assertEqual(len(options), 2)
        self.assertEqual(options[0]['platform'], 'Viator')
        self.assertEqual(options[0]['commission'], '8%')

    def test_default_values(self):
        """Test default values"""
        self.assertEqual(self.tour.duration_days, 1)
        self.assertEqual(self.tour.duration_nights, 0)
        self.assertEqual(self.tour.min_group_size, 1)
        self.assertEqual(self.tour.max_group_size, 20)
        self.assertEqual(self.tour.difficulty_level, 'easy')


class TourBookingModelTests(TestCase):
    """Unit tests for TourBooking model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.tour = Tour.objects.create(
            name="Test Tour",
            slug="test-tour",
            tour_type="cultural",
            description="Test",
            highlights="Test",
            departure_city="Cairo",
            price_per_person=Decimal("100.00")
        )
        self.booking = TourBooking.objects.create(
            tour=self.tour,
            user=self.user,
            tour_date=date.today() + timedelta(days=7),
            number_of_adults=2,
            number_of_children=1,
            total_price=Decimal("250.00"),
            contact_name="John Doe",
            contact_email="john@example.com",
            contact_phone="+1234567890"
        )

    def test_booking_str_representation(self):
        """Test string representation of booking"""
        expected = f"Test Tour - testuser - {self.booking.tour_date}"
        self.assertEqual(str(self.booking), expected)

    def test_booking_status_choices(self):
        """Test valid booking statuses"""
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        for status in valid_statuses:
            self.booking.status = status
            self.booking.full_clean()

    def test_default_status_is_pending(self):
        """Test default status is pending"""
        self.assertEqual(self.booking.status, 'pending')

    def test_booking_date_auto_set(self):
        """Test booking_date is auto-set"""
        self.assertIsNotNone(self.booking.booking_date)


class UserProfileModelTests(TestCase):
    """Unit tests for UserProfile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Profile is auto-created by signal
        self.profile = self.user.profile

    def test_profile_auto_created_on_user_creation(self):
        """Test UserProfile is auto-created when User is created"""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str_representation(self):
        """Test string representation of profile"""
        self.assertEqual(str(self.profile), "testuser - Profile")

    def test_is_fully_verified_all_false(self):
        """Test is_fully_verified returns False when not all verified"""
        self.assertFalse(self.profile.is_fully_verified)

    def test_is_fully_verified_all_true(self):
        """Test is_fully_verified returns True when all verified"""
        self.profile.email_verified = True
        self.profile.phone_verified = True
        self.profile.identity_verified = True
        self.profile.save()
        self.assertTrue(self.profile.is_fully_verified)

    def test_generate_otp_creates_6_digit_code(self):
        """Test OTP generation creates 6-digit code"""
        otp = self.profile.generate_otp()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_generate_otp_sets_timestamp(self):
        """Test OTP generation sets timestamp"""
        self.profile.generate_otp()
        self.assertIsNotNone(self.profile.phone_otp_created)

    def test_verify_otp_success(self):
        """Test OTP verification succeeds with correct code"""
        otp = self.profile.generate_otp()
        success, message = self.profile.verify_otp(otp)
        self.assertTrue(success)
        self.assertEqual(message, "OTP verified successfully")
        self.assertTrue(self.profile.phone_verified)

    def test_verify_otp_fails_with_wrong_code(self):
        """Test OTP verification fails with wrong code"""
        self.profile.generate_otp()
        success, message = self.profile.verify_otp("000000")
        self.assertFalse(success)
        self.assertEqual(message, "Invalid OTP code")

    def test_verify_otp_fails_when_no_otp_generated(self):
        """Test OTP verification fails when no OTP exists"""
        success, message = self.profile.verify_otp("123456")
        self.assertFalse(success)
        self.assertEqual(message, "No OTP code generated")

    def test_verify_otp_fails_after_3_attempts(self):
        """Test OTP verification fails after 3 wrong attempts"""
        self.profile.generate_otp()
        for _ in range(3):
            self.profile.verify_otp("000000")
        success, message = self.profile.verify_otp("000000")
        self.assertFalse(success)
        self.assertIn("Too many attempts", message)

    def test_generate_backup_codes(self):
        """Test backup codes generation"""
        codes = self.profile.generate_backup_codes()
        self.assertEqual(len(codes), 10)
        for code in codes:
            self.assertEqual(len(code), 9)  # 4 + dash + 4
            self.assertIn('-', code)

    def test_verify_backup_code_success(self):
        """Test backup code verification"""
        codes = self.profile.generate_backup_codes()
        first_code = codes[0]
        result = self.profile.verify_backup_code(first_code)
        self.assertTrue(result)
        # Code should be consumed
        self.assertEqual(len(self.profile.backup_codes), 9)

    def test_verify_backup_code_fails_with_invalid_code(self):
        """Test backup code verification fails with invalid code"""
        self.profile.generate_backup_codes()
        result = self.profile.verify_backup_code("XXXX-XXXX")
        self.assertFalse(result)

    def test_get_masked_phone(self):
        """Test phone number masking"""
        self.profile.phone = "+1234567890"
        self.profile.save()
        masked = self.profile.get_masked_phone()
        self.assertEqual(masked, "***-***-7890")

    def test_get_masked_phone_returns_none_when_no_phone(self):
        """Test masking returns None when no phone"""
        self.assertIsNone(self.profile.get_masked_phone())


class NewsletterSubscriptionModelTests(TestCase):
    """Unit tests for NewsletterSubscription model"""

    def test_subscription_creation(self):
        """Test creating newsletter subscription"""
        sub = NewsletterSubscription.objects.create(
            email="test@example.com",
            name="Test User"
        )
        self.assertEqual(str(sub), "test@example.com")
        self.assertTrue(sub.is_active)
        self.assertIsNone(sub.unsubscribed_at)

    def test_unsubscribe_method(self):
        """Test unsubscribe method"""
        sub = NewsletterSubscription.objects.create(email="test@example.com")
        sub.unsubscribe()
        self.assertFalse(sub.is_active)
        self.assertIsNotNone(sub.unsubscribed_at)

    def test_email_uniqueness(self):
        """Test email must be unique"""
        NewsletterSubscription.objects.create(email="test@example.com")
        with self.assertRaises(Exception):
            NewsletterSubscription.objects.create(email="test@example.com")


class ContactMessageModelTests(TestCase):
    """Unit tests for ContactMessage model"""

    def test_contact_message_creation(self):
        """Test creating contact message"""
        msg = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test message content"
        )
        self.assertEqual(str(msg), "John Doe - Test Subject")
        self.assertFalse(msg.is_read)
        self.assertFalse(msg.is_replied)

    def test_default_values(self):
        """Test default values"""
        msg = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            subject="Test",
            message="Test"
        )
        self.assertFalse(msg.is_read)
        self.assertFalse(msg.is_replied)
        self.assertIsNone(msg.replied_at)


class FAQItemModelTests(TestCase):
    """Unit tests for FAQItem model"""

    def test_faq_creation(self):
        """Test creating FAQ item"""
        faq = FAQItem.objects.create(
            question="What is Egy360?",
            answer="Egypt tourism platform",
            category="general"
        )
        self.assertEqual(str(faq), "What is Egy360?")

    def test_category_choices(self):
        """Test valid category choices"""
        valid_categories = ['general', 'booking', 'payment', 'cancellation', 'safety', 'other']
        for category in valid_categories:
            faq = FAQItem(question="Test?", answer="Test", category=category)
            faq.full_clean()


class AffiliateClickModelTests(TestCase):
    """Unit tests for AffiliateClick model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            accommodation_type="hotel",
            description="Test",
            city="Cairo",
            address="Test Address",
            price_per_night=Decimal("100.00")
        )
        self.content_type = ContentType.objects.get_for_model(Accommodation)
        self.click = AffiliateClick.objects.create(
            user=self.user,
            platform="booking_com",
            item_type="accommodation",
            content_type=self.content_type,
            object_id=self.accommodation.id,
            affiliate_url="https://booking.com/test",
            estimated_commission=Decimal("4.00")
        )

    def test_click_str_representation(self):
        """Test string representation"""
        self.assertIn("booking_com", str(self.click))
        self.assertIn("accommodation", str(self.click))

    def test_platform_choices(self):
        """Test valid platform choices"""
        valid_platforms = [
            'booking_com', 'hotellook', 'agoda', 'hotels_com',
            'viator', 'getyourguide', 'travelpayouts', 'aviasales',
            'discovercars', 'world_nomads', 'direct', 'other'
        ]
        for platform in valid_platforms:
            self.click.platform = platform
            self.click.full_clean()

    def test_item_type_choices(self):
        """Test valid item type choices"""
        valid_types = ['accommodation', 'tour', 'flight', 'transportation', 'insurance', 'car_rental']
        for item_type in valid_types:
            self.click.item_type = item_type
            self.click.full_clean()

    def test_generic_foreign_key(self):
        """Test generic foreign key resolves correctly"""
        self.assertEqual(self.click.content_object, self.accommodation)

    def test_default_converted_is_false(self):
        """Test default converted status is False"""
        self.assertFalse(self.click.converted)

    def test_anonymous_click_allowed(self):
        """Test click can be created without user"""
        click = AffiliateClick.objects.create(
            platform="viator",
            item_type="tour",
            content_type=self.content_type,
            object_id=self.accommodation.id,
            affiliate_url="https://viator.com/test"
        )
        self.assertIsNone(click.user)


class DailyRevenueSummaryModelTests(TestCase):
    """Unit tests for DailyRevenueSummary model"""

    def test_summary_creation(self):
        """Test creating daily summary"""
        summary = DailyRevenueSummary.objects.create(
            date=date.today(),
            total_clicks=100,
            accommodation_clicks=60,
            tour_clicks=40,
            estimated_revenue=Decimal("25.00")
        )
        self.assertIn(str(date.today()), str(summary))

    def test_date_uniqueness(self):
        """Test date must be unique"""
        DailyRevenueSummary.objects.create(date=date.today())
        with self.assertRaises(Exception):
            DailyRevenueSummary.objects.create(date=date.today())

    def test_default_values(self):
        """Test default values are zero"""
        summary = DailyRevenueSummary.objects.create(date=date.today())
        self.assertEqual(summary.total_clicks, 0)
        self.assertEqual(summary.accommodation_clicks, 0)
        self.assertEqual(summary.estimated_revenue, Decimal("0"))
        self.assertEqual(summary.conversion_rate, Decimal("0"))
