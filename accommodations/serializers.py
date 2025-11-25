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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'slug', 'accommodation_type', 'city',
                  'star_rating', 'price_per_night', 'average_rating',
                  'image', 'amenities']

    def get_image(self, obj):
        """Return image_url if available, otherwise main_image URL"""
        if obj.image_url:
            return obj.image_url
        elif obj.main_image:
            return obj.main_image.url
        return ''


class AccommodationSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Accommodation
        fields = '__all__'

    def get_image(self, obj):
        """Return image_url if available, otherwise main_image URL"""
        if obj.image_url:
            return obj.image_url
        elif obj.main_image:
            return obj.main_image.url
        return ''