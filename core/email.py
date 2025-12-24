"""
Email utilities for Egy360
Handles sending transactional emails for bookings, notifications, etc.
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_booking_confirmation(booking, booking_type='tour'):
    """
    Send booking confirmation email to user

    Args:
        booking: TourBooking or Booking instance
        booking_type: 'tour' or 'accommodation'
    """
    try:
        if booking_type == 'tour':
            subject = f'Booking Confirmation - {booking.tour.name}'
            context = {
                'booking': booking,
                'tour': booking.tour,
                'user_name': booking.contact_name or booking.user.get_full_name(),
                'booking_date': booking.tour_date,
                'adults': booking.number_of_adults,
                'children': booking.number_of_children,
                'total_price': booking.total_price,
                'status': booking.get_status_display(),
            }
            template = 'emails/tour_booking_confirmation.html'
            to_email = booking.contact_email or booking.user.email
        else:
            subject = f'Booking Confirmation - #{booking.id}'
            context = {
                'booking': booking,
                'user_name': booking.user.get_full_name(),
                'total_amount': getattr(booking, 'total_amount', 0),
                'status': booking.get_status_display(),
            }
            template = 'emails/booking_confirmation.html'
            to_email = booking.user.email

        # Try to render HTML template, fall back to plain text
        try:
            html_content = render_to_string(template, context)
            text_content = strip_tags(html_content)
        except Exception as e:
            # Fallback to simple text email
            logger.warning(f"Failed to render email template {template}: {e}")
            text_content = _get_booking_text(booking, booking_type)
            html_content = None

        _send_email(
            subject=subject,
            text_content=text_content,
            html_content=html_content,
            to_email=to_email
        )

        logger.info(f"Booking confirmation sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send booking confirmation: {e}")
        return False


def send_booking_status_update(booking, booking_type='tour'):
    """
    Send booking status update email
    """
    try:
        if booking_type == 'tour':
            subject = f'Booking Update - {booking.tour.name}'
            to_email = booking.contact_email or booking.user.email
            item_name = booking.tour.name
        else:
            subject = f'Booking Update - #{booking.id}'
            to_email = booking.user.email
            item_name = f'Booking #{booking.id}'

        status_messages = {
            'confirmed': f'Great news! Your booking for {item_name} has been confirmed.',
            'cancelled': f'Your booking for {item_name} has been cancelled.',
            'completed': f'Thank you for traveling with us! Your booking for {item_name} is now complete.',
            'pending': f'Your booking for {item_name} is pending confirmation.',
        }

        status = booking.status
        message = status_messages.get(status, f'Your booking status has been updated to: {status}')

        text_content = f"""
Dear {booking.user.get_full_name() or 'Valued Customer'},

{message}

Booking Details:
- Booking ID: {booking.id}
- Status: {booking.get_status_display()}

If you have any questions, please contact us at support@360egy.com

Thank you for choosing Egy360!

Best regards,
The Egy360 Team
        """

        _send_email(
            subject=subject,
            text_content=text_content,
            to_email=to_email
        )

        logger.info(f"Status update sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send status update: {e}")
        return False


def send_contact_notification(contact_message):
    """
    Send notification to admin when new contact form is submitted
    """
    try:
        subject = f'New Contact Form: {contact_message.subject}'

        text_content = f"""
New contact form submission on Egy360:

From: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone or 'Not provided'}
Subject: {contact_message.subject}

Message:
{contact_message.message}

---
Submitted at: {contact_message.created_at}
        """

        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@360egy.com')

        _send_email(
            subject=subject,
            text_content=text_content,
            to_email=admin_email
        )

        logger.info(f"Contact notification sent to admin")
        return True

    except Exception as e:
        logger.error(f"Failed to send contact notification: {e}")
        return False


def send_newsletter_welcome(subscription):
    """
    Send welcome email to new newsletter subscribers
    """
    try:
        subject = 'Welcome to Egy360 Newsletter!'

        text_content = f"""
Welcome to Egy360!

Thank you for subscribing to our newsletter. You'll now receive:

- Exclusive travel deals and discounts
- New tour announcements
- Travel tips for Egypt
- Special offers from our partners

Stay tuned for amazing content!

Best regards,
The Egy360 Team

---
To unsubscribe, visit: https://360egy.com/newsletter/unsubscribe?email={subscription.email}
        """

        _send_email(
            subject=subject,
            text_content=text_content,
            to_email=subscription.email
        )

        logger.info(f"Newsletter welcome sent to {subscription.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send newsletter welcome: {e}")
        return False


def _send_email(subject, text_content, to_email, html_content=None):
    """
    Internal helper to send emails
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@360egy.com')

    if html_content:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
    else:
        send_mail(
            subject=subject,
            message=text_content,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False
        )


def _get_booking_text(booking, booking_type):
    """
    Generate plain text booking confirmation
    """
    if booking_type == 'tour':
        return f"""
Dear {booking.contact_name or booking.user.get_full_name()},

Thank you for your booking with Egy360!

Booking Details:
- Tour: {booking.tour.name}
- Date: {booking.tour_date}
- Adults: {booking.number_of_adults}
- Children: {booking.number_of_children}
- Total: ${booking.total_price}
- Status: {booking.get_status_display()}

We will contact you shortly to confirm your booking.

Best regards,
The Egy360 Team
        """
    else:
        return f"""
Dear {booking.user.get_full_name()},

Thank you for your booking with Egy360!

Booking ID: {booking.id}
Status: {booking.get_status_display()}

We will contact you shortly with more details.

Best regards,
The Egy360 Team
        """
