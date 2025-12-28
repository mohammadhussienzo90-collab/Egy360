# payments/paymob_integration.py
"""
PayMob Payment Gateway Integration for Egy360
==============================================

PayMob is Egypt's leading payment gateway supporting:
- Credit/Debit Cards (Visa, Mastercard, Meeza)
- Mobile Wallets (Vodafone Cash, Orange Money, Etisalat Cash, WE Pay)
- Fawry (Cash payments at retail locations)
- ValU (Buy now, pay later)

Integration Flow:
1. Get authentication token from PayMob API
2. Create order with booking details
3. Generate payment key for the iframe
4. User completes payment in PayMob iframe
5. PayMob sends callback to our webhook
6. We verify and update booking status

Documentation: https://docs.paymob.com/docs/accept-standard-redirect
"""

import requests
import hmac
import hashlib
import logging
from decimal import Decimal
from django.conf import settings

logger = logging.getLogger(__name__)


class PayMobGateway:
    """
    PayMob payment gateway wrapper.

    Handles all communication with PayMob Accept API.
    """

    # PayMob API endpoints
    BASE_URL = "https://accept.paymob.com/api"
    AUTH_URL = f"{BASE_URL}/auth/tokens"
    ORDER_URL = f"{BASE_URL}/ecommerce/orders"
    PAYMENT_KEY_URL = f"{BASE_URL}/acceptance/payment_keys"

    # Payment method integration IDs (set in admin.paymob.com)
    # These are obtained from your PayMob dashboard
    CARD_INTEGRATION_ID = None  # For card payments
    WALLET_INTEGRATION_ID = None  # For mobile wallets
    FAWRY_INTEGRATION_ID = None  # For Fawry cash payments

    def __init__(self):
        """Initialize PayMob gateway with credentials from settings."""
        self.api_key = getattr(settings, 'PAYMOB_API_KEY', '')
        self.hmac_secret = getattr(settings, 'PAYMOB_HMAC_SECRET', '')

        # Integration IDs from settings
        self.CARD_INTEGRATION_ID = getattr(settings, 'PAYMOB_CARD_INTEGRATION_ID', '')
        self.WALLET_INTEGRATION_ID = getattr(settings, 'PAYMOB_WALLET_INTEGRATION_ID', '')
        self.FAWRY_INTEGRATION_ID = getattr(settings, 'PAYMOB_FAWRY_INTEGRATION_ID', '')

        # Iframe ID for card payments
        self.iframe_id = getattr(settings, 'PAYMOB_IFRAME_ID', '')

    def is_configured(self):
        """Check if PayMob credentials are configured."""
        return bool(self.api_key and self.CARD_INTEGRATION_ID)

    def _get_auth_token(self):
        """
        Step 1: Get authentication token from PayMob.

        This token is required for all subsequent API calls.
        Token is valid for 1 hour.

        Returns:
            str: Authentication token or None on failure
        """
        try:
            response = requests.post(
                self.AUTH_URL,
                json={"api_key": self.api_key},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get('token')
        except requests.RequestException as e:
            logger.error(f"PayMob auth failed: {e}")
            return None

    def _create_order(self, auth_token, amount_cents, booking_reference, items=None):
        """
        Step 2: Register an order with PayMob.

        Args:
            auth_token: Token from step 1
            amount_cents: Total amount in cents (piasters for EGP)
            booking_reference: Our booking reference number
            items: Optional list of items for the order

        Returns:
            dict: Order data including order ID, or None on failure
        """
        if items is None:
            items = []

        payload = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": str(int(amount_cents)),
            "currency": "EGP",
            "merchant_order_id": booking_reference,
            "items": items,
        }

        try:
            response = requests.post(
                self.ORDER_URL,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"PayMob order creation failed: {e}")
            return None

    def _get_payment_key(self, auth_token, order_id, amount_cents,
                         billing_data, integration_id, expiration=3600):
        """
        Step 3: Generate payment key for iframe.

        This key is used to initialize the payment iframe.

        Args:
            auth_token: Token from step 1
            order_id: Order ID from step 2
            amount_cents: Amount in cents
            billing_data: Customer billing information
            integration_id: PayMob integration ID for payment method
            expiration: Key expiration in seconds (default 1 hour)

        Returns:
            str: Payment key for iframe, or None on failure
        """
        payload = {
            "auth_token": auth_token,
            "amount_cents": str(int(amount_cents)),
            "expiration": expiration,
            "order_id": str(order_id),
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": integration_id,
            "lock_order_when_paid": "true",
        }

        try:
            response = requests.post(
                self.PAYMENT_KEY_URL,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get('token')
        except requests.RequestException as e:
            logger.error(f"PayMob payment key failed: {e}")
            return None

    def create_payment_session(self, amount, booking, payment_method='card'):
        """
        Create a complete payment session for a booking.

        This is the main method to call from views.

        Args:
            amount: Decimal amount in EGP
            booking: Booking model instance
            payment_method: 'card', 'wallet', or 'fawry'

        Returns:
            dict: {
                'success': bool,
                'payment_key': str (for iframe),
                'iframe_url': str (full iframe URL),
                'order_id': int (PayMob order ID),
                'error': str (if failed)
            }
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'PayMob is not configured. Please add API credentials.'
            }

        # Convert amount to cents (piasters)
        # PayMob expects amount in smallest currency unit
        amount_cents = int(Decimal(str(amount)) * 100)

        # Step 1: Get auth token
        auth_token = self._get_auth_token()
        if not auth_token:
            return {
                'success': False,
                'error': 'Failed to authenticate with PayMob'
            }

        # Step 2: Create order
        order_items = [{
            "name": f"Booking {booking.booking_reference}",
            "amount_cents": str(amount_cents),
            "quantity": "1",
        }]

        order_data = self._create_order(
            auth_token,
            amount_cents,
            booking.booking_reference,
            order_items
        )

        if not order_data:
            return {
                'success': False,
                'error': 'Failed to create PayMob order'
            }

        order_id = order_data.get('id')

        # Step 3: Prepare billing data
        # PayMob requires specific billing data format
        billing_data = {
            "first_name": booking.contact_name.split()[0] if booking.contact_name else "Guest",
            "last_name": booking.contact_name.split()[-1] if booking.contact_name and len(booking.contact_name.split()) > 1 else "User",
            "email": booking.contact_email or "guest@egy360.com",
            "phone_number": booking.contact_phone or "+201000000000",
            "apartment": "NA",
            "floor": "NA",
            "street": "NA",
            "building": "NA",
            "shipping_method": "NA",
            "postal_code": "NA",
            "city": "Cairo",
            "country": "EG",
            "state": "NA",
        }

        # Select integration ID based on payment method
        if payment_method == 'wallet':
            integration_id = self.WALLET_INTEGRATION_ID
        elif payment_method == 'fawry':
            integration_id = self.FAWRY_INTEGRATION_ID
        else:
            integration_id = self.CARD_INTEGRATION_ID

        # Step 4: Get payment key
        payment_key = self._get_payment_key(
            auth_token,
            order_id,
            amount_cents,
            billing_data,
            integration_id
        )

        if not payment_key:
            return {
                'success': False,
                'error': 'Failed to generate payment key'
            }

        # Build iframe URL
        iframe_url = f"https://accept.paymob.com/api/acceptance/iframes/{self.iframe_id}?payment_token={payment_key}"

        return {
            'success': True,
            'payment_key': payment_key,
            'iframe_url': iframe_url,
            'order_id': order_id,
            'amount_cents': amount_cents,
        }

    def verify_callback(self, request_data):
        """
        Verify PayMob callback/webhook signature.

        PayMob sends transaction data to your callback URL.
        This method verifies the HMAC signature to ensure
        the callback is authentic.

        Args:
            request_data: dict of callback parameters

        Returns:
            bool: True if signature is valid
        """
        # PayMob sends these fields in the callback
        # They must be concatenated in this specific order for HMAC
        hmac_fields = [
            'amount_cents',
            'created_at',
            'currency',
            'error_occured',
            'has_parent_transaction',
            'id',
            'integration_id',
            'is_3d_secure',
            'is_auth',
            'is_capture',
            'is_refunded',
            'is_standalone_payment',
            'is_voided',
            'order',
            'owner',
            'pending',
            'source_data_pan',
            'source_data_sub_type',
            'source_data_type',
            'success',
        ]

        # Build the string to hash
        hmac_string = ""
        for field in hmac_fields:
            value = request_data.get(field, '')
            hmac_string += str(value)

        # Calculate HMAC
        calculated_hmac = hmac.new(
            self.hmac_secret.encode('utf-8'),
            hmac_string.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        # Compare with received HMAC
        received_hmac = request_data.get('hmac', '')

        return hmac.compare_digest(calculated_hmac, received_hmac)

    def get_transaction_status(self, transaction_id):
        """
        Get the status of a transaction.

        Args:
            transaction_id: PayMob transaction ID

        Returns:
            dict: Transaction details or None
        """
        auth_token = self._get_auth_token()
        if not auth_token:
            return None

        try:
            url = f"{self.BASE_URL}/acceptance/transactions/{transaction_id}"
            response = requests.get(
                url,
                params={"token": auth_token},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get transaction status: {e}")
            return None


# Create a singleton instance
paymob_gateway = PayMobGateway()


def get_paymob_iframe_id():
    """Helper to get PayMob iframe ID from settings."""
    return getattr(settings, 'PAYMOB_IFRAME_ID', '')
