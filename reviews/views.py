# FILE: reviews/views.py
# ============================================================
"""
API Views for Reviews App

This module provides REST API endpoints for:
- Reviews: User reviews and ratings (full CRUD with restrictions)
- ReviewImages: Photos attached to reviews (nested)
- ReviewResponses: Provider responses to reviews (restricted)
- ReviewReports: Flagging fake/inappropriate reviews

Complex features:
- Users can only edit/delete their own reviews
- Verified purchase badge
- Helpful/unhelpful voting
- Provider response system
- Review reporting and moderation
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from .models import Review, ReviewImage, ReviewResponse, ReviewReport
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewImageSerializer,
    ReviewResponseSerializer,
    ReviewReportSerializer,
    ReviewHelpfulSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews (restricted CRUD)

    list:
    Return list of all approved reviews
    Uses ReviewListSerializer for performance

    retrieve:
    Return complete review with images and response
    Uses ReviewDetailSerializer

    create:
    Create new review (authenticated users only)
    Uses ReviewCreateSerializer
    Validates verified purchase if applicable

    update/partial_update:
    Update own review only
    Uses ReviewUpdateSerializer

    destroy:
    Delete own review only

    Filters: rating, is_verified_purchase, is_approved
    Search: title, review_text
    Ordering: created_at, helpful_count, rating

    Custom actions:
    - by_content: Get reviews for specific object
    - my_reviews: Get current user's reviews
    - mark_helpful: Vote review as helpful
    - report: Report inappropriate review
    - top_rated: Get highest rated reviews
    """
    queryset = Review.objects.filter(status='approved')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'is_verified_booking', 'status']
    search_fields = ['title', 'comment']
    ordering_fields = ['created_at', 'helpful_count', 'rating']
    ordering = ['-helpful_count', '-created_at']

    def get_serializer_class(self):
        """
        Use different serializers based on action
        - List: ReviewListSerializer (minimal data)
        - Detail: ReviewDetailSerializer (complete data)
        - Create: ReviewCreateSerializer (writable)
        - Update: ReviewUpdateSerializer (limited fields)
        """
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action == 'create':
            return ReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        return ReviewDetailSerializer

    def get_queryset(self):
        """
        Customize queryset based on user and filters
        """
        queryset = super().get_queryset()

        # Filter by content object
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                pass

        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

    def perform_create(self, serializer):
        """
        Override create to set user automatically
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Only allow users to update their own reviews
        """
        if serializer.instance.user != self.request.user:
            raise PermissionError("You can only edit your own reviews")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Only allow users to delete their own reviews
        """
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionError("You can only delete your own reviews")
        instance.delete()

    @action(detail=False, methods=['get'])
    def by_content(self, request):
        """
        Get reviews for specific content object

        GET /api/v1/reviews/reviews/by_content/?content_type=accommodation&object_id=1

        Query params:
        - content_type: Model name (accommodation, tour, route)
        - object_id: Object ID

        Returns all approved reviews for specified object
        """
        content_type = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')

        if not content_type or not object_id:
            return Response(
                {'error': 'content_type and object_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ct = ContentType.objects.get(model=content_type)
            reviews = self.queryset.filter(content_type=ct, object_id=object_id)
        except ContentType.DoesNotExist:
            return Response(
                {'error': 'Invalid content_type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paginate results
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        """
        Get current user's reviews

        GET /api/v1/reviews/reviews/my_reviews/

        Returns all reviews written by authenticated user
        """
        my_reviews = Review.objects.filter(user=request.user)

        page = self.paginate_queryset(my_reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        """
        Mark review as helpful or unhelpful

        POST /api/v1/reviews/reviews/{id}/mark_helpful/

        Body:
        {
            "is_helpful": true  // or false for unhelpful
        }

        Increments helpful_count or unhelpful_count
        """
        review = self.get_object()

        # Validate input
        serializer = ReviewHelpfulSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_helpful = serializer.validated_data['is_helpful']

        # Update counts
        with transaction.atomic():
            if is_helpful:
                review.helpful_count += 1
            else:
                review.not_helpful_count += 1
            review.save()

        return Response({
            'status': 'success',
            'helpful_count': review.helpful_count,
            'not_helpful_count': review.not_helpful_count
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def report(self, request, pk=None):
        """
        Report review as fake/inappropriate

        POST /api/v1/reviews/reviews/{id}/report/

        Body:
        {
            "reason": "fake",  // fake, spam, inappropriate, other
            "description": "This review seems fake because..."
        }

        Creates report for admin investigation
        """
        review = self.get_object()

        # Cannot report own review
        if review.user == request.user:
            return Response(
                {'error': 'Cannot report your own review'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already reported this review
        existing_report = ReviewReport.objects.filter(
            review=review,
            reported_by=request.user
        ).exists()

        if existing_report:
            return Response(
                {'error': 'You have already reported this review'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create report
        serializer = ReviewReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = ReviewReport.objects.create(
            review=review,
            reported_by=request.user,
            reason=serializer.validated_data['reason'],
            details=serializer.validated_data.get('description', '')
        )

        # Automatically set review to pending if multiple reports
        report_count = ReviewReport.objects.filter(review=review).count()
        if report_count >= 3:
            review.status = 'pending'
            review.moderation_notes = 'Multiple reports received - under review'
            review.save()

        return Response({
            'status': 'reported',
            'message': 'Review has been reported for investigation'
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def respond(self, request, pk=None):
        """
        Provider response to review

        POST /api/v1/reviews/reviews/{id}/respond/

        Body:
        {
            "response_text": "Thank you for your feedback. We apologize..."
        }

        Only providers can respond
        Creates/updates review response
        """
        review = self.get_object()

        # Check if user is provider (staff users can respond to reviews)
        if not request.user.is_staff:
            return Response(
                {'error': 'Only providers can respond to reviews'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if response already exists
        try:
            response = review.response
            response.response_text = request.data.get('response_text', '')
            response.responder = request.user
            response.save()
            message = 'Response updated successfully'
        except ReviewResponse.DoesNotExist:
            response = ReviewResponse.objects.create(
                review=review,
                responder=request.user,
                response_text=request.data.get('response_text', ''),
                is_approved=True  # Auto-approve provider responses
            )
            message = 'Response created successfully'

        serializer = ReviewResponseSerializer(response)
        return Response({
            'status': 'success',
            'message': message,
            'response': serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """
        Get highest rated reviews

        GET /api/v1/reviews/reviews/top_rated/?limit=10

        Query params:
        - limit: Number of reviews to return (default: 10)

        Returns reviews with highest ratings
        """
        limit = int(request.query_params.get('limit', 10))
        top_reviews = self.queryset.filter(
            rating=5
        ).order_by('-helpful_count')[:limit]

        serializer = self.get_serializer(top_reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def verified_only(self, request):
        """
        Get verified purchase reviews only

        GET /api/v1/reviews/reviews/verified_only/

        Returns only reviews from verified bookings
        """
        verified = self.queryset.filter(is_verified_booking=True)

        page = self.paginate_queryset(verified)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(verified, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_photos(self, request):
        """
        Get reviews with photos

        GET /api/v1/reviews/reviews/with_photos/

        Returns reviews that have uploaded images
        """
        with_photos = self.queryset.filter(images__isnull=False).distinct()

        page = self.paginate_queryset(with_photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(with_photos, many=True)
        return Response(serializer.data)


class ReviewReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for review reports (read-only for users, staff can moderate)

    list:
    Return all reports (staff only)

    retrieve:
    Return a single report (staff only)

    Users can only see reports they created
    Staff can see all reports
    """
    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['review', 'reason', 'is_reviewed']
    ordering = ['-reported_at']

    def get_queryset(self):
        """
        Filter based on user permissions
        """
        if self.request.user.is_staff:
            return ReviewReport.objects.all()
        return ReviewReport.objects.filter(reported_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resolve(self, request, pk=None):
        """
        Mark report as resolved (staff only)

        POST /api/v1/reviews/reports/{id}/resolve/

        Staff action to close investigation
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff can resolve reports'},
                status=status.HTTP_403_FORBIDDEN
            )

        report = self.get_object()
        report.is_reviewed = True
        report.reviewed_by = request.user
        from django.utils import timezone
        report.reviewed_at = timezone.now()
        report.save()

        return Response({
            'status': 'resolved',
            'message': 'Report marked as reviewed'
        })