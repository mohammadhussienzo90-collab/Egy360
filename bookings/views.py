"""
Views for Bookings App
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking


@login_required
def booking_checkout(request):
    """
    Booking checkout page
    Template: booking_checkout.html
    """
    if request.method == 'POST':
        # Process booking
        messages.success(request, 'Booking confirmed!')
        return redirect('bookings:confirmation', booking_id=1)

    return render(request, 'booking_checkout.html')


@login_required
def booking_confirmation(request, booking_id):
    """
    Booking confirmation page
    Template: booking_confirmation.html
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    context = {
        'booking': booking,
    }

    return render(request, 'booking_confirmation.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('dashboard:user-dashboard')

    return render(request, 'bookings/cancel_confirmation.html', {'booking': booking})