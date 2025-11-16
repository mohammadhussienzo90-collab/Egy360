from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Accommodation


class AccommodationSearchView(ListView):
    model = Accommodation
    template_name = 'accommodation_search.html'
    context_object_name = 'accommodations'
    paginate_by = 20

    def get_queryset(self):
        queryset = Accommodation.objects.all()

        # Filter by city if provided
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_results'] = self.get_queryset().count()
        return context


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'accommodation_detail.html'
    context_object_name = 'accommodation'