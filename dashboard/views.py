# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
import json


@login_required
def dashboard_view(request):
    """Main dashboard view with user statistics"""
    user = request.user

    # Initialize context with defaults
    context = {
        'user': user,
        'total_bookings': 0,
        'upcoming_tours': 0,
        'completed_tours': 0,
        'reviews_count': 0,
        'saved_items': 0,
        'recent_bookings': [],
        'upcoming_tour_bookings': [],
        'total_spent': 0,
    }

    # Get booking statistics
    try:
        from bookings.models import Booking
        user_bookings = Booking.objects.filter(user=user)
        context['total_bookings'] = user_bookings.count()
        context['recent_bookings'] = user_bookings.order_by('-created_at')[:5]

        # Calculate total spent
        total = user_bookings.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total']
        context['total_spent'] = total or 0
    except Exception:
        pass

    # Get tour booking statistics
    try:
        from tours.models import TourBooking
        tour_bookings = TourBooking.objects.filter(user=user)
        today = datetime.now().date()

        # Upcoming tours
        upcoming = tour_bookings.filter(
            tour_date__gte=today,
            status__in=['pending', 'confirmed']
        )
        context['upcoming_tours'] = upcoming.count()
        context['upcoming_tour_bookings'] = upcoming.select_related('tour').order_by('tour_date')[:3]

        # Completed tours
        context['completed_tours'] = tour_bookings.filter(status='completed').count()
    except Exception:
        pass

    # Get review statistics
    try:
        from reviews.models import Review
        context['reviews_count'] = Review.objects.filter(user=user).count()
    except Exception:
        pass

    # Get user profile
    try:
        from accounts.models import UserProfile
        context['profile'] = UserProfile.objects.get(user=user)
    except Exception:
        context['profile'] = None

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def my_bookings(request):
    """User bookings view with filtering"""
    bookings = []
    tour_bookings = []
    status_filter = request.GET.get('status', '')

    # Get generic bookings
    try:
        from bookings.models import Booking
        qs = Booking.objects.filter(user=request.user)
        if status_filter:
            qs = qs.filter(status=status_filter)
        bookings = qs.order_by('-created_at')
    except Exception:
        pass

    # Get tour bookings
    try:
        from tours.models import TourBooking
        qs = TourBooking.objects.filter(user=request.user)
        if status_filter:
            qs = qs.filter(status=status_filter)
        tour_bookings = qs.select_related('tour').order_by('-booking_date')
    except Exception:
        pass

    context = {
        'bookings': bookings,
        'tour_bookings': tour_bookings,
        'status_filter': status_filter,
        'status_choices': [
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ]
    }
    return render(request, 'dashboard/bookings.html', context)


@login_required
def my_reviews(request):
    """User reviews view"""
    reviews = []

    try:
        from reviews.models import Review
        reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    except Exception:
        pass

    return render(request, 'dashboard/reviews.html', {'reviews': reviews})


@login_required
def settings_view(request):
    """User settings and profile view"""
    user = request.user
    profile = None

    try:
        from accounts.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
    except Exception:
        pass

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            # Update user info
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()

            # Update profile if exists
            if profile:
                profile.phone = request.POST.get('phone', profile.phone)
                profile.bio = request.POST.get('bio', profile.bio)
                profile.nationality = request.POST.get('nationality', profile.nationality)
                profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard:settings')

        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
            return redirect('dashboard:settings')

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'dashboard/settings.html', context)


@login_required
@require_http_methods(["POST"])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    try:
        # Try tour booking first
        from tours.models import TourBooking
        booking = TourBooking.objects.filter(
            id=booking_id,
            user=request.user,
            status__in=['pending', 'confirmed']
        ).first()

        if booking:
            booking.status = 'cancelled'
            booking.save()
            # Send cancellation email
            try:
                from core.email import send_booking_status_update
                send_booking_status_update(booking, booking_type='tour')
            except Exception:
                pass
            return JsonResponse({
                'success': True,
                'message': 'Booking cancelled successfully.'
            })

        # Try generic booking
        from bookings.models import Booking
        booking = Booking.objects.filter(
            id=booking_id,
            user=request.user,
            status__in=['pending', 'confirmed']
        ).first()

        if booking:
            booking.status = 'cancelled'
            booking.save()
            # Send cancellation email
            try:
                from core.email import send_booking_status_update
                send_booking_status_update(booking, booking_type='accommodation')
            except Exception:
                pass
            return JsonResponse({
                'success': True,
                'message': 'Booking cancelled successfully.'
            })

        return JsonResponse({
            'success': False,
            'error': 'Booking not found or cannot be cancelled.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while cancelling the booking.'
        }, status=500)


@login_required
def booking_detail(request, booking_id):
    """View details of a specific booking"""
    booking = None
    booking_type = request.GET.get('type', 'tour')

    try:
        if booking_type == 'tour':
            from tours.models import TourBooking
            booking = TourBooking.objects.select_related('tour').get(
                id=booking_id,
                user=request.user
            )
        else:
            from bookings.models import Booking
            booking = Booking.objects.get(id=booking_id, user=request.user)
    except Exception:
        messages.error(request, 'Booking not found.')
        return redirect('dashboard:bookings')

    return render(request, 'dashboard/booking_detail.html', {
        'booking': booking,
        'booking_type': booking_type
    })
