# accommodations/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import Accommodation, Room, Amenity

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'accommodation_type', 'star_rating',
                   'average_rating', 'is_featured', 'is_active', 'has_image']
    list_filter = ['accommodation_type', 'city', 'star_rating', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'city']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['populate_images_action']

    def has_image(self, obj):
        return bool(obj.image_url or obj.main_image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

    def populate_images_action(self, request, queryset):
        """Populate selected accommodations with Unsplash hotel images"""
        hotel_images = [
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
            'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400',
            'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400',
            'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400',
            'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400',
            'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400',
            'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400',
            'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400',
            'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400',
            'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400',
        ]

        updated = 0
        for i, acc in enumerate(queryset):
            if not acc.image_url:
                acc.image_url = hotel_images[i % len(hotel_images)]
                acc.save(update_fields=['image_url'])
                updated += 1

        self.message_user(
            request,
            f'Successfully populated {updated} accommodation(s) with images.',
            messages.SUCCESS
        )
    populate_images_action.short_description = 'Populate with hotel images'

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
            'fields': ('main_image', 'image_url')
        }),
        ('Affiliate Links (Monetization)', {
            'fields': ('booking_com_id', 'booking_com_url', 'agoda_url', 'hotels_com_url', 'direct_booking_url', 'commission_rate', 'total_bookings', 'total_commission_earned'),
            'description': 'Add affiliate links to earn commission from bookings'
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