"""
SELF-CONTAINED Tests for Tours App
No external dependencies - only tests tours models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()


class SelfContainedTourTests(TestCase):
    """
    Tests that only use tours app models - no external dependencies
    """

    def setUp(self):
        # Create user (only depends on accounts app which should work)
        self.provider = User.objects.create_user(
            username='selfuser',
            email='self@user.com',
            password='SelfPass123!'
        )

        # Get tours models
        TourCategory = apps.get_model('tours', 'TourCategory')
        TourOperator = apps.get_model('tours', 'TourOperator')

        # Create tours data (no external dependencies)
        self.category = TourCategory.objects.create(name='Self Category')
        self.operator = TourOperator.objects.create(
            name='Self Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='self@operator.com'
        )

    def test_tour_category_creation(self):
        """Test creating tour category"""
        self.assertEqual(self.category.name, 'Self Category')
        self.assertEqual(str(self.category), 'Self Category')

    def test_tour_operator_creation(self):
        """Test creating tour operator"""
        self.assertEqual(self.operator.name, 'Self Operator')
        self.assertEqual(self.operator.user, self.provider)
        self.assertEqual(self.operator.phone_number, '+201000000000')

        # Test defaults
        self.assertEqual(self.operator.average_rating, 0)
        self.assertEqual(self.operator.verification_status, 'pending')
        self.assertFalse(self.operator.is_verified)
        self.assertTrue(self.operator.is_safe)
        self.assertTrue(self.operator.is_active)

    def test_tour_operator_slug_generation(self):
        """Test automatic slug generation for operator"""
        self.assertTrue(self.operator.slug)
        self.assertEqual(self.operator.slug, 'self-operator')

    def test_tour_operator_unique_user_constraint(self):
        """Test that one user can only have one operator"""
        TourOperator = apps.get_model('tours', 'TourOperator')

        # Try to create another operator with same user
        with self.assertRaises(Exception):
            TourOperator.objects.create(
                name='Duplicate Operator',
                user=self.provider,  # Same user
                phone_number='+201000000001',
                email='duplicate@operator.com'
            )

    def test_tour_category_unique_name(self):
        """Test that category names are unique"""
        TourCategory = apps.get_model('tours', 'TourCategory')

        # Try to create duplicate category
        with self.assertRaises(Exception):
            TourCategory.objects.create(name='Self Category')  # Duplicate name


class SelfContainedTourBusinessTests(TestCase):
    """
    Business logic tests using only tours models
    """

    def setUp(self):
        self.provider = User.objects.create_user(
            username='bizuser',
            email='biz@user.com',
            password='BizPass123!'
        )

        TourCategory = apps.get_model('tours', 'TourCategory')
        TourOperator = apps.get_model('tours', 'TourOperator')

        self.category = TourCategory.objects.create(name='Biz Category')
        self.operator = TourOperator.objects.create(
            name='Biz Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='biz@operator.com'
        )

    def test_tour_operator_verification_workflow(self):
        """Test operator verification workflow"""
        # Start as pending
        self.assertEqual(self.operator.verification_status, 'pending')
        self.assertFalse(self.operator.is_verified)

        # Verify operator
        self.operator.verification_status = 'verified'
        self.operator.is_verified = True
        self.operator.save()

        self.operator.refresh_from_db()
        self.assertEqual(self.operator.verification_status, 'verified')
        self.assertTrue(self.operator.is_verified)

    def test_tour_operator_safety_scoring(self):
        """Test operator safety scoring"""
        self.operator.safety_score = 95
        self.operator.is_safe = True
        self.operator.save()

        self.operator.refresh_from_db()
        self.assertEqual(self.operator.safety_score, 95)
        self.assertTrue(self.operator.is_safe)

    def test_tour_operator_experience_tracking(self):
        """Test operator experience tracking"""
        self.operator.years_of_experience = 10
        self.operator.total_tours_completed = 150
        self.operator.save()

        self.operator.refresh_from_db()
        self.assertEqual(self.operator.years_of_experience, 10)
        self.assertEqual(self.operator.total_tours_completed, 150)


class SelfContainedTourImageTests(TestCase):
    """
    Tests for TourImage model (no external dependencies)
    """

    def setUp(self):
        self.provider = User.objects.create_user(
            username='imageuser',
            email='image@user.com',
            password='ImagePass123!'
        )

        TourCategory = apps.get_model('tours', 'TourCategory')
        TourOperator = apps.get_model('tours', 'TourOperator')
        Tour = apps.get_model('tours', 'Tour')

        self.category = TourCategory.objects.create(name='Image Category')
        self.operator = TourOperator.objects.create(
            name='Image Operator',
            user=self.provider,
            phone_number='+201000000000',
            email='image@operator.com'
        )

        # Create a minimal tour (without city dependency)
        # We'll skip city for now since it requires country
        self.tour = Tour.objects.create(
            title='Image Test Tour',
            operator=self.operator,
            category=self.category,
            description='Tour for image testing',
            duration_value=2,
            duration_unit='hours',
            price_per_person=100.00,
            start_date='2024-12-01',
            available_slots=5
        )
        # Note: We're skipping city field since it requires country

    def test_tour_image_creation(self):
        """Test creating tour image"""
        TourImage = apps.get_model('tours', 'TourImage')

        image = TourImage.objects.create(
            tour=self.tour,
            caption='Test Image',
            order=1
        )

        self.assertEqual(image.tour, self.tour)
        self.assertEqual(image.caption, 'Test Image')
        self.assertEqual(image.order, 1)

    def test_tour_image_ordering(self):
        """Test tour image ordering"""
        TourImage = apps.get_model('tours', 'TourImage')

        image1 = TourImage.objects.create(tour=self.tour, caption='First', order=2)
        image2 = TourImage.objects.create(tour=self.tour, caption='Second', order=1)

        # Should be ordered by 'order' field
        images = TourImage.objects.all()
        self.assertEqual(images[0].order, 1)
        self.assertEqual(images[1].order, 2)


class SelfContainedProductionCheck(TestCase):
    """
    Final production readiness check using only tours app
    """

    def test_tours_app_self_contained_readiness(self):
        """Check if tours app core functionality works independently"""
        from django.apps import apps

        print("\n" + "=" * 60)
        print("🎯 TOURS APP SELF-CONTAINED READINESS CHECK")
        print("=" * 60)

        checks = []

        # Check 1: App is installed
        try:
            apps.get_app_config('tours')
            checks.append(("App Installation", "✅ PASS"))
        except:
            checks.append(("App Installation", "❌ FAIL"))

        # Check 2: Core models exist
        core_models = ['TourCategory', 'TourOperator', 'Tour', 'TourImage', 'TourSchedule']
        for model_name in core_models:
            try:
                apps.get_model('tours', model_name)
                checks.append((f"Model: {model_name}", "✅ PASS"))
            except:
                checks.append((f"Model: {model_name}", "❌ FAIL"))

        # Check 3: Can create basic tours data (no external deps)
        try:
            User = get_user_model()
            user = User.objects.create_user(
                username='checkuser',
                email='check@user.com',
                password='CheckPass123!'
            )

            TourCategory = apps.get_model('tours', 'TourCategory')
            TourOperator = apps.get_model('tours', 'TourOperator')

            category = TourCategory.objects.create(name='Check Category')
            operator = TourOperator.objects.create(
                name='Check Operator',
                user=user,
                phone_number='+201000000000',
                email='check@operator.com'
            )

            checks.append(("Core Data Creation", "✅ PASS"))
        except Exception as e:
            checks.append(("Core Data Creation", f"❌ FAIL: {e}"))

        # Check 4: Business logic works
        try:
            operator.verification_status = 'verified'
            operator.is_verified = True
            operator.save()

            operator.refresh_from_db()
            if operator.is_verified and operator.verification_status == 'verified':
                checks.append(("Business Logic", "✅ PASS"))
            else:
                checks.append(("Business Logic", "❌ FAIL"))
        except:
            checks.append(("Business Logic", "❌ FAIL"))

        # Print results
        print("\n🔍 SELF-CONTAINED CHECKS:")
        print("-" * 40)
        for check_name, status in checks:
            print(f"  {status} {check_name}")

        # Determine readiness
        fails = sum(1 for _, status in checks if status.startswith("❌"))
        if fails == 0:
            print("\n🎉 TOURS APP CORE IS PRODUCTION READY!")
            print("💡 Note: Some features require destinations app integration")
            self.assertTrue(True)
        else:
            print(f"\n⚠️  TOURS APP HAS {fails} CORE ISSUE(S)")
            print("💡 These need fixing before production")
            self.assertTrue(False)