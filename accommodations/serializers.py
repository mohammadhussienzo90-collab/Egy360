# accommodations/serializers.py
from rest_framework import serializers
from .models import Accommodation, Room, Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class AccommodationListSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'slug', 'accommodation_type', 'city',
                  'star_rating', 'price_per_night', 'average_rating',
                  'main_image', 'amenities']


class AccommodationSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Accommodation
        fields = '__all__'