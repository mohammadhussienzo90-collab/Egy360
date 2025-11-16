# bookings/serializers.py
"""
Bookings App Serializers

Comprehensive serializers for booking management including:
- Booking creation and updates
- Booking history tracking
- Payment processing
- Availability checking
- Status management
"""

from rest_framework import serializers
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction

from .models import Booking, BookingHistory
from accommodations.models import Accommodation, Room
from tours.models import Tour, TourSchedule
from accounts.models import CustomUser


# ==============================================================================
# BOOKING SERIALIZERS
# ==============================================================================

class BookingListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing bookings.

    Includes minimal information for efficient list views.
    Used in booking lists and admin panels.
    """

    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # Content object details
    content_object_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'booking_number',
            'user',
            'user_full_name',
            'booking_type',
            'booking_type_display',
            'status',
            'status_display',
            'content_object_name',
            'check_in_date',
            'number_of_nights',
            'number_of_guests',
            'total_amount',
            'currency',
            'created_at',
        ]
        read_only_fields = ['booking_number', 'created_at']

    def get_content_object_name(self, obj):
        """Get the name of the booked content object"""
        if obj.content_object:
            if hasattr(obj.content_object, 'name'):
                return obj.content_object.name
            elif hasattr(obj.content_object, 'title'):
                return obj.content_object.title
        return None


class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for booking retrieval and display.

    Includes all booking information, user details, and content object data.
    Used for booking detail views and confirmation pages.
    """

    user_details = serializers.SerializerMethodField()
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    # Content object details
    accommodation_details = serializers.SerializerMethodField()
    room_details = serializers.SerializerMethodField()
    tour_details = serializers.SerializerMethodField()
    tour_schedule_details = serializers.SerializerMethodField()

    # Computed fields
    nights_remaining = serializers.SerializerMethodField()
    is_cancellable = serializers.SerializerMethodField()
    is_modifiable = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'booking_number',
            'user',
            'user_details',
            'booking_type',
            'booking_type_display',
            'status',
            'status_display',
            'payment_status',
            'payment_status_display',
            'accommodation',
            'accommodation_details',
            'room',
            'room_details',
            'tour',
            'tour_details',
            'tour_schedule',
            'tour_schedule_details',
            'check_in_date',
            'check_out_date',
            'number_of_nights',
            'number_of_rooms',
            'number_of_guests',
            'guest_details',
            'special_requests',
            'subtotal',
            'tax_amount',
            'service_fee',
            'discount_amount',
            'total_amount',
            'currency',
            'contact_name',
            'contact_email',
            'contact_phone',
            'cancellation_reason',
            'cancellation_date',
            'refund_amount',
            'nights_remaining',
            'is_cancellable',
            'is_modifiable',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'booking_number',
            'check_out_date',
            'subtotal',
            'tax_amount',
            'service_fee',
            'total_amount',
            'created_at',
            'updated_at',
        ]

    def get_user_details(self, obj):
        """Get user information"""
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
            'phone_number': user.phone_number,
        }

    def get_accommodation_details(self, obj):
        """Get accommodation details if booking is for accommodation"""
        if obj.booking_type == 'accommodation' and obj.accommodation:
            acc = obj.accommodation
            return {
                'id': acc.id,
                'name': acc.name,
                'address': acc.address,
                'city': acc.city.name if acc.city else None,
                'star_rating': acc.star_rating,
                'phone_number': acc.phone_number,
            }
        return None

    def get_room_details(self, obj):
        """Get room details if booking includes a room"""
        if obj.room:
            room = obj.room
            return {
                'id': room.id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'capacity': room.capacity,
                'price_per_night': str(room.price_per_night),
            }
        return None

    def get_tour_details(self, obj):
        """Get tour details if booking is for a tour"""
        if obj.booking_type == 'tour' and obj.tour:
            tour = obj.tour
            return {
                'id': tour.id,
                'title': tour.title,
                'description': tour.short_description or tour.description[:200],
                'duration': f"{tour.duration_value} {tour.duration_unit}",
                'difficulty_level': tour.difficulty_level,
                'operator': tour.operator.name if tour.operator else None,
            }
        return None

    def get_tour_schedule_details(self, obj):
        """Get tour schedule details if applicable"""
        if obj.tour_schedule:
            schedule = obj.tour_schedule
            return {
                'id': schedule.id,
                'date': schedule.date,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'available_spots': schedule.available_spots,
            }
        return None

    def get_nights_remaining(self, obj):
        """Calculate nights remaining until check-in"""
        if obj.check_in_date and obj.status in ['pending', 'confirmed']:
            today = timezone.now().date()
            if obj.check_in_date > today:
                return (obj.check_in_date - today).days
        return None

    def get_is_cancellable(self, obj):
        """Check if booking can be cancelled"""
        if obj.status in ['cancelled', 'completed', 'refunded']:
            return False

        if obj.check_in_date:
            # Allow cancellation up to 24 hours before check-in
            cutoff = timezone.now() + timedelta(hours=24)
            return timezone.make_aware(
                datetime.combine(obj.check_in_date, datetime.min.time())
            ) > cutoff

        return obj.status in ['pending', 'confirmed']

    def get_is_modifiable(self, obj):
        """Check if booking can be modified"""
        if obj.status not in ['pending', 'confirmed']:
            return False

        if obj.check_in_date:
            # Allow modification up to 48 hours before check-in
            cutoff = timezone.now() + timedelta(hours=48)
            return timezone.make_aware(
                datetime.combine(obj.check_in_date, datetime.min.time())
            ) > cutoff

        return True


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new bookings.

    Handles validation, availability checking, and price calculation.
    Supports both accommodation and tour bookings.
    """

    # Make user optional (will be set from request.user)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False
    )

    # Type-specific fields
    accommodation_id = serializers.IntegerField(required=False, write_only=True)
    room_id = serializers.IntegerField(required=False, write_only=True)
    tour_id = serializers.IntegerField(required=False, write_only=True)
    tour_schedule_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Booking
        fields = [
            'user',
            'booking_type',
            'accommodation_id',
            'room_id',
            'tour_id',
            'tour_schedule_id',
            'check_in_date',
            'number_of_nights',
            'number_of_rooms',
            'number_of_guests',
            'guest_details',
            'special_requests',
            'contact_name',
            'contact_email',
            'contact_phone',
            'discount_amount',
        ]

    def validate(self, data):
        """Comprehensive validation for booking creation"""
        booking_type = data.get('booking_type')

        # Validate based on booking type
        if booking_type == 'accommodation':
            self._validate_accommodation_booking(data)
        elif booking_type == 'tour':
            self._validate_tour_booking(data)
        else:
            raise serializers.ValidationError({
                'booking_type': 'Invalid booking type'
            })

        return data

    def _validate_accommodation_booking(self, data):
        """Validate accommodation booking data"""
        # Check required fields
        if 'accommodation_id' not in data:
            raise serializers.ValidationError({
                'accommodation_id': 'Accommodation is required for accommodation bookings'
            })

        if 'check_in_date' not in data:
            raise serializers.ValidationError({
                'check_in_date': 'Check-in date is required'
            })

        if 'number_of_nights' not in data or data['number_of_nights'] < 1:
            raise serializers.ValidationError({
                'number_of_nights': 'Number of nights must be at least 1'
            })

        # Validate check-in date is in the future
        if data['check_in_date'] <= timezone.now().date():
            raise serializers.ValidationError({
                'check_in_date': 'Check-in date must be in the future'
            })

        # Verify accommodation exists
        try:
            accommodation = Accommodation.objects.get(id=data['accommodation_id'])
            data['accommodation'] = accommodation
        except Accommodation.DoesNotExist:
            raise serializers.ValidationError({
                'accommodation_id': 'Accommodation not found'
            })

        # Verify room if specified
        if 'room_id' in data:
            try:
                room = Room.objects.get(
                    id=data['room_id'],
                    accommodation=accommodation
                )
                data['room'] = room

                # Check room capacity
                if data.get('number_of_guests', 1) > room.capacity:
                    raise serializers.ValidationError({
                        'number_of_guests': f'Room capacity is {room.capacity} guests'
                    })
            except Room.DoesNotExist:
                raise serializers.ValidationError({
                    'room_id': 'Room not found or does not belong to this accommodation'
                })

    def _validate_tour_booking(self, data):
        """Validate tour booking data"""
        # Check required fields
        if 'tour_id' not in data:
            raise serializers.ValidationError({
                'tour_id': 'Tour is required for tour bookings'
            })

        # Verify tour exists
        try:
            tour = Tour.objects.get(id=data['tour_id'])
            data['tour'] = tour
        except Tour.DoesNotExist:
            raise serializers.ValidationError({
                'tour_id': 'Tour not found'
            })

        # Verify tour schedule if specified
        if 'tour_schedule_id' in data:
            try:
                schedule = TourSchedule.objects.get(
                    id=data['tour_schedule_id'],
                    tour=tour
                )

                # Check availability
                if not schedule.is_available or schedule.available_spots < data.get('number_of_guests', 1):
                    raise serializers.ValidationError({
                        'tour_schedule_id': 'This tour schedule is not available or fully booked'
                    })

                data['tour_schedule'] = schedule
                data['check_in_date'] = schedule.date
            except TourSchedule.DoesNotExist:
                raise serializers.ValidationError({
                    'tour_schedule_id': 'Tour schedule not found'
                })

        # Validate group size
        num_guests = data.get('number_of_guests', 1)
        if num_guests < tour.min_group_size:
            raise serializers.ValidationError({
                'number_of_guests': f'Minimum group size is {tour.min_group_size}'
            })
        if num_guests > tour.max_group_size:
            raise serializers.ValidationError({
                'number_of_guests': f'Maximum group size is {tour.max_group_size}'
            })

    @transaction.atomic
    def create(self, validated_data):
        """Create booking with automatic calculations"""
        # Remove write-only fields
        validated_data.pop('accommodation_id', None)
        validated_data.pop('room_id', None)
        validated_data.pop('tour_id', None)
        validated_data.pop('tour_schedule_id', None)

        # Set user from context if not provided
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user

        # Calculate check-out date for accommodations
        if validated_data.get('booking_type') == 'accommodation':
            check_in = validated_data['check_in_date']
            nights = validated_data.get('number_of_nights', 1)
            validated_data['check_out_date'] = check_in + timedelta(days=nights)

        # Create booking
        booking = Booking.objects.create(**validated_data)

        # Calculate amounts
        booking.calculate_amounts()
        booking.save()

        return booking


class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing bookings.

    Allows modification of guest details, special requests, and contact info.
    Prevents modification of critical fields after confirmation.
    """

    class Meta:
        model = Booking
        fields = [
            'number_of_guests',
            'guest_details',
            'special_requests',
            'contact_name',
            'contact_email',
            'contact_phone',
        ]

    def validate(self, data):
        """Validate booking can be updated"""
        booking = self.instance

        if booking.status not in ['pending', 'confirmed']:
            raise serializers.ValidationError(
                'Cannot update booking with status: {}'.format(booking.status)
            )

        # Check if modification deadline has passed
        if booking.check_in_date:
            cutoff = timezone.now() + timedelta(hours=48)
            check_in_datetime = timezone.make_aware(
                datetime.combine(booking.check_in_date, datetime.min.time())
            )
            if check_in_datetime <= cutoff:
                raise serializers.ValidationError(
                    'Cannot modify booking within 48 hours of check-in'
                )

        return data


