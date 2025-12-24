"""
Custom template tags for optimized image handling.
Usage: {% load image_tags %}
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def optimized_img(src, alt="", css_class="", width="", height="", placeholder=""):
    """
    Renders an optimized image tag with lazy loading and placeholder.

    Usage:
        {% optimized_img image_url "Alt text" "img-fluid" "400" "300" %}
    """
    if not src:
        src = placeholder or "https://via.placeholder.com/400x300?text=No+Image"

    attrs = [
        f'src="{src}"',
        f'alt="{alt}"',
        'loading="lazy"',
        'decoding="async"',
    ]

    if css_class:
        attrs.append(f'class="{css_class}"')
    if width:
        attrs.append(f'width="{width}"')
    if height:
        attrs.append(f'height="{height}"')

    return mark_safe(f'<img {" ".join(attrs)}>')


@register.simple_tag
def responsive_img(src, alt="", css_class="", sizes=""):
    """
    Renders a responsive image with srcset for different screen sizes.
    Assumes Cloudinary or Unsplash URL that supports width parameters.

    Usage:
        {% responsive_img image_url "Alt text" "img-fluid" "(max-width: 768px) 100vw, 50vw" %}
    """
    if not src:
        return mark_safe('<img src="https://via.placeholder.com/800x600" alt="Placeholder" loading="lazy">')

    # Generate srcset for common breakpoints
    widths = [400, 600, 800, 1200]
    srcset_items = []

    for w in widths:
        if 'unsplash.com' in src:
            # Unsplash format
            modified_src = f"{src.split('?')[0]}?w={w}&q=80"
        elif 'cloudinary' in src.lower():
            # Cloudinary format - add width transformation
            modified_src = src.replace('/upload/', f'/upload/w_{w},q_auto/')
        else:
            # For other URLs, just use the original
            modified_src = src
        srcset_items.append(f"{modified_src} {w}w")

    srcset = ", ".join(srcset_items)
    sizes = sizes or "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"

    attrs = [
        f'src="{src}"',
        f'srcset="{srcset}"',
        f'sizes="{sizes}"',
        f'alt="{alt}"',
        'loading="lazy"',
        'decoding="async"',
    ]

    if css_class:
        attrs.append(f'class="{css_class}"')

    return mark_safe(f'<img {" ".join(attrs)}>')


@register.simple_tag
def background_img(src, fallback_color="#f0f0f0"):
    """
    Returns inline style for lazy-loaded background image.

    Usage:
        <div style="{% background_img image_url %}">
    """
    if not src:
        return mark_safe(f'background-color: {fallback_color};')

    return mark_safe(f'background-image: url({src}); background-size: cover; background-position: center;')


@register.inclusion_tag('includes/picture_element.html')
def picture(src, alt="", css_class="", webp_src=""):
    """
    Renders a picture element with WebP support.

    Usage:
        {% picture image_url "Alt text" "img-fluid" webp_url %}
    """
    return {
        'src': src,
        'webp_src': webp_src or src,  # Fallback to same src if no webp
        'alt': alt,
        'css_class': css_class,
    }


@register.filter
def cloudinary_optimize(url, transformation="w_800,q_auto,f_auto"):
    """
    Apply Cloudinary transformations to an image URL.

    Usage:
        {{ image_url|cloudinary_optimize:"w_400,q_80" }}
    """
    if not url or 'cloudinary' not in str(url).lower():
        return url

    # Insert transformation after /upload/
    if '/upload/' in url:
        return url.replace('/upload/', f'/upload/{transformation}/')
    return url


@register.filter
def unsplash_resize(url, size="800"):
    """
    Resize an Unsplash image URL.

    Usage:
        {{ image_url|unsplash_resize:"400" }}
    """
    if not url or 'unsplash.com' not in str(url):
        return url

    base = url.split('?')[0]
    return f"{base}?w={size}&q=80"
