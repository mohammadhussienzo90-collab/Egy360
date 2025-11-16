from rest_framework import serializers
from .models import (
    BlogCategory,
    Tag,
    BlogPost,
    BlogImage,
    BlogComment,
    Newsletter,
    BlogSeries,
    BlogPostSeries,
)

"""
BLOG SERIALIZERS
================
These serializers handle conversion between:
- Django Blog models (Python objects)
- JSON format (API responses)

STRATEGIC IMPORTANCE:
Blog = Content Marketing Engine
- SEO traffic (Google loves fresh content)
- Tourist education (trust building)
- Organic growth (no paid ads needed)
- User engagement (comments, shares)
- Email list building (newsletter)

Blog is how Egy360 gets DISCOVERED.
Without blog, you need to pay for ads.
With blog, tourists find you naturally.

Pattern: Content-focused, SEO-optimized, engagement-driven
"""


class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for blog categories

    WHAT IT DOES:
    - Organizes blog posts into categories
    - Examples: Safety Tips, Cultural Info, Food Guide, Visa Info
    - Users browse by category

    WHY CATEGORIES MATTER:
    - Tourist looking for safety info → finds it easily
    - Tourist wants cultural tips → finds it easily
    - Improves user experience
    - Helps with SEO (category pages rank)
    """

    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'post_count',
        )
        read_only_fields = ('id', 'slug', 'post_count')

    def get_post_count(self, obj):
        """How many posts in this category"""
        return obj.posts.filter(is_published=True).count()


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for blog tags

    WHAT IT DOES:
    - Tags help organize posts by topic
    - Examples: #Cairo, #Pyramids, #SafeTravel, #VeganeFood
    - Users can find related posts

    WHY TAGS MATTER:
    - Cross-category organization
    - Related posts feature
    - SEO keywords
    - User navigation
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id', 'slug')


class BlogImageSerializer(serializers.ModelSerializer):
    """
    Serializer for blog post images

    WHAT IT DOES:
    - Images within blog posts
    - Captions for accessibility
    - Alt text for SEO

    WHY IMAGES MATTER:
    - Breaks up text (better UX)
    - Shows real scenes (builds trust)
    - SEO (Google images)
    - Shareable (social media)
    """

    class Meta:
        model = BlogImage
        fields = (
            'id',
            'image',
            'caption',
            'alt_text',
            'order',
        )
        read_only_fields = ('id',)


class BlogCommentListSerializer(serializers.ModelSerializer):
    """
    List view serializer - comments on blog post

    WHAT IT DOES:
    - Shows approved comments below post
    - Builds community
    - Shows engagement

    COMMENT QUALITY:
    - Only approved comments show (spam filtered)
    - Verified purchase badge (if applicable)
    - Helpful votes visible
    - Encourages real discussion
    """

    author_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = BlogComment
        fields = (
            'id',
            'author_name',
            'content',
            'rating',
            'status',
            'status_display',
            'is_verified_purchase',
            'helpful_count',
            'unhelpful_count',
            'created_at',
        )
        read_only_fields = (
            'id',
            'author_name',
            'status_display',
            'created_at',
        )

    def get_author_name(self, obj):
        """Get comment author's name"""
        return obj.author.get_full_name() or obj.author.username


class BlogCommentDetailSerializer(serializers.ModelSerializer):
    """
    Detail view serializer - full comment with responses

    WHAT IT DOES:
    - Shows complete comment thread
    - Author info, timestamp, helpful votes
    - Used on comment detail page
    """

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogComment
        fields = (
            'id',
            'post',
            'author',
            'content',
            'rating',
            'status',
            'is_verified_purchase',
            'helpful_count',
            'unhelpful_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'post',
            'author',
            'created_at',
            'updated_at',
        )


