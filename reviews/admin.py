"""
Reviews Admin - Corrected
Path: reviews/admin.py

Fixed: Correct model imports (Review, not ReviewRating)
"""

from django.contrib import admin
from .models import (
    Review,
    ReviewImage,
    ReviewResponse,
    ReviewHelpful,
    ReviewReport
)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'rating', 'status', 'is_verified_booking', 'created_at']
    list_filter = ['status', 'rating', 'is_verified_booking', 'created_at']
    search_fields = ['user__username', 'title', 'comment', 'booking_reference']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count', 'not_helpful_count']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'content_type', 'object_id', 'title', 'comment')
        }),
        ('Ratings', {
            'fields': ('rating', 'cleanliness_rating', 'location_rating', 'value_rating', 'service_rating')
        }),
        ('Verification', {
            'fields': ('is_verified_booking', 'booking_reference')
        }),
        ('Status', {
            'fields': ('status', 'moderated_by', 'moderated_at', 'moderation_notes')
        }),
        ('Engagement', {
            'fields': ('helpful_count', 'not_helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        for review in queryset:
            review.approve(request.user)
        self.message_user(request, f"{queryset.count()} reviews approved.")

    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        for review in queryset:
            review.reject(request.user)
        self.message_user(request, f"{queryset.count()} reviews rejected.")

    reject_reviews.short_description = "Reject selected reviews"


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'caption']


@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ['review', 'responded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__title', 'response_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'is_helpful', 'created_at']
    list_filter = ['is_helpful', 'created_at']
    search_fields = ['review__title', 'user__username']
    readonly_fields = ['created_at']


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ['review', 'reason', 'reported_by', 'is_reviewed', 'reported_at']
    list_filter = ['reason', 'is_reviewed', 'reported_at']
    search_fields = ['review__title', 'reported_by__username', 'details']
    readonly_fields = ['reported_at', 'reviewed_at']

    fieldsets = (
        ('Report Information', {
            'fields': ('review', 'reported_by', 'reason', 'details')
        }),
        ('Review Status', {
            'fields': ('is_reviewed', 'reviewed_by', 'reviewed_at', 'action_taken')
        }),
        ('Timestamps', {
            'fields': ('reported_at',)
        }),
    )