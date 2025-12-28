# payments/views.py
"""
Payments App Views

Comprehensive API views for payment management including:
- Payment method management
- Payment processing with Stripe integration
- Refund handling
- Transaction logging
"""

import logging
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    PaymentMethod,
    Payment,
    Refund,
    Transaction,
)
from .serializers import (
    PaymentMethodSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentProcessSerializer,
    RefundSerializer,
    RefundRequestSerializer,
    TransactionLogSerializer,
)
from .stripe_integration import stripe_gateway, get_stripe_public_key
from core.throttling import PaymentRateThrottle

logger = logging.getLogger(__name__)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's saved payment methods (cards).

    List: Get user's saved payment methods
    Create: Save a new payment method
    Retrieve: Get specific payment method details
    Delete: Remove a saved payment method
    """

    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['card_type', 'is_active', 'is_default']
    search_fields = ['card_holder_name', 'last_four_digits']
    ordering_fields = ['is_default', 'created_at']

    def get_queryset(self):
        """Return only the current user's payment methods"""
        return PaymentMethod.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-is_default', '-created_at')


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.

    Provides payment processing and management.

    List: Authenticated users see their payments (or staff see all)
    Create: Disabled - use process action
    Retrieve: Get payment details
    Update/Delete: Disabled

    Custom Actions:
    - process: Process a new payment
    - confirm: Confirm payment
    - refund: Request refund
    - my_payments: Get current user's payments
    - download_invoice: Download payment invoice
    """

    queryset = Payment.objects.all().select_related(
        'user',
        'booking',
        'payment_method'
    ).order_by('-created_at')

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [PaymentRateThrottle]  # Strict rate limiting for payments

    filterset_fields = ['status', 'payment_method', 'booking']
    search_fields = ['transaction_id', 'reference_number']
    ordering_fields = ['created_at', 'amount']

    def get_queryset(self):
        """Filter queryset based on user role"""
        user = self.request.user

        if user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(user=user)

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action == 'retrieve':
            return PaymentDetailSerializer
        elif self.action == 'process':
            return PaymentProcessSerializer
        return PaymentDetailSerializer

    def create(self, request, *args, **kwargs):
        """Disable create - use process action instead"""
        return Response(
            {'detail': 'Use the process action to create payments'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        """Disable update"""
        return Response(
            {'detail': 'Payments cannot be updated directly'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        """Disable delete"""
        return Response(
            {'detail': 'Payments cannot be deleted. Use refund action instead'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['post'])
    def process(self, request):
        """
        Process a new payment.

        Creates a Stripe PaymentIntent and returns client_secret for frontend.
        """
        serializer = PaymentProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        currency = serializer.validated_data.get('currency', 'EGP')
        booking_id = serializer.validated_data.get('booking_id')

        # Create Stripe PaymentIntent
        stripe_result = stripe_gateway.create_payment_intent(
            amount=amount,
            currency=currency,
            metadata={
                'user_id': str(request.user.id),
                'booking_id': str(booking_id) if booking_id else '',
            }
        )

        if not stripe_result['success']:
            logger.error(f"Stripe error for user {request.user.id}: {stripe_result.get('error')}")
            return Response(
                {'error': stripe_result.get('error', 'Payment processing failed')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create pending payment record
        payment = Payment.objects.create(
            user=request.user,
            booking_id=booking_id,
            payment_method=serializer.validated_data.get('payment_method', 'stripe'),
            amount=amount,
            currency=currency,
            status='pending',
            gateway='stripe',
            transaction_id=stripe_result['payment_intent_id']
        )

        # Log transaction
        Transaction.objects.create(
            payment=payment,
            transaction_type='payment',
            user=request.user,
            amount=amount,
            currency=currency,
            description='Payment initiated via Stripe'
        )

        logger.info(f"Payment {payment.id} created for user {request.user.id}")

        return Response({
            'payment_id': payment.id,
            'client_secret': stripe_result['client_secret'],
            'public_key': get_stripe_public_key(),
            'amount': str(amount),
            'currency': currency,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def config(self, request):
        """
        Get Stripe public key for frontend initialization.
        """
        return Response({
            'public_key': get_stripe_public_key(),
            'is_configured': stripe_gateway.is_configured(),
        })

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm a payment.

        Verifies payment with Stripe and updates status to completed.
        """
        payment = self.get_object()

        if payment.status != 'pending':
            return Response(
                {'detail': f'Cannot confirm payment with status: {payment.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify with Stripe if we have a transaction_id
        if payment.transaction_id and payment.gateway == 'stripe':
            stripe_result = stripe_gateway.confirm_payment_intent(payment.transaction_id)

            if not stripe_result['success']:
                return Response(
                    {'detail': 'Could not verify payment with payment gateway'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if stripe_result['status'] != 'succeeded':
                return Response(
                    {'detail': f'Payment not yet complete. Status: {stripe_result["status"]}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.save()

        # Log transaction
        Transaction.objects.create(
            payment=payment,
            transaction_type='payment',
            user=payment.user,
            amount=payment.amount,
            currency=payment.currency,
            description='Payment confirmed'
        )

        # Update booking payment status if applicable
        if payment.booking:
            payment.booking.payment_status = 'paid'
            payment.booking.save()

        logger.info(f"Payment {payment.id} confirmed")

        return Response(
            PaymentDetailSerializer(payment).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """
        Request a refund for a payment.

        Creates a refund request and processes via Stripe if applicable.
        """
        payment = self.get_object()

        if payment.status != 'completed':
            return Response(
                {'detail': 'Can only refund completed payments'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RefundRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refund_amount = serializer.validated_data['amount']
        reason = serializer.validated_data['reason']

        # Process refund via Stripe if applicable
        stripe_refund_id = None
        if payment.transaction_id and payment.gateway == 'stripe':
            stripe_result = stripe_gateway.process_refund(
                payment.transaction_id,
                amount=refund_amount,
                reason='requested_by_customer'
            )

            if not stripe_result['success']:
                logger.error(f"Stripe refund failed for payment {payment.id}: {stripe_result.get('error')}")
                return Response(
                    {'detail': stripe_result.get('error', 'Refund processing failed')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stripe_refund_id = stripe_result.get('refund_id')

        # Create refund record
        refund = Refund.objects.create(
            payment=payment,
            amount=refund_amount,
            reason=reason,
            status='completed' if stripe_refund_id else 'pending',
            transaction_id=stripe_refund_id or '',
            requested_by=request.user
        )

        # Log transaction
        Transaction.objects.create(
            payment=payment,
            refund=refund,
            transaction_type='refund',
            user=request.user,
            amount=refund_amount,
            currency=payment.currency,
            description=f'Refund processed: {reason}'
        )

        # Update payment status if fully refunded
        if refund_amount >= payment.amount:
            payment.status = 'refunded'
            payment.save()

        logger.info(f"Refund {refund.id} created for payment {payment.id}")

        return Response(
            RefundSerializer(refund).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """
        Get current user's payments.

        Returns all payments for the authenticated user.
        """
        payments = self.get_queryset().filter(user=request.user)

        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            payments = payments.filter(status=status_filter)

        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = PaymentListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_invoice(self, request, pk=None):
        """
        Download payment invoice.

        Generates and returns a PDF invoice for the payment.
        """
        payment = self.get_object()

        if payment.status != 'completed':
            return Response(
                {'detail': 'Invoice only available for completed payments'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Here you would generate PDF invoice
        # For now, return payment details
        return Response({
            'message': 'Invoice generation not yet implemented',
            'payment': PaymentDetailSerializer(payment).data
        })


class PaymentRefundViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing refunds.

    Read-only access to refund information.

    List: Get refunds (filtered by permission)
    Retrieve: Get specific refund details

    Custom Actions:
    - my_refunds: Get current user's refunds
    """

    queryset = Refund.objects.all().select_related(
        'payment',
        'requested_by'
    ).order_by('-requested_at')

    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['status', 'payment']
    search_fields = ['reason', 'reason_details']
    ordering_fields = ['requested_at', 'amount']

    def get_queryset(self):
        """Filter refunds based on user role"""
        user = self.request.user

        if user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(payment__user=user)

    @action(detail=False, methods=['get'])
    def my_refunds(self, request):
        """
        Get current user's refunds.

        Returns all refunds for the authenticated user.
        """
        refunds = self.get_queryset().filter(payment__user=request.user)

        page = self.paginate_queryset(refunds)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(refunds, many=True)
        return Response(serializer.data)


class TransactionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing transaction logs.

    Read-only access to transaction history.
    Staff only.

    List: Get all transaction logs
    Retrieve: Get specific log entry
    """

    queryset = Transaction.objects.all().select_related(
        'payment'
    ).order_by('-created_at')

    serializer_class = TransactionLogSerializer
    permission_classes = [permissions.IsAdminUser]

    filterset_fields = ['payment', 'transaction_type']
    search_fields = ['description', 'notes']
    ordering_fields = ['created_at']


# Stripe Webhook Handler
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhook events.

    Processes payment confirmation, failure, and refund events.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    event = stripe_gateway.verify_webhook_signature(payload, sig_header)

    if not event:
        logger.warning("Invalid Stripe webhook signature")
        return HttpResponse(status=400)

    event_type = event['type']
    data = event['data']['object']

    logger.info(f"Received Stripe webhook: {event_type}")

    try:
        if event_type == 'payment_intent.succeeded':
            # Payment successful
            payment_intent_id = data['id']
            payment = Payment.objects.filter(
                transaction_id=payment_intent_id,
                gateway='stripe'
            ).first()

            if payment and payment.status == 'pending':
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.save()

                # Log transaction
                Transaction.objects.create(
                    payment=payment,
                    transaction_type='payment',
                    user=payment.user,
                    amount=payment.amount,
                    currency=payment.currency,
                    description='Payment confirmed via Stripe webhook'
                )

                # Update booking if applicable
                if payment.booking:
                    payment.booking.payment_status = 'paid'
                    payment.booking.save()

                logger.info(f"Payment {payment.id} confirmed via webhook")

        elif event_type == 'payment_intent.payment_failed':
            # Payment failed
            payment_intent_id = data['id']
            payment = Payment.objects.filter(
                transaction_id=payment_intent_id,
                gateway='stripe'
            ).first()

            if payment and payment.status == 'pending':
                failure_message = data.get('last_payment_error', {}).get('message', 'Payment failed')
                payment.status = 'failed'
                payment.failed_at = timezone.now()
                payment.failure_reason = failure_message
                payment.save()

                logger.warning(f"Payment {payment.id} failed: {failure_message}")

        elif event_type == 'charge.refunded':
            # Refund processed
            charge_id = data['id']
            payment_intent_id = data.get('payment_intent')

            if payment_intent_id:
                payment = Payment.objects.filter(
                    transaction_id=payment_intent_id,
                    gateway='stripe'
                ).first()

                if payment:
                    refund_amount = data['amount_refunded'] / 100  # Convert from cents
                    if refund_amount >= float(payment.amount):
                        payment.status = 'refunded'
                        payment.save()

                    logger.info(f"Refund processed for payment {payment.id}")

    except Exception as e:
        logger.error(f"Error processing webhook {event_type}: {e}")
        # Still return 200 to prevent Stripe retries for processing errors
        return HttpResponse(status=200)

    return HttpResponse(status=200)


# =============================================================================
# PAYMENT CHECKOUT VIEWS
# =============================================================================
#
# These views handle the user-facing payment flow:
# 1. payment_checkout: Displays Stripe card form, creates PaymentIntent
# 2. payment_success: Verifies payment completion, updates booking status
#
# Flow: User fills booking form -> Redirected here -> Enters card -> Success page
# =============================================================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking


@login_required
def payment_checkout(request, booking_id):
    """
    Payment checkout page with Stripe Elements card form.

    This view:
    1. Validates the booking belongs to the current user
    2. Checks if already paid (prevents double-payment)
    3. Creates a Stripe PaymentIntent for secure card processing
    4. Creates/updates a Payment record in our database
    5. Renders the checkout template with Stripe.js integration

    Args:
        request: HTTP request object
        booking_id: ID of the booking to pay for

    Returns:
        Rendered checkout template or redirect on error/already paid
    """
    # Security: Ensure user can only pay for their own bookings
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Prevent double-payment - redirect if already paid
    if booking.payment_status == 'paid':
        messages.info(request, 'This booking has already been paid.')
        return redirect('bookings:confirmation', booking_id=booking.id)

    # Get the actual item (Accommodation or Tour) via GenericForeignKey
    item = booking.content_object

    # Create Stripe PaymentIntent - this is required for secure card processing
    # The client_secret is used by Stripe.js on the frontend to confirm payment
    result = stripe_gateway.create_payment_intent(
        amount=float(booking.total_amount),
        currency='EGP',  # Egyptian Pounds
        metadata={
            # Metadata helps identify the payment in Stripe Dashboard
            'booking_id': str(booking.id),
            'booking_reference': booking.booking_reference,
            'user_id': str(request.user.id),
        }
    )

    # Handle Stripe initialization failure (API keys invalid, network error, etc.)
    if not result.get('success'):
        messages.error(request, f"Payment initialization failed: {result.get('error', 'Unknown error')}")
        return redirect('bookings:detail', booking_id=booking.id)

    # Create or get existing Payment record
    # Using get_or_create prevents duplicate records if user refreshes page
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        user=request.user,
        defaults={
            'payment_method': 'stripe',
            'amount': booking.total_amount,
            'currency': 'EGP',
            'status': 'pending',
            'gateway': 'stripe',
            'transaction_id': result['payment_intent_id'],
        }
    )

    # If payment record already exists but is pending, update with new PaymentIntent
    # This handles cases where user abandoned checkout and returned
    if not created and payment.status == 'pending':
        payment.transaction_id = result['payment_intent_id']
        payment.save()

    # Prepare context for template
    # client_secret and stripe_public_key are required by Stripe.js
    context = {
        'booking': booking,
        'item': item,
        'payment': payment,
        'client_secret': result['client_secret'],  # For Stripe.js confirmCardPayment()
        'stripe_public_key': get_stripe_public_key(),  # For Stripe() initialization
        'amount': booking.total_amount,
        'currency': 'EGP',
    }

    return render(request, 'payments/checkout.html', context)


@login_required
def payment_success(request, booking_id):
    """
    Payment success page after Stripe payment completion.

    This view:
    1. Retrieves the booking and associated payment
    2. Verifies payment status with Stripe API (double-check)
    3. Updates payment and booking status to confirmed/paid
    4. Creates transaction log for audit trail
    5. Displays success confirmation to user

    Note: Payment confirmation also happens via Stripe webhooks as backup.
    This view provides immediate feedback to users after payment.

    Args:
        request: HTTP request object
        booking_id: ID of the paid booking

    Returns:
        Rendered success template with booking/payment details
    """
    # Security: Ensure user can only view their own booking success
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Get the most recent payment for this booking
    payment = Payment.objects.filter(booking=booking).order_by('-created_at').first()

    # Get the actual item (Accommodation or Tour)
    item = booking.content_object

    # Verify and update payment status if still pending
    # This provides immediate confirmation without waiting for webhook
    if payment and payment.transaction_id and payment.status == 'pending':
        # Call Stripe API to verify payment succeeded
        stripe_result = stripe_gateway.confirm_payment_intent(payment.transaction_id)

        if stripe_result.get('success') and stripe_result.get('status') == 'succeeded':
            # Update payment record
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()

            # Update booking to confirmed status
            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.save()

            # Create transaction log for financial audit trail
            Transaction.objects.create(
                payment=payment,
                transaction_type='payment',
                user=request.user,
                amount=payment.amount,
                currency=payment.currency,
                description='Payment completed successfully'
            )

            logger.info(f"Payment {payment.id} confirmed for booking {booking.id}")

    context = {
        'booking': booking,
        'item': item,
        'payment': payment,
    }

    return render(request, 'payments/success.html', context)