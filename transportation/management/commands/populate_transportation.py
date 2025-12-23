"""
Management command to populate Egyptian transportation services
Real services commonly available for tourists in Egypt
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from transportation.models import TransportationService, Driver


class Command(BaseCommand):
    help = 'Populate database with Egyptian transportation services'

    def handle(self, *args, **options):
        self.stdout.write('Populating transportation services...')

        # Transportation services data
        services = [
            # Airport Transfers
            {
                'name': 'Cairo Airport VIP Transfer',
                'service_type': 'airport_transfer',
                'description': 'Premium airport transfer service from Cairo International Airport (CAI) to any destination in Cairo or Giza. Meet and greet service with name board, flight tracking, and complimentary water. Professional English-speaking drivers available 24/7.',
                'vehicle_model': 'Mercedes E-Class',
                'max_passengers': 3,
                'max_luggage': 4,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 45.00,
                'average_rating': 4.8,
                'total_reviews': 342,
            },
            {
                'name': 'Luxor Airport Transfer',
                'service_type': 'airport_transfer',
                'description': 'Reliable airport transfer from Luxor International Airport to hotels in Luxor city or West Bank. Experienced drivers familiar with all hotels and attractions. Air-conditioned vehicles with bottled water included.',
                'vehicle_model': 'Toyota Hiace',
                'max_passengers': 8,
                'max_luggage': 8,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 25.00,
                'average_rating': 4.6,
                'total_reviews': 187,
            },
            {
                'name': 'Hurghada Airport Shuttle',
                'service_type': 'airport_transfer',
                'description': 'Comfortable transfer from Hurghada International Airport to Red Sea resorts. Service covers all major resort areas including El Gouna, Makadi Bay, and Sahl Hasheesh. 24-hour service with flight monitoring.',
                'vehicle_model': 'Hyundai H1',
                'max_passengers': 6,
                'max_luggage': 6,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 30.00,
                'average_rating': 4.5,
                'total_reviews': 256,
            },
            {
                'name': 'Sharm El Sheikh Airport Transfer',
                'service_type': 'airport_transfer',
                'description': 'Professional transfer service from Sharm El Sheikh International Airport to Naama Bay, Sharks Bay, and surrounding areas. Modern vehicles with professional drivers who speak English and Arabic.',
                'vehicle_model': 'Toyota Fortuner',
                'max_passengers': 5,
                'max_luggage': 5,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 35.00,
                'average_rating': 4.7,
                'total_reviews': 198,
            },
            {
                'name': 'Aswan Airport Transfer',
                'service_type': 'airport_transfer',
                'description': 'Efficient airport transfer from Aswan International Airport to hotels and Nile cruise ships. Drivers familiar with all cruise ship docking locations. Complimentary cold water and tissues provided.',
                'vehicle_model': 'Peugeot 508',
                'max_passengers': 4,
                'max_luggage': 4,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 22.00,
                'average_rating': 4.6,
                'total_reviews': 134,
            },

            # Private Cars
            {
                'name': 'Cairo Full Day Private Car',
                'service_type': 'private_car',
                'description': 'Full day private car service in Cairo with professional driver. Visit the Pyramids, Egyptian Museum, Khan El Khalili, and more at your own pace. Flexible itinerary with unlimited stops. Includes fuel and parking fees.',
                'vehicle_model': 'Mercedes V-Class',
                'max_passengers': 6,
                'max_luggage': 6,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'price_per_hour': 15.00,
                'average_rating': 4.9,
                'total_reviews': 412,
            },
            {
                'name': 'Luxor-Aswan Private Transfer',
                'service_type': 'private_car',
                'description': 'Private car service between Luxor and Aswan with optional stops at Edfu Temple, Kom Ombo Temple, and other attractions along the way. Comfortable journey through scenic Upper Egypt.',
                'vehicle_model': 'Chevrolet Captiva',
                'max_passengers': 5,
                'max_luggage': 5,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 120.00,
                'average_rating': 4.7,
                'total_reviews': 167,
            },
            {
                'name': 'Alexandria Day Trip Car',
                'service_type': 'private_car',
                'description': 'Private car service from Cairo to Alexandria for a day trip. Visit the Bibliotheca Alexandrina, Citadel of Qaitbay, Montaza Palace, and enjoy fresh seafood by the Mediterranean.',
                'vehicle_model': 'Toyota Camry',
                'max_passengers': 4,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 150.00,
                'average_rating': 4.8,
                'total_reviews': 234,
            },

            # Limousines
            {
                'name': 'Cairo Luxury Limousine',
                'service_type': 'limousine',
                'description': 'Premium limousine service for special occasions, business meetings, or luxury sightseeing in Cairo. Professional chauffeur in formal attire. Complimentary refreshments and WiFi included.',
                'vehicle_model': 'Mercedes S-Class',
                'max_passengers': 3,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_hour': 50.00,
                'average_rating': 4.9,
                'total_reviews': 89,
            },
            {
                'name': 'Wedding Limousine Service',
                'service_type': 'limousine',
                'description': 'Elegant limousine service for weddings and special events. Decorated vehicle available upon request. Red carpet service and professional photography coordination.',
                'vehicle_model': 'Lincoln Town Car Stretch',
                'max_passengers': 8,
                'max_luggage': 2,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_hour': 100.00,
                'average_rating': 4.8,
                'total_reviews': 45,
            },

            # Minivans
            {
                'name': 'Family Minivan Cairo',
                'service_type': 'minivan',
                'description': 'Spacious minivan perfect for families visiting Cairo attractions. Comfortable seating for up to 7 passengers with ample luggage space. Child seats available upon request.',
                'vehicle_model': 'Toyota Previa',
                'max_passengers': 7,
                'max_luggage': 7,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': True,
                'price_per_hour': 12.00,
                'average_rating': 4.6,
                'total_reviews': 178,
            },
            {
                'name': 'Group Minivan Luxor Tours',
                'service_type': 'minivan',
                'description': 'Comfortable minivan for group tours in Luxor. Perfect for visiting Valley of the Kings, Karnak Temple, and Luxor Temple. Air-conditioned with experienced local driver.',
                'vehicle_model': 'Hyundai Staria',
                'max_passengers': 9,
                'max_luggage': 9,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'price_per_hour': 10.00,
                'average_rating': 4.7,
                'total_reviews': 145,
            },

            # Bus Tours
            {
                'name': 'Nile Valley Bus Tour',
                'service_type': 'bus',
                'description': 'Comfortable coach bus for group tours along the Nile Valley. Modern bus with reclining seats, AC, and onboard restroom. Perfect for groups of 20+ travelers.',
                'vehicle_model': 'Mercedes Tourismo',
                'max_passengers': 45,
                'max_luggage': 45,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 500.00,
                'average_rating': 4.5,
                'total_reviews': 67,
            },
            {
                'name': 'Red Sea Resort Shuttle Bus',
                'service_type': 'bus',
                'description': 'Daily shuttle bus service between Hurghada resorts and popular attractions. Stops at Marina, downtown Hurghada, and El Gouna. Affordable and convenient for solo travelers.',
                'vehicle_model': 'King Long Coach',
                'max_passengers': 30,
                'max_luggage': 30,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 10.00,
                'average_rating': 4.3,
                'total_reviews': 234,
            },

            # Taxi Services
            {
                'name': 'Cairo White Taxi',
                'service_type': 'taxi',
                'description': 'Official metered white taxi service in Cairo. Clean, air-conditioned vehicles with licensed drivers. Transparent metered pricing. Available for short trips within Cairo.',
                'vehicle_model': 'Hyundai Accent',
                'max_passengers': 4,
                'max_luggage': 2,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_km': 0.50,
                'average_rating': 4.2,
                'total_reviews': 567,
            },
            {
                'name': 'Uber Egypt',
                'service_type': 'taxi',
                'description': 'Uber ride-hailing service available in Cairo, Alexandria, and major cities. Download the app for transparent pricing and cashless payment. Various vehicle options from economy to premium.',
                'vehicle_model': 'Various',
                'max_passengers': 4,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_km': 0.40,
                'average_rating': 4.4,
                'total_reviews': 1234,
            },
            {
                'name': 'Careem Egypt',
                'service_type': 'taxi',
                'description': 'Popular ride-hailing app in Egypt. Available in Cairo, Giza, Alexandria, and tourist areas. Multiple payment options including cash and card. Female-only driver option available.',
                'vehicle_model': 'Various',
                'max_passengers': 4,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_km': 0.45,
                'average_rating': 4.3,
                'total_reviews': 987,
            },
            {
                'name': 'Luxor Taxi Service',
                'service_type': 'taxi',
                'description': 'Reliable taxi service in Luxor for short trips to temples, train station, and Nile cruises. Negotiable fixed prices for common routes. English-speaking drivers available.',
                'vehicle_model': 'Peugeot 301',
                'max_passengers': 4,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 5.00,
                'average_rating': 4.1,
                'total_reviews': 312,
            },
        ]

        created_count = 0
        for service_data in services:
            slug = slugify(service_data['name'])
            service, created = TransportationService.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': service_data['name'],
                    'service_type': service_data['service_type'],
                    'description': service_data['description'],
                    'vehicle_model': service_data['vehicle_model'],
                    'max_passengers': service_data['max_passengers'],
                    'max_luggage': service_data['max_luggage'],
                    'has_ac': service_data['has_ac'],
                    'has_wifi': service_data['has_wifi'],
                    'has_gps': service_data['has_gps'],
                    'has_child_seat': service_data['has_child_seat'],
                    'price_per_hour': service_data.get('price_per_hour'),
                    'price_per_km': service_data.get('price_per_km'),
                    'fixed_price': service_data.get('fixed_price'),
                    'average_rating': service_data['average_rating'],
                    'total_reviews': service_data['total_reviews'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created: {service.name}')
            else:
                self.stdout.write(f'  Updated: {service.name}')

        # Create some sample drivers
        drivers = [
            {
                'name': 'Ahmed Hassan',
                'phone': '+20 100 123 4567',
                'license_number': 'CAI-2019-45678',
                'years_experience': 12,
                'languages_spoken': ['Arabic', 'English'],
                'average_rating': 4.9,
                'total_trips': 1456,
                'bio': 'Professional driver with 12 years of experience in Cairo. Expert knowledge of all tourist attractions and hidden gems.',
            },
            {
                'name': 'Mohamed Ali',
                'phone': '+20 101 234 5678',
                'license_number': 'LXR-2017-12345',
                'years_experience': 15,
                'languages_spoken': ['Arabic', 'English', 'French'],
                'average_rating': 4.8,
                'total_trips': 2134,
                'bio': 'Luxor native with extensive knowledge of Upper Egypt. Specializes in temple tours and Nile Valley excursions.',
            },
            {
                'name': 'Khaled Ibrahim',
                'phone': '+20 102 345 6789',
                'license_number': 'HRG-2020-67890',
                'years_experience': 8,
                'languages_spoken': ['Arabic', 'English', 'German'],
                'average_rating': 4.7,
                'total_trips': 876,
                'bio': 'Red Sea specialist. Airport transfers and desert safari expert. German-speaking.',
            },
            {
                'name': 'Omar Mahmoud',
                'phone': '+20 103 456 7890',
                'license_number': 'SSH-2018-34567',
                'years_experience': 10,
                'languages_spoken': ['Arabic', 'English', 'Russian'],
                'average_rating': 4.6,
                'total_trips': 1234,
                'bio': 'Sharm El Sheikh driver specializing in resort transfers and Sinai tours. Russian-speaking.',
            },
        ]

        for driver_data in drivers:
            driver, created = Driver.objects.update_or_create(
                license_number=driver_data['license_number'],
                defaults={
                    'name': driver_data['name'],
                    'phone': driver_data['phone'],
                    'years_experience': driver_data['years_experience'],
                    'languages_spoken': driver_data['languages_spoken'],
                    'average_rating': driver_data['average_rating'],
                    'total_trips': driver_data['total_trips'],
                    'bio': driver_data['bio'],
                    'is_active': True,
                    'is_verified': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} driver: {driver.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully populated {len(services)} transportation services and {len(drivers)} drivers'
        ))
