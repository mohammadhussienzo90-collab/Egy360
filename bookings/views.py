# bookings/views.py
"""
Bookings App Views
==================

This module handles all booking-related views for Egy360:
- Checkout flow for accommodations and tours
- Booking confirmation and details
- User's booking history
- Booking cancellation

The booking flow:
1. User clicks "Book Now" on accommodation/tour detail page
2. Redirected to checkout form (booking_checkout)
3. Fills in dates, guests, contact info
4. Form submitted -> Booking created -> Redirect to payment
5. After payment -> Booking confirmed

Key Models:
- Booking: Main booking record with GenericForeignKey to item
- AccommodationBooking: Extra details for hotel bookings
"""
import uuid
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Booking, AccommodationBooking
from .forms import BookingInquiryForm, TourBookingForm
from accommodations.models import Accommodation
from tours.models import Tour


def generate_booking_reference():
    """
    Generate a unique booking reference in format: EGY-XXXXXXXX

    Uses UUID4 for uniqueness, truncated to 8 chars for readability.
    Example: EGY-A1B2C3D4
    """
    return f"EGY-{uuid.uuid4().hex[:8].upper()}"


@login_required
def booking_checkout(request, booking_type, item_id):
    """
    Booking checkout page for accommodations or tours.

    This is the main booking form where users enter:
    - Check-in/check-out dates (or tour date)
    - Number of guests/participants
    - Contact information
    - Special requests

    After successful form submission:
    1. Booking record is created (status: pending)
    2. Confirmation email is sent
    3. User is redirected to payment page

    Args:
        booking_type: 'accommodation' or 'tour'
        item_id: ID of the Accommodation or Tour to book

    URL: /bookings/checkout/<booking_type>/<item_id>/
    """
    # =========================================================================
    # STEP 1: Determine item type and get the item from database
    # =========================================================================
    if booking_type == 'accommodation':
        item = get_object_or_404(Accommodation, id=item_id, is_active=True)
        form_class = BookingInquiryForm
        template = 'bookings/checkout_accommodation.html'
    elif booking_type == 'tour':
        item = get_object_or_404(Tour, id=item_id, is_active=True)
        form_class = TourBookingForm
        template = 'bookings/checkout_tour.html'
    else:
        messages.error(request, 'Invalid booking type.')
        return redirect('homepage')

    # =========================================================================
    # STEP 2: Handle form submission (POST) or display form (GET)
    # =========================================================================
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Get ContentType for GenericForeignKey (allows booking any model type)
            content_type = ContentType.objects.get_for_model(item)

            # -----------------------------------------------------------------
            # Calculate total price based on booking type
            # -----------------------------------------------------------------
            if booking_type == 'accommodation':
                check_in = form.cleaned_data['check_in_date']
                check_out = form.cleaned_data['check_out_date']
                nights = (check_out - check_in).days
                total_amount = item.price_per_night * nights * form.cleaned_data['number_of_rooms']
            else:
                # Tours: single date, price per person
                check_in = form.cleaned_data['tour_date']
                check_out = None
                nights = 1
                total_amount = item.price_per_person * form.cleaned_data['number_of_participants']

            # -----------------------------------------------------------------
            # Create the main Booking record
            # -----------------------------------------------------------------
            booking = Booking.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=item.id,
                booking_type=booking_type,
                booking_reference=generate_booking_reference(),
                check_in_date=check_in,
                check_out_date=check_out,
                total_amount=total_amount,
                contact_name=form.cleaned_data['contact_name'],
                contact_email=form.cleaned_data['contact_email'],
                contact_phone=form.cleaned_data['contact_phone'],
                special_requests=form.cleaned_data.get('special_requests', ''),
                status='pending'
            )

            # -----------------------------------------------------------------
            # Create accommodation-specific details (rooms, guests)
            # -----------------------------------------------------------------
            if booking_type == 'accommodation':
                AccommodationBooking.objects.create(
                    booking=booking,
                    accommodation=item,
                    number_of_guests=form.cleaned_data['number_of_guests'],
                    number_of_rooms=form.cleaned_data['number_of_rooms']
                )

            # -----------------------------------------------------------------
            # Send confirmation email (async-safe with try/except)
            # -----------------------------------------------------------------
            try:
                from core.email import send_booking_confirmation
                send_booking_confirmation(booking, booking_type=booking_type)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to send booking email: {e}")

            # -----------------------------------------------------------------
            # Redirect to payment page to complete the booking
            # -----------------------------------------------------------------
            messages.info(request, 'Please complete payment to confirm your booking.')
            return redirect('payments:checkout', booking_id=booking.id)

    # =========================================================================
    # STEP 3: Display form (GET request) - pre-fill with user data
    # =========================================================================
    else:
        # Pre-fill contact info from user profile
        initial_data = {
            'contact_name': request.user.get_full_name() or request.user.username,
            'contact_email': request.user.email,
        }
        if hasattr(request.user, 'profile') and request.user.profile.phone:
            initial_data['contact_phone'] = request.user.profile.phone

        # Get dates from query params if provided
        if booking_type == 'accommodation':
            if request.GET.get('check_in'):
                initial_data['check_in_date'] = request.GET.get('check_in')
            if request.GET.get('check_out'):
                initial_data['check_out_date'] = request.GET.get('check_out')
            if request.GET.get('guests'):
                initial_data['number_of_guests'] = request.GET.get('guests')
        elif booking_type == 'tour':
            if request.GET.get('tour_date'):
                initial_data['tour_date'] = request.GET.get('tour_date')
            if request.GET.get('adults'):
                initial_data['number_of_participants'] = int(request.GET.get('adults', 1))
                # Add children count to participants
                if request.GET.get('children'):
                    initial_data['number_of_participants'] += int(request.GET.get('children', 0))

        form = form_class(initial=initial_data)

    context = {
        'form': form,
        'item': item,
        'booking_type': booking_type,
    }

    return render(request, template, context)


