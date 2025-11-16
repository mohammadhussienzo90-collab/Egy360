# tours/admin.py
from django.contrib import admin
from .models import Tour, TourItinerary, TourBooking

class TourItineraryInline(admin.TabularInline):
    model = TourItinerary
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'tour_type', 'duration_days', 'price_per_person', 
                   'average_rating', 'is_featured', 'is_active']
    list_filter = ['tour_type', 'difficulty_level', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'departure_city']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourItineraryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'tour_type', 'description', 'highlights')
        }),
        ('Duration & Logistics', {
            'fields': ('duration_days', 'duration_nights', 'departure_city', 
                      'destinations', 'difficulty_level')
        }),
        ('Group Details', {
            'fields': ('min_group_size', 'max_group_size')
        }),
        ('Pricing', {
            'fields': ('price_per_person', 'child_discount')
        }),
        ('Details', {
            'fields': ('includes', 'excludes', 'languages')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
    )

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ['tour', 'user', 'tour_date', 'status', 'total_price']
    list_filter = ['status', 'tour_date']
    search_fields = ['tour__name', 'user__username', 'contact_email']
    date_hierarchy = 'tour_date'