class BookingCancellationSerializer(serializers.Serializer):
    """
    Serializer for booking cancellation.

    Handles cancellation validation and refund calculation.
    """

    cancellation_reason = serializers.CharField(
        max_length=500,
        required=True,
        help_text="Reason for cancellation"
    )

    def validate(self, data):
        """Validate cancellation is allowed"""
        booking = self.context.get('booking')

        if not booking:
            raise serializers.ValidationError('Booking not found')

        if booking.status in ['cancelled', 'refunded']:
            raise serializers.ValidationError('Booking is already cancelled')

        if booking.status == 'completed':
            raise serializers.ValidationError('Cannot cancel completed booking')

        # Check cancellation deadline
        if booking.check_in_date:
            cutoff = timezone.now() + timedelta(hours=24)
            check_in_datetime = timezone.make_aware(
                datetime.combine(booking.check_in_date, datetime.min.time())
            )
            if check_in_datetime <= cutoff:
                raise serializers.ValidationError(
                    'Cannot cancel booking within 24 hours of check-in'
                )

        return data


class BookingConfirmationSerializer(serializers.Serializer):
    """
    Serializer for booking confirmation.

    Used by providers to confirm pending bookings.
    """

    confirmation_notes = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="Optional notes from provider"
    )

    def validate(self, data):
        """Validate confirmation is allowed"""
        booking = self.context.get('booking')

        if not booking:
            raise serializers.ValidationError('Booking not found')

        if booking.status != 'pending':
            raise serializers.ValidationError(
                f'Can only confirm pending bookings. Current status: {booking.status}'
            )

        return data


