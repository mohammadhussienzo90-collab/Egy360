"""
Debug tests to identify specific issues
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class DebugTests(TestCase):
    def test_debug_user_creation(self):
        """Debug: Can we create users?"""
        try:
            user = User.objects.create_user('debug@test.com', 'testpass')
            print("✓ User creation works")
            self.assertTrue(True)
        except Exception as e:
            print(f"✗ User creation failed: {e}")
            self.fail(f"User creation failed: {e}")

    def test_debug_content_type(self):
        """Debug: Can we get content types?"""
        try:
            ct = ContentType.objects.first()
            print(f"✓ ContentType works: {ct}")
            self.assertTrue(True)
        except Exception as e:
            print(f"✗ ContentType failed: {e}")
            self.fail(f"ContentType failed: {e}")

    def test_debug_import_models(self):
        """Debug: Can we import review models?"""
        try:
            from .models import ReviewRating
            print("✓ Review models import works")
            self.assertTrue(True)
        except Exception as e:
            print(f"✗ Model import failed: {e}")
            self.fail(f"Model import failed: {e}")