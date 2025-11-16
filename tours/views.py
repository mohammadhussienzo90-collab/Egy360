from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Tour

class TourListView(ListView):
    model = Tour
    template_name = 'tour_listing.html'
    context_object_name = 'tours'
    paginate_by = 20

    def get_queryset(self):
        return Tour.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_results'] = self.get_queryset().count()
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tour_detail.html'
    context_object_name = 'tour'