# reviews/templatetags/review_tags.py
"""
Custom template tags and filters for the reviews app.
Usage: {% load review_tags %}
"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a variable key.

    Usage:
        {{ my_dict|get_item:key_variable }}

    Example:
        {% for i in "54321" %}
            Count: {{ distribution|get_item:i }}
        {% endfor %}
    """
    if dictionary is None:
        return 0

    # Try to convert key to int if it's a string digit
    try:
        if isinstance(key, str) and key.isdigit():
            key = int(key)
    except (ValueError, AttributeError):
        pass

    # Try to get from dictionary
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)

    return 0


@register.filter
def star_range(value):
    """
    Return a range for star display.

    Usage:
        {% for i in rating|star_range %}
            <i class="fas fa-star"></i>
        {% endfor %}
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_star_range(value, max_stars=5):
    """
    Return a range for empty stars (remaining after filled).

    Usage:
        {% for i in rating|empty_star_range:5 %}
            <i class="far fa-star"></i>
        {% endfor %}
    """
    try:
        filled = int(value)
        return range(max_stars - filled)
    except (ValueError, TypeError):
        return range(max_stars)


@register.simple_tag
def review_stars(rating, max_rating=5):
    """
    Render star rating HTML.

    Usage:
        {% review_stars review.rating %}
    """
    from django.utils.safestring import mark_safe

    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = max_rating - full_stars - half_star

    html = ''
    html += '<i class="fas fa-star text-warning"></i>' * full_stars
    if half_star:
        html += '<i class="fas fa-star-half-alt text-warning"></i>'
    html += '<i class="far fa-star text-warning"></i>' * empty_stars

    return mark_safe(html)
