"""
SEO utilities for 360egy.com
Dynamic sitemap generation, robots.txt, and structured data helpers
"""
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime, timedelta
import json


def generate_sitemap(request):
    """
    Generate dynamic XML sitemap for search engines
    Includes all pages, blog posts, destinations, tours, and hotels
    """
    root = Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    root.set('xmlns:news', 'http://www.google.com/schemas/sitemap-news/0.9')

    base_url = 'https://360egy.com'
    now = timezone.now()

    # Static pages with high priority
    static_pages = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': '/blog/', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/destinations/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': '/tours/', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/accommodations/', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/flights/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': '/transportation/', 'priority': '0.7', 'changefreq': 'weekly'},
        {'loc': '/hotels-search/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'loc': '/about/', 'priority': '0.5', 'changefreq': 'monthly'},
        {'loc': '/contact/', 'priority': '0.5', 'changefreq': 'monthly'},
        {'loc': '/faq/', 'priority': '0.6', 'changefreq': 'monthly'},
        {'loc': '/terms/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'loc': '/privacy/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'loc': '/affiliate-disclosure/', 'priority': '0.3', 'changefreq': 'yearly'},
    ]

    for page in static_pages:
        url = SubElement(root, 'url')
        SubElement(url, 'loc').text = base_url + page['loc']
        SubElement(url, 'lastmod').text = now.strftime('%Y-%m-%d')
        SubElement(url, 'changefreq').text = page['changefreq']
        SubElement(url, 'priority').text = page['priority']

    # Blog posts
    try:
        from blog.models import BlogPost
        posts = BlogPost.objects.filter(status='published').order_by('-published_at')
        for post in posts:
            url = SubElement(root, 'url')
            SubElement(url, 'loc').text = f"{base_url}/blog/{post.slug}/"
            if post.updated_at:
                SubElement(url, 'lastmod').text = post.updated_at.strftime('%Y-%m-%d')
            elif post.published_at:
                SubElement(url, 'lastmod').text = post.published_at.strftime('%Y-%m-%d')
            SubElement(url, 'changefreq').text = 'weekly'
            SubElement(url, 'priority').text = '0.8' if post.is_featured else '0.7'

            # Add image if available
            if post.image_url:
                image = SubElement(url, 'image:image')
                SubElement(image, 'image:loc').text = post.image_url
                SubElement(image, 'image:title').text = post.title[:100]
    except Exception as e:
        print(f"Sitemap blog error: {e}")

    # Destinations
    try:
        from destinations.models import City, Attraction
        cities = City.objects.filter(is_active=True)
        for city in cities:
            url = SubElement(root, 'url')
            SubElement(url, 'loc').text = f"{base_url}/destinations/{city.slug}/"
            SubElement(url, 'changefreq').text = 'weekly'
            SubElement(url, 'priority').text = '0.8'

        attractions = Attraction.objects.filter(is_active=True)
        for attraction in attractions:
            url = SubElement(root, 'url')
            SubElement(url, 'loc').text = f"{base_url}/destinations/attraction/{attraction.slug}/"
            SubElement(url, 'changefreq').text = 'weekly'
            SubElement(url, 'priority').text = '0.7'
    except Exception as e:
        print(f"Sitemap destinations error: {e}")

    # Tours
    try:
        from tours.models import Tour
        tours = Tour.objects.filter(is_active=True)
        for tour in tours:
            url = SubElement(root, 'url')
            SubElement(url, 'loc').text = f"{base_url}/tours/{tour.slug}/"
            SubElement(url, 'changefreq').text = 'weekly'
            SubElement(url, 'priority').text = '0.7'
    except Exception as e:
        print(f"Sitemap tours error: {e}")

    # Accommodations
    try:
        from accommodations.models import Accommodation
        hotels = Accommodation.objects.filter(is_active=True)
        for hotel in hotels:
            url = SubElement(root, 'url')
            SubElement(url, 'loc').text = f"{base_url}/accommodations/{hotel.slug}/"
            SubElement(url, 'changefreq').text = 'weekly'
            SubElement(url, 'priority').text = '0.7'
    except Exception as e:
        print(f"Sitemap accommodations error: {e}")

    xml_content = tostring(root, encoding='unicode')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'

    return HttpResponse(
        xml_declaration + xml_content,
        content_type='application/xml'
    )


def robots_txt(request):
    """
    Generate robots.txt for search engine crawlers
    """
    content = """# robots.txt for 360egy.com
# Egypt's Premier Travel Platform

User-agent: *
Allow: /

# Sitemap location
Sitemap: https://360egy.com/sitemap.xml

# Crawl-delay for politeness
Crawl-delay: 1

# Disallow admin and private areas
Disallow: /admin/
Disallow: /dashboard/
Disallow: /accounts/
Disallow: /api/
Disallow: /static/admin/

# Allow static assets
Allow: /static/css/
Allow: /static/js/
Allow: /static/images/

# Allow specific bots full access
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: Pinterest
Allow: /

# Block bad bots
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: MJ12bot
Disallow: /
"""
    return HttpResponse(content, content_type='text/plain')


