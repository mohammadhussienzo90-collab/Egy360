from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tour, TourCategory, TourOperator
from .serializers import (
    TourSerializer,
    TourDetailSerializer,
    TourCategorySerializer,
    TourOperatorSerializer
)


class TourViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tours
    """
    queryset = Tour.objects.filter(is_active=True).select_related(
        'city', 'category', 'operator'
    )
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'category', 'difficulty_level', 'language']
    search_fields = ['title', 'description']
    ordering_fields = ['price_per_person', 'average_rating', 'start_date']
    ordering = ['-average_rating']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TourDetailSerializer
        return TourSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured tours"""
        featured_tours = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_tours, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get tours grouped by category"""
        category_id = request.query_params.get('category_id')
        if category_id:
            tours = self.queryset.filter(category_id=category_id)
            serializer = self.get_serializer(tours, many=True)
            return Response(serializer.data)
        return Response({'error': 'category_id parameter required'}, status=400)


class TourCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tour categories
    """
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer


class TourOperatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tour operators
    """
    queryset = TourOperator.objects.filter(is_active=True, is_verified=True)
    serializer_class = TourOperatorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['average_rating', 'total_tours_completed']
    ordering = ['-average_rating']
    lookup_field = 'slug'