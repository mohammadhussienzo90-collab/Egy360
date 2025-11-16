# destinations/models.py
from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True)
    flag_emoji = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Details
    population = models.IntegerField(null=True, blank=True)
    elevation = models.IntegerField(help_text="Elevation in meters", null=True, blank=True)
    timezone = models.CharField(max_length=50, default='Africa/Cairo')

    # Tourism Info
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    average_temperature_summer = models.IntegerField(null=True, blank=True)
    average_temperature_winter = models.IntegerField(null=True, blank=True)

    # Features
    is_popular = models.BooleanField(default=False)
    is_capital = models.BooleanField(default=False)
    has_airport = models.BooleanField(default=False)

    # Images
    main_image = models.ImageField(upload_to='cities/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Attraction(models.Model):
    ATTRACTION_TYPES = [
        ('historical', 'Historical Site'),
        ('museum', 'Museum'),
        ('religious', 'Religious Site'),
        ('natural', 'Natural Wonder'),
        ('beach', 'Beach'),
        ('market', 'Market/Bazaar'),
        ('modern', 'Modern Attraction'),
        ('archaeological', 'Archaeological Site'),
    ]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    attraction_type = models.CharField(max_length=20, choices=ATTRACTION_TYPES)
    description = models.TextField()

    # Location
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Visit Information
    opening_hours = models.TextField(blank=True)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    visit_duration = models.CharField(max_length=50, help_text="e.g., 2-3 hours", blank=True)

    # Features
    is_unesco = models.BooleanField(default=False)
    is_must_see = models.BooleanField(default=False)
    is_family_friendly = models.BooleanField(default=True)
    accessibility_info = models.TextField(blank=True)

    # Images
    main_image = models.ImageField(upload_to='attractions/', null=True, blank=True)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_must_see', 'name']

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class TravelGuide(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='guides')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Categories
    is_transportation = models.BooleanField(default=False)
    is_accommodation = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)
    is_safety = models.BooleanField(default=False)
    is_culture = models.BooleanField(default=False)

    # SEO
    meta_description = models.CharField(max_length=160, blank=True)

    # Publishing
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city.name}"