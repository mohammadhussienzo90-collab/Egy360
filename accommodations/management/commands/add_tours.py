from django.core.management.base import BaseCommand
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.hashers import make_password

from destinations.models import City
from tours.models import TourCategory, TourOperator, Tour, TourSchedule
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Add tours data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Adding tours...')

        try:
            # Step 1: Get or create a dummy user
            dummy_user = self.get_or_create_dummy_user()

            # Step 2: Get or create dummy operator
            dummy_operator = self.get_or_create_dummy_operator(dummy_user)

            # Step 3: Create tours
            self.create_tours(dummy_operator)

            self.stdout.write(self.style.SUCCESS('✅ Tours added successfully!'))
            self.stdout.write(f'Total tours: {Tour.objects.count()}')
            self.stdout.write('Visit: http://localhost:8000/tours/')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            import traceback
            traceback.print_exc()

    def get_or_create_dummy_user(self):
        """Get or create a dummy user for tour operator"""
        email = 'dummy@egy360.com'

        # Try to find existing user
        user = CustomUser.objects.filter(email=email).first()

        if user:
            self.stdout.write(f'  → Found existing dummy user')
            return user

        # Create user DIRECTLY without using manager
        self.stdout.write(f'  → Creating dummy user directly...')

        user = CustomUser()
        user.email = email
        user.first_name = 'Tour'
        user.last_name = 'Operator'
        user.password = make_password('dummy123')  # Hash the password
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()

        self.stdout.write(f'  ✓ Dummy user created')
        return user

    def get_or_create_dummy_operator(self, user):
        """Get or create dummy tour operator"""
        operator = TourOperator.objects.filter(name='Egy360 Tours').first()

        if operator:
            self.stdout.write(f'  → Found existing operator')
            return operator

        self.stdout.write(f'  → Creating tour operator...')
        operator = TourOperator.objects.create(
            name='Egy360 Tours',
            user=user,
            description='Official Egy360 tour operator',
            phone_number='+20 2 1234 5678',
            email='tours@egy360.com',
            license_number='EG-TOUR-2024-001',
            is_verified=True,
            average_rating=4.8,
            total_reviews=500,
            total_tours_completed=1000,
            is_safe=True,
            safety_score=98,
            has_insurance=True,
            years_of_experience=10,
            is_active=True
        )

        self.stdout.write(f'  ✓ Tour operator created')
        return operator

    def create_tours(self, operator):
        """Create tours with given operator"""
        self.stdout.write('Creating tour categories...')

        # Categories
        categories = {}
        for name in ['Historical & Cultural', 'Adventure & Sports', 'Beach & Diving', 'Desert Safari']:
            cat, _ = TourCategory.objects.get_or_create(
                name=name,
                defaults={'icon': '🎭', 'description': f'{name} tours'}
            )
            categories[name] = cat

        self.stdout.write(f'  ✓ {len(categories)} categories ready')

        # Get cities
        cities = {c.name: c for c in City.objects.all()}

        # Tours data
        tours_data = [
            {
                'title': 'Pyramids & Sphinx Tour',
                'city': 'Giza',
                'category': 'Historical & Cultural',
                'price': 850,
                'duration': 6,
                'description': 'Visit the iconic Pyramids of Giza and the Great Sphinx with expert Egyptologist guide.',
            },
            {
                'title': 'Egyptian Museum Tour',
                'city': 'Cairo',
                'category': 'Historical & Cultural',
                'price': 650,
                'duration': 4,
                'description': 'Explore the world\'s most extensive collection of ancient Egyptian artifacts.',
            },
            {
                'title': 'Valley of the Kings Full Day',
                'city': 'Luxor',
                'category': 'Historical & Cultural',
                'price': 1800,
                'duration': 10,
                'description': 'Full day tour exploring ancient tombs and temples of Luxor.',
            },
            {
                'title': 'Red Sea Snorkeling Adventure',
                'city': 'Hurghada',
                'category': 'Beach & Diving',
                'price': 900,
                'duration': 7,
                'description': 'Explore vibrant coral reefs and amazing marine life in the Red Sea.',
            },
            {
                'title': 'Desert Safari & Bedouin Dinner',
                'city': 'Hurghada',
                'category': 'Desert Safari',
                'price': 1100,
                'duration': 6,
                'description': 'Quad biking adventure followed by traditional Bedouin dinner under the stars.',
            },
            {
                'title': 'Nile Dinner Cruise',
                'city': 'Cairo',
                'category': 'Historical & Cultural',
                'price': 1200,
                'duration': 4,
                'description': 'Evening cruise on the Nile with buffet dinner and belly dance show.',
            },
            {
                'title': 'Hot Air Balloon Over Luxor',
                'city': 'Luxor',
                'category': 'Adventure & Sports',
                'price': 2100,
                'duration': 3,
                'description': 'Breathtaking sunrise hot air balloon ride over ancient temples.',
            },
            {
                'title': 'Alexandria Day Trip',
                'city': 'Alexandria',
                'category': 'Historical & Cultural',
                'price': 1400,
                'duration': 12,
                'description': 'Visit Alexandria\'s Mediterranean landmarks and ancient library.',
            },
        ]

        created = 0

        for data in tours_data:
            # Skip if already exists
            if Tour.objects.filter(title=data['title']).exists():
                self.stdout.write(f"  → '{data['title']}' already exists")
                continue

            tour = Tour.objects.create(
                title=data['title'],
                city=cities.get(data['city']),
                category=categories.get(data['category']),
                operator=operator,
                description=data['description'],
                itinerary=f"Detailed day-by-day itinerary for {data['title']}",
                included_items="Hotel pickup/drop-off, Expert guide, Entrance fees, Lunch, Bottled water",
                excluded_items="Personal expenses, Tips, Extra beverages",
                main_image='',  # Empty for now
                duration_value=data['duration'],
                duration_unit='hours',
                difficulty_level='easy',
                min_group_size=2,
                max_group_size=20,
                price_per_person=Decimal(str(data['price'])),
                start_date=date.today() + timedelta(days=7),
                available_slots=20,
                language='en',
                guide_name='Expert Guide',
                guide_certification='Licensed Tour Guide',
                average_rating=4.7,
                total_reviews=100,
                is_featured=True,
                safety_score=95,
            )

            # Create 3 schedules for each tour
            for i in range(3):
                TourSchedule.objects.create(
                    tour=tour,
                    start_date=date.today() + timedelta(days=7 + i * 7),
                    start_time='09:00:00',
                    available_slots=20,
                    booked_slots=0,
                    price=Decimal(str(data['price'])),
                    is_available=True
                )

            created += 1
            self.stdout.write(f"  ✓ Created '{data['title']}'")

        self.stdout.write(self.style.SUCCESS(f'\n  ✓ Created {created} tours with schedules'))