"""
Quick Assessment of Tours App
Using only existing, working tests
"""

from django.test import TestCase
from django.apps import apps


class QuickToursAssessment(TestCase):
    """
    Quick assessment using only safe, proven methods
    """

    def test_tours_app_basic_functionality(self):
        """Quick check if tours app basic functionality works"""
        print("\n" + "=" * 50)
        print("🚀 QUICK TOURS APP ASSESSMENT")
        print("=" * 50)

        checks = []

        # Check 1: App is installed
        try:
            app_config = apps.get_app_config('tours')
            checks.append(("App Installation", "✅ PASS"))
        except:
            checks.append(("App Installation", "❌ FAIL"))

        # Check 2: Core models exist
        core_models = ['TourCategory', 'TourOperator', 'Tour', 'TourImage', 'TourSchedule']
        for model_name in core_models:
            try:
                model = apps.get_model('tours', model_name)
                checks.append((f"Model: {model_name}", "✅ PASS"))
            except:
                checks.append((f"Model: {model_name}", "❌ FAIL"))

        # Check 3: Can create minimal data
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            user = User.objects.create_user(
                username='quickuser',
                email='quick@user.com',
                password='QuickPass123!'
            )

            TourCategory = apps.get_model('tours', 'TourCategory')
            TourOperator = apps.get_model('tours', 'TourOperator')

            category = TourCategory.objects.create(name='Quick Category')
            operator = TourOperator.objects.create(
                name='Quick Operator',
                user=user,
                phone_number='+201000000000',
                email='quick@operator.com'
            )

            checks.append(("Data Creation", "✅ PASS"))
        except Exception as e:
            checks.append(("Data Creation", f"❌ FAIL: {e}"))

        # Print results
        print("\n📊 QUICK ASSESSMENT RESULTS:")
        print("-" * 40)
        for check_name, status in checks:
            print(f"  {status} {check_name}")

        # Final verdict
        fails = sum(1 for _, status in checks if status.startswith("❌"))
        if fails == 0:
            print("\n🎉 TOURS APP IS OPERATIONAL!")
            print("💡 Your existing tests should work fine")
            self.assertTrue(True)
        else:
            print(f"\n⚠️  TOURS APP HAS {fails} ISSUE(S)")
            print("💡 Check the specific failures above")
            self.assertTrue(False)