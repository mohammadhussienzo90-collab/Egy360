# destinations/serializers.py
from rest_framework import serializers
from .models import Country, City, Attraction, TravelGuide


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CityListSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'slug', 'country_name', 'description',
                  'is_popular', 'main_image']


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    attractions_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = '__all__'

    def get_attractions_count(self, obj):
        return obj.attractions.count()


class AttractionSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Attraction
        fields = '__all__'


class TravelGuideSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = TravelGuide
        fields = '__all__'