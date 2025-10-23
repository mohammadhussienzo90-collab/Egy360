# FILE: accounts/tests.py
# ============================================================
"""
Tests for Accounts App

These tests cover:
- User registration with validation
- User login with JWT tokens
- Profile viewing and updating
- Password changes
- Profile picture uploads
- Provider information endpoints
- Permission and authentication
"""

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Tests for CustomUser model
    """

    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'tourist',
            'phone_number': '+201001234567',
        }

    def test_create_user(self):
        """Test creating a regular user"""
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'tourist')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!'
        )

        self.assertEqual(superuser.username, 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_type_methods(self):
        """Test user type helper methods"""
        tourist = CustomUser.objects.create_user(
            username='tourist',
            email='tourist@example.com',
            password='pass123',
            user_type='tourist'
        )

        provider = CustomUser.objects.create_user(
            username='provider',
            email='provider@example.com',
            password='pass123',
            user_type='provider'
        )

        self.assertTrue(tourist.is_tourist())
        self.assertFalse(tourist.is_provider())
        self.assertTrue(provider.is_provider())
        self.assertFalse(provider.is_tourist())

    def test_get_full_name(self):
        """Test get_full_name method"""
        user = CustomUser.objects.create_user(
            username='fullnameuser',
            email='fullname@example.com',
            password='pass123',
            first_name='John',
            last_name='Doe'
        )

        self.assertEqual(user.get_full_name(), 'John Doe')
        self.assertEqual(str(user), 'John Doe (Tourist)')

    def test_user_verification_fields(self):
        """Test verification fields default values"""
        user = CustomUser.objects.create_user(
            username='verifyuser',
            email='verify@example.com',
            password='pass123'
        )

        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_phone_verified)
        self.assertFalse(user.is_identity_verified)
        self.assertFalse(user.is_licensed)


class UserRegistrationTest(APITestCase):
    """
    Tests for user registration endpoint
    """

    def setUp(self):
        """Set up test client and URLs"""
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'user_type': 'tourist',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+201001234567',
        }

    def test_successful_registration(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['message'], 'Registration successful!')

        # Check user was created
        user = CustomUser.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.user_type, 'tourist')

    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'DifferentPass123!'

        response = self.client.post(self.register_url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create first user
        self.client.post(self.register_url, self.valid_data)

        # Try to create another user with same username
        duplicate_data = self.valid_data.copy()
        duplicate_data['email'] = 'different@example.com'

        response = self.client.post(self.register_url, duplicate_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create first user
        self.client.post(self.register_url, self.valid_data)

        # Try to create another user with same email
        duplicate_data = self.valid_data.copy()
        duplicate_data['username'] = 'differentuser'

        response = self.client.post(self.register_url, duplicate_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_missing_required_fields(self):
        """Test registration with missing required fields"""
        incomplete_data = {
            'username': 'incomplete',
            'password': 'pass123',
            'password2': 'pass123',
        }

        response = self.client.post(self.register_url, incomplete_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserLoginTest(APITestCase):
    """
    Tests for user login endpoint
    """

    def setUp(self):
        """Set up test user and URLs"""
        self.client = APIClient()
        self.login_url = reverse('user-login')

        # Create test user
        self.user = CustomUser.objects.create_user(
            username='testlogin',
            email='login@example.com',
            password='LoginPass123!',
            user_type='tourist'
        )

    def test_successful_login(self):
        """Test successful user login"""
        login_data = {
            'username': 'testlogin',
            'password': 'LoginPass123!'
        }

        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['message'], 'Login successful!')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_data = {
            'username': 'testlogin',
            'password': 'WrongPassword123!'
        }

        response = self.client.post(self.login_url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        invalid_data = {
            'username': 'nonexistent',
            'password': 'SomePass123!'
        }

        response = self.client.post(self.login_url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


class UserProfileTest(APITestCase):
    """
    Tests for user profile endpoints
    """

    def setUp(self):
        """Set up authenticated user"""
        self.client = APIClient()
        self.me_url = reverse('user-me')
        self.update_profile_url = reverse('user-update-profile')

        # Create and authenticate user
        self.user = CustomUser.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='ProfilePass123!',
            first_name='Profile',
            last_name='User',
            user_type='tourist'
        )

        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_profile_authenticated(self):
        """Test getting profile when authenticated"""
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')
        self.assertEqual(response.data['email'], 'profile@example.com')
        self.assertEqual(response.data['first_name'], 'Profile')
        self.assertEqual(response.data['last_name'], 'User')

    def test_get_profile_unauthenticated(self):
        """Test getting profile when not authenticated"""
        client = APIClient()  # No authentication
        response = client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Test updating user profile"""
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': '+201009876543',
            'bio': 'Updated bio text',
            'language_preference': 'ar'
        }

        response = self.client.put(self.update_profile_url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully!')

        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.phone_number, '+201009876543')
        self.assertEqual(self.user.bio, 'Updated bio text')
        self.assertEqual(self.user.language_preference, 'ar')

    def test_partial_update_profile(self):
        """Test partially updating user profile"""
        update_data = {
            'bio': 'New bio text only',
        }

        response = self.client.put(self.update_profile_url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'New bio text only')
        # Other fields should remain unchanged
        self.assertEqual(self.user.first_name, 'Profile')


