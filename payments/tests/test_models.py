# payments/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from bookings.models import Booking
from payments.models import PaymentMethod, Payment, PaymentRefund

User = get_user_model()


class PaymentModelTests(TestCase):
    """Tests that MUST pass - core payment functionality"""

    def setUp(self):
        """Create test data that will make tests pass"""
        self.user = User.objects.create_user(
            email='test@egy360.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Create a simple booking (minimal required fields)
        self.booking = Booking.objects.create(
            user=self.user,
            booking_number='TEST001',
            status='confirmed',
            total_amount=1000.00
        )

        self.payment_method = PaymentMethod.objects.create(
            name='Test Credit Card',
            method_type='credit_card',
            is_active=True
        )

    def test_payment_method_creation(self):
        """Test that payment methods can be created"""
        self.assertEqual(self.payment_method.name, 'Test Credit Card')
        self.assertEqual(self.payment_method.method_type, 'credit_card')
        self.assertTrue(self.payment_method.is_active)

    def test_payment_creation(self):
        """Test that payments can be created with auto-generated numbers"""
        payment = Payment.objects.create(
            booking=self.booking,
            user=self.user,
            payment_method=self.payment_method,
            amount=1000.00,
            status='pending'
        )

        # These should automatically be set
        self.assertIsNotNone(payment.payment_number)
        self.assertTrue(payment.payment_number.startswith('PAY'))
        self.assertEqual(payment.amount, 1000.00)
        self.assertEqual(payment.status, 'pending')

    def test_payment_string_representation(self):
        """Test the string representation for admin readability"""
        payment = Payment.objects.create(
            booking=self.booking,
            user=self.user,
            payment_method=self.payment_method,
            amount=1500.00,
            status='completed'
        )

        expected_str = f"Payment #{payment.payment_number} - 1500.00 EGP"
        self.assertEqual(str(payment), expected_str)

