# accommodations/admin.py
from django.contrib import admin
from .models import Accommodation, Room, Amenity

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'accommodation_type', 'star_rating',
                   'average_rating', 'is_featured', 'is_active']
    list_filter = ['accommodation_type', 'city', 'star_rating', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'city']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'accommodation_type', 'description')
        }),
        ('Location', {
            'fields': ('city', 'address', 'latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('star_rating', 'total_rooms', 'check_in_time', 'check_out_time')
        }),
        ('Pricing', {
            'fields': ('price_per_night', 'weekend_surcharge')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_verified', 'is_active')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'accommodation', 'room_type', 'max_occupancy', 'base_price']
    list_filter = ['room_type', 'accommodation']
    search_fields = ['name', 'accommodation__name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']