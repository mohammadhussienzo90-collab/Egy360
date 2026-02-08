import logging
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Min, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# from django.core.cache import cache  # Disabled due to Railway Redis issues
import json

logger = logging.getLogger(__name__)

from .models import Tour, TourItinerary, TourBooking


class TourListView(ListView):
    """List and filter tours with advanced options"""
    model = Tour
    template_name = 'tour_listing.html'
    context_object_name = 'tours'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        # Auto-seed if no tours exist (Railway ephemeral storage fix)
        import sys
        try:
            if Tour.objects.count() == 0:
                print("AUTO-SEED TOURS: No tours found, seeding now...", file=sys.stderr)
                self._auto_seed_tours()
                print(f"AUTO-SEED TOURS: Completed. Total tours: {Tour.objects.count()}", file=sys.stderr)
        except Exception as e:
            print(f"AUTO-SEED TOURS ERROR: {str(e)}", file=sys.stderr)
        return super().dispatch(request, *args, **kwargs)

    def _auto_seed_tours(self):
        """Auto-seed tours when database is empty"""
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
                'description': 'Fly to Luxor for an unforgettable day exploring ancient Thebes. Visit the Valley of the Kings, Temple of Hatshepsut, Colossi of Memnon, Karnak Temple, and Luxor Temple.',
                'highlights': 'Valley of the Kings|Temple of Hatshepsut|Colossi of Memnon|Karnak Temple|Luxor Temple|Round-trip flights',
                'duration_days': 1,
                'departure_city': 'Cairo',
                'destinations': ['Luxor', 'Valley of the Kings', 'Karnak'],
                'price_per_person': 350,
                'difficulty_level': 'moderate',
                'includes': ['Round-trip flights Cairo-Luxor', 'Hotel transfers', 'Egyptologist guide', 'Lunch', 'All entrance fees'],
                'excludes': ['Tomb of Tutankhamun (optional)', 'Gratuities'],
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
                'description': 'Sail the legendary Nile aboard a 5-star cruise ship. Visit Luxor temples, Edfu, Kom Ombo, and Aswan highlights. All meals and guided tours included.',
                'highlights': 'Luxor Temple|Karnak Temple|Valley of the Kings|Edfu Temple|Kom Ombo Temple|Philae Temple|5-star cruise ship',
                'duration_days': 4,
                'duration_nights': 3,
                'departure_city': 'Luxor',
                'destinations': ['Luxor', 'Edfu', 'Kom Ombo', 'Aswan'],
                'price_per_person': 450,
                'difficulty_level': 'easy',
                'includes': ['3 nights cruise accommodation', 'Full board meals', 'All temple visits', 'Egyptologist guide'],
                'excludes': ['Flights to/from Luxor', 'Abu Simbel excursion', 'Gratuities'],
                'languages': ['English', 'German', 'French', 'Spanish'],
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
                'highlights': 'White Desert National Park|Crystal Mountain|Black Desert|Bahariya Oasis|Bedouin dinner|Stargazing',
                'duration_days': 2,
                'duration_nights': 1,
                'departure_city': 'Cairo',
                'destinations': ['Bahariya Oasis', 'White Desert', 'Black Desert'],
                'price_per_person': 180,
                'difficulty_level': 'moderate',
                'includes': ['4x4 jeep safari', 'Camping equipment', 'All meals', 'Bedouin guide', 'Park fees'],
                'excludes': ['Sleeping bag rental', 'Gratuities'],
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
                'description': 'Visit the magnificent temples of Abu Simbel, Ramesses II\'s greatest monument. Early morning departure to witness the temples in beautiful morning light.',
                'highlights': 'Great Temple of Ramesses II|Temple of Nefertari|UNESCO World Heritage Site|Lake Nasser views',
                'duration_days': 1,
                'departure_city': 'Aswan',
                'destinations': ['Abu Simbel'],
                'price_per_person': 95,
                'difficulty_level': 'easy',
                'includes': ['Air-conditioned minibus', 'Egyptologist guide', 'Entrance fees', 'Breakfast box'],
                'excludes': ['Lunch', 'Gratuities'],
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
                'highlights': 'Al-Azhar Mosque|Sultan Hassan Mosque|Al-Muizz Street|Khan El-Khalili Bazaar|Traditional coffee',
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
                'description': 'Sail to the famous reefs of Tiran Island for world-class snorkeling. Crystal-clear waters, vibrant coral, and abundant marine life await.',
                'highlights': 'Tiran Island reefs|Jackson Reef|Gordon Reef|Dolphins possible|Lunch on boat|All snorkeling gear',
                'duration_days': 1,
                'departure_city': 'Sharm El Sheikh',
                'destinations': ['Tiran Island', 'Red Sea'],
                'price_per_person': 55,
                'difficulty_level': 'easy',
                'includes': ['Boat trip', 'Snorkeling equipment', 'Lunch & drinks', 'Guide', 'Hotel transfers'],
                'excludes': ['Underwater camera rental', 'Gratuities'],
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
                'highlights': 'Pyramids & Sphinx|Egyptian Museum|Luxor Temple|Valley of the Kings|Karnak|Nile Cruise|Aswan',
                'duration_days': 8,
                'duration_nights': 7,
                'departure_city': 'Cairo',
                'destinations': ['Cairo', 'Giza', 'Luxor', 'Aswan'],
                'price_per_person': 1200,
                'difficulty_level': 'easy',
                'includes': ['7 nights accommodation', 'Domestic flights', '3-night Nile cruise', 'All meals on cruise', 'Expert guides', 'All entrance fees'],
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
                'description': 'Discover Egypt\'s Mediterranean gem. Visit the Bibliotheca Alexandrina, Catacombs, Citadel of Qaitbay, and enjoy fresh seafood lunch.',
                'highlights': 'Bibliotheca Alexandrina|Catacombs of Kom el Shoqafa|Citadel of Qaitbay|Corniche promenade|Seafood lunch',
                'duration_days': 1,
                'departure_city': 'Cairo',
                'destinations': ['Alexandria'],
                'price_per_person': 85,
                'difficulty_level': 'easy',
                'includes': ['Air-conditioned vehicle', 'Egyptologist guide', 'Entrance fees', 'Seafood lunch', 'Hotel pickup'],
                'excludes': ['Drinks', 'Gratuities'],
                'languages': ['English', 'French', 'Spanish', 'German'],
                'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
                'is_featured': False,
                'average_rating': 4.6,
                'total_reviews': 720,
            },
        ]

        for tour_data in tours_data:
            Tour.objects.update_or_create(
                slug=tour_data['slug'],
                defaults={
                    **tour_data,
                    'is_active': True,
                    'min_group_size': 1,
                    'max_group_size': 15,
                    'child_discount': 25,
                    'duration_nights': tour_data.get('duration_nights', 0),
                }
            )

    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True)

        # Search query (name, description, highlights)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(highlights__icontains=query)
            )

        # Filter by tour type
        tour_type = self.request.GET.get('type')
        if tour_type:
            queryset = queryset.filter(tour_type=tour_type)

        # Filter by difficulty level
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by duration (days)
        min_days = self.request.GET.get('min_days')
        max_days = self.request.GET.get('max_days')
        if min_days:
            queryset = queryset.filter(duration_days__gte=min_days)
        if max_days:
            queryset = queryset.filter(duration_days__lte=max_days)

        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_person__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_person__lte=max_price)

        # Filter by departure city
        departure = self.request.GET.get('departure')
        if departure:
            queryset = queryset.filter(departure_city__icontains=departure)

        # Filter by featured
        if self.request.GET.get('featured'):
            queryset = queryset.filter(is_featured=True)

        # Sorting
        sort = self.request.GET.get('sort', '-is_featured')
        sort_options = {
            'price_low': 'price_per_person',
            'price_high': '-price_per_person',
            'rating': '-average_rating',
            'duration_short': 'duration_days',
            'duration_long': '-duration_days',
            'popular': '-booking_count',
            'name': 'name',
            'newest': '-created_at',
        }
        queryset = queryset.order_by(sort_options.get(sort, '-is_featured'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass filter options to template
        context['tour_types'] = Tour.TOUR_TYPES
        context['difficulty_levels'] = Tour.DIFFICULTY_LEVELS

        # Get departure cities directly (cache disabled due to Railway Redis issues)
        departure_cities = list(Tour.objects.filter(
            is_active=True
        ).values_list('departure_city', flat=True).distinct().order_by('departure_city'))
        context['departure_cities'] = departure_cities

        # Current filter values for form persistence
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'type': self.request.GET.get('type', ''),
            'difficulty': self.request.GET.get('difficulty', ''),
            'min_days': self.request.GET.get('min_days', ''),
            'max_days': self.request.GET.get('max_days', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'departure': self.request.GET.get('departure', ''),
            'sort': self.request.GET.get('sort', ''),
        }

        context['total_results'] = self.get_queryset().count()

        # Get price and duration ranges directly (cache disabled due to Railway Redis issues)
        price_stats = Tour.objects.filter(is_active=True).aggregate(
            min_price=Min('price_per_person'),
            max_price=Max('price_per_person')
        )
        context['price_range'] = price_stats

        duration_stats = Tour.objects.filter(is_active=True).aggregate(
            min_days=Min('duration_days'),
            max_days=Max('duration_days')
        )
        context['duration_range'] = duration_stats

        return context


class TourDetailView(DetailView):
    """Detailed view of a single tour with itinerary"""
    model = Tour
    template_name = 'tour_detail.html'
    context_object_name = 'tour'

    def get_queryset(self):
        return Tour.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object

        # Get itinerary for this tour
        context['itinerary'] = tour.itinerary.all().order_by('day')

        # Parse JSON fields for display
        context['includes'] = tour.includes if isinstance(tour.includes, list) else []
        context['excludes'] = tour.excludes if isinstance(tour.excludes, list) else []
        context['languages'] = tour.languages if isinstance(tour.languages, list) else []
        context['destinations'] = tour.destinations if isinstance(tour.destinations, list) else []

        # Get similar tours (same type or departure city)
        context['similar_tours'] = Tour.objects.filter(
            is_active=True
        ).filter(
            Q(tour_type=tour.tour_type) | Q(departure_city=tour.departure_city)
        ).exclude(
            id=tour.id
        ).order_by('-average_rating')[:4]

        # Get reviews using the reviews helper function
        try:
            from reviews.web_views import get_reviews_for_object
            context['reviews_data'] = get_reviews_for_object(tour)
            context['item_type'] = 'tour'
            context['item'] = tour
        except (ImportError, Exception):
            context['reviews_data'] = {'reviews': [], 'stats': {}, 'distribution': {}}
            context['item_type'] = 'tour'
            context['item'] = tour

        # Calculate child price
        if tour.child_discount > 0:
            context['child_price'] = tour.price_per_person * (1 - tour.child_discount / 100)
        else:
            context['child_price'] = tour.price_per_person

        return context


def tour_by_type(request, tour_type):
    """View all tours of a specific type"""
    from django.core.paginator import Paginator

    type_display = dict(Tour.TOUR_TYPES).get(tour_type, tour_type)
    tours = Tour.objects.filter(
        tour_type=tour_type,
        is_active=True
    ).order_by('-is_featured', '-average_rating')

    # Pagination
    paginator = Paginator(tours, 12)  # 12 per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'tours': page_obj,
        'page_obj': page_obj,
        'tour_type': tour_type,
        'type_display': type_display,
        'total_results': paginator.count,
        'page_title': f'{type_display} Tours in Egypt - Egy360',
        'tour_types': Tour.TOUR_TYPES,
        'difficulty_levels': Tour.DIFFICULTY_LEVELS,
    }
    return render(request, 'tour_listing.html', context)


def tour_by_destination(request, destination):
    """View all tours that include a specific destination"""
    from django.core.paginator import Paginator

    # Try database-level filtering first (works for PostgreSQL JSONField)
    # Fall back to limited in-memory filtering for SQLite
    try:
        # Attempt case-insensitive JSON contains lookup
        tours = Tour.objects.filter(
            is_active=True,
            destinations__icontains=destination
        ).order_by('-is_featured', '-average_rating')
        total_count = tours.count()
    except Exception:
        # Fallback: Load only necessary fields and filter in memory
        tours = Tour.objects.filter(
            is_active=True
        ).only(
            'id', 'name', 'slug', 'description', 'tour_type', 'duration_days',
            'price_per_person', 'destinations', 'main_image', 'is_featured',
            'average_rating', 'departure_city'
        ).order_by('-is_featured', '-average_rating')

        # Filter tours that include this destination in their JSON field
        tours = [
            tour for tour in tours
            if destination.lower() in [d.lower() for d in (tour.destinations or [])]
        ]
        total_count = len(tours)

    # Pagination
    paginator = Paginator(tours, 12)  # 12 per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'tours': page_obj,
        'page_obj': page_obj,
        'destination': destination,
        'total_results': total_count,
        'page_title': f'Tours to {destination} - Egy360',
        'tour_types': Tour.TOUR_TYPES,
        'difficulty_levels': Tour.DIFFICULTY_LEVELS,
    }
    return render(request, 'tour_listing.html', context)


