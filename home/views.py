"""
Views for the Home app - Main pages of Egy360
Handles homepage, about, contact, and error pages
"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

# Import models from other apps as needed
from accommodations.models import Accommodation
from tours.models import Tour
from destinations.models import City
from .models import NewsletterSubscription, ContactMessage, FAQItem


def home(request):
    """
    Main homepage view
    Displays featured content and search forms
    """
    context = {
        'featured_accommodations': Accommodation.objects.filter(
            is_featured=True,
            is_active=True
        )[:6],

        'featured_tours': Tour.objects.filter(
            is_featured=True,
            is_active=True
        )[:6],

        'popular_destinations': City.objects.filter(
            is_popular=True
        )[:8],

        'page_title': 'Egy360 - Discover Egypt Safely',
        'meta_description': 'Egypt\'s premier tourism platform. Find verified accommodations, tours, and transportation at the best prices.',
    }

    # Handle search form if submitted via GET
    if request.GET.get('search_type'):
        search_type = request.GET.get('search_type')
        if search_type == 'accommodations':
            return redirect('accommodations:accommodation-search', query_params=request.GET.urlencode())
        elif search_type == 'tours':
            return redirect('tours:tour-list', query_params=request.GET.urlencode())
        elif search_type == 'transportation':
            return redirect('transportation:transport-search', query_params=request.GET.urlencode())

    return render(request, 'home.html', context)


def about(request):
    """About page view"""
    context = {
        'page_title': 'About Egy360 - Your Trusted Egypt Travel Partner',
        'meta_description': 'Learn about Egy360, Egypt\'s leading tourism platform dedicated to providing safe, verified, and affordable travel experiences.',
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', 'General Inquiry').strip()
        message_text = request.POST.get('message', '').strip()

        # Validate form data
        if not all([name, email, message_text]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html', {'form_data': request.POST})

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'contact.html', {'form_data': request.POST})

        # Save message to database (always works, doesn't depend on email config)
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text,
        )

        # Try to send email notification (optional, fails silently)
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@360egy.com')
            send_mail(
                f'Egy360 Contact: {subject}',
                f"New contact from {name} ({email}):\n\n{message_text}",
                from_email,
                ['info@360egy.com'],
                fail_silently=True,  # Don't fail if email doesn't work
            )
        except Exception:
            pass  # Email is optional, message is already saved to DB

        messages.success(request, 'Thank you for contacting us! We\'ll respond within 24 hours.')
        return redirect('home:contact')

    context = {
        'page_title': 'Contact Egy360 - Get in Touch',
        'meta_description': 'Contact Egy360 for any questions about Egypt travel, bookings, or partnerships.',
    }
    return render(request, 'contact.html', context)


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'privacy_policy.html', {
        'page_title': 'Privacy Policy - Egy360',
    })


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'terms_of_service.html', {
        'page_title': 'Terms of Service - Egy360',
    })


def faq(request):
    """FAQ page with database-driven content"""
    # Get FAQs from database, grouped by category
    faqs = FAQItem.objects.filter(is_active=True)

    # Group FAQs by category
    faq_categories = {}
    for faq_item in faqs:
        category = faq_item.get_category_display()
        if category not in faq_categories:
            faq_categories[category] = []
        faq_categories[category].append(faq_item)

    return render(request, 'faq.html', {
        'page_title': 'Frequently Asked Questions - Egy360',
        'faq_categories': faq_categories,
        'faqs': faqs,  # Also pass flat list for backwards compatibility
    })


# Error handlers
def error_404(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)


def error_403(request, exception):
    """Custom 403 error page"""
    return render(request, '403.html', status=403)


# API endpoint for newsletter subscription
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()

        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address'}, status=400)

        # Check if already subscribed
        existing = NewsletterSubscription.objects.filter(email=email).first()
        if existing:
            if existing.is_active:
                return JsonResponse({
                    'success': True,
                    'message': 'You are already subscribed to our newsletter!'
                })
            else:
                # Reactivate subscription
                existing.is_active = True
                existing.unsubscribed_at = None
                existing.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Welcome back! Your subscription has been reactivated.'
                })

        # Create new subscription
        subscription = NewsletterSubscription.objects.create(email=email, name=name)

        # Send welcome email
        try:
            from core.email import send_newsletter_welcome
            send_newsletter_welcome(subscription)
        except Exception:
            pass  # Don't fail if email fails

        return JsonResponse({
            'success': True,
            'message': 'Successfully subscribed to newsletter!'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)


# Quick search autocomplete API
def search_autocomplete(request):
    """Provide autocomplete suggestions for search"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')

    suggestions = []

    if len(query) >= 2:
        if search_type in ['all', 'accommodations']:
            # Add accommodation suggestions
            accommodations = Accommodation.objects.filter(
                name__icontains=query,
                is_active=True
            ).values('name', 'city')[:5]
            suggestions.extend([
                {'type': 'accommodation', 'name': a['name'], 'city': a['city']}
                for a in accommodations
            ])

        if search_type in ['all', 'tours']:
            # Add tour suggestions
            tours = Tour.objects.filter(
                title__icontains=query,
                is_active=True
            ).values('title', 'duration')[:5]
            suggestions.extend([
                {'type': 'tour', 'name': t['title'], 'duration': t['duration']}
                for t in tours
            ])

        if search_type in ['all', 'destinations']:
            # Add destination suggestions
            cities = City.objects.filter(
                name__icontains=query
            ).select_related('country').values('name', 'country__name')[:5]
            suggestions.extend([
                {'type': 'destination', 'name': c['name'], 'country': c['country__name']}
                for c in cities
            ])

    return JsonResponse({'suggestions': suggestions})


# Stats for homepage (can be cached)
def get_platform_stats(request):
    """Get platform statistics for display"""
    stats = {
        'total_accommodations': Accommodation.objects.filter(is_active=True).count(),
        'total_tours': Tour.objects.filter(is_active=True).count(),
        'total_bookings': 5000,  # You can get this from bookings model
        'happy_customers': 50000,
    }
    return JsonResponse(stats)