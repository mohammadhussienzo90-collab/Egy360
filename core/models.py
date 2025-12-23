"""
Core models for Egy360
Includes affiliate tracking and analytics models
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class AffiliateClick(models.Model):
    """
    Track all affiliate link clicks for revenue analytics
    """
    PLATFORM_CHOICES = [
        ('booking_com', 'Booking.com'),
        ('hotellook', 'Hotellook'),
        ('agoda', 'Agoda'),
        ('hotels_com', 'Hotels.com'),
        ('viator', 'Viator'),
        ('getyourguide', 'GetYourGuide'),
        ('travelpayouts', 'Travelpayouts'),
        ('aviasales', 'Aviasales'),
        ('discovercars', 'Discovercars'),
        ('world_nomads', 'World Nomads'),
        ('direct', 'Direct Booking'),
        ('other', 'Other'),
    ]

    ITEM_TYPE_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('tour', 'Tour'),
        ('flight', 'Flight'),
        ('transportation', 'Transportation'),
        ('insurance', 'Insurance'),
        ('car_rental', 'Car Rental'),
    ]

    # User tracking (nullable for anonymous users)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='affiliate_clicks'
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)

    # Click details
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)

    # Generic relation to the clicked item
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # URL and referrer
    affiliate_url = models.URLField(max_length=1000)
    referrer_url = models.URLField(max_length=500, blank=True, null=True)

    # Tracking data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)  # mobile, desktop, tablet

    # Revenue tracking
    estimated_commission = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated commission if booking completes"
    )
    converted = models.BooleanField(
        default=False,
        help_text="Whether this click resulted in a confirmed booking"
    )
    conversion_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual commission earned if converted"
    )

    # Timestamps
    clicked_at = models.DateTimeField(auto_now_add=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'affiliate_clicks'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['platform'], name='affiliate_platform_idx'),
            models.Index(fields=['item_type'], name='affiliate_item_type_idx'),
            models.Index(fields=['clicked_at'], name='affiliate_clicked_idx'),
            models.Index(fields=['user'], name='affiliate_user_idx'),
            models.Index(fields=['converted'], name='affiliate_converted_idx'),
        ]
        verbose_name = 'Affiliate Click'
        verbose_name_plural = 'Affiliate Clicks'

    def __str__(self):
        return f"{self.platform} - {self.item_type} - {self.clicked_at.strftime('%Y-%m-%d %H:%M')}"


class DailyRevenueSummary(models.Model):
    """
    Aggregated daily revenue statistics for dashboard
    """
    date = models.DateField(unique=True)

    # Click counts
    total_clicks = models.IntegerField(default=0)
    accommodation_clicks = models.IntegerField(default=0)
    tour_clicks = models.IntegerField(default=0)
    flight_clicks = models.IntegerField(default=0)
    other_clicks = models.IntegerField(default=0)

    # Platform breakdown
    booking_com_clicks = models.IntegerField(default=0)
    viator_clicks = models.IntegerField(default=0)
    other_platform_clicks = models.IntegerField(default=0)

    # Revenue estimates
    estimated_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    confirmed_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Conversion metrics
    conversions = models.IntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Traffic
    unique_visitors = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_revenue_summary'
        ordering = ['-date']
        verbose_name = 'Daily Revenue Summary'
        verbose_name_plural = 'Daily Revenue Summaries'

    def __str__(self):
        return f"Revenue Summary - {self.date}"
