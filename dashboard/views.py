# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    """Main dashboard view"""
    user = request.user

    # Get user statistics
    context = {
        'user': user,
        'total_bookings': 0,  # Will be updated when bookings model is ready
        'upcoming_tours': 0,
        'reviews_count': 0,
        'saved_items': 0,
        'recent_bookings': [],
    }

    # Try to get actual data if models exist
    try:
        from bookings.models import Booking
        context['total_bookings'] = Booking.objects.filter(user=user).count()
        context['recent_bookings'] = Booking.objects.filter(user=user).order_by('-created_at')[:5]
    except:
        pass

    try:
        from tours.models import TourBooking
        upcoming = TourBooking.objects.filter(
            user=user,
            tour_date__gte=datetime.now().date(),
            status='confirmed'
        ).count()
        context['upcoming_tours'] = upcoming
    except:
        pass

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def my_bookings(request):
    """User bookings view"""
    bookings = []

    try:
        from bookings.models import Booking
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    except:
        pass

    return render(request, 'dashboard/bookings.html', {'bookings': bookings})

@login_required
def my_reviews(request):
    """User reviews view"""
    reviews = []

    try:
        from reviews.models import Review
        reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    except:
        pass

    return render(request, 'dashboard/reviews.html', {'reviews': reviews})

@login_required
def settings_view(request):
    """User settings view"""
    return render(request, 'dashboard/settings.html', {'user': request.user})