"""
Content generation engine for Egy360 social media posts.

Creates platform-optimized captions and hashtags from BlogPost data
for Pinterest, Facebook, and Instagram.
"""

import re


# ---------------------------------------------------------------------------
# Hashtag banks
# ---------------------------------------------------------------------------

UNIVERSAL_HASHTAGS = [
    "#egypt", "#egypttravel", "#visitegypt", "#travelegypt", "#360egy",
]

PLATFORM_HASHTAGS = {
    "pinterest": [
        "#travelinspiration", "#bucketlist", "#travelguide",
        "#traveltips", "#wanderlust", "#exploremore",
    ],
    "facebook": [
        "#travel", "#explore", "#adventure", "#tourism", "#history",
    ],
    "instagram": [
        "#travelgram", "#instatravel", "#igtravel", "#travelphoto",
        "#travelblogger", "#traveltheworld", "#globetrotter",
        "#explorepage", "#beautifuldestinations", "#passportready",
        "#doyoutravel", "#traveladdict", "#welltravelled",
        "#travelphotography", "#seetheworld", "#travellife",
    ],
}

CATEGORY_HASHTAGS = {
    "Ancient Egypt":      ["#ancientegypt", "#pharaohs", "#pyramids", "#egyptology"],
    "Modern Egypt":       ["#modernegypt", "#cairo", "#egyptlife", "#cairolife"],
    "Egyptian Culture":   ["#egyptianculture", "#arabculture", "#middleeast", "#northafrica"],
    "Travel Guide":       ["#egyptguide", "#travelguide", "#egypttips", "#traveltips"],
    "Egyptian Food":      ["#egyptianfood", "#middleeasternfood", "#arabfood", "#foodie"],
    "Egyptian History":   ["#egyptianhistory", "#historylovers", "#ancienthistory", "#archaeology"],
    "Nile River":         ["#nileriver", "#nilecruise", "#luxor", "#aswan"],
    "Red Sea":            ["#redsea", "#hurghada", "#sharmelsheikh", "#diving", "#snorkeling"],
    "Desert & Oasis":     ["#sahara", "#whitedesert", "#siwa", "#desertlife"],
    "Islamic Heritage":   ["#islamicart", "#islamicarchitecture", "#mosque", "#islamicheritage"],
    "Coptic Heritage":    ["#copticegypt", "#copticart", "#copticchurch", "#christianegypt"],
}

# Default max hashtag counts per platform.
DEFAULT_MAX_HASHTAGS = {
    "pinterest": 15,
    "facebook": 5,
    "instagram": 30,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def strip_html(text):
    """Remove HTML tags from *text* and collapse extra whitespace."""
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def truncate(text, max_length):
    """Truncate *text* to *max_length* characters at a word boundary."""
    if not text or len(text) <= max_length:
        return text or ""
    truncated = text[:max_length]
    # Cut back to the last space so we don't split a word.
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated.rstrip() + "..."


# ---------------------------------------------------------------------------
# Hashtag builder
# ---------------------------------------------------------------------------

def _build_hashtags(blog_post, platform, max_count=None):
    """Build a hashtag string from multiple sources.

    Sources (in order):
        1. Universal hashtags
        2. Platform-specific bank
        3. Category-based hashtags
        4. Article tags converted to hashtags

    Args:
        blog_post: BlogPost instance.
        platform: Platform name string.
        max_count: Maximum number of hashtags. Falls back to platform default.

    Returns:
        Space-separated hashtag string.
    """
    if max_count is None:
        max_count = DEFAULT_MAX_HASHTAGS.get(platform, 10)

    tags = list(UNIVERSAL_HASHTAGS)

    # Platform-specific tags.
    tags.extend(PLATFORM_HASHTAGS.get(platform, []))

    # Category-based tags.
    if blog_post.category:
        category_name = blog_post.category.name
        tags.extend(CATEGORY_HASHTAGS.get(category_name, []))

    # Convert article tags to hashtags.
    if blog_post.tags:
        for raw_tag in blog_post.tags.split(","):
            tag = raw_tag.strip().lower()
            if not tag:
                continue
            hashtag = "#" + re.sub(r"[^a-z0-9]", "", tag.replace(" ", ""))
            if hashtag != "#" and hashtag not in tags:
                tags.append(hashtag)

    # Deduplicate while preserving order, then cap at max_count.
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)

    return " ".join(unique[:max_count])


# ---------------------------------------------------------------------------
# Platform-specific caption generators
# ---------------------------------------------------------------------------

def _generate_pinterest(blog_post, utm_url):
    """SEO-rich, keyword-heavy caption for Pinterest (max 500 chars)."""
    title = strip_html(blog_post.title)
    description = strip_html(blog_post.meta_description or blog_post.excerpt or "")

    cta = f"Read the full guide: {utm_url}"
    # Reserve room for title line + blank line + CTA line.
    available = 500 - len(title) - len(cta) - 4  # 4 for newlines/separators
    description = truncate(description, max(available, 80))

    caption = f"{title}\n\n{description}\n\n{cta}"
    caption = truncate(caption, 500)
    return caption


def _generate_facebook(blog_post, utm_url):
    """Conversational 2-3 sentence caption with a CTA for Facebook."""
    title = strip_html(blog_post.title)
    excerpt = strip_html(blog_post.excerpt or blog_post.meta_description or "")
    excerpt = truncate(excerpt, 300)

    caption = f"{title}\n\n{excerpt}\n\nRead the full article: {utm_url}"
    return caption


def _generate_instagram(blog_post, utm_url):
    """Story-style caption for Instagram (up to 2200 chars)."""
    title = strip_html(blog_post.title)
    excerpt = strip_html(blog_post.excerpt or blog_post.meta_description or "")
    excerpt = truncate(excerpt, 800)

    caption = (
        f"{title}\n"
        f"\n"
        f"{excerpt}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"Save this for your next Egypt trip!\n"
        f"Full guide: link in bio"
    )
    return truncate(caption, 2200)


# Platform dispatcher.
_GENERATORS = {
    "pinterest":  _generate_pinterest,
    "facebook":   _generate_facebook,
    "instagram":  _generate_instagram,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_caption(blog_post, platform, utm_url):
    """Generate a platform-optimized caption and hashtag string.

    Args:
        blog_post: BlogPost instance.
        platform: One of 'pinterest', 'facebook', 'instagram'.
        utm_url: Fully-formed UTM URL string.

    Returns:
        Tuple of (caption, hashtags) where both are plain strings.

    Raises:
        ValueError: If *platform* is not supported.
    """
    generator = _GENERATORS.get(platform)
    if generator is None:
        raise ValueError(f"Unsupported platform: {platform}")

    caption = generator(blog_post, utm_url)
    hashtags = _build_hashtags(blog_post, platform)
    return caption, hashtags
