"""
Egy360 Core App Views - UPDATED WITH BOOKING FLOW
Includes all page views for the tourism platform
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# ==================== HOME ====================
@require_http_methods(["GET"])
def home(request):
    """
    Homepage view with hero section, search, and featured content
    """
    return render(request, 'home.html')


# ==================== ACCOMMODATIONS ====================
@require_http_methods(["GET"])
def accommodation_search(request):
    """
    Accommodation search page with filters and results
    """
    # Get search parameters from URL
    city = request.GET.get('city', '')
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    guests = request.GET.get('guests', '2')

    context = {
        'city': city,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
    }

    return render(request, 'accommodation_search.html', context)


@require_http_methods(["GET"])
def accommodation_detail(request, accommodation_id):
    """
    Individual accommodation detail page
    """
    context = {
        'accommodation_id': accommodation_id,
    }

    return render(request, 'accommodation_detail.html', context)


# ==================== TOURS ====================
@require_http_methods(["GET"])
def tour_listing(request):
    """
    Tour listing page with filters
    """
    # Get search parameters from URL
    city = request.GET.get('city', '')
    date = request.GET.get('date', '')
    category = request.GET.get('category', '')
    travelers = request.GET.get('travelers', '2')

    context = {
        'city': city,
        'date': date,
        'category': category,
        'travelers': travelers,
    }

    return render(request, 'tour_listing.html', context)


@require_http_methods(["GET"])
def tour_detail(request, tour_id):
    """
    Individual tour detail page
    """
    context = {
        'tour_id': tour_id,
    }

    return render(request, 'tour_detail.html', context)


# ==================== USER DASHBOARD ====================
@require_http_methods(["GET"])
def user_dashboard(request):
    """
    User dashboard with bookings, favorites, and profile
    """
    return render(request, 'user_dashboard.html')


# ==================== BOOKING FLOW ====================
@require_http_methods(["GET"])
def booking_checkout(request):
    """
    Booking checkout page for accommodations and tours
    Handles both accommodation and tour bookings

    URL Parameters:
    - type: 'accommodation' or 'tour'
    - id: property/tour ID
    - Optional: pre-filled dates, guests, etc.
    """
    # Get booking parameters
    booking_type = request.GET.get('type', 'accommodation')
    item_id = request.GET.get('id', '1')

    # Pre-fill data if coming from detail page
    city = request.GET.get('city', '')
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    tour_date = request.GET.get('tour_date', '')
    guests = request.GET.get('guests', '2')
    room_type = request.GET.get('room_type', 'standard')

    context = {
        'booking_type': booking_type,
        'item_id': item_id,
        'city': city,
        'check_in': check_in,
        'check_out': check_out,
        'tour_date': tour_date,
        'guests': guests,
        'room_type': room_type,
    }

    return render(request, 'booking_checkout.html', context)


@require_http_methods(["GET"])
def booking_confirmation(request):
    """
    Booking confirmation page
    Shows booking details and confirmation message

    URL Parameters:
    - id: booking reference ID
    """
    booking_id = request.GET.get('id', 'BK00000000')

    context = {
        'booking_id': booking_id,
    }

    return render(request, 'booking_confirmation.html', context)