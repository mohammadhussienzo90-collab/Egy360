# transportation/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import TransportationService, Driver, TransportBooking


class TransportationListView(ListView):
    model = TransportationService
    template_name = 'transportation/list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        # CHANGED from is_available to is_active
        queryset = super().get_queryset().filter(is_active=True)
        service_type = self.request.GET.get('type')
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        return queryset


class TransportationDetailView(DetailView):
    model = TransportationService
    template_name = 'transportation/detail.html'
    context_object_name = 'service'


def book_transport(request, pk):
    service = get_object_or_404(TransportationService, pk=pk)
    return render(request, 'transportation/booking.html', {'service': service})