@login_required
@require_http_methods(["POST"])
def book_tour(request, slug):
    """Handle tour booking submission"""
    tour = get_object_or_404(Tour, slug=slug, is_active=True)

    try:
        data = json.loads(request.body)

        tour_date = data.get('tour_date')
        adults = int(data.get('adults', 1))
        children = int(data.get('children', 0))
        contact_name = data.get('contact_name', '')
        contact_email = data.get('contact_email', '')
        contact_phone = data.get('contact_phone', '')
        special_requests = data.get('special_requests', '')

        # Validate
        if not tour_date:
            return JsonResponse({'success': False, 'error': 'Tour date is required'}, status=400)
        if adults < 1:
            return JsonResponse({'success': False, 'error': 'At least 1 adult is required'}, status=400)
        if adults + children > tour.max_group_size:
            return JsonResponse({
                'success': False,
                'error': f'Maximum group size is {tour.max_group_size}'
            }, status=400)

        # Calculate total price
        adult_price = tour.price_per_person * adults
        child_price = tour.price_per_person * (1 - tour.child_discount / 100) * children
        total_price = adult_price + child_price

        # Create booking
        booking = TourBooking.objects.create(
            tour=tour,
            user=request.user,
            tour_date=tour_date,
            number_of_adults=adults,
            number_of_children=children,
            total_price=total_price,
            contact_name=contact_name or request.user.get_full_name(),
            contact_email=contact_email or request.user.email,
            contact_phone=contact_phone,
            special_requests=special_requests,
            status='pending'
        )

        # Update tour booking count
        tour.booking_count += 1
        tour.save()

        # Send confirmation email
        try:
            from core.email import send_booking_confirmation
            send_booking_confirmation(booking, booking_type='tour')
        except Exception as e:
            logger.error(f"Failed to send confirmation email for booking {booking.id}: {e}")

        return JsonResponse({
            'success': True,
            'message': 'Booking submitted successfully! Check your email for confirmation.',
            'booking_id': booking.id,
            'total_price': str(total_price)
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)
