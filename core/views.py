"""
Egy360 Core App Views - UPDATED WITH BOOKING FLOW
Includes all page views for the tourism platform
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
import json


# ==================== AFFILIATE TRACKING ====================
@require_http_methods(["POST"])
def track_affiliate_click(request):
    """
    API endpoint to track affiliate link clicks
    Called via JavaScript when user clicks an affiliate link
    """
    from .models import AffiliateClick

    try:
        data = json.loads(request.body)

        # Get content type for the item
        item_type = data.get('item_type', 'accommodation')
        item_id = data.get('item_id')
        platform = data.get('platform', 'other')
        affiliate_url = data.get('url', '')

        # Map item type to model
        model_map = {
            'accommodation': ('accommodations', 'accommodation'),
            'tour': ('tours', 'tour'),
            'transportation': ('transportation', 'transportationservice'),
        }

        app_label, model_name = model_map.get(item_type, ('accommodations', 'accommodation'))

        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            content_type = None

        # Get user info
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        # Get IP and user agent
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

        # Detect device type
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            device_type = 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        # Estimate commission based on platform
        commission_rates = {
            'booking_com': 4.0,
            'hotellook': 2.5,
            'viator': 8.0,
            'getyourguide': 8.0,
            'agoda': 5.0,
        }
        avg_booking_values = {
            'accommodation': 100,
            'tour': 80,
            'flight': 400,
            'transportation': 50,
        }

        rate = commission_rates.get(platform, 3.0)
        avg_value = avg_booking_values.get(item_type, 100)
        estimated_commission = (avg_value * rate / 100) * 0.5  # 50% estimated conversion

        # Create click record
        if content_type and item_id:
            click = AffiliateClick.objects.create(
                user=user,
                session_key=session_key,
                platform=platform,
                item_type=item_type,
                content_type=content_type,
                object_id=item_id,
                affiliate_url=affiliate_url[:1000],
                referrer_url=request.META.get('HTTP_REFERER', '')[:500],
                ip_address=ip_address,
                user_agent=user_agent,
                device_type=device_type,
                estimated_commission=estimated_commission,
            )

            return JsonResponse({
                'success': True,
                'click_id': click.id,
                'message': 'Click tracked successfully'
            })

        return JsonResponse({
            'success': True,
            'message': 'Click logged (partial data)'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


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