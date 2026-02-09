"""
Views for the Home app - Main pages of Egy360
Handles homepage, about, contact, and error pages
"""
import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
import json

logger = logging.getLogger(__name__)


def health_check(request):
    """Simple health check endpoint for Railway"""
    return JsonResponse({'status': 'ok', 'service': 'egy360'})


# Import models from other apps as needed
from accommodations.models import Accommodation
from tours.models import Tour
from destinations.models import City
from .models import NewsletterSubscription, ContactMessage, FAQItem


def home(request):
    """
    Main homepage view
    Displays featured content and search forms
    Auto-seeds content if database is empty (Railway ephemeral storage fix)
    """
    import sys

    # Auto-seed ALL content if database is empty (Railway ephemeral storage fix)
    try:
        needs_seed = (
            Accommodation.objects.count() == 0 or
            Tour.objects.count() == 0 or
            City.objects.count() == 0
        )
        if needs_seed:
            print("AUTO-SEED HOMEPAGE: Database empty, seeding all content...", file=sys.stderr)
            _auto_seed_all_content()
            print("AUTO-SEED HOMEPAGE: Completed seeding all content", file=sys.stderr)
    except Exception as e:
        print(f"AUTO-SEED HOMEPAGE ERROR: {str(e)}", file=sys.stderr)

    # Gracefully handle database errors (e.g., during initial deployment)
    try:
        featured_accommodations = list(Accommodation.objects.filter(
            is_featured=True,
            is_active=True
        )[:6])
    except Exception as e:
        logger.warning(f"Could not load accommodations: {e}")
        featured_accommodations = []

    try:
        featured_tours = list(Tour.objects.filter(
            is_featured=True,
            is_active=True
        )[:6])
    except Exception as e:
        logger.warning(f"Could not load tours: {e}")
        featured_tours = []

    try:
        popular_destinations = list(City.objects.filter(
            is_popular=True
        )[:8])
    except Exception as e:
        logger.warning(f"Could not load destinations: {e}")
        popular_destinations = []

    context = {
        'featured_accommodations': featured_accommodations,
        'featured_tours': featured_tours,
        'popular_destinations': popular_destinations,
        'page_title': 'Egy360 - Discover Egypt Safely',
        'meta_description': 'Egypt\'s premier tourism platform. Find verified accommodations, tours, and transportation at the best prices.',
    }

    # Handle search form if submitted via GET
    if request.GET.get('search_type'):
        search_type = request.GET.get('search_type')
        if search_type == 'accommodations':
            return redirect('accommodations:accommodation-search', query_params=request.GET.urlencode())
        elif search_type == 'tours':
            return redirect('tours:tour-list', query_params=request.GET.urlencode())
        elif search_type == 'transportation':
            return redirect('transportation:transport-search', query_params=request.GET.urlencode())

    return render(request, 'home.html', context)


