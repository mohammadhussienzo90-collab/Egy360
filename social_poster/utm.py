"""
UTM URL builder for Egy360 social media posts.

Generates tracked URLs for blog posts shared across social platforms.
"""

BASE_URL = "https://360egy.com"


def build_utm_url(blog_post, platform):
    """Build a blog post URL with UTM tracking parameters.

    Args:
        blog_post: BlogPost instance (must have .slug attribute).
        platform: Platform name string (e.g. 'pinterest', 'facebook', 'instagram').

    Returns:
        Full URL string with UTM parameters.
    """
    return (
        f"{BASE_URL}/blog/{blog_post.slug}/"
        f"?utm_source={platform}"
        f"&utm_medium=social"
        f"&utm_campaign=auto_post"
        f"&utm_content={blog_post.slug}"
    )
