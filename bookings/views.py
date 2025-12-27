# bookings/views.py
"""
Views for Bookings App
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
    """Generate a unique booking reference"""
    return f"EGY-{uuid.uuid4().hex[:8].upper()}"


@login_required
def booking_checkout(request, booking_type, item_id):
    """
    Booking checkout page for accommodations or tours
    """
    # Get the item being booked
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

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Create the booking
            content_type = ContentType.objects.get_for_model(item)

            # Calculate nights/price for accommodations
            if booking_type == 'accommodation':
                check_in = form.cleaned_data['check_in_date']
                check_out = form.cleaned_data['check_out_date']
                nights = (check_out - check_in).days
                total_amount = item.price_per_night * nights * form.cleaned_data['number_of_rooms']
            else:
                check_in = form.cleaned_data['tour_date']
                check_out = None
                nights = 1
                total_amount = item.price_per_person * form.cleaned_data['number_of_participants']

            # Create booking
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

            # Create accommodation-specific details
            if booking_type == 'accommodation':
                AccommodationBooking.objects.create(
                    booking=booking,
                    accommodation=item,
                    number_of_guests=form.cleaned_data['number_of_guests'],
                    number_of_rooms=form.cleaned_data['number_of_rooms']
                )

            messages.success(request, 'Booking request submitted successfully!')
            return redirect('bookings:confirmation', booking_id=booking.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'contact_name': request.user.get_full_name() or request.user.username,
            'contact_email': request.user.email,
        }
        if hasattr(request.user, 'profile') and request.user.profile.phone:
            initial_data['contact_phone'] = request.user.profile.phone

        # Get dates from query params if provided
        if request.GET.get('check_in'):
            initial_data['check_in_date'] = request.GET.get('check_in')
        if request.GET.get('check_out'):
            initial_data['check_out_date'] = request.GET.get('check_out')
        if request.GET.get('guests'):
            initial_data['number_of_guests'] = request.GET.get('guests')

        form = form_class(initial=initial_data)

    context = {
        'form': form,
        'item': item,
        'booking_type': booking_type,
    }

    return render(request, template, context)


@login_required
def booking_confirmation(request, booking_id):
    """
    Booking confirmation page
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Get the booked item
    item = booking.content_object

    context = {
        'booking': booking,
        'item': item,
    }

    return render(request, 'bookings/confirmation.html', context)


@login_required
def my_bookings(request):
    """
    User's bookings list
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'bookings': bookings,
    }

    return render(request, 'bookings/my_bookings.html', context)


@login_required
def booking_detail(request, booking_id):
    """
    Booking detail page
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    item = booking.content_object

    context = {
        'booking': booking,
        'item': item,
    }

    return render(request, 'bookings/detail.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status in ['cancelled', 'completed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', booking_id=booking.id)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:my_bookings')

    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})


@require_POST
@login_required
def quick_book(request):
    """
    Quick booking via AJAX - saves booking intent
    """
    booking_type = request.POST.get('booking_type')
    item_id = request.POST.get('item_id')

    if booking_type == 'accommodation':
        item = get_object_or_404(Accommodation, id=item_id)
    elif booking_type == 'tour':
        item = get_object_or_404(Tour, id=item_id)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid booking type'})

    # Return checkout URL
    return JsonResponse({
        'success': True,
        'checkout_url': f'/bookings/checkout/{booking_type}/{item_id}/'
    })