# =============================================================================
# BOOKING DETAIL & HISTORY VIEWS
# =============================================================================

@login_required
def booking_confirmation(request, booking_id):
    """
    Display booking confirmation after successful payment.

    Shows booking details, reference number, and next steps.
    Users are redirected here after completing payment.
    """
    # Security: Only allow users to view their own bookings
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Get the booked item (Accommodation or Tour) via GenericForeignKey
    item = booking.content_object

    context = {
        'booking': booking,
        'item': item,
    }

    return render(request, 'bookings/confirmation.html', context)


@login_required
def my_bookings(request):
    """
    Display user's booking history.

    Shows all bookings (past, current, cancelled) ordered by date.
    Accessible via user dashboard or navigation menu.
    """
    # Get all bookings for current user, newest first
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'bookings': bookings,
    }

    return render(request, 'bookings/my_bookings.html', context)


@login_required
def booking_detail(request, booking_id):
    """
    Display detailed view of a single booking.

    Shows complete booking information, payment status,
    and actions (cancel, modify if applicable).
    """
    # Security: Only allow users to view their own bookings
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    item = booking.content_object

    context = {
        'booking': booking,
        'item': item,
    }

    return render(request, 'bookings/detail.html', context)


# =============================================================================
# BOOKING CANCELLATION
# =============================================================================

@login_required
def cancel_booking(request, booking_id):
    """
    Handle booking cancellation requests.

    GET: Display cancellation confirmation page
    POST: Process cancellation, update status, send notification

    Cancellation rules:
    - Cannot cancel already cancelled bookings
    - Cannot cancel completed bookings
    - Refund processing handled separately via payments app
    """
    # Security: Only allow users to cancel their own bookings
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Validate booking can be cancelled
    if booking.status in ['cancelled', 'completed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', booking_id=booking.id)

    if request.method == 'POST':
        # Update booking status
        booking.status = 'cancelled'
        booking.save()

        # Send cancellation notification email
        try:
            from core.email import send_booking_status_update
            send_booking_status_update(booking, booking_type=booking.booking_type)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Failed to send cancellation email: {e}")

        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:my_bookings')

    # GET: Show confirmation page
    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})


# =============================================================================
# AJAX ENDPOINTS
# =============================================================================

@require_POST
@login_required
def quick_book(request):
    """
    AJAX endpoint for quick booking intent.

    Used by "Book Now" buttons that need to verify item exists
    before redirecting to checkout. Returns checkout URL.

    Request (POST):
        booking_type: 'accommodation' or 'tour'
        item_id: ID of the item

    Response (JSON):
        success: boolean
        checkout_url: URL to redirect to (if success)
        message: error message (if failure)
    """
    booking_type = request.POST.get('booking_type')
    item_id = request.POST.get('item_id')

    # Validate item exists
    if booking_type == 'accommodation':
        item = get_object_or_404(Accommodation, id=item_id)
    elif booking_type == 'tour':
        item = get_object_or_404(Tour, id=item_id)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid booking type'})

    # Return checkout URL for redirect
    return JsonResponse({
        'success': True,
        'checkout_url': f'/bookings/checkout/{booking_type}/{item_id}/'
    })
