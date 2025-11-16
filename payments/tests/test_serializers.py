# payments/tests/test_serializers.py
from django.test import TestCase
from payments.serializers import PaymentMethodSerializer, PaymentListSerializer
from payments.models import PaymentMethod


class PaymentSerializerTests(TestCase):
    """Tests for payment serializers - data validation"""

    def test_payment_method_serializer(self):
        """Test payment method serialization"""
        payment_method = PaymentMethod.objects.create(
            name='Visa Credit Card',
            method_type='credit_card',
            description='Secure credit card payments',
            is_active=True
        )

        serializer = PaymentMethodSerializer(payment_method)

        # These fields should be correctly serialized
        self.assertEqual(serializer.data['name'], 'Visa Credit Card')
        self.assertEqual(serializer.data['method_type'], 'credit_card')
        self.assertEqual(serializer.data['is_active'], True)

    def test_payment_method_serializer_validation(self):
        """Test that valid payment method data passes validation"""
        valid_data = {
            'name': 'MasterCard',
            'method_type': 'credit_card',
            'is_active': True
        }

        serializer = PaymentMethodSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())