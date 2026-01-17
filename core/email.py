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
        # Handle TourBooking model (from tours app)
        if hasattr(booking, 'tour') and booking_type == 'tour':
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

        # Handle Booking model (from bookings app) for tours
        elif booking_type == 'tour':
            item = booking.content_object
            subject = f'Booking Confirmation - {item.name}'
            context = {
                'booking': booking,
                'tour': item,
                'user_name': booking.contact_name or booking.user.get_full_name(),
                'booking_date': booking.check_in_date,
                'adults': 1,
                'children': 0,
                'total_price': booking.total_amount,
                'status': booking.get_status_display(),
            }
            template = 'emails/tour_booking_confirmation.html'
            to_email = booking.contact_email or booking.user.email

        # Handle accommodation bookings
        else:
            item = booking.content_object
            subject = f'Booking Confirmation - {item.name if item else "Your Stay"}'
            # Get accommodation booking details if available
            acc_booking = getattr(booking, 'accommodation_details', None)
            context = {
                'booking': booking,
                'accommodation': item,
                'user_name': booking.contact_name or booking.user.get_full_name(),
                'check_in': booking.check_in_date,
                'check_out': booking.check_out_date,
                'nights': (booking.check_out_date - booking.check_in_date).days if booking.check_out_date else 1,
                'guests': acc_booking.number_of_guests if acc_booking else 1,
                'rooms': acc_booking.number_of_rooms if acc_booking else 1,
                'total_amount': booking.total_amount,
                'status': booking.get_status_display(),
            }
            template = 'emails/accommodation_booking_confirmation.html'
            to_email = booking.contact_email or booking.user.email

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


def send_lead_magnet_email(email, name, lead_magnet='egypt-travel-guide'):
    """
    Send lead magnet download email with PDF link.

    Args:
        email: Recipient email
        name: Recipient name
        lead_magnet: Type of lead magnet ('egypt-travel-guide', etc.)
    """
    try:
        # Lead magnet metadata
        lead_magnets = {
            'egypt-travel-guide': {
                'name': '7-Day Egypt Travel Guide',
                'description': 'Your complete guide to exploring Egypt',
                # Replace with actual PDF URL when uploaded
                'download_url': 'https://360egy.com/static/downloads/egypt-travel-guide.pdf',
            }
        }

        magnet_info = lead_magnets.get(lead_magnet, lead_magnets['egypt-travel-guide'])
        first_name = name.split()[0] if name else 'Traveler'

        subject = f"Your Free {magnet_info['name']} is Ready!"

        text_content = f"""
Hi {first_name}!

Thank you for downloading our {magnet_info['name']}!

DOWNLOAD YOUR GUIDE:
{magnet_info['download_url']}

What's inside:
- Complete 7-day itinerary for Cairo, Luxor & Aswan
- Budget breakdown and money-saving tips
- Top hotel recommendations for every budget
- Scam-avoidance tips from locals
- Must-try Egyptian food and restaurants
- Best times to visit each attraction

NEXT STEPS:
1. Download and save your guide
2. Browse our verified hotels: https://360egy.com/accommodations/
3. Explore our top-rated tours: https://360egy.com/tours/

Have questions about your Egypt trip? Reply to this email and we'll help you plan the perfect adventure!

Happy travels,
The Egy360 Team

---
https://360egy.com
Your trusted guide to Egyptian tourism

To unsubscribe: https://360egy.com/newsletter/unsubscribe?email={email}
        """

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #c41e3a, #9a1830); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .download-btn {{ display: inline-block; background: #c41e3a; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
        .features {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .feature-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">Your Free Guide is Ready!</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{magnet_info['name']}</p>
        </div>
        <div class="content">
            <p>Hi {first_name}!</p>
            <p>Thank you for downloading our comprehensive Egypt travel guide. Your adventure starts here!</p>

            <div style="text-align: center;">
                <a href="{magnet_info['download_url']}" class="download-btn">Download Your Guide</a>
            </div>

            <div class="features">
                <h3 style="margin-top: 0;">What's Inside:</h3>
                <div class="feature-item">Complete 7-day itinerary for Cairo, Luxor & Aswan</div>
                <div class="feature-item">Budget breakdown and money-saving tips</div>
                <div class="feature-item">Top hotel recommendations for every budget</div>
                <div class="feature-item">Scam-avoidance tips from locals</div>
                <div class="feature-item">Must-try Egyptian food and restaurants</div>
                <div class="feature-item">Best times to visit each attraction</div>
            </div>

            <h3>Ready to Book?</h3>
            <p>
                <a href="https://360egy.com/accommodations/">Browse Verified Hotels</a> |
                <a href="https://360egy.com/tours/">Explore Top Tours</a>
            </p>

            <p>Have questions? Just reply to this email!</p>

            <p>Happy travels,<br><strong>The Egy360 Team</strong></p>
        </div>
        <div class="footer">
            <p><a href="https://360egy.com">360egy.com</a> - Your trusted guide to Egyptian tourism</p>
            <p><a href="https://360egy.com/newsletter/unsubscribe?email={email}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
        """

        _send_email(
            subject=subject,
            text_content=text_content,
            html_content=html_content,
            to_email=email
        )

        logger.info(f"Lead magnet email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send lead magnet email: {e}")
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
