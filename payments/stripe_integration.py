# payments/stripe_integration.py
"""
Stripe Payment Gateway Integration for Egy360

Handles:
- Payment Intent creation
- Payment confirmation
- Refund processing
- Webhook handling
"""

import logging
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

logger = logging.getLogger(__name__)

# Try to import stripe, make it optional for development
try:
    import stripe
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    STRIPE_AVAILABLE = True
except ImportError:
    stripe = None
    STRIPE_AVAILABLE = False
    logger.warning("Stripe module not installed. Payment processing will be unavailable.")


class StripePaymentGateway:
    """
    Stripe payment gateway wrapper for Egy360
    """

    def __init__(self):
        self.public_key = getattr(settings, 'STRIPE_PUBLIC_KEY', '')
        self.secret_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        self.webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

        if not self.secret_key:
            logger.warning("Stripe secret key not configured")

    def is_configured(self):
        """Check if Stripe is properly configured"""
        return STRIPE_AVAILABLE and bool(self.secret_key and self.public_key)

    def create_payment_intent(self, amount, currency='EGP', metadata=None):
        """
        Create a Stripe PaymentIntent

        Args:
            amount: Amount in cents (for USD) or smallest currency unit
            currency: Currency code (default EGP)
            metadata: Optional metadata dict

        Returns:
            dict with client_secret and payment_intent_id, or error
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Payment gateway not configured'
            }

        try:
            # Stripe expects amount in smallest currency unit (cents/piastres)
            amount_in_cents = int(Decimal(str(amount)) * 100)

            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency=currency.lower(),
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True},
            )

            logger.info(f"Created PaymentIntent: {intent.id}")

            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
            }

        except stripe.error.CardError as e:
            logger.warning(f"Card error: {e.user_message}")
            return {
                'success': False,
                'error': e.user_message,
                'code': e.code
            }
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Invalid request to Stripe: {e}")
            return {
                'success': False,
                'error': 'Invalid payment request'
            }
        except stripe.error.AuthenticationError:
            logger.error("Stripe authentication failed - check API keys")
            return {
                'success': False,
                'error': 'Payment service configuration error'
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            return {
                'success': False,
                'error': 'Payment processing error. Please try again.'
            }

    def confirm_payment_intent(self, payment_intent_id):
        """
        Retrieve and confirm payment intent status

        Args:
            payment_intent_id: Stripe PaymentIntent ID

        Returns:
            dict with status and details
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Payment gateway not configured'
            }

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            return {
                'success': True,
                'status': intent.status,
                'amount': intent.amount / 100,  # Convert back from cents
                'currency': intent.currency.upper(),
                'payment_method': intent.payment_method,
                'metadata': intent.metadata,
            }

        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving PaymentIntent {payment_intent_id}: {e}")
            return {
                'success': False,
                'error': 'Could not verify payment status'
            }

    def process_refund(self, payment_intent_id, amount=None, reason='requested_by_customer'):
        """
        Process a refund for a payment

        Args:
            payment_intent_id: Stripe PaymentIntent ID
            amount: Optional partial refund amount (full refund if None)
            reason: Refund reason

        Returns:
            dict with refund details or error
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Payment gateway not configured'
            }

        try:
            refund_params = {
                'payment_intent': payment_intent_id,
                'reason': reason,
            }

            if amount:
                # Convert to cents
                refund_params['amount'] = int(Decimal(str(amount)) * 100)

            refund = stripe.Refund.create(**refund_params)

            logger.info(f"Created refund: {refund.id}")

            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100,
            }

        except stripe.error.StripeError as e:
            logger.error(f"Refund error: {e}")
            return {
                'success': False,
                'error': 'Refund processing error'
            }

    def verify_webhook_signature(self, payload, sig_header):
        """
        Verify Stripe webhook signature

        Args:
            payload: Request body
            sig_header: Stripe-Signature header

        Returns:
            Stripe Event object or None
        """
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured")
            return None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event
        except ValueError:
            logger.error("Invalid webhook payload")
            return None
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid webhook signature")
            return None


# Singleton instance
stripe_gateway = StripePaymentGateway()


def get_stripe_public_key():
    """Get Stripe public key for frontend"""
    return getattr(settings, 'STRIPE_PUBLIC_KEY', '')
