# transportation/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TransportationService(models.Model):
    SERVICE_TYPES = [
        ('airport_transfer', 'Airport Transfer'),
        ('private_car', 'Private Car'),
        ('taxi', 'Taxi Service'),
        ('bus', 'Bus Tour'),
        ('minivan', 'Minivan'),
        ('limousine', 'Limousine'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()

    # Vehicle Details
    vehicle_model = models.CharField(max_length=100)
    max_passengers = models.IntegerField(validators=[MinValueValidator(1)])
    max_luggage = models.IntegerField(validators=[MinValueValidator(0)])

    # Features
    has_ac = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=False)
    has_gps = models.BooleanField(default=True)
    has_child_seat = models.BooleanField(default=False)

    # Pricing
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Availability - CHANGED from is_available to is_active
    is_active = models.BooleanField(default=True)

    # Images
    main_image = models.ImageField(upload_to='transportation/', null=True, blank=True)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-average_rating', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    # Credentials
    license_number = models.CharField(max_length=50)
    years_experience = models.IntegerField(default=0)

    # Languages
    languages_spoken = models.JSONField(default=list)

    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_trips = models.IntegerField(default=0)

    # Profile
    profile_image = models.ImageField(upload_to='drivers/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TransportBooking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_bookings')
    service = models.ForeignKey(TransportationService, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    # Pickup & Drop-off
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    # Passenger Details
    number_of_passengers = models.IntegerField()
    number_of_luggage = models.IntegerField(default=0)

    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')

    # Contact
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)

    # Special Requests
    special_requests = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.name} - {self.pickup_date}"