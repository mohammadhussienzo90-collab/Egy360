"""
Payments Models - Complete and Corrected
Path: payments/models.py

All user references use Django's built-in User model (not CustomUser)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bookings.models import Booking
import uuid


class Payment(models.Model):
    """
    Payment records for bookings
    """
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('wallet', 'Digital Wallet'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    # Payment reference
    payment_reference = models.CharField(max_length=50, unique=True, blank=True)

    # Related booking
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')

    # User who made payment
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EGP')

    # Transaction details
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Payment gateway transaction ID")
    gateway = models.CharField(max_length=50, blank=True, help_text="Payment gateway used")

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Additional info
    description = models.TextField(blank=True)
    payment_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Failure details
    failure_reason = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_reference']),
            models.Index(fields=['booking', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"{self.payment_reference} - {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.payment_reference:
            self.payment_reference = self.generate_payment_reference()
        super().save(*args, **kwargs)

    def generate_payment_reference(self):
        """Generate unique payment reference"""
        prefix = 'PAY'
        unique_id = str(uuid.uuid4().int)[:12]
        return f"{prefix}{unique_id}"

    def mark_completed(self):
        """Mark payment as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

        # Update booking status
        if self.booking:
            self.booking.confirm()

    def mark_failed(self, reason=''):
        """Mark payment as failed"""
        self.status = 'failed'
        self.failed_at = timezone.now()
        self.failure_reason = reason
        self.save()

    @property
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'completed'


class Refund(models.Model):
    """
    Refund records for payments
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    REASON_CHOICES = [
        ('customer_request', 'Customer Request'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('service_not_provided', 'Service Not Provided'),
        ('overcharged', 'Overcharged'),
        ('duplicate_payment', 'Duplicate Payment'),
        ('other', 'Other'),
    ]

    # Refund reference
    refund_reference = models.CharField(max_length=50, unique=True, blank=True)

    # Related payment
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')

    # Refund details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EGP')

    # Reason
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    reason_details = models.TextField(blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Transaction details
    transaction_id = models.CharField(max_length=100, blank=True)

    # Processed by
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='refunds_requested')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='refunds_processed')

    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['refund_reference']),
            models.Index(fields=['payment', '-requested_at']),
        ]

    def __str__(self):
        return f"{self.refund_reference} - {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.refund_reference:
            self.refund_reference = self.generate_refund_reference()
        super().save(*args, **kwargs)

    def generate_refund_reference(self):
        """Generate unique refund reference"""
        prefix = 'REF'
        unique_id = str(uuid.uuid4().int)[:12]
        return f"{prefix}{unique_id}"

    def mark_completed(self):
        """Mark refund as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class PaymentMethod(models.Model):
    """
    Saved payment methods for users
    """
    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')

    # Card details (encrypted in production)
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, blank=True)
    last_four_digits = models.CharField(max_length=4, blank=True)
    card_holder_name = models.CharField(max_length=200, blank=True)
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)

    # Token from payment gateway
    payment_token = models.CharField(max_length=255, blank=True)
    gateway = models.CharField(max_length=50, blank=True)

    # Status
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        if self.last_four_digits:
            return f"{self.card_type} ending in {self.last_four_digits}"
        return f"Payment method for {self.user.username}"

    def save(self, *args, **kwargs):
        # If this is set as default, unset all other defaults for this user
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """
    Invoices for completed payments
    """
    # Invoice details
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')

    # Customer details
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_address = models.TextField(blank=True)
    customer_tax_id = models.CharField(max_length=100, blank=True)

    # Invoice amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EGP')

    # Notes
    notes = models.TextField(blank=True)

    # PDF file
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    # Timestamps
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-issued_at']
        indexes = [
            models.Index(fields=['invoice_number']),
        ]

    def __str__(self):
        return f"Invoice {self.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        """Generate unique invoice number"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m')
        unique_id = str(uuid.uuid4().int)[:8]
        return f"INV-{date_str}-{unique_id}"


class Transaction(models.Model):
    """
    Transaction log for all financial activities
    """
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('payout', 'Payout'),
        ('fee', 'Fee'),
        ('adjustment', 'Adjustment'),
    ]

    # Transaction reference
    transaction_reference = models.CharField(max_length=50, unique=True, blank=True)

    # Type
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)

    # Related records
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    refund = models.ForeignKey(Refund, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')

    # User involved
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')

    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EGP')

    # Details
    description = models.TextField()
    notes = models.TextField(blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_reference']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.transaction_reference} - {self.transaction_type}"

    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            self.transaction_reference = self.generate_transaction_reference()
        super().save(*args, **kwargs)

    def generate_transaction_reference(self):
        """Generate unique transaction reference"""
        prefix = 'TXN'
        unique_id = str(uuid.uuid4().int)[:12]
        return f"{prefix}{unique_id}"