class PasswordChangeTest(APITestCase):
    """
    Tests for password change endpoint
    """

    def setUp(self):
        """Set up authenticated user"""
        self.client = APIClient()
        self.password_change_url = reverse('user-password-change')

        # Create and authenticate user
        self.user = CustomUser.objects.create_user(
            username='passuser',
            email='pass@example.com',
            password='OldPass123!'
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_successful_password_change(self):
        """Test successful password change"""
        change_data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }

        response = self.client.post(self.password_change_url, change_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password changed successfully!')

        # Verify new password works
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))

    def test_password_change_wrong_old_password(self):
        """Test password change with wrong old password"""
        change_data = {
            'old_password': 'WrongOldPass!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }

        response = self.client.post(self.password_change_url, change_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)

    def test_password_change_mismatched_new_passwords(self):
        """Test password change with mismatched new passwords"""
        change_data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'DifferentPass789!'
        }

        response = self.client.post(self.password_change_url, change_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)


class ProfilePictureTest(APITestCase):
    """
    Tests for profile picture upload
    """

    def setUp(self):
        """Set up authenticated user"""
        self.client = APIClient()
        self.upload_picture_url = reverse('user-upload-profile-picture')

        # Create and authenticate user
        self.user = CustomUser.objects.create_user(
            username='picuser',
            email='pic@example.com',
            password='PicPass123!'
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_upload_profile_picture(self):
        """Test uploading a profile picture"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",  # Simple binary content
            content_type="image/jpeg"
        )

        response = self.client.post(
            self.upload_picture_url,
            {'profile_picture': image},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile_picture', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Profile picture uploaded!')


class ProviderInfoTest(APITestCase):
    """
    Tests for provider information endpoint
    """

    def setUp(self):
        """Set up test users"""
        self.client = APIClient()
        self.provider_info_url = reverse('user-provider-info')

        # Create a provider user
        self.provider = CustomUser.objects.create_user(
            username='hotelprovider',
            email='hotel@example.com',
            password='ProviderPass123!',
            user_type='provider',
            first_name='Cairo',
            last_name='Hotels',
            business_name='Cairo Luxury Hotels',
            is_verified=True,
            is_licensed=True
        )

        # Create a tourist user (should not be accessible via provider_info)
        self.tourist = CustomUser.objects.create_user(
            username='touristuser',
            email='tourist@example.com',
            password='TouristPass123!',
            user_type='tourist'
        )

    def test_get_provider_info(self):
        """Test getting provider information"""
        response = self.client.get(
            self.provider_info_url,
            {'user_id': self.provider.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'hotelprovider')
        self.assertEqual(response.data['business_name'], 'Cairo Luxury Hotels')
        self.assertTrue(response.data['is_verified'])
        self.assertTrue(response.data['is_licensed'])

    def test_get_provider_info_nonexistent(self):
        """Test getting info for non-existent provider"""
        response = self.client.get(
            self.provider_info_url,
            {'user_id': 9999}  # Non-existent ID
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_provider_info_tourist(self):
        """Test getting info for tourist (should fail)"""
        response = self.client.get(
            self.provider_info_url,
            {'user_id': self.tourist.id}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_provider_info_missing_user_id(self):
        """Test getting provider info without user_id parameter"""
        response = self.client.get(self.provider_info_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class UserListViewTest(APITestCase):
    """
    Tests for user list view
    """

    def setUp(self):
        """Set up test users"""
        self.client = APIClient()
        self.user_list_url = reverse('user-list')

        # Create multiple users
        self.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123',
            user_type='tourist'
        )

        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123',
            user_type='provider'
        )

    def test_user_list_unauthenticated(self):
        """Test user list without authentication (should work - read only)"""
        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Paginated response

    def test_user_list_authenticated(self):
        """Test user list with authentication"""
        # Authenticate as one user
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class UserDeleteTest(APITestCase):
    """
    Tests for user deletion
    """

    def setUp(self):
        """Set up test users"""
        self.client = APIClient()

        # Create users
        self.user1 = CustomUser.objects.create_user(
            username='deleteuser1',
            email='delete1@example.com',
            password='pass123'
        )

        self.user2 = CustomUser.objects.create_user(
            username='deleteuser2',
            email='delete2@example.com',
            password='pass123'
        )

        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

    def test_user_delete_own_account(self):
        """Test user deleting their own account"""
        # Authenticate as user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        user_detail_url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.delete(user_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify user was deleted
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=self.user1.id)

    def test_user_delete_other_account(self):
        """Test user trying to delete another user's account"""
        # Authenticate as user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Try to delete user2's account
        user_detail_url = reverse('user-detail', kwargs={'pk': self.user2.id})
        response = self.client.delete(user_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_admin_delete_any_account(self):
        """Test admin deleting any user account"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Delete user1's account
        user_detail_url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.delete(user_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify user was deleted
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=self.user1.id)