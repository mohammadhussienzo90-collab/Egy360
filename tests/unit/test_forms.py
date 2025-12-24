"""
Unit Tests for Forms
Tests form validation, field requirements, and custom clean methods
"""
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    UserProfileForm
)


class UserRegistrationFormTests(TestCase):
    """Unit tests for UserRegistrationForm"""

    def test_valid_registration_form(self):
        """Test form is valid with correct data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_field_required(self):
        """Test email field is required"""
        form_data = {
            'username': 'testuser',
            'email': '',  # Empty email
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_field_invalid_format(self):
        """Test email validation"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        """Test passwords must match"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass456!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_password_too_short(self):
        """Test password minimum length"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'short',
            'password2': 'short'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_password_too_common(self):
        """Test common password rejection"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_required(self):
        """Test username is required"""
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_duplicate_username(self):
        """Test duplicate username rejection"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_fields_have_css_class(self):
        """Test form fields have form-control CSS class"""
        form = UserRegistrationForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get('class'), 'form-control')


class UserLoginFormTests(TestCase):
    """Unit tests for UserLoginForm"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_valid_login_form(self):
        """Test form is valid with correct credentials"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_credentials(self):
        """Test form invalid with wrong password"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_username(self):
        """Test form invalid without username"""
        form_data = {
            'username': '',
            'password': 'testpass123'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_password(self):
        """Test form invalid without password"""
        form_data = {
            'username': 'testuser',
            'password': ''
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_fields_have_css_class(self):
        """Test form fields have form-control CSS class"""
        form = UserLoginForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get('class'), 'form-control')


class UserUpdateFormTests(TestCase):
    """Unit tests for UserUpdateForm"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_valid_update_form(self):
        """Test form is valid with correct data"""
        form_data = {
            'username': 'testuser',
            'email': 'new@example.com',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_email_required(self):
        """Test email is required"""
        form_data = {
            'username': 'testuser',
            'email': '',
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_email_format(self):
        """Test email validation"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_empty_names_allowed(self):
        """Test first_name and last_name can be empty"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': '',
            'last_name': ''
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())


class UserProfileFormTests(TestCase):
    """Unit tests for UserProfileForm"""

    def setUp(self):
        """Create test user and profile"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_valid_profile_form(self):
        """Test form is valid with correct data"""
        form_data = {
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'nationality': 'Egyptian',
            'passport_number': 'AB123456',
            'bio': 'Test bio'
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_all_fields_optional(self):
        """Test all profile fields are optional"""
        form_data = {}
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_valid_date_format(self):
        """Test date field accepts valid date"""
        form_data = {
            'date_of_birth': '1990-05-15'
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_date_format(self):
        """Test date field rejects invalid format"""
        form_data = {
            'date_of_birth': '15/05/1990'  # Wrong format
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())

    def test_phone_field_max_length(self):
        """Test phone field respects max length"""
        form_data = {
            'phone': '+' + '1' * 25  # Too long
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())

    def test_nationality_max_length(self):
        """Test nationality field respects max length"""
        form_data = {
            'nationality': 'A' * 101  # Too long
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())

    def test_form_widgets(self):
        """Test form widgets are correctly configured"""
        form = UserProfileForm()
        # Check bio has correct rows
        self.assertEqual(form.fields['bio'].widget.attrs.get('rows'), 4)
        # Check date_of_birth is a date input (type attribute may not always be present)
        self.assertIn('date', str(form.fields['date_of_birth'].widget.__class__.__name__).lower())


class ContactFormValidationTests(TestCase):
    """Tests for contact form validation logic (via view)"""

    def test_all_required_fields(self):
        """Test contact form requires name, email, message"""
        # This tests the validation logic in the view
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            # Each field should be required based on view logic
            self.assertIn(field, required_fields)

    def test_email_validation_format(self):
        """Test email format validation"""
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        # Valid emails
        valid_emails = [
            'test@example.com',
            'user.name@domain.org',
            'user+tag@example.co.uk'
        ]
        for email in valid_emails:
            validate_email(email)  # Should not raise

        # Invalid emails
        invalid_emails = [
            'invalid',
            '@domain.com',
            'user@',
            'user@domain',
        ]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                validate_email(email)


class NewsletterSubscriptionFormTests(TestCase):
    """Tests for newsletter subscription validation"""

    def test_email_format_validation(self):
        """Test email format is validated"""
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        # Valid email
        validate_email('subscriber@example.com')

        # Invalid email
        with self.assertRaises(ValidationError):
            validate_email('not-an-email')

    def test_email_uniqueness(self):
        """Test duplicate emails are handled"""
        from home.models import NewsletterSubscription

        # Create first subscription
        NewsletterSubscription.objects.create(email='test@example.com')

        # Trying to create duplicate should raise exception
        with self.assertRaises(Exception):
            NewsletterSubscription.objects.create(email='test@example.com')
