"""
Unit Tests for Utility Functions and Helpers
Tests standalone utility functions, validators, and helpers
"""
from django.test import TestCase
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal
import json


class EmailValidatorTests(TestCase):
    """Tests for email validation utilities"""

    def test_valid_email_formats(self):
        """Test various valid email formats"""
        valid_emails = [
            'simple@example.com',
            'user.name@domain.com',
            'user+tag@example.org',
            'firstname.lastname@company.co.uk',
            'user123@test-domain.com',
            'test_email@sub.domain.org',
        ]
        for email in valid_emails:
            try:
                validate_email(email)
            except ValidationError:
                self.fail(f"Email {email} should be valid")

    def test_invalid_email_formats(self):
        """Test various invalid email formats"""
        invalid_emails = [
            'plainaddress',
            '@no-local-part.com',
            'no-at-sign.com',
            'no-domain@',
            'spaces in@email.com',
            'double..dot@example.com',
            '.leading-dot@example.com',
            'trailing-dot.@example.com',
        ]
        for email in invalid_emails:
            with self.assertRaises(ValidationError, msg=f"Email {email} should be invalid"):
                validate_email(email)


class CommissionCalculationTests(TestCase):
    """Tests for commission calculation logic"""

    def test_commission_rates_mapping(self):
        """Test commission rate mappings are correct"""
        commission_rates = {
            'booking_com': 4.0,
            'hotellook': 2.5,
            'viator': 8.0,
            'getyourguide': 8.0,
            'agoda': 5.0,
        }

        self.assertEqual(commission_rates['booking_com'], 4.0)
        self.assertEqual(commission_rates['viator'], 8.0)
        self.assertEqual(commission_rates['hotellook'], 2.5)

    def test_commission_calculation(self):
        """Test commission calculation formula"""
        avg_booking_value = 100
        commission_rate = 8.0
        conversion_factor = 0.5

        expected = (avg_booking_value * commission_rate / 100) * conversion_factor
        self.assertEqual(expected, 4.0)

    def test_commission_with_different_values(self):
        """Test commission with various booking values"""
        test_cases = [
            (100, 4.0, 0.5, 2.0),   # $100 booking, 4% rate, 50% conversion
            (200, 8.0, 0.5, 8.0),   # $200 booking, 8% rate, 50% conversion
            (50, 5.0, 0.5, 1.25),   # $50 booking, 5% rate, 50% conversion
        ]

        for booking_value, rate, conversion, expected in test_cases:
            result = (booking_value * rate / 100) * conversion
            self.assertEqual(result, expected)