class BookingPaymentSerializer(serializers.Serializer):
    """
    Serializer for processing booking payments.

    Used for initiating payment transactions for confirmed bookings.
    """

    booking_id = serializers.IntegerField(required=True)
    payment_method_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    currency = serializers.CharField(
        max_length=3,
        default='EGP'
    )
    payment_details = serializers.JSONField(required=False)
    notes = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    def validate_booking_id(self, value):
        """Validate booking exists and is confirmed"""
        try:
            booking = Booking.objects.get(id=value)
            if booking.status != 'confirmed':
                raise serializers.ValidationError(
                    'Can only process payment for confirmed bookings'
                )
            return value
        except Booking.DoesNotExist:
            raise serializers.ValidationError('Booking not found')

    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError(
                'Payment amount must be greater than 0'
            )
        return value

    def validate(self, data):
        """Cross-field validation"""
        booking = Booking.objects.get(id=data['booking_id'])

        # Verify amount matches booking total
        if data['amount'] != booking.total_amount:
            raise serializers.ValidationError({
                'amount': f'Amount must match booking total: {booking.total_amount}'
            })

        return data


# ==============================================================================
# BOOKING HISTORY SERIALIZERS
# ==============================================================================

class BookingHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for booking history entries.

    Tracks all changes and status transitions for bookings.
    """

    changed_by_name = serializers.CharField(
        source='changed_by.get_full_name',
        read_only=True
    )
    status_from_display = serializers.SerializerMethodField()
    status_to_display = serializers.SerializerMethodField()

    class Meta:
        model = BookingHistory
        fields = [
            'id',
            'booking',
            'status_from',
            'status_from_display',
            'status_to',
            'status_to_display',
            'changed_by',
            'changed_by_name',
            'reason',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def get_status_from_display(self, obj):
        """Get display name for status_from"""
        return dict(Booking.STATUS_CHOICES).get(obj.status_from, obj.status_from)

    def get_status_to_display(self, obj):
        """Get display name for status_to"""
        return dict(Booking.STATUS_CHOICES).get(obj.status_to, obj.status_to)


class BookingHistoryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for booking history lists.
    """

    changed_by_name = serializers.CharField(
        source='changed_by.get_full_name',
        read_only=True
    )
    status_from_display = serializers.SerializerMethodField()
    status_to_display = serializers.SerializerMethodField()

    class Meta:
        model = BookingHistory
        fields = [
            'id',
            'status_from',
            'status_from_display',
            'status_to',
            'status_to_display',
            'changed_by_name',
            'reason',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def get_status_from_display(self, obj):
        """Get display name for status_from"""
        return dict(Booking.STATUS_CHOICES).get(obj.status_from, obj.status_from)

    def get_status_to_display(self, obj):
        """Get display name for status_to"""
        return dict(Booking.STATUS_CHOICES).get(obj.status_to, obj.status_to)


# ==============================================================================
# STATISTICS AND REPORTING SERIALIZERS
# ==============================================================================

class BookingStatisticsSerializer(serializers.Serializer):
    """
    Serializer for booking statistics.

    Provides aggregated data for dashboards and reports.
    """

    total_bookings = serializers.IntegerField()
    pending_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    cancelled_bookings = serializers.IntegerField()
    completed_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_booking_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    cancellation_rate = serializers.FloatField()