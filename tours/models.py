# tours/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tour(models.Model):
    TOUR_TYPES = [
        ('cultural', 'Cultural & Historical'),
        ('adventure', 'Adventure'),
        ('desert', 'Desert Safari'),
        ('cruise', 'Nile Cruise'),
        ('diving', 'Diving & Snorkeling'),
        ('religious', 'Religious'),
        ('luxury', 'Luxury'),
        ('budget', 'Budget'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES)
    description = models.TextField()
    highlights = models.TextField()

    # Duration
    duration_days = models.IntegerField(default=1)
    duration_nights = models.IntegerField(default=0)

    # Logistics
    departure_city = models.CharField(max_length=100)
    destinations = models.JSONField(default=list)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='easy')

    # Group Details
    min_group_size = models.IntegerField(default=1)
    max_group_size = models.IntegerField(default=20)

    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    child_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Includes/Excludes
    includes = models.JSONField(default=list)
    excludes = models.JSONField(default=list)

    # Languages
    languages = models.JSONField(default=list)

    # Images
    main_image = models.ImageField(upload_to='tours/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct URL to tour image")

    # Affiliate Links (for monetization)
    viator_url = models.URLField(max_length=500, blank=True, null=True, help_text="Viator affiliate URL")
    getyourguide_url = models.URLField(max_length=500, blank=True, null=True, help_text="GetYourGuide affiliate URL")
    travelpayouts_url = models.URLField(max_length=500, blank=True, null=True, help_text="Travelpayouts tours URL")

    # Commission tracking
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Expected commission % (e.g., 8.0 for 8%)")
    total_affiliate_clicks = models.IntegerField(default=0, help_text="Total clicks to affiliate links")
    total_commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total commission earned ($)")

    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    booking_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-average_rating']
        indexes = [
            models.Index(fields=['tour_type'], name='tour_type_idx'),
            models.Index(fields=['is_active'], name='tour_active_idx'),
            models.Index(fields=['is_featured'], name='tour_featured_idx'),
            models.Index(fields=['departure_city'], name='tour_departure_idx'),
            models.Index(fields=['average_rating'], name='tour_rating_idx'),
            models.Index(fields=['is_active', 'tour_type'], name='tour_filter_idx'),
        ]

    def __str__(self):
        return self.name

    def get_primary_affiliate_url(self):
        """Returns the primary affiliate booking URL (prioritizes Viator)"""
        if self.viator_url:
            return self.viator_url
        elif self.getyourguide_url:
            return self.getyourguide_url
        elif self.travelpayouts_url:
            return self.travelpayouts_url
        return None

    def has_affiliate_options(self):
        """Check if any affiliate links are available"""
        return bool(self.viator_url or self.getyourguide_url or self.travelpayouts_url)

    def get_all_affiliate_options(self):
        """Returns all available affiliate options as a list of dicts"""
        options = []
        if self.viator_url:
            options.append({'platform': 'Viator', 'url': self.viator_url, 'commission': '8%'})
        if self.getyourguide_url:
            options.append({'platform': 'GetYourGuide', 'url': self.getyourguide_url, 'commission': '8%'})
        if self.travelpayouts_url:
            options.append({'platform': 'Travelpayouts', 'url': self.travelpayouts_url, 'commission': '5%'})
        return options

class TourItinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary')
    day = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    meals_included = models.CharField(max_length=100, blank=True)
    overnight_location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['day']
        verbose_name_plural = 'Tour Itineraries'

    def __str__(self):
        return f"Day {self.day}: {self.title}"

class TourBooking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour_bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_bookings')

    # Booking Details
    booking_date = models.DateTimeField(auto_now_add=True)
    tour_date = models.DateField()
    number_of_adults = models.IntegerField(default=1)
    number_of_children = models.IntegerField(default=0)

    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')

    # Contact
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Special Requests
    special_requests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tour.name} - {self.user.username} - {self.tour_date}"