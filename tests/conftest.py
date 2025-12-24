"""
Pytest Configuration and Fixtures
Provides common fixtures and configuration for the test suite
"""
import pytest
from django.contrib.auth.models import User
from decimal import Decimal


@pytest.fixture
def test_user(db):
    """Create a standard test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def authenticated_client(client, test_user):
    """Return a client logged in as test_user"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Return a client logged in as admin"""
    client.login(username='admin', password='adminpass123')
    return client


@pytest.fixture
def sample_accommodation(db):
    """Create a sample accommodation"""
    from accommodations.models import Accommodation
    return Accommodation.objects.create(
        name="Test Hotel",
        slug="test-hotel",
        accommodation_type="hotel",
        description="A test hotel",
        city="Cairo",
        address="123 Test Street",
        price_per_night=Decimal("150.00"),
        is_active=True
    )


@pytest.fixture
def sample_tour(db):
    """Create a sample tour"""
    from tours.models import Tour
    return Tour.objects.create(
        name="Test Tour",
        slug="test-tour",
        tour_type="cultural",
        description="A test tour",
        highlights="Test highlights",
        departure_city="Cairo",
        price_per_person=Decimal("89.00"),
        is_active=True
    )


@pytest.fixture
def sample_newsletter_subscription(db):
    """Create a sample newsletter subscription"""
    from home.models import NewsletterSubscription
    return NewsletterSubscription.objects.create(
        email='subscriber@example.com',
        name='Test Subscriber',
        is_active=True
    )
