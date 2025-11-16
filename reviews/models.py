"""
Reviews Models - Complete and Corrected
Path: reviews/models.py

All user references use Django's built-in User model (not CustomUser)
Generic review system for accommodations and tours
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Review(models.Model):
    """
    Generic review model - can review accommodations or tours
    Uses ContentType for polymorphic relationships
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Moderation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # User who wrote the review
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    # Polymorphic relationship - can review accommodation or tour
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Review content
    title = models.CharField(max_length=200)
    comment = models.TextField()

    # Overall rating
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall rating (1-5 stars)"
    )

    # Detailed ratings
    cleanliness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    location_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    value_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    service_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

    # Verification
    is_verified_booking = models.BooleanField(
        default=False,
        help_text="Review from verified booking"
    )
    booking_reference = models.CharField(max_length=20, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Moderation
    moderated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_reviews'
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    moderation_notes = models.TextField(blank=True)

    # Helpful votes
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'status']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['-rating', '-created_at']),
        ]
        # Ensure one review per user per object
        unique_together = ['user', 'content_type', 'object_id']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def average_detailed_rating(self):
        """Calculate average of detailed ratings"""
        ratings = [
            self.cleanliness_rating,
            self.location_rating,
            self.value_rating,
            self.service_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return self.rating

    def approve(self, moderator):
        """Approve the review"""
        self.status = 'approved'
        self.moderated_by = moderator
        self.moderated_at = timezone.now()
        self.save()

        # Update the related object's rating
        self.update_object_rating()

    def reject(self, moderator, notes=''):
        """Reject the review"""
        self.status = 'rejected'
        self.moderated_by = moderator
        self.moderated_at = timezone.now()
        self.moderation_notes = notes
        self.save()

    def update_object_rating(self):
        """Update the average rating of the reviewed object"""
        # Get all approved reviews for this object
        approved_reviews = Review.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            status='approved'
        )

        if approved_reviews.exists():
            avg_rating = approved_reviews.aggregate(
                models.Avg('rating')
            )['rating__avg']

            total_reviews = approved_reviews.count()

            # Update the object's rating
            obj = self.content_object
            if hasattr(obj, 'average_rating'):
                obj.average_rating = round(avg_rating, 2)
            if hasattr(obj, 'total_reviews'):
                obj.total_reviews = total_reviews
            obj.save()


class ReviewImage(models.Model):
    """
    Images attached to reviews
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review Image'
        verbose_name_plural = 'Review Images'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for review: {self.review.title}"


class ReviewResponse(models.Model):
    """
    Property owner/operator response to reviews
    """
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')

    # Response content
    response_text = models.TextField()

    # Responder (property owner or admin)
    responded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_responses')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review Response'
        verbose_name_plural = 'Review Responses'
        ordering = ['-created_at']

    def __str__(self):
        return f"Response to: {self.review.title}"


class ReviewHelpful(models.Model):
    """
    Track which users found a review helpful
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpful_votes')
    is_helpful = models.BooleanField(help_text="True if helpful, False if not helpful")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review Helpful Vote'
        verbose_name_plural = 'Review Helpful Votes'
        unique_together = ['review', 'user']

    def __str__(self):
        vote_type = "helpful" if self.is_helpful else "not helpful"
        return f"{self.user.username} found review {vote_type}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the review's helpful counts
        self.review.helpful_count = self.review.helpful_votes.filter(is_helpful=True).count()
        self.review.not_helpful_count = self.review.helpful_votes.filter(is_helpful=False).count()
        self.review.save()


class ReviewReport(models.Model):
    """
    Reports for inappropriate reviews
    """
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('offensive', 'Offensive Language'),
        ('fake', 'Fake Review'),
        ('irrelevant', 'Irrelevant Content'),
        ('personal_info', 'Contains Personal Information'),
        ('other', 'Other'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_reports')

    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True)

    # Status
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports'
    )
    action_taken = models.TextField(blank=True)

    # Timestamps
    reported_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Review Report'
        verbose_name_plural = 'Review Reports'
        ordering = ['-reported_at']

    def __str__(self):
        return f"Report on review: {self.review.title}"