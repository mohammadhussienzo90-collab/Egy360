# bookings/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    BOOKING_TYPES = [
        ('accommodation', 'Accommodation'),
        ('tour', 'Tour'),
        ('transportation', 'Transportation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    # Generic relation to different booking types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    booking_reference = models.CharField(max_length=20, unique=True)

    # Dates
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')

    # Contact
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Additional info
    special_requests = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status'], name='booking_user_status_idx'),
            models.Index(fields=['status'], name='booking_status_idx'),
            models.Index(fields=['booking_type'], name='booking_type_idx'),
            models.Index(fields=['content_type', 'object_id'], name='booking_content_idx'),
            models.Index(fields=['booking_date'], name='booking_date_idx'),
        ]

    def __str__(self):
        return f"{self.booking_reference} - {self.user.username}"

    def confirm(self):
        """Mark booking as confirmed"""
        self.status = 'confirmed'
        self.save()

    def cancel(self):
        """Mark booking as cancelled"""
        self.status = 'cancelled'
        self.save()

    def complete(self):
        """Mark booking as completed"""
        self.status = 'completed'
        self.save()

class AccommodationBooking(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='accommodation_details')
    accommodation = models.ForeignKey('accommodations.Accommodation', on_delete=models.CASCADE)
    room = models.ForeignKey('accommodations.Room', on_delete=models.CASCADE, null=True, blank=True)

    number_of_guests = models.IntegerField(default=1)
    number_of_rooms = models.IntegerField(default=1)

    def __str__(self):
        return f"Accommodation booking for {self.accommodation.name}"

class BookingModification(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='modifications')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    modification_date = models.DateTimeField(auto_now_add=True)

    old_data = models.JSONField()
    new_data = models.JSONField()
    reason = models.TextField()

    def __str__(self):
        return f"Modification for {self.booking.booking_reference}"

class BookingCancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='cancellation')
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cancellation_date = models.DateTimeField(auto_now_add=True)

    reason = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Cancellation for {self.booking.booking_reference}"