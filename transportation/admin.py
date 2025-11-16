# transportation/admin.py
from django.contrib import admin
from .models import TransportationService, Driver, TransportBooking

@admin.register(TransportationService)
class TransportationServiceAdmin(admin.ModelAdmin):
    # CHANGED from is_available to is_active
    list_display = ['name', 'service_type', 'max_passengers', 'is_active', 'average_rating']
    list_filter = ['service_type', 'is_active', 'has_ac', 'has_wifi']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'years_experience', 'is_active', 'is_verified', 'average_rating']
    list_filter = ['is_active', 'is_verified']
    search_fields = ['name', 'phone', 'email']

@admin.register(TransportBooking)
class TransportBookingAdmin(admin.ModelAdmin):
    list_display = ['service', 'user', 'pickup_date', 'status', 'total_price']
    list_filter = ['status', 'pickup_date']
    search_fields = ['user__username', 'contact_name', 'contact_phone']
    date_hierarchy = 'pickup_date'