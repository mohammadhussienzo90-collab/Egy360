# bookings/permissions.py
"""
Custom Permissions for Bookings App

Defines role-based permissions for booking operations.
"""

from rest_framework import permissions


class IsBookingOwnerOrProvider(permissions.BasePermission):
    """
    Permission to allow booking owner or related provider to access/modify booking.

    - Booking owner can always access their booking
    - Provider who owns the accommodation/tour can access booking
    - Staff can access all bookings
    """

    def has_object_permission(self, request, view, obj):
        # Staff can access everything
        if request.user.is_staff:
            return True

        # Owner can access their own booking
        if obj.user == request.user:
            return True

        # Provider can access bookings for their properties/tours
        if request.user.user_type == 'provider':
            if obj.accommodation and hasattr(obj.accommodation, 'owner'):
                if obj.accommodation.owner == request.user:
                    return True
            if obj.tour and hasattr(obj.tour, 'operator'):
                if hasattr(obj.tour.operator, 'owner') and obj.tour.operator.owner == request.user:
                    return True

        return False


class IsProvider(permissions.BasePermission):
    """
    Permission to allow only providers to access certain actions.

    Used for provider-specific actions like confirming bookings.
    """

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                (request.user.user_type == 'provider' or request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True

        # Provider must own the accommodation/tour
        if request.user.user_type == 'provider':
            if obj.accommodation and hasattr(obj.accommodation, 'owner'):
                if obj.accommodation.owner == request.user:
                    return True
            if obj.tour and hasattr(obj.tour, 'operator'):
                if hasattr(obj.tour.operator, 'owner') and obj.tour.operator.owner == request.user:
                    return True

        return False


class IsBookingOwner(permissions.BasePermission):
    """
    Permission to allow only the booking owner to access.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff