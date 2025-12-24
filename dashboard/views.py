# dashboard/views.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from django.utils import timezone
import json

logger = logging.getLogger(__name__)


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
    except Exception as e:
        logger.warning(f"Error loading booking stats for user {user.id}: {e}")

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
    except Exception as e:
        logger.warning(f"Error loading tour booking stats for user {user.id}: {e}")

    # Get review statistics
    try:
        from reviews.models import Review
        context['reviews_count'] = Review.objects.filter(user=user).count()
    except Exception as e:
        logger.warning(f"Error loading review stats for user {user.id}: {e}")

    # Get user profile
    try:
        from accounts.models import UserProfile
        context['profile'] = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        context['profile'] = None
    except Exception as e:
        logger.warning(f"Error loading profile for user {user.id}: {e}")
        context['profile'] = None

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def my_bookings(request):
    """User bookings view with filtering"""
    bookings = []
    tour_bookings = []
    status_filter = request.GET.get('status', '')

    # Get generic bookings with related data
    try:
        from bookings.models import Booking
        qs = Booking.objects.filter(user=request.user).select_related('user')
        if status_filter:
            qs = qs.filter(status=status_filter)
        bookings = qs.order_by('-created_at')
    except Exception as e:
        logger.warning(f"Error loading bookings for user {request.user.id}: {e}")

    # Get tour bookings
    try:
        from tours.models import TourBooking
        qs = TourBooking.objects.filter(user=request.user)
        if status_filter:
            qs = qs.filter(status=status_filter)
        tour_bookings = qs.select_related('tour').order_by('-booking_date')
    except Exception as e:
        logger.warning(f"Error loading tour bookings for user {request.user.id}: {e}")

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
    except Exception as e:
        logger.warning(f"Error loading reviews for user {request.user.id}: {e}")

    return render(request, 'dashboard/reviews.html', {'reviews': reviews})


@login_required
def settings_view(request):
    """User settings and profile view"""
    user = request.user
    profile = None

    try:
        from accounts.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
    except Exception as e:
        logger.warning(f"Error loading profile for settings view, user {user.id}: {e}")

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
            except Exception as e:
                logger.error(f"Failed to send cancellation email for tour booking {booking_id}: {e}")
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
            except Exception as e:
                logger.error(f"Failed to send cancellation email for booking {booking_id}: {e}")
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

    from django.core.exceptions import ObjectDoesNotExist
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
    except ObjectDoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('dashboard:bookings')
    except Exception as e:
        logger.error(f"Error loading booking {booking_id}: {e}")
        messages.error(request, 'Error loading booking details.')
        return redirect('dashboard:bookings')

    return render(request, 'dashboard/booking_detail.html', {
        'booking': booking,
        'booking_type': booking_type
    })


@staff_member_required
def revenue_dashboard(request):
    """Admin revenue dashboard with affiliate analytics"""
    from core.models import AffiliateClick
    from accommodations.models import Accommodation
    from tours.models import Tour

    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_start = today.replace(month=1, day=1)

    # Get date filter from request
    period = request.GET.get('period', 'week')
    if period == 'today':
        start_date = today
    elif period == 'week':
        start_date = week_ago
    elif period == 'month':
        start_date = month_ago
    elif period == 'year':
        start_date = year_start
    else:
        start_date = week_ago

    # Click statistics
    clicks = AffiliateClick.objects.filter(clicked_at__date__gte=start_date)

    total_clicks = clicks.count()
    total_estimated_revenue = clicks.aggregate(total=Sum('estimated_commission'))['total'] or 0
    converted_clicks = clicks.filter(converted=True).count()
    conversion_rate = (converted_clicks / total_clicks * 100) if total_clicks > 0 else 0

    # Platform breakdown
    platform_stats = clicks.values('platform').annotate(
        count=Count('id'),
        revenue=Sum('estimated_commission')
    ).order_by('-count')

    # Item type breakdown
    type_stats = clicks.values('item_type').annotate(
        count=Count('id'),
        revenue=Sum('estimated_commission')
    ).order_by('-count')

    # Device breakdown
    device_stats = clicks.values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # Daily trend data for chart - single query with date grouping
    from django.db.models.functions import TruncDate
    daily_stats = clicks.annotate(
        date=TruncDate('clicked_at')
    ).values('date').annotate(
        clicks=Count('id'),
        revenue=Sum('estimated_commission')
    ).order_by('date')

    # Convert to list format for chart
    daily_clicks = [
        {
            'date': stat['date'].strftime('%Y-%m-%d') if stat['date'] else '',
            'clicks': stat['clicks'],
            'revenue': float(stat['revenue'] or 0)
        }
        for stat in daily_stats
    ]

    # Top performing items - aggregate click counts
    top_hotels_stats = clicks.filter(item_type='accommodation').values(
        'object_id'
    ).annotate(
        click_count=Count('id')
    ).order_by('-click_count')[:5]

    top_tours_stats = clicks.filter(item_type='tour').values(
        'object_id'
    ).annotate(
        click_count=Count('id')
    ).order_by('-click_count')[:5]

    # Batch fetch all hotels and tours in single queries (fixes N+1)
    hotel_ids = [item['object_id'] for item in top_hotels_stats]
    tour_ids = [item['object_id'] for item in top_tours_stats]

    hotels_map = {
        h.id: h for h in Accommodation.objects.filter(id__in=hotel_ids).only('id', 'name', 'city')
    }
    tours_map = {
        t.id: t for t in Tour.objects.filter(id__in=tour_ids).only('id', 'name', 'tour_type')
    }

    # Build result lists
    top_hotels_list = []
    for item in top_hotels_stats:
        hotel = hotels_map.get(item['object_id'])
        if hotel:
            top_hotels_list.append({
                'name': hotel.name,
                'clicks': item['click_count'],
                'city': hotel.city
            })

    top_tours_list = []
    for item in top_tours_stats:
        tour = tours_map.get(item['object_id'])
        if tour:
            top_tours_list.append({
                'name': tour.name,
                'clicks': item['click_count'],
                'type': tour.get_tour_type_display()
            })

    # Inventory stats
    total_hotels = Accommodation.objects.filter(is_active=True).count()
    total_tours = Tour.objects.filter(is_active=True).count()
    hotels_with_affiliates = Accommodation.objects.filter(
        is_active=True
    ).exclude(booking_com_url='').exclude(booking_com_url__isnull=True).count()
    tours_with_affiliates = Tour.objects.filter(
        is_active=True
    ).exclude(viator_url='').exclude(viator_url__isnull=True).count()

    context = {
        'period': period,
        'start_date': start_date,
        'total_clicks': total_clicks,
        'total_estimated_revenue': total_estimated_revenue,
        'converted_clicks': converted_clicks,
        'conversion_rate': conversion_rate,
        'platform_stats': platform_stats,
        'type_stats': type_stats,
        'device_stats': device_stats,
        'daily_clicks': json.dumps(daily_clicks),
        'top_hotels': top_hotels_list,
        'top_tours': top_tours_list,
        'total_hotels': total_hotels,
        'total_tours': total_tours,
        'hotels_with_affiliates': hotels_with_affiliates,
        'tours_with_affiliates': tours_with_affiliates,
    }

    return render(request, 'dashboard/revenue.html', context)
