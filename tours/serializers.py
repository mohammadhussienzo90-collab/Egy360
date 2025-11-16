# tours/serializers.py
from rest_framework import serializers
from .models import Tour, TourItinerary, TourBooking


class TourItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItinerary
        fields = '__all__'


class TourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['id', 'name', 'slug', 'tour_type', 'duration_days',
                  'price_per_person', 'average_rating', 'main_image']


class TourSerializer(serializers.ModelSerializer):
    itinerary = TourItinerarySerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'


class TourBookingSerializer(serializers.ModelSerializer):
    tour_name = serializers.ReadOnlyField(source='tour.name')

    class Meta:
        model = TourBooking
        fields = '__all__'