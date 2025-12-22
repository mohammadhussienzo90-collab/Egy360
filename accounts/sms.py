# accounts/sms.py
"""
SMS service for sending OTP codes via Twilio
"""
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_otp_sms(phone_number, otp_code):
    """
    Send OTP code via SMS using Twilio

    Args:
        phone_number: Full phone number with country code (e.g., +201234567890)
        otp_code: 6-digit OTP code

    Returns:
        tuple: (success: bool, message: str, sid: str or None)
    """
    # Check if Twilio is configured
    if not all([
        getattr(settings, 'TWILIO_ACCOUNT_SID', ''),
        getattr(settings, 'TWILIO_AUTH_TOKEN', ''),
        getattr(settings, 'TWILIO_PHONE_NUMBER', '')
    ]):
        logger.warning("Twilio not configured. SMS not sent. OTP: %s", otp_code)
        # In development, just log the OTP
        return True, f"Development mode - OTP: {otp_code}", None

    try:
        from twilio.rest import Client

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        message = client.messages.create(
            body=f"Your Egy360 verification code is: {otp_code}. This code expires in 5 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        logger.info("SMS sent successfully to %s, SID: %s", phone_number[-4:], message.sid)
        return True, "SMS sent successfully", message.sid

    except ImportError:
        logger.error("Twilio library not installed")
        return False, "SMS service not available", None
    except Exception as e:
        logger.error("Failed to send SMS: %s", str(e))
        return False, f"Failed to send SMS: {str(e)}", None


def send_2fa_sms(phone_number, otp_code):
    """
    Send 2FA verification code via SMS

    Args:
        phone_number: Full phone number with country code
        otp_code: 6-digit verification code

    Returns:
        tuple: (success: bool, message: str, sid: str or None)
    """
    # Check if Twilio is configured
    if not all([
        getattr(settings, 'TWILIO_ACCOUNT_SID', ''),
        getattr(settings, 'TWILIO_AUTH_TOKEN', ''),
        getattr(settings, 'TWILIO_PHONE_NUMBER', '')
    ]):
        logger.warning("Twilio not configured. 2FA SMS not sent. Code: %s", otp_code)
        return True, f"Development mode - 2FA Code: {otp_code}", None

    try:
        from twilio.rest import Client

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        message = client.messages.create(
            body=f"Your Egy360 login verification code is: {otp_code}. Do not share this code with anyone.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        logger.info("2FA SMS sent successfully to %s, SID: %s", phone_number[-4:], message.sid)
        return True, "2FA SMS sent successfully", message.sid

    except ImportError:
        logger.error("Twilio library not installed")
        return False, "SMS service not available", None
    except Exception as e:
        logger.error("Failed to send 2FA SMS: %s", str(e))
        return False, f"Failed to send 2FA SMS: {str(e)}", None


def validate_phone_number(phone_number):
    """
    Validate and format phone number

    Args:
        phone_number: Phone number string

    Returns:
        tuple: (is_valid: bool, formatted_number: str or None, error: str or None)
    """
    try:
        import phonenumbers

        # Parse the phone number
        parsed = phonenumbers.parse(phone_number, None)

        # Check if it's a valid number
        if not phonenumbers.is_valid_number(parsed):
            return False, None, "Invalid phone number"

        # Format to E.164 format (+1234567890)
        formatted = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

        return True, formatted, None

    except ImportError:
        # If phonenumbers library is not installed, do basic validation
        clean_number = ''.join(filter(str.isdigit, phone_number))
        if phone_number.startswith('+'):
            clean_number = '+' + clean_number
        if len(clean_number) >= 10:
            return True, clean_number, None
        return False, None, "Invalid phone number format"

    except Exception as e:
        return False, None, str(e)
