# payments/views.py
"""
Payments App Views

Comprehensive API views for payment management including:
- Payment method management
- Payment processing
- Refund handling
- Transaction logging
"""

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
    TransactionLog,
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


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing available payment methods.

    Read-only access to payment methods.

    List: Get all active payment methods
    Retrieve: Get specific payment method details
    """

    queryset = PaymentMethod.objects.filter(is_active=True).order_by('name')
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = ['method_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


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

        Creates and processes a payment transaction.
        Integrates with payment gateway.
        """
        serializer = PaymentProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Here you would integrate with payment gateway
        # For now, we'll create a pending payment

        payment = Payment.objects.create(
            user=request.user,
            booking_id=serializer.validated_data.get('booking_id'),
            payment_method_id=serializer.validated_data['payment_method_id'],
            amount=serializer.validated_data['amount'],
            currency=serializer.validated_data.get('currency', 'EGP'),
            status='pending',
            transaction_id=f'TXN-{timezone.now().strftime("%Y%m%d%H%M%S")}-{request.user.id}'
        )

        # Log transaction
        TransactionLog.objects.create(
            payment=payment,
            action='payment_initiated',
            status='pending',
            message='Payment initiated by user'
        )

        return Response(
            PaymentDetailSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm a payment.

        Updates payment status to completed after gateway confirmation.
        Staff only action.
        """
        if not request.user.is_staff:
            return Response(
                {'detail': 'Only staff can confirm payments'},
                status=status.HTTP_403_FORBIDDEN
            )

        payment = self.get_object()

        if payment.status != 'pending':
            return Response(
                {'detail': f'Cannot confirm payment with status: {payment.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.save()

        # Log transaction
        TransactionLog.objects.create(
            payment=payment,
            action='payment_confirmed',
            status='completed',
            message='Payment confirmed by staff'
        )

        # Update booking payment status if applicable
        if payment.booking:
            payment.booking.payment_status = 'paid'
            payment.booking.save()

        return Response(
            PaymentDetailSerializer(payment).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """
        Request a refund for a payment.

        Creates a refund request for a completed payment.
        """
        payment = self.get_object()

        if payment.status != 'completed':
            return Response(
                {'detail': 'Can only refund completed payments'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RefundRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create refund
        refund = Refund.objects.create(
            payment=payment,
            amount=serializer.validated_data['amount'],
            reason=serializer.validated_data['reason'],
            status='pending',
            requested_by=request.user
        )

        # Log transaction
        TransactionLog.objects.create(
            payment=payment,
            action='refund_requested',
            status='pending',
            message=f'Refund requested: {serializer.validated_data["reason"]}'
        )

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
    ).order_by('-created_at')

    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['status', 'payment']
    search_fields = ['reason']
    ordering_fields = ['created_at', 'amount']

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

    queryset = TransactionLog.objects.all().select_related(
        'payment'
    ).order_by('-created_at')

    serializer_class = TransactionLogSerializer
    permission_classes = [permissions.IsAdminUser]

    filterset_fields = ['payment', 'action', 'status']
    search_fields = ['message', 'response_data']
    ordering_fields = ['created_at']