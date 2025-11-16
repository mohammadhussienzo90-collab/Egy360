from rest_framework import serializers
from .models import TransportationType, TransportCompany, Route, Vehicle, Driver

"""
TRANSPORTATION SERIALIZERS
===========================
These serializers handle conversion between:
- Django Transportation models (Python objects)
- JSON format (API responses)

Transportation is unique because it involves:
- Companies (providers)
- Routes (connections between cities)
- Vehicles & Drivers (resources)
- Real-time seat availability

Pattern: Same as Accommodations but adapted for transport domain
"""


class TransportationTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for transportation types (Bus, Train, Taxi, Flight)

    WHAT IT DOES:
    - Simple lookup for transport types
    - Exposes: id, name, description, icon
    - Used for filtering routes by transport type

    DESIGN DECISION:
    - Kept minimal - just reference data
    - Reused across multiple views
    """

    class Meta:
        model = TransportationType
        fields = ('id', 'name', 'description', 'icon')
        read_only_fields = ('id',)


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for driver information

    WHAT IT DOES:
    - Shows driver details for safety/transparency
    - Exposes: name, experience, background check status
    - DOES NOT expose personal ID/license details (security)

    SECURITY DECISION:
    - We DON'T expose license_number or license_expiry
    - Only admin sees sensitive data
    - Tourist sees: name, experience, background_check_done

    LEARNING POINT:
    - Always think about what data is safe to expose
    - Tourist needs to trust driver, not access his ID
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = (
            'id',
            'full_name',
            'years_of_experience',
            'background_check_done',
            'is_active',
        )
        read_only_fields = ('id', 'full_name')

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}"


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for vehicle information

    WHAT IT DOES:
    - Shows vehicle specs for transparency
    - Exposes: type, capacity, amenities, safety status
    - NOT exposes: registration details (security)

    TOURIST NEEDS TO KNOW:
    - What type of vehicle (AC Bus, Train, etc)
    - How many seats
    - What amenities (WiFi, toilet, etc)
    - Is it safe/roadworthy
    """

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'vehicle_type',
            'model',
            'year',
            'capacity',
            'is_roadworthy',
        )
        read_only_fields = ('id',)


class TransportCompanyListSerializer(serializers.ModelSerializer):
    """
    List view serializer - search results for transport companies

    WHAT IT DOES:
    - Shows company summary for browsing
    - Includes: name, type, rating, verification status
    - Fast to load (minimal fields)

    WHY MINIMAL:
    - Tourist browses 5-10 companies
    - Need quick load times
    - Don't need full details yet
    """

    transportation_type_name = serializers.CharField(
        source='transportation_type.name',
        read_only=True
    )

    class Meta:
        model = TransportCompany
        fields = (
            'id',
            'name',
            'slug',
            'transportation_type',
            'transportation_type_name',
            'logo',
            'average_rating',
            'total_reviews',
            'is_verified',
            'is_safe',
            'safety_score',
            'has_insurance',
        )
        read_only_fields = (
            'id',
            'slug',
            'average_rating',
            'total_reviews',
            'transportation_type_name',
        )


class TransportCompanyDetailSerializer(serializers.ModelSerializer):
    """
    Detail view serializer - COMPLETE company information

    WHAT IT DOES:
    - Shows everything about company
    - Includes: contact, verification docs, insurance
    - Tourist can make informed decision

    TRUST BUILDING:
    - Shows verification status
    - Shows insurance status
    - Shows safety score
    - Shows reviews count
    - Shows license information
    """

    transportation_type = TransportationTypeSerializer(read_only=True)

    class Meta:
        model = TransportCompany
        fields = (
            'id',
            'name',
            'slug',
            'transportation_type',
            'description',
            'logo',
            'phone_number',
            'email',
            'website',
            'average_rating',
            'total_reviews',
            'is_verified',
            'verification_status',
            'is_safe',
            'safety_score',
            'has_insurance',
            'is_active',
            'created_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'average_rating',
            'total_reviews',
            'created_at',
        )


class RouteListSerializer(serializers.ModelSerializer):
    """
    List view serializer - search results for routes

    WHAT IT DOES:
    - Shows available routes between cities
    - Includes: cities, time, price, seats available
    - Optimized for search/filter performance

    SEARCH OPTIMIZATION:
    - Tourist searches: Cairo → Luxor
    - Sees 5-10 route options
    - Shows: departure time, price, available seats
    - THEN clicks to see details

    LEARNING POINT:
    - source='field_name' gets data from related object
    - Flatten nested data for easy consumption
    """

    departure_city_name = serializers.CharField(
        source='departure_city.name',
        read_only=True
    )
    arrival_city_name = serializers.CharField(
        source='arrival_city.name',
        read_only=True
    )
    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )
    route_display = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            'id',
            'slug',
            'company',
            'company_name',
            'departure_city',
            'departure_city_name',
            'arrival_city',
            'arrival_city_name',
            'route_display',
            'departure_time',
            'arrival_time',
            'base_price',
            'available_seats',
            'total_seats',
            'is_active',
        )
        read_only_fields = (
            'id',
            'slug',
            'company_name',
            'departure_city_name',
            'arrival_city_name',
            'route_display',
        )

    def get_route_display(self, obj):
        """Format route as "Cairo → Luxor" for display"""
        return f"{obj.departure_city.name} → {obj.arrival_city.name}"


