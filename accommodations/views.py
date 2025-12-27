from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg, Min, Max
# from django.core.cache import cache  # Disabled due to Railway Redis issues
from .models import Accommodation, Room, Amenity


class AccommodationSearchView(ListView):
    """Search and filter accommodations with advanced options"""
    model = Accommodation
    template_name = 'accommodation_search.html'
    context_object_name = 'accommodations'
    paginate_by = 12

    def get_queryset(self):
        queryset = Accommodation.objects.filter(is_active=True)

        # Search query (name, city, description)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(city__icontains=query) |
                Q(description__icontains=query)
            )

        # Filter by city
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Filter by accommodation type
        acc_type = self.request.GET.get('type')
        if acc_type:
            queryset = queryset.filter(accommodation_type=acc_type)

        # Filter by star rating
        stars = self.request.GET.get('stars')
        if stars:
            queryset = queryset.filter(star_rating=stars)

        # Filter by minimum star rating
        min_stars = self.request.GET.get('min_stars')
        if min_stars:
            queryset = queryset.filter(star_rating__gte=min_stars)

        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        # Filter by features
        if self.request.GET.get('featured'):
            queryset = queryset.filter(is_featured=True)
        if self.request.GET.get('verified'):
            queryset = queryset.filter(is_verified=True)

        # Filter by amenities
        amenities = self.request.GET.getlist('amenities')
        if amenities:
            for amenity_id in amenities:
                queryset = queryset.filter(amenities__id=amenity_id)

        # Sorting
        sort = self.request.GET.get('sort', '-is_featured')
        sort_options = {
            'price_low': 'price_per_night',
            'price_high': '-price_per_night',
            'rating': '-average_rating',
            'stars': '-star_rating',
            'name': 'name',
            'newest': '-created_at',
        }
        queryset = queryset.order_by(sort_options.get(sort, '-is_featured'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass filter options to template
        context['accommodation_types'] = Accommodation.ACCOMMODATION_TYPES

        # Get amenities directly (cache disabled due to Railway Redis issues)
        context['amenities'] = list(Amenity.objects.all())

        # Get cities directly (cache disabled due to Railway Redis issues)
        context['cities'] = list(Accommodation.objects.filter(
            is_active=True
        ).values_list('city', flat=True).distinct().order_by('city'))

        # Current filter values for form persistence
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'city': self.request.GET.get('city', ''),
            'type': self.request.GET.get('type', ''),
            'stars': self.request.GET.get('stars', ''),
            'min_stars': self.request.GET.get('min_stars', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'sort': self.request.GET.get('sort', ''),
            'amenities': self.request.GET.getlist('amenities'),
        }

        context['total_results'] = self.get_queryset().count()

        # Get price range directly (cache disabled due to Railway Redis issues)
        price_stats = Accommodation.objects.filter(is_active=True).aggregate(
            min_price=Min('price_per_night'),
            max_price=Max('price_per_night')
        )
        context['price_range'] = price_stats

        return context


class AccommodationDetailView(DetailView):
    """Detailed view of a single accommodation"""
    model = Accommodation
    template_name = 'accommodation_detail.html'
    context_object_name = 'accommodation'

    def get_queryset(self):
        return Accommodation.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accommodation = self.object

        # Get rooms for this accommodation
        context['rooms'] = accommodation.rooms.all()

        # Get amenities
        context['amenities'] = accommodation.amenities.all()

        # Get all booking options
        context['booking_options'] = accommodation.get_all_booking_options()
        context['primary_booking_url'] = accommodation.get_primary_booking_url()

        # Get similar accommodations (same city or type)
        context['similar_accommodations'] = Accommodation.objects.filter(
            is_active=True
        ).filter(
            Q(city=accommodation.city) | Q(accommodation_type=accommodation.accommodation_type)
        ).exclude(
            id=accommodation.id
        ).order_by('-average_rating')[:4]

        # Reviews disabled temporarily
        context['reviews_data'] = {'reviews': [], 'stats': {'total_count': 0}, 'distribution': {}}
        context['item_type'] = 'accommodation'
        context['item'] = accommodation

        return context


def accommodation_by_city(request, city):
    """View all accommodations in a specific city"""
    from django.core.paginator import Paginator

    accommodations = Accommodation.objects.filter(
        city__iexact=city,
        is_active=True
    ).order_by('-is_featured', '-average_rating')

    # Pagination
    paginator = Paginator(accommodations, 12)  # 12 per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'accommodations': page_obj,
        'page_obj': page_obj,
        'city': city,
        'total_results': paginator.count,
        'page_title': f'Accommodations in {city} - Egy360',
    }
    return render(request, 'accommodation_search.html', context)


def accommodation_by_type(request, acc_type):
    """View all accommodations of a specific type"""
    from django.core.paginator import Paginator

    type_display = dict(Accommodation.ACCOMMODATION_TYPES).get(acc_type, acc_type)
    accommodations = Accommodation.objects.filter(
        accommodation_type=acc_type,
        is_active=True
    ).order_by('-is_featured', '-average_rating')

    # Pagination
    paginator = Paginator(accommodations, 12)  # 12 per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'accommodations': page_obj,
        'page_obj': page_obj,
        'accommodation_type': acc_type,
        'type_display': type_display,
        'total_results': paginator.count,
        'page_title': f'{type_display}s in Egypt - Egy360',
    }
    return render(request, 'accommodation_search.html', context)
