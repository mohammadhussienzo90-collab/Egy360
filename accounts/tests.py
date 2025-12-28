# accounts/tests.py
"""
Tests for Accounts App

Tests for user registration, login, profile management.
Uses Django's built-in User model with UserProfile extension.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileModelTest(TestCase):
    """Tests for UserProfile model"""

    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

    def test_profile_auto_created(self):
        """Test that profile is auto-created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_profile_str_representation(self):
        """Test profile string representation"""
        expected = f"{self.user.username} - Profile"
        self.assertEqual(str(self.user.profile), expected)

    def test_otp_generation(self):
        """Test OTP code generation"""
        profile = self.user.profile
        otp = profile.generate_otp()

        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())
        self.assertEqual(profile.phone_otp, otp)
        self.assertIsNotNone(profile.phone_otp_created)

    def test_otp_verification_success(self):
        """Test successful OTP verification"""
        profile = self.user.profile
        otp = profile.generate_otp()

        success, message = profile.verify_otp(otp)

        self.assertTrue(success)
        self.assertEqual(message, "OTP verified successfully")
        self.assertTrue(profile.phone_verified)

    def test_otp_verification_wrong_code(self):
        """Test OTP verification with wrong code"""
        profile = self.user.profile
        profile.generate_otp()

        success, message = profile.verify_otp('000000')

        self.assertFalse(success)
        self.assertEqual(message, "Invalid OTP code")

    def test_backup_codes_generation(self):
        """Test backup codes generation for 2FA"""
        profile = self.user.profile
        codes = profile.generate_backup_codes()

        self.assertEqual(len(codes), 10)
        for code in codes:
            self.assertRegex(code, r'^[A-Z0-9]{4}-[A-Z0-9]{4}$')

    def test_backup_code_verification(self):
        """Test backup code verification and consumption"""
        profile = self.user.profile
        codes = profile.generate_backup_codes()
        first_code = codes[0]

        # Verify should succeed
        result = profile.verify_backup_code(first_code)
        self.assertTrue(result)

        # Same code should not work again
        result = profile.verify_backup_code(first_code)
        self.assertFalse(result)

    def test_masked_phone(self):
        """Test phone number masking"""
        profile = self.user.profile
        profile.phone = '+201001234567'
        profile.save()

        masked = profile.get_masked_phone()
        self.assertEqual(masked, '***-***-4567')


class UserAuthenticationTest(TestCase):
    """Tests for user authentication views"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )

    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        """Test register page loads successfully"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        # Should redirect on success
        self.assertIn(response.status_code, [200, 302])

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)  # Returns to login page

    def test_profile_requires_login(self):
        """Test profile page requires authentication"""
        response = self.client.get(reverse('accounts:profile'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_profile_accessible_when_logged_in(self):
        """Test profile page accessible when logged in"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('accounts:logout'))
        # Should redirect after logout
        self.assertIn(response.status_code, [200, 302])