def _auto_seed_all_content():
    """
    Auto-seed tours, hotels, and destinations when database is empty.
    Called from homepage to ensure content exists for Railway ephemeral storage.
    """
    from destinations.models import Country, City, Attraction

    # ============ SEED DESTINATIONS ============
    egypt, _ = Country.objects.get_or_create(
        code='EGY',
        defaults={
            'name': 'Egypt',
            'description': 'The land of pharaohs, pyramids, and ancient wonders.',
            'flag_emoji': '🇪🇬'
        }
    )

    cities_data = [
        {
            'name': 'Cairo', 'slug': 'cairo',
            'description': 'Cairo, the capital of Egypt, is a sprawling metropolis where ancient history meets modern life. Home to the iconic Pyramids of Giza and the Sphinx.',
            'population': 21000000, 'is_popular': True, 'is_capital': True, 'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Pyramids of Giza', 'slug': 'pyramids-of-giza', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True, 'description': 'The last surviving Wonder of the Ancient World.', 'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800'},
                {'name': 'Egyptian Museum', 'slug': 'egyptian-museum', 'type': 'museum', 'is_must_see': True, 'description': "Home to the world's largest collection of ancient Egyptian artifacts.", 'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800'},
                {'name': 'Khan El-Khalili Bazaar', 'slug': 'khan-el-khalili', 'type': 'market', 'is_must_see': True, 'description': "Cairo's famous 14th-century bazaar.", 'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800'},
            ]
        },
        {
            'name': 'Luxor', 'slug': 'luxor',
            'description': "Luxor is the world's greatest open-air museum. Once ancient Thebes, capital of the pharaohs, Luxor houses the Valley of the Kings and Karnak Temple.",
            'population': 500000, 'is_popular': True, 'has_airport': True,
            'best_time_to_visit': 'October to March',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'attractions': [
                {'name': 'Valley of the Kings', 'slug': 'valley-of-kings', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True, 'description': "The royal burial ground of Egypt's pharaohs.", 'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800'},
                {'name': 'Karnak Temple', 'slug': 'karnak-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True, 'description': 'The largest ancient religious complex in the world.', 'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800'},
            ]
        },
        {
            'name': 'Aswan', 'slug': 'aswan',
            'description': "Aswan is Egypt's sunniest southern city, known for beautiful Nile scenery, Nubian culture, and gateway to Abu Simbel.",
            'population': 300000, 'is_popular': True, 'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200',
            'attractions': [
                {'name': 'Abu Simbel Temples', 'slug': 'abu-simbel', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True, 'description': "Ramesses II's magnificent rock-cut temples.", 'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=800'},
                {'name': 'Philae Temple', 'slug': 'philae-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True, 'description': 'Beautiful island temple dedicated to goddess Isis.', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
            ]
        },
        {
            'name': 'Hurghada', 'slug': 'hurghada',
            'description': "Hurghada is Egypt's premier Red Sea resort destination. World-class diving, beautiful beaches, and year-round sunshine.",
            'population': 250000, 'is_popular': True, 'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
            'attractions': [
                {'name': 'Giftun Islands', 'slug': 'giftun-islands', 'type': 'natural', 'is_must_see': True, 'description': 'Protected marine park with pristine beaches.', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
            ]
        },
        {
            'name': 'Sharm El Sheikh', 'slug': 'sharm-el-sheikh',
            'description': 'Sharm El Sheikh sits at the tip of the Sinai Peninsula, offering world-famous diving at Ras Mohammed National Park.',
            'population': 100000, 'is_popular': True, 'has_airport': True,
            'best_time_to_visit': 'Year-round, best March to May',
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
            'attractions': [
                {'name': 'Ras Mohammed National Park', 'slug': 'ras-mohammed', 'type': 'natural', 'is_must_see': True, 'description': 'World-renowned marine park with spectacular diving.', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
            ]
        },
        {
            'name': 'Alexandria', 'slug': 'alexandria',
            'description': "Alexandria, Egypt's Mediterranean jewel, was founded by Alexander the Great. Known for the legendary ancient library.",
            'population': 5000000, 'is_popular': True, 'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Bibliotheca Alexandrina', 'slug': 'bibliotheca-alexandrina', 'type': 'modern', 'is_must_see': True, 'description': 'Modern tribute to the ancient Library of Alexandria.', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
            ]
        },
    ]

    for city_data in cities_data:
        attractions_data = city_data.pop('attractions', [])
        city, _ = City.objects.update_or_create(
            slug=city_data['slug'],
            defaults={**city_data, 'country': egypt}
        )
        # Create attractions for this city
        for attr in attractions_data:
            Attraction.objects.update_or_create(
                slug=attr['slug'],
                defaults={
                    'city': city,
                    'name': attr['name'],
                    'attraction_type': attr['type'],
                    'description': attr['description'],
                    'address': f"{attr['name']}, {city.name}, Egypt",
                    'is_unesco': attr.get('is_unesco', False),
                    'is_must_see': attr.get('is_must_see', False),
                    'image_url': attr.get('image_url', ''),
                    'average_rating': 4.5,
                    'total_reviews': 150,
                }
            )

    # ============ SEED HOTELS ============
    hotels_data = [
        {'name': 'Marriott Mena House Cairo', 'slug': 'marriott-mena-house-cairo', 'accommodation_type': 'hotel', 'city': 'Cairo', 'address': '6 Pyramids Road, Giza', 'star_rating': 5, 'price_per_night': 250, 'description': 'Historic luxury hotel with direct views of the Pyramids of Giza.', 'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200', 'is_featured': True, 'average_rating': 4.8, 'total_reviews': 2500},
        {'name': 'Four Seasons Cairo at Nile Plaza', 'slug': 'four-seasons-nile-plaza', 'accommodation_type': 'hotel', 'city': 'Cairo', 'address': '1089 Corniche El Nil', 'star_rating': 5, 'price_per_night': 350, 'description': 'Elegant luxury hotel on the banks of the Nile with stunning river views.', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200', 'is_featured': True, 'average_rating': 4.9, 'total_reviews': 1800},
        {'name': 'Steigenberger Nile Palace Luxor', 'slug': 'steigenberger-nile-palace-luxor', 'accommodation_type': 'hotel', 'city': 'Luxor', 'address': 'Khaled Ibn El Walid Street', 'star_rating': 5, 'price_per_night': 180, 'description': 'Beautiful hotel on the East Bank of Luxor with panoramic Nile views.', 'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200', 'is_featured': True, 'average_rating': 4.6, 'total_reviews': 1200},
        {'name': 'Sofitel Legend Old Cataract Aswan', 'slug': 'sofitel-old-cataract-aswan', 'accommodation_type': 'hotel', 'city': 'Aswan', 'address': 'Abtal El Tahrir Street', 'star_rating': 5, 'price_per_night': 320, 'description': 'Legendary palace hotel perched above the Nile with breathtaking views.', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200', 'is_featured': True, 'average_rating': 4.8, 'total_reviews': 800},
        {'name': 'Oberoi Sahl Hasheesh', 'slug': 'oberoi-sahl-hasheesh', 'accommodation_type': 'resort', 'city': 'Hurghada', 'address': 'Sahl Hasheesh Bay', 'star_rating': 5, 'price_per_night': 400, 'description': 'Ultra-luxury beachfront resort with stunning Moorish architecture.', 'image_url': 'https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1200', 'is_featured': True, 'average_rating': 4.9, 'total_reviews': 600},
        {'name': 'Rixos Premium Sharm El Sheikh', 'slug': 'rixos-premium-sharm', 'accommodation_type': 'resort', 'city': 'Sharm El Sheikh', 'address': 'Nabq Bay', 'star_rating': 5, 'price_per_night': 220, 'description': 'Ultra all-inclusive luxury resort with private beach and aqua park.', 'image_url': 'https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1200', 'is_featured': True, 'average_rating': 4.7, 'total_reviews': 2200},
    ]

    for hotel_data in hotels_data:
        Accommodation.objects.update_or_create(
            slug=hotel_data['slug'],
            defaults={**hotel_data, 'is_active': True, 'is_verified': True, 'total_rooms': 200}
        )

    # ============ SEED TOURS ============
    tours_data = [
        {'name': 'Pyramids of Giza & Sphinx Day Tour', 'slug': 'pyramids-giza-sphinx-day-tour', 'tour_type': 'cultural', 'description': 'Experience the wonder of the ancient world! Visit the Great Pyramids of Giza, marvel at the Sphinx, and explore the Solar Boat Museum.', 'highlights': 'Great Pyramid of Khufu|Pyramid of Khafre|The Great Sphinx|Solar Boat Museum', 'duration_days': 1, 'departure_city': 'Cairo', 'destinations': ['Giza', 'Pyramids'], 'price_per_person': 75, 'difficulty_level': 'easy', 'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200', 'is_featured': True, 'average_rating': 4.8, 'total_reviews': 3500},
        {'name': 'Luxor Full Day Tour from Cairo by Flight', 'slug': 'luxor-day-tour-from-cairo-flight', 'tour_type': 'cultural', 'description': 'Fly to Luxor for an unforgettable day exploring ancient Thebes. Visit Valley of the Kings, Karnak Temple, and more.', 'highlights': 'Valley of the Kings|Temple of Hatshepsut|Karnak Temple|Luxor Temple', 'duration_days': 1, 'departure_city': 'Cairo', 'destinations': ['Luxor'], 'price_per_person': 350, 'difficulty_level': 'moderate', 'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200', 'is_featured': True, 'average_rating': 4.7, 'total_reviews': 1200},
        {'name': '4-Day Nile Cruise: Luxor to Aswan', 'slug': 'nile-cruise-luxor-aswan-4-days', 'tour_type': 'cruise', 'description': 'Sail the legendary Nile aboard a 5-star cruise ship. Visit ancient temples, enjoy onboard entertainment.', 'highlights': 'Luxor Temple|Karnak Temple|Valley of the Kings|Edfu Temple|Kom Ombo|Philae Temple', 'duration_days': 4, 'departure_city': 'Luxor', 'destinations': ['Luxor', 'Edfu', 'Aswan'], 'price_per_person': 450, 'difficulty_level': 'easy', 'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200', 'is_featured': True, 'average_rating': 4.9, 'total_reviews': 800},
        {'name': 'White Desert Overnight Camping Safari', 'slug': 'white-desert-camping-safari', 'tour_type': 'desert', 'description': 'Adventure into Egypt\'s surreal White Desert. Camp under the stars and experience authentic Bedouin hospitality.', 'highlights': 'White Desert National Park|Crystal Mountain|Black Desert|Stargazing', 'duration_days': 2, 'departure_city': 'Cairo', 'destinations': ['Bahariya Oasis', 'White Desert'], 'price_per_person': 180, 'difficulty_level': 'moderate', 'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200', 'is_featured': True, 'average_rating': 4.8, 'total_reviews': 650},
        {'name': 'Red Sea Diving Day Trip - Hurghada', 'slug': 'red-sea-diving-hurghada', 'tour_type': 'diving', 'description': 'Discover the underwater wonders of the Red Sea. Two dives at spectacular coral reef sites.', 'highlights': 'Two dive sites|Coral reefs|Marine life|Professional PADI instructors', 'duration_days': 1, 'departure_city': 'Hurghada', 'destinations': ['Red Sea', 'Giftun Islands'], 'price_per_person': 75, 'difficulty_level': 'moderate', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200', 'is_featured': True, 'average_rating': 4.7, 'total_reviews': 1500},
        {'name': 'Abu Simbel Day Tour from Aswan', 'slug': 'abu-simbel-day-tour-aswan', 'tour_type': 'cultural', 'description': 'Visit the magnificent temples of Abu Simbel, Ramesses II\'s greatest monument.', 'highlights': 'Great Temple of Ramesses II|Temple of Nefertari|UNESCO World Heritage Site', 'duration_days': 1, 'departure_city': 'Aswan', 'destinations': ['Abu Simbel'], 'price_per_person': 95, 'difficulty_level': 'easy', 'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200', 'is_featured': True, 'average_rating': 4.9, 'total_reviews': 950},
    ]

    for tour_data in tours_data:
        Tour.objects.update_or_create(
            slug=tour_data['slug'],
            defaults={**tour_data, 'is_active': True, 'min_group_size': 1, 'max_group_size': 15, 'child_discount': 25}
        )


def about(request):
    """About page view"""
    context = {
        'page_title': 'About Egy360 - Your Trusted Egypt Travel Partner',
        'meta_description': 'Learn about Egy360, Egypt\'s leading tourism platform dedicated to providing safe, verified, and affordable travel experiences.',
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', 'General Inquiry').strip()
        message_text = request.POST.get('message', '').strip()

        # Validate form data
        if not all([name, email, message_text]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html', {'form_data': request.POST})

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'contact.html', {'form_data': request.POST})

        # Save message to database (always works, doesn't depend on email config)
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text,
        )

        # Try to send email notification (optional, fails silently)
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@360egy.com')
            send_mail(
                f'Egy360 Contact: {subject}',
                f"New contact from {name} ({email}):\n\n{message_text}",
                from_email,
                ['info@360egy.com'],
                fail_silently=True,  # Don't fail if email doesn't work
            )
        except Exception as e:
            logger.warning(f"Failed to send contact notification email: {e}")

        messages.success(request, 'Thank you for contacting us! We\'ll respond within 24 hours.')
        return redirect('home:contact')

    context = {
        'page_title': 'Contact Egy360 - Get in Touch',
        'meta_description': 'Contact Egy360 for any questions about Egypt travel, bookings, or partnerships.',
    }
    return render(request, 'contact.html', context)


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'privacy.html', {
        'page_title': 'Privacy Policy - Egy360',
    })


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'terms.html', {
        'page_title': 'Terms of Service - Egy360',
    })


def affiliate_disclosure(request):
    """Affiliate disclosure page - required for affiliate program compliance"""
    return render(request, 'affiliate-disclosure.html', {
        'page_title': 'Affiliate Disclosure - Egy360',
        'meta_description': 'Egy360 affiliate disclosure - transparency about our partnerships with travel booking platforms.',
    })


def cookie_policy(request):
    """Cookie policy page - required for GDPR and affiliate program compliance"""
    return render(request, 'cookie-policy.html', {
        'page_title': 'Cookie Policy - Egy360',
        'meta_description': 'Learn how Egy360 uses cookies and tracking technologies.',
    })


def faq(request):
    """FAQ page with database-driven content"""
    # Get FAQs from database, grouped by category
    faqs = FAQItem.objects.filter(is_active=True)

    # Group FAQs by category
    faq_categories = {}
    for faq_item in faqs:
        category = faq_item.get_category_display()
        if category not in faq_categories:
            faq_categories[category] = []
        faq_categories[category].append(faq_item)

    return render(request, 'faq.html', {
        'page_title': 'Frequently Asked Questions - Egy360',
        'faq_categories': faq_categories,
        'faqs': faqs,  # Also pass flat list for backwards compatibility
    })


# Error handlers
def flights(request):
    """Flights page with Travelpayouts search widget"""
    context = {
        'page_title': 'Flights to Egypt - Find Cheap Airfare | Egy360',
        'meta_description': 'Compare flight prices from 100+ airlines to Egypt. Find cheap flights to Cairo, Luxor, Hurghada, Sharm El Sheikh and more.',
    }
    return render(request, 'flights.html', context)


def hotels_search(request):
    """Hotels comparison page with Travelpayouts Hotellook widget"""
    context = {
        'page_title': 'Compare Hotel Prices in Egypt - Best Rates | Egy360',
        'meta_description': 'Compare hotel prices from 70+ booking sites. Find the best rates for hotels in Cairo, Luxor, Hurghada, Sharm El Sheikh and more.',
    }
    return render(request, 'hotels-search.html', context)


def insurance(request):
    """Travel insurance page with affiliate links"""
    context = {
        'page_title': 'Travel Insurance for Egypt - Protect Your Trip | Egy360',
        'meta_description': 'Get comprehensive travel insurance for your Egypt trip. Coverage for medical emergencies, trip cancellation, lost luggage, and adventure activities.',
    }
    return render(request, 'insurance.html', context)


def deals(request):
    """Deals and discounts page"""
    context = {
        'page_title': 'Egypt Travel Deals & Discounts | Egy360',
        'meta_description': 'Find the best deals on Egypt hotels, tours, and flights. Exclusive discounts and promo codes for your Egyptian adventure.',
    }
    return render(request, 'deals.html', context)


def social_links(request):
    """Social media link-in-bio page for Instagram and Facebook"""
    # Define all the links with UTM tracking
    links = [
        {
            'title': 'Best Pyramids Tours',
            'description': 'Top-rated guided tours of the Pyramids of Giza',
            'url': '/tours/?destination=cairo&utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-landmark',
            'color': '#c41e3a',
        },
        {
            'title': 'Top Cairo Hotels',
            'description': 'Best hotels near the Pyramids & downtown Cairo',
            'url': '/accommodations/?city=cairo&utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-hotel',
            'color': '#2563eb',
        },
        {
            'title': 'Red Sea Beach Resorts',
            'description': 'Hurghada & Sharm El Sheikh resorts',
            'url': '/accommodations/?city=hurghada&utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-umbrella-beach',
            'color': '#0891b2',
        },
        {
            'title': 'Book Flights to Egypt',
            'description': 'Compare prices from 100+ airlines',
            'url': '/flights/?utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-plane',
            'color': '#7c3aed',
        },
        {
            'title': 'Travel Guides & Tips',
            'description': 'Everything you need to know about Egypt',
            'url': '/blog/?utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-book-open',
            'color': '#059669',
        },
        {
            'title': 'Nile Cruise Packages',
            'description': 'Luxor to Aswan cruise experiences',
            'url': '/tours/?type=cruise&utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-ship',
            'color': '#dc2626',
        },
        {
            'title': 'Travel Insurance',
            'description': 'Protect your Egypt trip',
            'url': '/insurance/?utm_source=social&utm_medium=bio&utm_campaign=link_in_bio',
            'icon': 'fa-shield-halved',
            'color': '#ca8a04',
        },
    ]

    context = {
        'page_title': 'Egy360 Links - Your Egypt Travel Guide',
        'meta_description': 'All links from Egy360 - Best Egypt tours, hotels, flights, and travel guides in one place.',
        'links': links,
    }
    return render(request, 'social_links.html', context)


def error_404(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)


def error_403(request, exception):
    """Custom 403 error page"""
    return render(request, '403.html', status=403)


# API endpoint for newsletter subscription
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()

        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address'}, status=400)

        # Check if already subscribed
        existing = NewsletterSubscription.objects.filter(email=email).first()
        if existing:
            if existing.is_active:
                return JsonResponse({
                    'success': True,
                    'message': 'You are already subscribed to our newsletter!'
                })
            else:
                # Reactivate subscription
                existing.is_active = True
                existing.unsubscribed_at = None
                existing.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Welcome back! Your subscription has been reactivated.'
                })

        # Create new subscription
        subscription = NewsletterSubscription.objects.create(email=email, name=name)

        # Sync to Mailchimp for email marketing campaigns
        try:
            from core.mailchimp_integration import sync_subscriber_to_mailchimp
            sync_subscriber_to_mailchimp(email, name)
        except Exception as e:
            logger.warning(f"Failed to sync subscriber to Mailchimp {email}: {e}")

        # Send welcome email
        try:
            from core.email import send_newsletter_welcome
            send_newsletter_welcome(subscription)
        except Exception as e:
            logger.warning(f"Failed to send newsletter welcome email to {email}: {e}")

        return JsonResponse({
            'success': True,
            'message': 'Successfully subscribed to newsletter!'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)


# Lead magnet landing page
def lead_magnet_page(request):
    """Display lead magnet landing page for email capture"""
    return render(request, 'lead-magnet.html')


# Lead magnet download API endpoint
@require_http_methods(["POST"])
def lead_magnet_download(request):
    """
    Handle lead magnet download requests.

    Captures email, syncs to Mailchimp with 'lead-magnet' tag,
    and sends the PDF guide via email.
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        lead_magnet = data.get('lead_magnet', 'egypt-travel-guide')

        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address'}, status=400)

        # Create or get newsletter subscription
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'name': name, 'is_active': True}
        )

        if not created and not subscription.is_active:
            subscription.is_active = True
            subscription.name = name or subscription.name
            subscription.save()

        # Sync to Mailchimp with lead-magnet tag
        try:
            from core.mailchimp_integration import mailchimp_client
            if mailchimp_client.is_configured():
                parts = name.split(' ', 1) if name else ['', '']
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''

                mailchimp_client.add_subscriber(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    tags=['lead-magnet', lead_magnet, 'egypt-travel']
                )
        except Exception as e:
            logger.warning(f"Failed to sync lead magnet subscriber to Mailchimp {email}: {e}")

        # Send lead magnet email with download link
        try:
            from core.email import send_lead_magnet_email
            send_lead_magnet_email(email, name, lead_magnet)
        except Exception as e:
            logger.warning(f"Failed to send lead magnet email to {email}: {e}")
            # Don't fail the request - still show success

        return JsonResponse({
            'success': True,
            'message': 'Check your email for the download link!'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'}, status=400)
    except Exception as e:
        logger.error(f"Lead magnet error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)


# Quick search autocomplete API
def search_autocomplete(request):
    """Provide autocomplete suggestions for search"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')

    suggestions = []

    if len(query) >= 2:
        if search_type in ['all', 'accommodations']:
            # Add accommodation suggestions
            accommodations = Accommodation.objects.filter(
                name__icontains=query,
                is_active=True
            ).values('name', 'city')[:5]
            suggestions.extend([
                {'type': 'accommodation', 'name': a['name'], 'city': a['city']}
                for a in accommodations
            ])

        if search_type in ['all', 'tours']:
            # Add tour suggestions
            tours = Tour.objects.filter(
                title__icontains=query,
                is_active=True
            ).values('title', 'duration')[:5]
            suggestions.extend([
                {'type': 'tour', 'name': t['title'], 'duration': t['duration']}
                for t in tours
            ])

        if search_type in ['all', 'destinations']:
            # Add destination suggestions
            cities = City.objects.filter(
                name__icontains=query
            ).select_related('country').values('name', 'country__name')[:5]
            suggestions.extend([
                {'type': 'destination', 'name': c['name'], 'country': c['country__name']}
                for c in cities
            ])

    return JsonResponse({'suggestions': suggestions})


# Stats for homepage (cached for 1 hour)
@cache_page(3600)
def get_platform_stats(request):
    """Get platform statistics for display - cached for performance"""
    # Try to get from cache first
    stats = cache.get('platform_stats')
    if stats is None:
        from transportation.models import TransportationService
        stats = {
            'total_accommodations': Accommodation.objects.filter(is_active=True).count(),
            'total_tours': Tour.objects.filter(is_active=True).count(),
            'total_transport': TransportationService.objects.filter(is_active=True).count(),
            'total_bookings': 5000,  # Placeholder - can be from bookings model
            'happy_customers': 50000,
        }
        cache.set('platform_stats', stats, 3600)  # Cache for 1 hour
    return JsonResponse(stats)


def help_center(request):
    """Help center page with common questions and support options"""
    help_topics = [
        {
            'title': 'Booking Tours',
            'icon': 'fa-map-marked-alt',
            'questions': [
                {'q': 'How do I book a tour?', 'a': 'Browse our tours section, select your preferred tour, choose your dates, and complete the booking through our secure payment system.'},
                {'q': 'Can I modify my booking?', 'a': 'Yes, you can modify most bookings up to 48 hours before the tour date. Contact us for assistance.'},
                {'q': 'What payment methods are accepted?', 'a': 'We accept all major credit cards, PayPal, and bank transfers for tour bookings.'},
            ]
        },
        {
            'title': 'Hotels & Accommodations',
            'icon': 'fa-hotel',
            'questions': [
                {'q': 'How do hotel bookings work?', 'a': 'We partner with major booking platforms like Booking.com and Agoda to find you the best rates. Click through to complete your booking on their secure sites.'},
                {'q': 'Are the hotel prices final?', 'a': 'Prices shown are the best available rates at the time of search. Final prices are confirmed on the booking platform.'},
                {'q': 'Can I get a refund?', 'a': 'Refund policies depend on the hotel and rate type. Check the cancellation policy before booking.'},
            ]
        },
        {
            'title': 'Flights',
            'icon': 'fa-plane',
            'questions': [
                {'q': 'How do I search for flights?', 'a': 'Use our flight search tool to compare prices from 100+ airlines. Enter your departure city, destination, and dates to see available options.'},
                {'q': 'Is it safe to book through Egy360?', 'a': 'Yes! We partner with trusted booking platforms. All payments are processed securely through our partners.'},
                {'q': 'Can I book multi-city flights?', 'a': 'Yes, our flight search supports one-way, round-trip, and multi-city bookings.'},
            ]
        },
        {
            'title': 'Travel Insurance',
            'icon': 'fa-shield-halved',
            'questions': [
                {'q': 'Do I need travel insurance?', 'a': 'We highly recommend travel insurance for all Egypt trips. It covers medical emergencies, trip cancellations, and lost luggage.'},
                {'q': 'What does travel insurance cover?', 'a': 'Most policies cover medical expenses, trip cancellation, baggage loss, and emergency evacuation.'},
                {'q': 'When should I buy insurance?', 'a': 'Purchase travel insurance as soon as you book your trip for maximum coverage.'},
            ]
        },
        {
            'title': 'Account & Technical',
            'icon': 'fa-user-cog',
            'questions': [
                {'q': 'Do I need an account to book?', 'a': 'No account is required. However, creating an account helps you track bookings and receive exclusive deals.'},
                {'q': 'The website is not loading properly', 'a': 'Try clearing your browser cache, disabling ad blockers, or using a different browser. Contact us if issues persist.'},
                {'q': 'How do I unsubscribe from emails?', 'a': 'Click the unsubscribe link at the bottom of any email, or contact us directly.'},
            ]
        },
    ]

    context = {
        'page_title': 'Help Center - Egy360',
        'meta_description': 'Get help with booking tours, hotels, and flights on Egy360. Find answers to common questions about Egypt travel.',
        'help_topics': help_topics,
    }
    return render(request, 'help.html', context)


def careers(request):
    """Careers page showing job opportunities"""
    job_openings = [
        {
            'title': 'Content Writer - Egypt Travel',
            'location': 'Remote',
            'type': 'Full-time / Part-time',
            'description': 'Create engaging travel guides, destination articles, and SEO-optimized content about Egypt tourism.',
            'requirements': [
                'Excellent English writing skills',
                'Knowledge of Egypt history, culture, and tourism',
                'Experience with SEO content writing',
                'Ability to research and fact-check information',
            ],
        },
        {
            'title': 'Social Media Manager',
            'location': 'Remote',
            'type': 'Part-time',
            'description': 'Manage our social media presence across Instagram, Facebook, Twitter, and TikTok.',
            'requirements': [
                'Experience managing travel/tourism social accounts',
                'Knowledge of social media analytics and growth strategies',
                'Creative content creation skills',
                'Experience with Canva or similar design tools',
            ],
        },
        {
            'title': 'Tour Guide Partner',
            'location': 'Cairo, Luxor, Aswan, Hurghada',
            'type': 'Freelance',
            'description': 'Partner with us as a licensed tour guide to provide exceptional experiences to our customers.',
            'requirements': [
                'Valid Egyptian tour guide license',
                'Fluency in English (other languages a plus)',
                'Excellent customer service skills',
                'Knowledge of Egyptian history and culture',
            ],
        },
        {
            'title': 'Hotel Partnership Manager',
            'location': 'Cairo / Remote',
            'type': 'Full-time',
            'description': 'Build and manage relationships with hotels across Egypt to secure exclusive deals for our platform.',
            'requirements': [
                'Experience in hospitality or travel industry',
                'Strong negotiation and relationship-building skills',
                'Knowledge of Egyptian hotel market',
                'Business development experience',
            ],
        },
    ]

    context = {
        'page_title': 'Careers at Egy360 - Join Our Team',
        'meta_description': 'Join the Egy360 team! We\'re hiring content writers, social media managers, tour guides, and more. Work remotely and help travelers discover Egypt.',
        'job_openings': job_openings,
    }
    return render(request, 'careers.html', context)


def search(request):
    """Site-wide search functionality"""
    query = request.GET.get('q', '').strip()
    results = {
        'articles': [],
        'tours': [],
        'accommodations': [],
        'destinations': [],
    }
    total_results = 0

    if query and len(query) >= 2:
        # Search articles
        try:
            from blog.models import BlogPost
            articles = BlogPost.objects.filter(
                status='published'
            ).filter(
                models.Q(title__icontains=query) |
                models.Q(content__icontains=query) |
                models.Q(meta_description__icontains=query)
            )[:10]
            results['articles'] = list(articles)
            total_results += len(results['articles'])
        except Exception as e:
            logger.warning(f"Article search error: {e}")

        # Search tours
        try:
            tours = Tour.objects.filter(
                is_active=True
            ).filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
            results['tours'] = list(tours)
            total_results += len(results['tours'])
        except Exception as e:
            logger.warning(f"Tour search error: {e}")

        # Search accommodations
        try:
            accommodations = Accommodation.objects.filter(
                is_active=True
            ).filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
            results['accommodations'] = list(accommodations)
            total_results += len(results['accommodations'])
        except Exception as e:
            logger.warning(f"Accommodation search error: {e}")

        # Search destinations
        try:
            destinations = City.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
            results['destinations'] = list(destinations)
            total_results += len(results['destinations'])
        except Exception as e:
            logger.warning(f"Destination search error: {e}")

    context = {
        'page_title': f'Search Results for "{query}" - Egy360' if query else 'Search - Egy360',
        'meta_description': f'Search results for {query} on Egy360 - Find tours, hotels, and travel guides for Egypt.',
        'query': query,
        'results': results,
        'total_results': total_results,
    }
    return render(request, 'search.html', context)


def seed_all_content(request):
    """
    Seed all content: tours, hotels, and destinations.
    Access via: /seed-content/?key=egy360seed
    """
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from destinations.models import Country, City, Attraction
    from accommodations.models import Accommodation
    from tours.models import Tour

    results = {
        'destinations': {'created': 0, 'updated': 0},
        'hotels': {'created': 0, 'updated': 0},
        'tours': {'created': 0, 'updated': 0},
    }

    # ============ SEED DESTINATIONS ============
    # Create Egypt country
    egypt, _ = Country.objects.get_or_create(
        code='EGY',
        defaults={
            'name': 'Egypt',
            'description': 'The land of pharaohs, pyramids, and ancient wonders.',
            'flag_emoji': '🇪🇬'
        }
    )

    cities_data = [
        {
            'name': 'Cairo',
            'slug': 'cairo',
            'description': 'Cairo, the capital of Egypt, is a sprawling metropolis where ancient history meets modern life. Home to the iconic Pyramids of Giza and the Sphinx, Cairo offers world-class museums, vibrant bazaars, and a rich cultural tapestry spanning over 5,000 years of civilization.',
            'population': 21000000,
            'is_popular': True,
            'is_capital': True,
            'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Pyramids of Giza', 'slug': 'pyramids-of-giza', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The last surviving Wonder of the Ancient World. These magnificent structures have stood for over 4,500 years.',
                 'admission_fee': 200, 'visit_duration': '3-4 hours', 'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800'},
                {'name': 'Egyptian Museum', 'slug': 'egyptian-museum', 'type': 'museum', 'is_must_see': True,
                 'description': 'Home to the world\'s largest collection of ancient Egyptian artifacts, including Tutankhamun\'s treasures.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800'},
                {'name': 'Khan El-Khalili Bazaar', 'slug': 'khan-el-khalili', 'type': 'market', 'is_must_see': True,
                 'description': 'Cairo\'s famous 14th-century bazaar. Shop for spices, jewelry, souvenirs, and experience authentic Egyptian culture.',
                 'admission_fee': 0, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800'},
            ]
        },
        {
            'name': 'Luxor',
            'slug': 'luxor',
            'description': 'Luxor is the world\'s greatest open-air museum. Once ancient Thebes, capital of the pharaohs, Luxor houses the Valley of the Kings, Karnak Temple, and countless treasures from Egypt\'s golden age.',
            'population': 500000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'October to March',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'attractions': [
                {'name': 'Valley of the Kings', 'slug': 'valley-of-kings', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The royal burial ground of Egypt\'s pharaohs for 500 years. Over 60 tombs including Tutankhamun\'s.',
                 'admission_fee': 300, 'visit_duration': '3-4 hours', 'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800'},
                {'name': 'Karnak Temple', 'slug': 'karnak-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The largest ancient religious complex in the world. 2,000 years of construction by generations of pharaohs.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800'},
                {'name': 'Luxor Temple', 'slug': 'luxor-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'Beautiful temple in the heart of Luxor, particularly stunning when illuminated at night.',
                 'admission_fee': 200, 'visit_duration': '1-2 hours', 'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800'},
            ]
        },
        {
            'name': 'Aswan',
            'slug': 'aswan',
            'description': 'Aswan is Egypt\'s sunniest southern city, known for its beautiful Nile scenery, Nubian culture, and gateway to Abu Simbel. Felucca sailing at sunset and visits to Philae Temple are must-do experiences.',
            'population': 300000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200',
            'attractions': [
                {'name': 'Abu Simbel Temples', 'slug': 'abu-simbel', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'Ramesses II\'s magnificent rock-cut temples, relocated in a UNESCO engineering marvel.',
                 'admission_fee': 300, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=800'},
                {'name': 'Philae Temple', 'slug': 'philae-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'Beautiful island temple dedicated to goddess Isis, rescued from the rising waters of the Aswan Dam.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
            ]
        },
        {
            'name': 'Hurghada',
            'slug': 'hurghada',
            'description': 'Hurghada is Egypt\'s premier Red Sea resort destination. World-class diving, beautiful beaches, all-inclusive resorts, and year-round sunshine make it perfect for beach holidays.',
            'population': 250000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
            'attractions': [
                {'name': 'Giftun Islands', 'slug': 'giftun-islands', 'type': 'natural', 'is_must_see': True,
                 'description': 'Protected marine park with pristine beaches, crystal-clear waters, and excellent snorkeling.',
                 'admission_fee': 100, 'visit_duration': 'Full day', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
                {'name': 'Red Sea Coral Reefs', 'slug': 'red-sea-reefs', 'type': 'natural', 'is_must_see': True,
                 'description': 'Some of the world\'s best diving and snorkeling with vibrant coral and diverse marine life.',
                 'admission_fee': 0, 'visit_duration': '2-4 hours', 'image_url': 'https://images.unsplash.com/photo-1559825481-12a05cc00344?w=800'},
            ]
        },
        {
            'name': 'Sharm El Sheikh',
            'slug': 'sharm-el-sheikh',
            'description': 'Sharm El Sheikh sits at the tip of the Sinai Peninsula, offering world-famous diving at Ras Mohammed National Park, luxury resorts, and the stunning Thistlegorm wreck.',
            'population': 100000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'Year-round, best March to May',
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
            'attractions': [
                {'name': 'Ras Mohammed National Park', 'slug': 'ras-mohammed', 'type': 'natural', 'is_must_see': True,
                 'description': 'World-renowned marine park with spectacular diving, shark reef, and pristine coral walls.',
                 'admission_fee': 100, 'visit_duration': 'Full day', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
                {'name': 'Naama Bay', 'slug': 'naama-bay', 'type': 'beach', 'is_must_see': True,
                 'description': 'The heart of Sharm\'s nightlife and entertainment, with shops, restaurants, and beach activities.',
                 'admission_fee': 0, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800'},
            ]
        },
        {
            'name': 'Alexandria',
            'slug': 'alexandria',
            'description': 'Alexandria, Egypt\'s Mediterranean jewel, was founded by Alexander the Great. Known for the legendary ancient library, Roman catacombs, and beautiful Corniche seaside promenade.',
            'population': 5000000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Bibliotheca Alexandrina', 'slug': 'bibliotheca-alexandrina', 'type': 'modern', 'is_must_see': True,
                 'description': 'Modern tribute to the ancient Library of Alexandria. Stunning architecture and cultural center.',
                 'admission_fee': 70, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
                {'name': 'Catacombs of Kom el Shoqafa', 'slug': 'catacombs-kom-el-shoqafa', 'type': 'archaeological', 'is_must_see': True,
                 'description': 'Roman-era catacombs featuring unique blend of Egyptian, Greek, and Roman art.',
                 'admission_fee': 80, 'visit_duration': '1-2 hours', 'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800'},
            ]
        },
    ]

    for city_data in cities_data:
        attractions = city_data.pop('attractions', [])
        city, created = City.objects.update_or_create(
            slug=city_data['slug'],
            defaults={**city_data, 'country': egypt}
        )
        if created:
            results['destinations']['created'] += 1
        else:
            results['destinations']['updated'] += 1

        # Create attractions
        for attr_data in attractions:
            Attraction.objects.update_or_create(
                slug=attr_data['slug'],
                defaults={
                    'city': city,
                    'name': attr_data['name'],
                    'attraction_type': attr_data['type'],
                    'description': attr_data['description'],
                    'address': f"{attr_data['name']}, {city.name}, Egypt",
                    'admission_fee': attr_data.get('admission_fee', 0),
                    'visit_duration': attr_data.get('visit_duration', '1-2 hours'),
                    'is_unesco': attr_data.get('is_unesco', False),
                    'is_must_see': attr_data.get('is_must_see', False),
                    'image_url': attr_data.get('image_url', ''),
                    'average_rating': 4.5,
                    'total_reviews': 150,
                }
            )

    # ============ SEED HOTELS ============
    hotels_data = [
        {
            'name': 'Marriott Mena House Cairo',
            'slug': 'marriott-mena-house-cairo',
            'accommodation_type': 'hotel',
            'city': 'Cairo',
            'address': '6 Pyramids Road, Giza',
            'star_rating': 5,
            'price_per_night': 250,
            'description': 'Historic luxury hotel with direct views of the Pyramids of Giza. Once a royal hunting lodge, now offering world-class amenities, multiple restaurants, and an unbeatable location at the foot of the pyramids.',
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200',
            'is_featured': True,
            'average_rating': 4.8,
            'total_reviews': 2500,
        },
        {
            'name': 'Four Seasons Cairo at Nile Plaza',
            'slug': 'four-seasons-nile-plaza',
            'accommodation_type': 'hotel',
            'city': 'Cairo',
            'address': '1089 Corniche El Nil, Garden City',
            'star_rating': 5,
            'price_per_night': 350,
            'description': 'Elegant luxury hotel on the banks of the Nile with stunning river views, world-class dining, and impeccable service. Perfect location for exploring Cairo\'s attractions.',
            'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 1800,
        },
        {
            'name': 'Steigenberger Nile Palace Luxor',
            'slug': 'steigenberger-nile-palace-luxor',
            'accommodation_type': 'hotel',
            'city': 'Luxor',
            'address': 'Khaled Ibn El Walid Street',
            'star_rating': 5,
            'price_per_night': 180,
            'description': 'Beautiful hotel on the East Bank of Luxor with panoramic Nile views, lush gardens, and easy access to Luxor Temple and Karnak. Multiple pools and excellent dining.',
            'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200',
            'is_featured': True,
            'average_rating': 4.6,
            'total_reviews': 1200,
        },
        {
            'name': 'Sofitel Winter Palace Luxor',
            'slug': 'sofitel-winter-palace-luxor',
            'accommodation_type': 'hotel',
            'city': 'Luxor',
            'address': 'Corniche El Nil Street',
            'star_rating': 5,
            'price_per_night': 280,
            'description': 'Historic Victorian palace hotel where Agatha Christie wrote "Death on the Nile". Stunning gardens, timeless elegance, and royal heritage since 1886.',
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200',
            'is_featured': True,
            'average_rating': 4.7,
            'total_reviews': 950,
        },
        {
            'name': 'Sofitel Legend Old Cataract Aswan',
            'slug': 'sofitel-old-cataract-aswan',
            'accommodation_type': 'hotel',
            'city': 'Aswan',
            'address': 'Abtal El Tahrir Street',
            'star_rating': 5,
            'price_per_night': 320,
            'description': 'Legendary palace hotel perched above the Nile with breathtaking views of Elephantine Island. A favorite of royalty and celebrities since 1899.',
            'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1200',
            'is_featured': True,
            'average_rating': 4.8,
            'total_reviews': 800,
        },
        {
            'name': 'Oberoi Sahl Hasheesh',
            'slug': 'oberoi-sahl-hasheesh',
            'accommodation_type': 'resort',
            'city': 'Hurghada',
            'address': 'Sahl Hasheesh Bay',
            'star_rating': 5,
            'price_per_night': 400,
            'description': 'Ultra-luxury beachfront resort with stunning Moorish architecture, private beach, world-class spa, and exceptional dining. The ultimate Red Sea retreat.',
            'image_url': 'https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 600,
        },
        {
            'name': 'Sunrise Holidays Resort',
            'slug': 'sunrise-holidays-hurghada',
            'accommodation_type': 'resort',
            'city': 'Hurghada',
            'address': 'Hurghada, Red Sea',
            'star_rating': 4,
            'price_per_night': 85,
            'description': 'Popular all-inclusive resort with excellent beach, multiple pools, water sports, and family-friendly facilities. Great value for a Red Sea holiday.',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
            'is_featured': False,
            'average_rating': 4.3,
            'total_reviews': 3500,
        },
        {
            'name': 'Rixos Premium Sharm El Sheikh',
            'slug': 'rixos-premium-sharm',
            'accommodation_type': 'resort',
            'city': 'Sharm El Sheikh',
            'address': 'Nabq Bay',
            'star_rating': 5,
            'price_per_night': 220,
            'description': 'Ultra all-inclusive luxury resort with private beach, multiple restaurants, aqua park, and world-class entertainment. Perfect for families and couples.',
            'image_url': 'https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1200',
            'is_featured': True,
            'average_rating': 4.7,
            'total_reviews': 2200,
        },
        {
            'name': 'Four Seasons Resort Sharm El Sheikh',
            'slug': 'four-seasons-sharm',
            'accommodation_type': 'resort',
            'city': 'Sharm El Sheikh',
            'address': '1 Four Seasons Boulevard',
            'star_rating': 5,
            'price_per_night': 450,
            'description': 'Exclusive beachfront resort with private pools, exceptional dining, and direct access to pristine coral reefs. The epitome of luxury on the Red Sea.',
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 450,
        },
        {
            'name': 'Steigenberger Cecil Hotel Alexandria',
            'slug': 'steigenberger-cecil-alexandria',
            'accommodation_type': 'hotel',
            'city': 'Alexandria',
            'address': '16 Saad Zaghloul Square',
            'star_rating': 4,
            'price_per_night': 120,
            'description': 'Historic hotel in the heart of Alexandria overlooking the Mediterranean. Classic elegance, rich history, and prime location on the famous Corniche.',
            'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200',
            'is_featured': False,
            'average_rating': 4.4,
            'total_reviews': 900,
        },
    ]

    for hotel_data in hotels_data:
        hotel, created = Accommodation.objects.update_or_create(
            slug=hotel_data['slug'],
            defaults={
                **hotel_data,
                'is_active': True,
                'is_verified': True,
                'total_rooms': 200,
            }
        )
        if created:
            results['hotels']['created'] += 1
        else:
            results['hotels']['updated'] += 1

    # ============ SEED TOURS ============
    tours_data = [
        {
            'name': 'Pyramids of Giza & Sphinx Day Tour',
            'slug': 'pyramids-giza-sphinx-day-tour',
            'tour_type': 'cultural',
            'description': 'Experience the wonder of the ancient world! Visit the Great Pyramids of Giza, marvel at the Sphinx, and explore the Solar Boat Museum. Includes expert Egyptologist guide, hotel pickup, and traditional Egyptian lunch.',
            'highlights': 'Great Pyramid of Khufu|Pyramid of Khafre|Pyramid of Menkaure|The Great Sphinx|Solar Boat Museum|Panoramic photo stops',
            'duration_days': 1,
            'departure_city': 'Cairo',
            'destinations': ['Giza', 'Pyramids'],
            'price_per_person': 75,
            'difficulty_level': 'easy',
            'includes': ['Hotel pickup & drop-off', 'Air-conditioned vehicle', 'Egyptologist guide', 'Lunch', 'All entrance fees', 'Bottled water'],
            'excludes': ['Camel rides (optional)', 'Gratuities', 'Personal expenses'],
            'languages': ['English', 'Spanish', 'French', 'German', 'Arabic'],
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200',
            'is_featured': True,
            'average_rating': 4.8,
            'total_reviews': 3500,
        },
        {
            'name': 'Luxor Full Day Tour from Cairo by Flight',
            'slug': 'luxor-day-tour-from-cairo-flight',
            'tour_type': 'cultural',
            'description': 'Fly to Luxor for an unforgettable day exploring ancient Thebes. Visit the Valley of the Kings, Temple of Hatshepsut, Colossi of Memnon, Karnak Temple, and Luxor Temple. Includes flights, meals, and expert guide.',
            'highlights': 'Valley of the Kings|Temple of Hatshepsut|Colossi of Memnon|Karnak Temple|Luxor Temple|Round-trip flights',
            'duration_days': 1,
            'departure_city': 'Cairo',
            'destinations': ['Luxor', 'Valley of the Kings', 'Karnak'],
            'price_per_person': 350,
            'difficulty_level': 'moderate',
            'includes': ['Round-trip flights Cairo-Luxor', 'Hotel transfers', 'Egyptologist guide', 'Lunch', 'All entrance fees', 'Air-conditioned vehicle'],
            'excludes': ['Tomb of Tutankhamun (optional)', 'Gratuities', 'Personal expenses'],
            'languages': ['English', 'Spanish', 'French', 'German'],
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
            'is_featured': True,
            'average_rating': 4.7,
            'total_reviews': 1200,
        },
        {
            'name': '4-Day Nile Cruise: Luxor to Aswan',
            'slug': 'nile-cruise-luxor-aswan-4-days',
            'tour_type': 'cruise',
            'description': 'Sail the legendary Nile aboard a 5-star cruise ship. Visit Luxor\'s temples, Edfu, Kom Ombo, and Aswan\'s highlights. All meals, entertainment, and guided tours included.',
            'highlights': 'Luxor Temple|Karnak Temple|Valley of the Kings|Edfu Temple|Kom Ombo Temple|Philae Temple|High Dam|5-star cruise ship',
            'duration_days': 4,
            'duration_nights': 3,
            'departure_city': 'Luxor',
            'destinations': ['Luxor', 'Edfu', 'Kom Ombo', 'Aswan'],
            'price_per_person': 450,
            'difficulty_level': 'easy',
            'includes': ['3 nights cruise accommodation', 'Full board meals', 'All temple visits', 'Egyptologist guide', 'Entertainment on board'],
            'excludes': ['Flights to/from Luxor', 'Abu Simbel excursion', 'Gratuities', 'Drinks'],
            'languages': ['English', 'German', 'French', 'Spanish', 'Italian'],
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 800,
        },
        {
            'name': 'White Desert Overnight Camping Safari',
            'slug': 'white-desert-camping-safari',
            'tour_type': 'desert',
            'description': 'Adventure into Egypt\'s surreal White Desert with its otherworldly chalk formations. Camp under the stars, explore Crystal Mountain, and experience authentic Bedouin hospitality.',
            'highlights': 'White Desert National Park|Crystal Mountain|Black Desert|Bahariya Oasis|Bedouin dinner|Stargazing|4x4 desert safari',
            'duration_days': 2,
            'duration_nights': 1,
            'departure_city': 'Cairo',
            'destinations': ['Bahariya Oasis', 'White Desert', 'Black Desert'],
            'price_per_person': 180,
            'difficulty_level': 'moderate',
            'includes': ['4x4 jeep safari', 'Camping equipment', 'All meals', 'Bedouin guide', 'Park fees'],
            'excludes': ['Sleeping bag rental', 'Gratuities', 'Personal expenses'],
            'languages': ['English', 'Arabic'],
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200',
            'is_featured': True,
            'average_rating': 4.8,
            'total_reviews': 650,
        },
        {
            'name': 'Red Sea Diving Day Trip - Hurghada',
            'slug': 'red-sea-diving-hurghada',
            'tour_type': 'diving',
            'description': 'Discover the underwater wonders of the Red Sea. Two dives at spectacular coral reef sites, see colorful fish, and maybe dolphins! Suitable for beginners and certified divers.',
            'highlights': 'Two dive sites|Coral reefs|Marine life|Professional PADI instructors|All equipment included|Lunch on boat',
            'duration_days': 1,
            'departure_city': 'Hurghada',
            'destinations': ['Red Sea', 'Giftun Islands'],
            'price_per_person': 75,
            'difficulty_level': 'moderate',
            'includes': ['2 boat dives', 'All diving equipment', 'PADI instructor', 'Lunch & snacks', 'Hotel transfers'],
            'excludes': ['Underwater photos', 'Gratuities', 'Marine park fee ($5)'],
            'languages': ['English', 'German', 'Russian', 'Arabic'],
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
            'is_featured': True,
            'average_rating': 4.7,
            'total_reviews': 1500,
        },
        {
            'name': 'Abu Simbel Day Tour from Aswan',
            'slug': 'abu-simbel-day-tour-aswan',
            'tour_type': 'cultural',
            'description': 'Visit the magnificent temples of Abu Simbel, Ramesses II\'s greatest monument. Early morning departure to witness the temples in the beautiful morning light.',
            'highlights': 'Great Temple of Ramesses II|Temple of Nefertari|UNESCO World Heritage Site|Stunning Lake Nasser views',
            'duration_days': 1,
            'departure_city': 'Aswan',
            'destinations': ['Abu Simbel'],
            'price_per_person': 95,
            'difficulty_level': 'easy',
            'includes': ['Air-conditioned minibus', 'Egyptologist guide', 'Entrance fees', 'Breakfast box', 'Hotel pickup 3:30 AM'],
            'excludes': ['Lunch', 'Gratuities', 'Personal expenses'],
            'languages': ['English', 'French', 'Spanish', 'German'],
            'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 950,
        },
        {
            'name': 'Islamic Cairo Walking Tour',
            'slug': 'islamic-cairo-walking-tour',
            'tour_type': 'cultural',
            'description': 'Explore the medieval heart of Cairo. Walk through historic mosques, madrasas, and bazaars. Visit Al-Azhar Mosque, Sultan Hassan Mosque, and end at Khan El-Khalili.',
            'highlights': 'Al-Azhar Mosque|Sultan Hassan Mosque|Al-Muizz Street|Khan El-Khalili Bazaar|Historic gates|Traditional coffee',
            'duration_days': 1,
            'departure_city': 'Cairo',
            'destinations': ['Islamic Cairo', 'Khan El-Khalili'],
            'price_per_person': 45,
            'difficulty_level': 'easy',
            'includes': ['Licensed guide', 'Walking tour', 'Traditional coffee', 'Mosque entrance fees'],
            'excludes': ['Lunch', 'Shopping', 'Gratuities'],
            'languages': ['English', 'Arabic', 'French', 'Spanish'],
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'is_featured': False,
            'average_rating': 4.6,
            'total_reviews': 420,
        },
        {
            'name': 'Snorkeling Trip to Tiran Island',
            'slug': 'snorkeling-tiran-island-sharm',
            'tour_type': 'diving',
            'description': 'Sail to the famous reefs of Tiran Island for world-class snorkeling. Crystal-clear waters, vibrant coral, and abundant marine life await. Lunch and equipment included.',
            'highlights': 'Tiran Island reefs|Jackson Reef|Gordon Reef|Dolphins possible|Lunch on boat|All snorkeling gear',
            'duration_days': 1,
            'departure_city': 'Sharm El Sheikh',
            'destinations': ['Tiran Island', 'Red Sea'],
            'price_per_person': 55,
            'difficulty_level': 'easy',
            'includes': ['Boat trip', 'Snorkeling equipment', 'Lunch & drinks', 'Guide', 'Hotel transfers'],
            'excludes': ['Underwater camera rental', 'Gratuities', 'Marine park fee'],
            'languages': ['English', 'Russian', 'German', 'Arabic'],
            'image_url': 'https://images.unsplash.com/photo-1559825481-12a05cc00344?w=1200',
            'is_featured': False,
            'average_rating': 4.5,
            'total_reviews': 890,
        },
        {
            'name': '8-Day Egypt Highlights Tour',
            'slug': 'egypt-highlights-8-days',
            'tour_type': 'cultural',
            'description': 'The ultimate Egypt experience! Cairo, Pyramids, Luxor, Nile Cruise, and Aswan. Visit all major sites with expert guides, quality hotels, and seamless logistics.',
            'highlights': 'Pyramids & Sphinx|Egyptian Museum|Luxor Temple|Valley of the Kings|Karnak|Nile Cruise|Abu Simbel option|Aswan',
            'duration_days': 8,
            'duration_nights': 7,
            'departure_city': 'Cairo',
            'destinations': ['Cairo', 'Giza', 'Luxor', 'Aswan'],
            'price_per_person': 1200,
            'difficulty_level': 'easy',
            'includes': ['7 nights accommodation', 'Domestic flights', '3-night Nile cruise', 'All meals on cruise', 'Expert guides', 'All entrance fees', 'Transfers'],
            'excludes': ['International flights', 'Visa', 'Travel insurance', 'Gratuities'],
            'languages': ['English', 'Spanish', 'French', 'German', 'Italian'],
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'is_featured': True,
            'average_rating': 4.9,
            'total_reviews': 380,
        },
        {
            'name': 'Alexandria Day Trip from Cairo',
            'slug': 'alexandria-day-trip-cairo',
            'tour_type': 'cultural',
            'description': 'Discover Egypt\'s Mediterranean gem. Visit the Bibliotheca Alexandrina, Catacombs, Citadel of Qaitbay, and enjoy fresh seafood lunch. Experience a different side of Egypt.',
            'highlights': 'Bibliotheca Alexandrina|Catacombs of Kom el Shoqafa|Citadel of Qaitbay|Corniche promenade|Seafood lunch|Roman Amphitheater',
            'duration_days': 1,
            'departure_city': 'Cairo',
            'destinations': ['Alexandria'],
            'price_per_person': 85,
            'difficulty_level': 'easy',
            'includes': ['Air-conditioned vehicle', 'Egyptologist guide', 'Entrance fees', 'Seafood lunch', 'Hotel pickup & drop-off'],
            'excludes': ['Drinks', 'Gratuities', 'Personal expenses'],
            'languages': ['English', 'French', 'Spanish', 'German'],
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'is_featured': False,
            'average_rating': 4.6,
            'total_reviews': 720,
        },
    ]

    for tour_data in tours_data:
        tour, created = Tour.objects.update_or_create(
            slug=tour_data['slug'],
            defaults={
                **tour_data,
                'is_active': True,
                'min_group_size': 1,
                'max_group_size': 15,
                'child_discount': 25,
            }
        )
        if created:
            results['tours']['created'] += 1
        else:
            results['tours']['updated'] += 1

    return JsonResponse({
        'success': True,
        'results': results,
        'message': f"Seeded: {results['destinations']['created']+results['destinations']['updated']} destinations, {results['hotels']['created']+results['hotels']['updated']} hotels, {results['tours']['created']+results['tours']['updated']} tours"
    })
