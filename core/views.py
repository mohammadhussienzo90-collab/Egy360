"""
Egy360 Core App Views
=====================

This module contains core views for the Egy360 tourism platform:
- Affiliate click tracking (revenue generation)
- Homepage and basic page views
- Accommodation/tour search and detail views
- User dashboard
- Legacy booking flow views

Key Endpoints:
- POST /api/track-click/ - Track affiliate link clicks for revenue
- GET / - Homepage
- GET /accommodations/search/ - Search hotels
- GET /tours/ - Browse tours
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
import json


# =============================================================================
# AFFILIATE CLICK TRACKING
# =============================================================================
#
# This is the core revenue-generating feature. When users click affiliate links
# (Booking.com, Viator, etc.), we track the click for analytics and to estimate
# commissions. The actual commission is paid by the affiliate partner when the
# user completes a booking on their site.
#
# Flow:
# 1. User clicks "Book on Booking.com" button
# 2. JavaScript sends POST to /api/track-click/
# 3. We record the click with user/session/device info
# 4. User is redirected to affiliate site (happens client-side)
# 5. If user books, affiliate pays us commission (tracked separately)
# =============================================================================

@require_http_methods(["POST"])
def track_affiliate_click(request):
    """
    API endpoint to track affiliate link clicks for revenue analytics.

    Called asynchronously by JavaScript when user clicks any affiliate link.
    Does not block the user's navigation to the affiliate site.

    Request Body (JSON):
        item_type: 'accommodation', 'tour', 'transportation', 'flight'
        item_id: ID of the clicked item (optional)
        platform: 'booking_com', 'hotellook', 'viator', 'getyourguide', etc.
        url: The affiliate URL being clicked

    Response (JSON):
        success: boolean
        click_id: ID of created click record (if success)
        message: Status message

    Revenue Model:
        - Hotellook: ~2.5% commission on hotel bookings
        - Booking.com: ~4% commission
        - Viator/GetYourGuide: ~8% commission on tour bookings
    """
    from .models import AffiliateClick

    try:
        # Parse JSON request body
        data = json.loads(request.body)

        # Extract click information from request
        item_type = data.get('item_type', 'accommodation')
        item_id = data.get('item_id')
        platform = data.get('platform', 'other')
        affiliate_url = data.get('url', '')

        # -----------------------------------------------------------------
        # UTM Parameters for Social Media Attribution
        # These help track which Instagram post, TikTok video, or Facebook
        # ad drove this click. Essential for measuring ROI on social media.
        # -----------------------------------------------------------------
        utm_source = data.get('utm_source', '')    # e.g., 'instagram', 'facebook'
        utm_medium = data.get('utm_medium', '')    # e.g., 'social', 'cpc'
        utm_campaign = data.get('utm_campaign', '')  # e.g., 'egypt_tours_jan2025'
        utm_content = data.get('utm_content', '')  # e.g., 'pyramids_reel'

        # -----------------------------------------------------------------
        # Map item type to Django ContentType for GenericForeignKey
        # This allows us to link clicks to any model type
        # -----------------------------------------------------------------
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

        # -----------------------------------------------------------------
        # Extract user information (works for both logged in and anonymous)
        # -----------------------------------------------------------------
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        # Get IP address (handle proxy/load balancer forwarding)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Get user agent (truncate to prevent DB overflow)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

        # -----------------------------------------------------------------
        # Detect device type from user agent string
        # Used for analytics (mobile vs desktop conversion rates)
        # -----------------------------------------------------------------
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            device_type = 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        # -----------------------------------------------------------------
        # Estimate commission for revenue forecasting
        # These are approximate rates from affiliate programs (as %)
        # -----------------------------------------------------------------
        commission_rates = {
            'booking_com': 4.0,     # Booking.com pays ~4% commission
            'hotellook': 2.5,       # Hotellook/Travelpayouts pays ~2.5%
            'viator': 8.0,          # Viator pays ~8% on tour bookings
            'getyourguide': 8.0,    # GetYourGuide pays ~8%
            'agoda': 5.0,           # Agoda pays ~5%
        }

        # Average booking values by type (in USD for estimation)
        avg_booking_values = {
            'accommodation': 100,   # Average hotel booking
            'tour': 80,             # Average tour booking
            'flight': 400,          # Average flight booking
            'transportation': 50,   # Average transfer booking
        }

        # Calculate estimated commission (assuming 50% conversion rate)
        rate = commission_rates.get(platform, 3.0)
        avg_value = avg_booking_values.get(item_type, 100)
        estimated_commission = (avg_value * rate / 100) * 0.5

        # -----------------------------------------------------------------
        # Create click record in database
        # This record is used for:
        # 1. Revenue analytics dashboard
        # 2. Social media campaign ROI tracking
        # 3. Conversion rate optimization
        # -----------------------------------------------------------------
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
                # UTM parameters for social media attribution
                utm_source=utm_source[:100] if utm_source else None,
                utm_medium=utm_medium[:100] if utm_medium else None,
                utm_campaign=utm_campaign[:200] if utm_campaign else None,
                utm_content=utm_content[:200] if utm_content else None,
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