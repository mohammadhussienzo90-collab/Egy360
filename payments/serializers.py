# payments/serializers.py
"""
Payments App Serializers

Serializers for payment processing, refunds, and transaction logging.
"""

from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone

from .models import (
    PaymentMethod,
    Payment,
    Refund,  # ✅ Changed from PaymentRefund
    TransactionLog,
)
from bookings.models import Booking


# ==============================================================================
# PAYMENT METHOD SERIALIZERS
# ==============================================================================

class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializer for payment methods.
    
    Used for displaying available payment options.
    """
    
    method_type_display = serializers.CharField(
        source='get_method_type_display',
        read_only=True
    )
    
    class Meta:
        model = PaymentMethod
        fields = [
            'id',
            'name',
            'method_type',
            'method_type_display',
            'description',
            'icon',
            'is_active',
            'processing_fee_percentage',
            'min_amount',
            'max_amount',
        ]
        read_only_fields = ['processing_fee_percentage', 'min_amount', 'max_amount']


# ==============================================================================
# PAYMENT SERIALIZERS
# ==============================================================================

class PaymentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing payments.
    """
    
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    payment_method_name = serializers.CharField(source='payment_method.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'transaction_id',
            'user',
            'user_full_name',
            'payment_method',
            'payment_method_name',
            'amount',
            'currency',
            'status',
            'status_display',
            'created_at',
        ]
        read_only_fields = ['transaction_id', 'created_at']


class PaymentDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for payment information.
    """
    
    user_details = serializers.SerializerMethodField()
    payment_method_details = PaymentMethodSerializer(source='payment_method', read_only=True)
    booking_details = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'transaction_id',
            'reference_number',
            'user',
            'user_details',
            'booking',
            'booking_details',
            'payment_method',
            'payment_method_details',
            'amount',
            'currency',
            'processing_fee',
            'total_amount',
            'status',
            'status_display',
            'gateway_response',
            'failure_reason',
            'paid_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'transaction_id',
            'reference_number',
            'processing_fee',
            'total_amount',
            'gateway_response',
            'created_at',
            'updated_at',
        ]
    
    def get_user_details(self, obj):
        """Get user information"""
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
        }
    
    def get_booking_details(self, obj):
        """Get booking information if applicable"""
        if obj.booking:
            return {
                'id': obj.booking.id,
                'booking_number': obj.booking.booking_number,
                'booking_type': obj.booking.booking_type,
                'total_amount': str(obj.booking.total_amount),
            }
        return None


class PaymentProcessSerializer(serializers.Serializer):
    """
    Serializer for processing new payments.
    """
    
    booking_id = serializers.IntegerField(required=False)
    payment_method_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    currency = serializers.CharField(
        max_length=3,
        default='EGP'
    )
    payment_details = serializers.JSONField(required=False)
    
    def validate_payment_method_id(self, value):
        """Validate payment method exists and is active"""
        try:
            method = PaymentMethod.objects.get(id=value)
            if not method.is_active:
                raise serializers.ValidationError('Payment method is not active')
            return value
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError('Payment method not found')
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0')
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Validate booking if provided
        if 'booking_id' in data:
            try:
                booking = Booking.objects.get(id=data['booking_id'])
                if booking.status not in ['confirmed', 'pending']:
                    raise serializers.ValidationError({
                        'booking_id': 'Cannot process payment for this booking status'
                    })
                
                # Verify amount matches booking
                if data['amount'] != booking.total_amount:
                    raise serializers.ValidationError({
                        'amount': f'Amount must match booking total: {booking.total_amount}'
                    })
            except Booking.DoesNotExist:
                raise serializers.ValidationError({
                    'booking_id': 'Booking not found'
                })
        
        return data


# ==============================================================================
# REFUND SERIALIZERS
# ==============================================================================

class RefundSerializer(serializers.ModelSerializer):
    """
    Serializer for refund information.
    """
    
    payment_details = serializers.SerializerMethodField()
    requested_by_name = serializers.CharField(
        source='requested_by.get_full_name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Refund
        fields = [
            'id',
            'payment',
            'payment_details',
            'amount',
            'reason',
            'status',
            'status_display',
            'requested_by',
            'requested_by_name',
            'processed_by',
            'admin_notes',
            'refunded_at',
            'created_at',
        ]
        read_only_fields = [
            'requested_by',
            'processed_by',
            'refunded_at',
            'created_at',
        ]
    
    def get_payment_details(self, obj):
        """Get related payment information"""
        payment = obj.payment
        return {
            'id': payment.id,
            'transaction_id': payment.transaction_id,
            'amount': str(payment.amount),
            'currency': payment.currency,
        }


class RefundRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a refund.
    """
    
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    reason = serializers.CharField(
        max_length=500,
        required=True
    )
    
    def validate_amount(self, value):
        """Validate refund amount is positive"""
        if value <= 0:
            raise serializers.ValidationError('Refund amount must be greater than 0')
        return value
    
    def validate(self, data):
        """Validate refund amount doesn't exceed payment"""
        payment = self.context.get('payment')
        if payment and data['amount'] > payment.amount:
            raise serializers.ValidationError({
                'amount': f'Refund amount cannot exceed payment amount: {payment.amount}'
            })
        return data


# ==============================================================================
# TRANSACTION LOG SERIALIZERS
# ==============================================================================

class TransactionLogSerializer(serializers.ModelSerializer):
    """
    Serializer for transaction logs.
    """
    
    payment_transaction_id = serializers.CharField(
        source='payment.transaction_id',
        read_only=True
    )
    action_display = serializers.CharField(
        source='get_action_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = TransactionLog
        fields = [
            'id',
            'payment',
            'payment_transaction_id',
            'action',
            'action_display',
            'status',
            'status_display',
            'message',
            'request_data',
            'response_data',
            'created_at',
        ]
        read_only_fields = ['created_at']