"""
Context processors for making settings available in templates
"""
from django.conf import settings


def analytics(request):
    """
    Makes Google Analytics ID available in all templates
    """
    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', '')
    }
