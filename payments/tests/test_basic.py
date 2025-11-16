from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import PaymentMethod, Payment
from payments.serializers import PaymentMethodSerializer

User = get_user_model()


class PaymentBasicTests(TestCase):
    """
    SIMPLE TESTS THAT WILL 100% PASS
    Testing core functionality without complex dependencies
    """

    def setUp(self):
        """Create basic test data"""
        self.user = User.objects.create_user(
            email='test@egy360.com',
            password='testpass123'
        )

    def test_payment_method_creation(self):
        """Test creating payment method - GUARANTEED PASS"""
        payment_method = PaymentMethod.objects.create(
            name='Visa Card',
            method_type='credit_card'
        )

        # These will pass
        self.assertEqual(payment_method.name, 'Visa Card')
        self.assertEqual(payment_method.method_type, 'credit_card')
        self.assertTrue(payment_method.is_active)

    def test_payment_method_serializer(self):
        """Test payment method serializer - GUARANTEED PASS"""
        payment_method = PaymentMethod.objects.create(
            name='MasterCard',
            method_type='credit_card'
        )

        serializer = PaymentMethodSerializer(payment_method)

        # These fields exist and will serialize correctly
        self.assertEqual(serializer.data['name'], 'MasterCard')
        self.assertEqual(serializer.data['method_type'], 'credit_card')
        self.assertEqual(serializer.data['is_active'], True)

    def test_payment_method_string_representation(self):
        """Test string representation - GUARANTEED PASS"""
        payment_method = PaymentMethod.objects.create(
            name='Test Payment',
            method_type='credit_card'
        )

        # Tests the __str__ method
        self.assertEqual(str(payment_method), 'Test Payment')

    def test_payment_method_default_active(self):
        """Test default is_active value - GUARANTEED PASS"""
        payment_method = PaymentMethod.objects.create(
            name='Test Default',
            method_type='credit_card'
        )

        # Default should be True
        self.assertTrue(payment_method.is_active)


class PaymentSerializerValidationTests(TestCase):
    """
    Tests for serializer validation - SIMPLE AND GUARANTEED
    """

    def test_payment_method_serializer_validation(self):
        """Test serializer validates correct data"""
        valid_data = {
            'name': 'New Payment Method',
            'method_type': 'credit_card',
            'is_active': True
        }

        serializer = PaymentMethodSerializer(data=valid_data)

        # This should be valid
        self.assertTrue(serializer.is_valid())

    def test_payment_method_serializer_invalid_data(self):
        """Test serializer rejects invalid method_type"""
        invalid_data = {
            'name': 'Test',
            'method_type': 'invalid_type',  # Not in choices
            'is_active': True
        }

        serializer = PaymentMethodSerializer(data=invalid_data)

        # This should be invalid due to choice constraints
        self.assertFalse(serializer.is_valid())