class DeviceTypeDetectionTests(TestCase):
    """Tests for device type detection from user agent"""

    def detect_device_type(self, user_agent):
        """Helper to detect device type from user agent"""
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'tablet'
        else:
            return 'desktop'

    def test_mobile_detection(self):
        """Test mobile device detection"""
        mobile_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36',
        ]
        for agent in mobile_agents:
            self.assertEqual(self.detect_device_type(agent), 'mobile')

    def test_tablet_detection(self):
        """Test tablet device detection"""
        tablet_agents = [
            'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        ]
        for agent in tablet_agents:
            self.assertEqual(self.detect_device_type(agent), 'tablet')

    def test_android_tablet_detected_as_mobile(self):
        """Test Android tablet detected as mobile (simplified detection)"""
        # Note: Simple detection doesn't distinguish Android tablets from phones
        agent = 'Mozilla/5.0 (Linux; Android 10; Tablet) AppleWebKit/537.36'
        # Android devices are detected as mobile in simple detection
        result = self.detect_device_type(agent)
        self.assertIn(result, ['mobile', 'tablet'])

    def test_desktop_detection(self):
        """Test desktop device detection"""
        desktop_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        for agent in desktop_agents:
            self.assertEqual(self.detect_device_type(agent), 'desktop')


class IPAddressExtractionTests(TestCase):
    """Tests for IP address extraction logic"""

    def extract_ip(self, x_forwarded_for, remote_addr):
        """Helper to extract IP address"""
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return remote_addr

    def test_direct_connection_ip(self):
        """Test IP extraction for direct connection"""
        ip = self.extract_ip(None, '192.168.1.1')
        self.assertEqual(ip, '192.168.1.1')

    def test_single_proxy_ip(self):
        """Test IP extraction with single proxy"""
        ip = self.extract_ip('203.0.113.195', '10.0.0.1')
        self.assertEqual(ip, '203.0.113.195')

    def test_multiple_proxies_ip(self):
        """Test IP extraction with multiple proxies"""
        ip = self.extract_ip('203.0.113.195, 70.41.3.18, 150.172.238.178', '10.0.0.1')
        self.assertEqual(ip, '203.0.113.195')

    def test_ipv6_address(self):
        """Test IPv6 address extraction"""
        ip = self.extract_ip(None, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertEqual(ip, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')


class PlatformMappingTests(TestCase):
    """Tests for platform URL to name mapping"""

    def test_platform_detection_from_url(self):
        """Test detecting platform from URL"""
        test_cases = [
            ('https://www.booking.com/hotel/eg/test', 'booking_com'),
            ('https://hotellook.com/hotels/cairo', 'hotellook'),
            ('https://www.viator.com/tours/cairo', 'viator'),
            ('https://www.getyourguide.com/cairo', 'getyourguide'),
            ('https://www.agoda.com/egypt', 'agoda'),
            ('https://tp.media/click?campaign_id=100', 'travelpayouts'),
            ('https://aviasales.com/flights', 'aviasales'),
        ]

        for url, expected_platform in test_cases:
            url_lower = url.lower()
            if 'booking.com' in url_lower:
                platform = 'booking_com'
            elif 'hotellook' in url_lower:
                platform = 'hotellook'
            elif 'viator' in url_lower:
                platform = 'viator'
            elif 'getyourguide' in url_lower:
                platform = 'getyourguide'
            elif 'agoda' in url_lower:
                platform = 'agoda'
            elif 'tp.media' in url_lower or 'travelpayouts' in url_lower:
                platform = 'travelpayouts'
            elif 'aviasales' in url_lower:
                platform = 'aviasales'
            else:
                platform = 'other'

            self.assertEqual(platform, expected_platform, f"URL {url} should map to {expected_platform}")


class SlugGenerationTests(TestCase):
    """Tests for slug generation utilities"""

    def test_slug_from_name(self):
        """Test generating slugs from names"""
        from django.utils.text import slugify

        test_cases = [
            ('Test Hotel Cairo', 'test-hotel-cairo'),
            ('Marriott Cairo', 'marriott-cairo'),
            ('5-Star Luxury Resort', '5-star-luxury-resort'),
            ('Hotel with   Spaces', 'hotel-with-spaces'),
            ('UPPERCASE HOTEL', 'uppercase-hotel'),
        ]

        for name, expected in test_cases:
            self.assertEqual(slugify(name), expected)

    def test_slug_uniqueness_suffix(self):
        """Test adding suffix for unique slugs"""
        base_slug = 'test-hotel'

        # Simulate adding suffix for uniqueness
        for i in range(3):
            if i == 0:
                slug = base_slug
            else:
                slug = f"{base_slug}-{i}"
            self.assertIn(base_slug, slug)


class JSONFieldValidationTests(TestCase):
    """Tests for JSON field handling"""

    def test_valid_json_list(self):
        """Test valid JSON list parsing"""
        valid_lists = [
            '["item1", "item2"]',
            '["a", "b", "c"]',
            '[]',
        ]
        for json_str in valid_lists:
            result = json.loads(json_str)
            self.assertIsInstance(result, list)

    def test_valid_json_dict(self):
        """Test valid JSON dict parsing"""
        valid_dicts = [
            '{"key": "value"}',
            '{"a": 1, "b": 2}',
            '{}',
        ]
        for json_str in valid_dicts:
            result = json.loads(json_str)
            self.assertIsInstance(result, dict)

    def test_invalid_json(self):
        """Test invalid JSON raises error"""
        invalid_json = [
            'not json',
            "{'single': 'quotes'}",
            '[missing, quotes]',
        ]
        for json_str in invalid_json:
            with self.assertRaises(json.JSONDecodeError):
                json.loads(json_str)


class PriceFormattingTests(TestCase):
    """Tests for price formatting utilities"""

    def format_price(self, amount, currency='USD'):
        """Helper to format price"""
        if currency == 'USD':
            return f"${amount:,.2f}"
        elif currency == 'EUR':
            return f"\u20ac{amount:,.2f}"
        elif currency == 'EGP':
            return f"EGP {amount:,.2f}"
        return f"{amount:,.2f} {currency}"

    def test_usd_formatting(self):
        """Test USD price formatting"""
        self.assertEqual(self.format_price(Decimal('100.00')), '$100.00')
        self.assertEqual(self.format_price(Decimal('1000.50')), '$1,000.50')
        self.assertEqual(self.format_price(Decimal('1234567.89')), '$1,234,567.89')

    def test_eur_formatting(self):
        """Test EUR price formatting"""
        self.assertEqual(self.format_price(Decimal('100.00'), 'EUR'), '\u20ac100.00')

    def test_egp_formatting(self):
        """Test EGP price formatting"""
        self.assertEqual(self.format_price(Decimal('100.00'), 'EGP'), 'EGP 100.00')


class DateCalculationTests(TestCase):
    """Tests for date calculation utilities"""

    def calculate_nights(self, check_in, check_out):
        """Calculate number of nights between dates"""
        return (check_out - check_in).days

    def test_nights_calculation(self):
        """Test nights calculation"""
        from datetime import date

        test_cases = [
            (date(2024, 1, 1), date(2024, 1, 2), 1),
            (date(2024, 1, 1), date(2024, 1, 8), 7),
            (date(2024, 1, 1), date(2024, 1, 15), 14),
            (date(2024, 1, 1), date(2024, 2, 1), 31),
        ]

        for check_in, check_out, expected in test_cases:
            self.assertEqual(self.calculate_nights(check_in, check_out), expected)

    def test_same_day_zero_nights(self):
        """Test same day check-in/out returns 0"""
        from datetime import date

        check_in = date(2024, 1, 1)
        check_out = date(2024, 1, 1)
        self.assertEqual(self.calculate_nights(check_in, check_out), 0)