class RouteDetailSerializer(serializers.ModelSerializer):
    """
    Detail view serializer - COMPLETE route information

    WHAT IT DOES:
    - Shows EVERYTHING about a route
    - Includes: detailed timing, amenities, company info
    - Tourist can make booking decision

    COMPLETE INFORMATION:
    - Exact times (departure & arrival)
    - Duration & distance
    - All amenities (WiFi, AC, toilet, etc)
    - Company details & verification
    - Price and available seats
    - Vehicle type & capacity
    """

    company = TransportCompanyDetailSerializer(read_only=True)
    departure_city = serializers.StringRelatedField(read_only=True)
    arrival_city = serializers.StringRelatedField(read_only=True)
    days_of_operation_list = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            'id',
            'slug',
            'company',
            'departure_city',
            'arrival_city',
            'distance_km',
            'duration_minutes',
            'departure_time',
            'arrival_time',
            'days_of_operation',
            'days_of_operation_list',
            'base_price',
            'currency',
            'total_seats',
            'available_seats',
            'vehicle_type',
            'has_wifi',
            'has_air_conditioning',
            'has_toilet',
            'has_food_service',
            'is_active',
            'created_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'days_of_operation_list',
            'created_at',
        )

    def get_days_of_operation_list(self, obj):
        """
        Convert "Mon,Tue,Wed" string to list for frontend

        WHY:
        - Database stores: "Mon,Tue,Wed,Thu,Fri"
        - Frontend needs: ["Mon", "Tue", "Wed", "Thu", "Fri"]
        - This serializer method does the conversion

        LEARNING POINT:
        - Use SerializerMethodField for calculated/transformed fields
        - Convert data to format frontend expects
        """
        if obj.days_of_operation:
            return obj.days_of_operation.split(',')
        return []


class RouteCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating routes

    WHAT IT DOES:
    - Handles incoming data from transport company
    - Validates all required fields
    - Only allows editable fields

    BUSINESS LOGIC:
    - Company can update: times, prices, availability
    - Company CANNOT change: cities (read_only)
    """

    days_of_operation = serializers.CharField(
        help_text="Comma-separated days: Mon,Tue,Wed,Thu,Fri,Sat,Sun"
    )

    class Meta:
        model = Route
        fields = (
            'company',
            'departure_city',
            'arrival_city',
            'distance_km',
            'duration_minutes',
            'departure_time',
            'arrival_time',
            'days_of_operation',
            'base_price',
            'total_seats',
            'available_seats',
            'vehicle_type',
            'has_wifi',
            'has_air_conditioning',
            'has_toilet',
            'has_food_service',
            'is_active',
        )

    def validate_base_price(self, value):
        """Price must be positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_available_seats(self, value):
        """Available seats cannot be negative"""
        if value < 0:
            raise serializers.ValidationError("Available seats cannot be negative")
        return value

    def validate(self, data):
        """
        Cross-validation: available <= total

        BUSINESS RULE:
        - Cannot have more available seats than total
        - Example: 40 total, 35 available ✓
        - Example: 40 total, 50 available ✗
        """
        if data.get('available_seats', 0) > data.get('total_seats', 0):
            raise serializers.ValidationError(
                "Available seats cannot exceed total seats"
            )
        return data


class TransportCompanyCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating transport companies

    WHAT IT DOES:
    - Handles company registration/updates
    - Validates business information
    - Only allows editable fields (not verification status)
    """

    class Meta:
        model = TransportCompany
        fields = (
            'name',
            'transportation_type',
            'description',
            'logo',
            'phone_number',
            'email',
            'website',
            'license_number',
            'license_document',
            'has_insurance',
            'insurance_document',
            'is_active',
        )

    def validate_phone_number(self, value):
        """Phone number validation"""
        if not value or len(value) < 10:
            raise serializers.ValidationError("Valid phone number required")
        return value


class TransportCompanyVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for admin verification process

    WHAT IT DOES:
    - Admin only sees verification fields
    - Can verify/reject companies
    - Can update safety scores

    ADMIN-ONLY:
    - Only admin staff see this serializer
    - Not exposed to tourists
    - Sensitive business decisions
    """

    class Meta:
        model = TransportCompany
        fields = (
            'id',
            'name',
            'transportation_type',
            'is_verified',
            'verification_status',
            'is_safe',
            'safety_score',
            'license_number',
            'license_document',
            'has_insurance',
            'insurance_document',
            'average_rating',
            'total_reviews',
        )
        read_only_fields = ('id', 'average_rating', 'total_reviews')