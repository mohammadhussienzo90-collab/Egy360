# bookings/admin.py
from django.contrib import admin
from .models import Booking, AccommodationBooking, BookingModification, BookingCancellation

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'booking_type', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'booking_type', 'created_at']
    search_fields = ['booking_reference', 'user__username', 'contact_email']
    date_hierarchy = 'created_at'
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']

@admin.register(AccommodationBooking)
class AccommodationBookingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'accommodation', 'number_of_guests']
    search_fields = ['booking__booking_reference']

@admin.register(BookingModification)
class BookingModificationAdmin(admin.ModelAdmin):
    list_display = ['booking', 'modified_by', 'modification_date']
    date_hierarchy = 'modification_date'

@admin.register(BookingCancellation)
class BookingCancellationAdmin(admin.ModelAdmin):
    list_display = ['booking', 'cancelled_by', 'cancellation_date', 'refund_amount']
    list_filter = ['refund_status', 'cancellation_date']