class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog comments

    WHAT IT DOES:
    - Tourist leaves comment on blog post
    - Validates comment quality
    - Starts as pending (spam check)

    QUALITY CONTROL:
    - Minimum length check
    - Spam filter
    - Admin approval
    - Then published
    """

    class Meta:
        model = BlogComment
        fields = (
            'content',
            'rating',
        )

    def validate_content(self, value):
        """Comment must have minimum length"""
        if len(value) < 5:
            raise serializers.ValidationError(
                "Comment must be at least 5 characters"
            )
        if len(value) > 5000:
            raise serializers.ValidationError(
                "Comment cannot exceed 5000 characters"
            )
        return value


class BlogPostSeriesSerializer(serializers.ModelSerializer):
    """
    Serializer for multi-part blog series

    WHAT IT DOES:
    - Groups related posts as series
    - Example: "Complete Cairo Guide" Parts 1-5
    - Users read entire series

    WHY SERIES MATTER:
    - Keeps users engaged (read more content)
    - Better SEO (internal linking)
    - Shows expertise (deep dives)
    - Increases time on site
    """

    class Meta:
        model = BlogPostSeries
        fields = (
            'id',
            'series',
            'post',
            'order',
        )
        read_only_fields = ('id',)


class BlogSeriesDetailSerializer(serializers.ModelSerializer):
    """
    Detail serializer for blog series

    WHAT IT DOES:
    - Shows all posts in a series
    - Shows current position (Part 2 of 5)
    - Links to next/previous posts
    """

    posts = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogSeries
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'image',
            'post_count',
            'posts',
        )
        read_only_fields = ('id', 'slug')

    def get_posts(self, obj):
        """Get all posts in series, ordered"""
        posts = obj.posts.all().order_by('blogpostseries__order')
        return BlogPostListSerializer(posts, many=True).data

    def get_post_count(self, obj):
        """How many posts in series"""
        return obj.posts.count()


class BlogPostListSerializer(serializers.ModelSerializer):
    """
    List view serializer - blog posts in feed/search

    WHAT IT DOES:
    - Shows post preview for browsing
    - Includes: title, excerpt, image, date, category
    - Optimized for fast loading

    USER EXPERIENCE:
    - Tourist browses blog posts
    - Sees preview of each
    - Click to read full article
    - Fast page load

    SEO BENEFIT:
    - Blog index page ranks
    - Shows post previews
    - Encourages click-throughs
    """

    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(
        source='estimated_reading_time',
        read_only=True
    )

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title',
            'slug',
            'excerpt',
            'featured_image',
            'author',
            'category',
            'tags',
            'status',
            'is_featured',
            'view_count',
            'like_count',
            'comment_count',
            'reading_time',
            'published_date',
            'created_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'view_count',
            'like_count',
            'comment_count',
            'published_date',
            'created_at',
        )


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Detail view serializer - COMPLETE blog post

    WHAT IT DOES:
    - Shows FULL blog post content
    - Includes: full text, images, comments, related posts
    - SEO-optimized with metadata

    COMPLETE EXPERIENCE:
    - Full article text
    - All images in correct order
    - Author info
    - Share buttons data
    - Comments section
    - Related posts
    - Newsletter signup CTA

    SEO OPTIMIZATION:
    - Meta title (browser tab)
    - Meta description (search results)
    - Meta keywords
    - Canonical URL
    - Schema markup ready

    LEARNING POINT:
    - Include all content needed for post view
    - Nested images and comments
    - SEO fields for search engines
    - CTA fields for conversions
    """

    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = BlogImageSerializer(many=True, read_only=True)
    comments = BlogCommentListSerializer(
        many=True,
        read_only=True,
        source='comments.filter(status="approved")'
    )
    series_info = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'featured_image',
            'author',
            'category',
            'city',
            'tags',
            'images',
            'status',
            'is_featured',
            'allow_comments',
            'allow_sharing',
            'view_count',
            'like_count',
            'share_count',
            'comment_count',
            'estimated_reading_time',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'published_date',
            'comments',
            'series_info',
            'related_posts',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'slug',
            'view_count',
            'like_count',
            'share_count',
            'comment_count',
            'published_date',
            'comments',
            'series_info',
            'related_posts',
            'created_at',
            'updated_at',
        )

    def get_series_info(self, obj):
        """Get series this post belongs to"""
        series_items = obj.series_items.all()
        if series_items:
            series_item = series_items.first()
            return {
                'series_title': series_item.series.title,
                'part_number': series_item.order,
                'total_parts': series_item.series.posts.count(),
            }
        return None

    def get_related_posts(self, obj):
        """
        Get related posts (same category/tags)

        BUSINESS LOGIC:
        - Show 3-5 related posts
        - Keeps user on site longer
        - Increases pages viewed
        - Better engagement
        """
        related = BlogPost.objects.filter(
            is_published=True,
            category=obj.category
        ).exclude(id=obj.id)[:3]
        return BlogPostListSerializer(related, many=True).data


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating blog posts

    WHAT IT DOES:
    - Author writes blog post
    - Validates title, content, images
    - Starts as draft, then published

    WORKFLOW:
    1. Author creates draft
    2. Author uploads images
    3. Author writes content
    4. Author submits for review
    5. Editor publishes
    6. Post goes live
    """

    class Meta:
        model = BlogPost
        fields = (
            'title',
            'excerpt',
            'content',
            'featured_image',
            'category',
            'city',
            'tags',
            'status',
            'is_featured',
            'allow_comments',
            'allow_sharing',
            'estimated_reading_time',
            'meta_title',
            'meta_description',
            'meta_keywords',
        )

    def validate_title(self, value):
        """Title must be reasonable length"""
        if len(value) < 5:
            raise serializers.ValidationError("Title too short")
        if len(value) > 300:
            raise serializers.ValidationError("Title too long")
        return value

    def validate_content(self, value):
        """Content must be substantial"""
        if len(value) < 100:
            raise serializers.ValidationError(
                "Article too short (minimum 100 characters)"
            )
        return value

    def validate_excerpt(self, value):
        """Excerpt should summarize article"""
        if len(value) < 20:
            raise serializers.ValidationError("Excerpt too short")
        if len(value) > 500:
            raise serializers.ValidationError("Excerpt too long")
        return value


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for newsletter subscriptions

    WHAT IT DOES:
    - Tourists subscribe to email list
    - Receive weekly blog summaries
    - Stay engaged with brand

    EMAIL MARKETING:
    - Newsletter = recurring engagement
    - Remind tourists about Egy360
    - Drive repeat bookings
    - Build long-term relationships
    """

    class Meta:
        model = Newsletter
        fields = (
            'id',
            'email',
            'name',
            'categories',
            'is_active',
            'subscription_date',
        )
        read_only_fields = (
            'id',
            'subscription_date',
        )

    def validate_email(self, value):
        """Email must be valid"""
        if Newsletter.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError(
                "This email is already subscribed"
            )
        return value


class NewsletterSubscribeSerializer(serializers.Serializer):
    """
    Simple serializer for newsletter signup

    WHAT IT DOES:
    - Tourist enters email on blog
    - Click "Subscribe"
    - Added to newsletter list

    CONVERSION:
    - CTA below every blog post
    - Simple form (just email)
    - Quick subscription
    - Email confirmation sent
    """

    email = serializers.EmailField(required=True)
    name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    def validate_email(self, value):
        """Check if already subscribed"""
        if Newsletter.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("Already subscribed")
        return value