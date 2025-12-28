# payments/tests.py
"""
Tests for Payments App
Tests for payment processing and Stripe integration.
"""

from django.test import TestCase, Client
from django.urls import reverse


class PaymentListViewTest(TestCase):
    """Tests for payment list page"""

    def test_payment_list_loads(self):
        """Test payment list page loads"""
        response = self.client.get(reverse('payments:list'))
        self.assertEqual(response.status_code, 200)
