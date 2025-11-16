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
import json

# Import models from other apps as needed
from accommodations.models import Accommodation
from tours.models import Tour
from destinations.models import Destination


def home(request):
    """
    Main homepage view
    Displays featured content and search forms
    """
    context = {
        'featured_accommodations': Accommodation.objects.filter(
            is_featured=True,
            is_active=True
        )[:6] if 'accommodations.Accommodation' in dir() else [],

        'featured_tours': Tour.objects.filter(
            is_featured=True,
            is_active=True
        )[:6] if 'tours.Tour' in dir() else [],

        'popular_destinations': Destination.objects.filter(
            is_popular=True
        )[:8] if 'destinations.Destination' in dir() else [],

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
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'Contact Form Submission')
        message = request.POST.get('message')

        # Validate form data
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html', {'form_data': request.POST})

        try:
            # Send email (configure email settings in settings.py)
            email_message = f"""
            New contact form submission from Egy360:

            Name: {name}
            Email: {email}
            Subject: {subject}

            Message:
            {message}
            """

            send_mail(
                f'Egy360 Contact: {subject}',
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['support@egy360.com'],  # Replace with your email
                fail_silently=False,
            )

            messages.success(request, 'Thank you for contacting us! We\'ll respond within 24 hours.')
            return redirect('home:contact')

        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
            return render(request, 'contact.html', {'form_data': request.POST})

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
    """FAQ page"""
    faqs = [
        {
            'question': 'Is Egy360 safe to use?',
            'answer': 'Yes! All our partners are verified and we guarantee secure transactions.'
        },
        {
            'question': 'How do I book accommodations?',
            'answer': 'Simply search for your destination, select dates, and choose from verified options.'
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept all major credit cards, debit cards, and PayPal.'
        },
        {
            'question': 'Can I cancel my booking?',
            'answer': 'Yes, you can cancel up to 24 hours before your booking for a full refund.'
        },
    ]

    return render(request, 'faq.html', {
        'page_title': 'Frequently Asked Questions - Egy360',
        'faqs': faqs,
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


# API endpoint for newsletter subscription (example)
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX"""
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'})

        # TODO: Add email to newsletter service (MailChimp, SendGrid, etc.)
        # For now, just return success

        return JsonResponse({
            'success': True,
            'message': 'Successfully subscribed to newsletter!'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        })


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
            destinations = Destination.objects.filter(
                name__icontains=query
            ).values('name', 'country')[:5]
            suggestions.extend([
                {'type': 'destination', 'name': d['name'], 'country': d['country']}
                for d in destinations
            ])

    return JsonResponse({'suggestions': suggestions})


# Stats for homepage (can be cached)
def get_platform_stats(request):
    """Get platform statistics for display"""
    stats = {
        'total_accommodations': Accommodation.objects.filter(
            is_active=True).count() if 'accommodations.Accommodation' in dir() else 250,
        'total_tours': Tour.objects.filter(is_active=True).count() if 'tours.Tour' in dir() else 150,
        'total_bookings': 5000,  # You can get this from bookings model
        'happy_customers': 50000,
    }
    return JsonResponse(stats)