def generate_faq_schema(faqs):
    """
    Generate FAQ structured data schema
    faqs: list of dicts with 'question' and 'answer' keys
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }

    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['answer']
            }
        })

    return json.dumps(schema, indent=2)


def generate_howto_schema(title, description, steps, total_time=None, image=None):
    """
    Generate HowTo structured data schema
    steps: list of dicts with 'name' and 'text' keys
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "description": description,
        "step": []
    }

    if total_time:
        schema["totalTime"] = total_time

    if image:
        schema["image"] = image

    for i, step in enumerate(steps, 1):
        schema["step"].append({
            "@type": "HowToStep",
            "position": i,
            "name": step['name'],
            "text": step['text']
        })

    return json.dumps(schema, indent=2)


def generate_local_business_schema():
    """
    Generate LocalBusiness structured data for 360egy
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": "Egy360",
        "alternateName": "360egy",
        "url": "https://360egy.com",
        "logo": "https://360egy.com/static/images/logo.png",
        "image": "https://360egy.com/static/images/og-image.jpg",
        "description": "Egypt's premier travel platform. Book verified hotels, tours, flights, and transportation across Cairo, Luxor, Aswan, and all of Egypt.",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "EG",
            "addressLocality": "Cairo",
            "addressRegion": "Cairo Governorate"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "30.0444",
            "longitude": "31.2357"
        },
        "areaServed": {
            "@type": "Country",
            "name": "Egypt"
        },
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "sameAs": [
            "https://www.facebook.com/egy360travel",
            "https://www.instagram.com/egy360travel",
            "https://twitter.com/egy360travel",
            "https://www.tiktok.com/@egy360travel",
            "https://www.pinterest.com/egy360travel"
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Egypt Travel Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Hotel Booking",
                        "description": "Book verified hotels across Egypt"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Tour Packages",
                        "description": "Guided tours to pyramids, temples, and more"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Nile Cruises",
                        "description": "Luxury Nile cruise experiences"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Airport Transfers",
                        "description": "Safe and reliable airport transportation"
                    }
                }
            ]
        }
    }

    return json.dumps(schema, indent=2)


def generate_product_schema(name, description, image, price, currency='USD', url=None, rating=None, review_count=None):
    """
    Generate Product structured data for tours/packages
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description,
        "image": image,
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": currency,
            "availability": "https://schema.org/InStock"
        }
    }

    if url:
        schema["url"] = url

    if rating and review_count:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": rating,
            "reviewCount": review_count
        }

    return json.dumps(schema, indent=2)


# Common Egypt Travel FAQs for schema
EGYPT_TRAVEL_FAQS = [
    {
        "question": "Do I need a visa to visit Egypt?",
        "answer": "Most nationalities can obtain a visa on arrival at Egyptian airports for $25 USD, valid for 30 days. Some countries are eligible for e-visa applications online before travel. EU, US, UK, Canadian, and Australian citizens can get visa on arrival."
    },
    {
        "question": "What is the best time to visit Egypt?",
        "answer": "The best time to visit Egypt is from October to April when temperatures are cooler, ranging from 20-25°C (68-77°F). Summer months (June-August) can be extremely hot, especially in Upper Egypt, with temperatures exceeding 40°C (104°F)."
    },
    {
        "question": "Is Egypt safe for tourists?",
        "answer": "Yes, Egypt is generally safe for tourists. Major tourist areas like Cairo, Luxor, Aswan, and Red Sea resorts have strong security presence. Follow standard travel precautions, stay in tourist areas, and use reputable tour operators."
    },
    {
        "question": "What currency is used in Egypt?",
        "answer": "The Egyptian Pound (EGP) is the official currency. US Dollars and Euros are widely accepted at hotels, tourist shops, and for tours. ATMs are available in major cities. Credit cards are accepted at hotels and larger establishments."
    },
    {
        "question": "How many days do I need to see Egypt?",
        "answer": "A minimum of 7-10 days is recommended to see the highlights: Cairo and Giza (2-3 days), Luxor (2-3 days), Aswan (1-2 days), and optionally the Red Sea (2-3 days). A Nile cruise between Luxor and Aswan takes 3-4 days."
    },
    {
        "question": "What should I wear when visiting Egypt?",
        "answer": "Dress modestly, especially when visiting mosques and religious sites. Women should cover shoulders and knees. Light, loose-fitting cotton clothing is best for the heat. Comfortable walking shoes are essential for ancient sites."
    },
    {
        "question": "Can I drink tap water in Egypt?",
        "answer": "No, it's not recommended to drink tap water in Egypt. Bottled water is inexpensive and widely available. Use bottled water for drinking and brushing teeth. Ice in tourist restaurants is usually made from purified water."
    },
    {
        "question": "How do I get from Cairo to Luxor?",
        "answer": "Options include: domestic flights (1 hour, from $50), overnight sleeper train (10 hours, comfortable and scenic), or private car/bus (8-10 hours). Flights are fastest, while trains offer a unique experience of Egyptian countryside."
    }
]
