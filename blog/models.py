from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')

    excerpt = models.TextField(max_length=500, help_text='Short summary')
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External image URL (Unsplash, etc.)")

    # Video & Multimedia Support
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="YouTube/Vimeo embed URL")
    video_thumbnail = models.URLField(max_length=500, blank=True, null=True, help_text="Video thumbnail image")
    is_video_post = models.BooleanField(default=False, help_text="Featured as video content")

    # Content Type for variety
    content_type = models.CharField(
        max_length=30,
        choices=[
            ('article', 'Article'),
            ('story', 'True Story'),
            ('history', 'Historical'),
            ('culture', 'Culture'),
            ('guide', 'Travel Guide'),
            ('video', 'Video Post'),
            ('gallery', 'Photo Gallery'),
        ],
        default='article'
    )

    # Gallery images (JSON field for multiple images)
    gallery_images = models.TextField(blank=True, null=True, help_text="JSON array of image URLs for galleries")

    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived')
        ],
        default='draft'
    )
    is_featured = models.BooleanField(default=False)

    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    related_city = models.ForeignKey('destinations.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', '-published_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def is_active(self):
        return self.status == 'published'

    @property
    def get_image(self):
        """Returns image URL with fallback priority: image_url > featured_image > default"""
        if self.image_url:
            return self.image_url
        if self.featured_image:
            return self.featured_image.url
        return "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800&q=80"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    comment = models.TextField()

    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_blog_comments')

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Moderation'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    moderated_at = models.DateTimeField(null=True, blank=True)
    likes_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    @property
    def is_approved(self):
        return self.status == 'approved'