# accommodations/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('camp', 'Desert Camp'),
        ('cruise', 'Nile Cruise'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)
    description = models.TextField()
    
    # Location
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Details
    star_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    total_rooms = models.IntegerField(default=1)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    
    # Pricing
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    weekend_surcharge = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Images
    main_image = models.ImageField(upload_to='accommodations/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct URL to hotel image (from Booking.com, etc.)")

    # Affiliate Links (for monetization)
    booking_com_id = models.CharField(max_length=100, blank=True, null=True, help_text="Booking.com property ID")
    booking_com_url = models.URLField(max_length=500, blank=True, null=True, help_text="Full Booking.com affiliate URL")
    agoda_url = models.URLField(max_length=500, blank=True, null=True, help_text="Agoda affiliate URL")
    hotels_com_url = models.URLField(max_length=500, blank=True, null=True, help_text="Hotels.com affiliate URL")
    direct_booking_url = models.URLField(max_length=500, blank=True, null=True, help_text="Hotel's direct booking URL")

    # Commission tracking
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Expected commission % (e.g., 4.0 for 4%)")
    total_bookings = models.IntegerField(default=0, help_text="Total bookings through this site")
    total_commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total commission earned ($)")

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-average_rating']

    def __str__(self):
        return f"{self.name} - {self.city}"

    def get_primary_booking_url(self):
        """Returns the primary affiliate booking URL (prioritizes Booking.com)"""
        if self.booking_com_url:
            return self.booking_com_url
        elif self.agoda_url:
            return self.agoda_url
        elif self.hotels_com_url:
            return self.hotels_com_url
        elif self.direct_booking_url:
            return self.direct_booking_url
        return None

    def has_booking_options(self):
        """Check if any booking links are available"""
        return bool(self.booking_com_url or self.agoda_url or self.hotels_com_url or self.direct_booking_url)

    def get_all_booking_options(self):
        """Returns all available booking options as a list of tuples (name, url)"""
        options = []
        if self.booking_com_url:
            options.append(('Booking.com', self.booking_com_url))
        if self.agoda_url:
            options.append(('Agoda', self.agoda_url))
        if self.hotels_com_url:
            options.append(('Hotels.com', self.hotels_com_url))
        if self.direct_booking_url:
            options.append(('Hotel Direct', self.direct_booking_url))
        return options

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('twin', 'Twin Room'),
        ('suite', 'Suite'),
        ('family', 'Family Room'),
        ('deluxe', 'Deluxe Room'),
    ]
    
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Capacity
    max_occupancy = models.IntegerField()
    beds = models.CharField(max_length=100)
    room_size = models.IntegerField(help_text="Size in square meters", null=True, blank=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Availability
    total_rooms = models.IntegerField(default=1)
    available_rooms = models.IntegerField(default=1)
    
    # Features
    has_air_conditioning = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_minibar = models.BooleanField(default=False)
    has_safe = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.accommodation.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    accommodations = models.ManyToManyField(Accommodation, related_name='amenities')
    
    class Meta:
        verbose_name_plural = 'Amenities'
    
    def __str__(self):
        return self.name