# destinations/admin.py
from django.contrib import admin
from .models import Country, City, Attraction, TravelGuide


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'flag_emoji']
    search_fields = ['name', 'code']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_popular', 'is_capital', 'has_airport']
    list_filter = ['country', 'is_popular', 'is_capital', 'has_airport']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('country', 'name', 'slug', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'timezone')
        }),
        ('Details', {
            'fields': ('population', 'elevation', 'best_time_to_visit',
                       'average_temperature_summer', 'average_temperature_winter')
        }),
        ('Features', {
            'fields': ('is_popular', 'is_capital', 'has_airport')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
    )


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'attraction_type', 'is_must_see', 'is_unesco', 'average_rating']
    list_filter = ['attraction_type', 'is_must_see', 'is_unesco', 'is_family_friendly']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('city', 'name', 'slug', 'attraction_type', 'description')
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Visit Information', {
            'fields': ('opening_hours', 'admission_fee', 'visit_duration')
        }),
        ('Features', {
            'fields': ('is_unesco', 'is_must_see', 'is_family_friendly', 'accessibility_info')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_reviews')
        }),
    )


@admin.register(TravelGuide)
class TravelGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'is_transportation', 'is_accommodation',
                   'is_food', 'is_safety', 'is_culture']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}