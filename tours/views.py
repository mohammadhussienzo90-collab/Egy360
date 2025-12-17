from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Min, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .models import Tour, TourItinerary, TourBooking


class TourListView(ListView):
    """List and filter tours with advanced options"""
    model = Tour
    template_name = 'tour_listing.html'
    context_object_name = 'tours'
    paginate_by = 12

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
        context['departure_cities'] = Tour.objects.filter(
            is_active=True
        ).values_list('departure_city', flat=True).distinct().order_by('departure_city')

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

        # Price range for filter UI
        price_stats = Tour.objects.filter(is_active=True).aggregate(
            min_price=Min('price_per_person'),
            max_price=Max('price_per_person')
        )
        context['price_range'] = price_stats

        # Duration range for filter UI
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

        # Get reviews if reviews app is available
        try:
            from reviews.models import Review
            from django.contrib.contenttypes.models import ContentType
            content_type = ContentType.objects.get_for_model(Tour)
            context['reviews'] = Review.objects.filter(
                content_type=content_type,
                object_id=tour.id,
                is_approved=True
            ).order_by('-created_at')[:10]
        except (ImportError, Exception):
            context['reviews'] = []

        # Calculate child price
        if tour.child_discount > 0:
            context['child_price'] = tour.price_per_person * (1 - tour.child_discount / 100)
        else:
            context['child_price'] = tour.price_per_person

        return context


def tour_by_type(request, tour_type):
    """View all tours of a specific type"""
    type_display = dict(Tour.TOUR_TYPES).get(tour_type, tour_type)
    tours = Tour.objects.filter(
        tour_type=tour_type,
        is_active=True
    ).order_by('-is_featured', '-average_rating')

    context = {
        'tours': tours,
        'tour_type': tour_type,
        'type_display': type_display,
        'total_results': tours.count(),
        'page_title': f'{type_display} Tours in Egypt - Egy360',
        'tour_types': Tour.TOUR_TYPES,
        'difficulty_levels': Tour.DIFFICULTY_LEVELS,
    }
    return render(request, 'tour_listing.html', context)


def tour_by_destination(request, destination):
    """View all tours that include a specific destination"""
    tours = Tour.objects.filter(
        is_active=True
    ).order_by('-is_featured', '-average_rating')

    # Filter tours that include this destination in their JSON field
    filtered_tours = [
        tour for tour in tours
        if destination.lower() in [d.lower() for d in (tour.destinations or [])]
    ]

    context = {
        'tours': filtered_tours,
        'destination': destination,
        'total_results': len(filtered_tours),
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

        return JsonResponse({
            'success': True,
            'message': 'Booking submitted successfully!',
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
