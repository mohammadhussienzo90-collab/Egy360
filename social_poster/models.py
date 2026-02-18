from django.db import models
from django.utils import timezone
from blog.models import BlogPost


class SocialAccount(models.Model):
    """Stores social media platform credentials with encrypted tokens."""
    PLATFORM_CHOICES = [
        ('pinterest', 'Pinterest'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    account_name = models.CharField(max_length=200, help_text="Display name")
    account_id = models.CharField(max_length=200, blank=True, help_text="Platform-specific account/page ID")

    access_token_encrypted = models.TextField(blank=True)
    refresh_token_encrypted = models.TextField(blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    platform_metadata = models.JSONField(
        default=dict, blank=True,
        help_text="Platform config: board_id, page_id, ig_user_id, app_id, app_secret"
    )

    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'social_accounts'
        verbose_name = 'Social Account'
        verbose_name_plural = 'Social Accounts'

    def __str__(self):
        return f"{self.get_platform_display()} - {self.account_name}"

    @property
    def access_token(self):
        from .encryption import decrypt_token
        return decrypt_token(self.access_token_encrypted)

    @access_token.setter
    def access_token(self, value):
        from .encryption import encrypt_token
        self.access_token_encrypted = encrypt_token(value)

    @property
    def refresh_token(self):
        from .encryption import decrypt_token
        return decrypt_token(self.refresh_token_encrypted)

    @refresh_token.setter
    def refresh_token(self, value):
        from .encryption import encrypt_token
        self.refresh_token_encrypted = encrypt_token(value)

    @property
    def token_is_expired(self):
        if not self.token_expiry:
            return False
        return timezone.now() >= self.token_expiry

    @property
    def token_expires_soon(self):
        if not self.token_expiry:
            return False
        return timezone.now() >= (self.token_expiry - timezone.timedelta(hours=24))


class SocialPost(models.Model):
    """A single social media post in the queue."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('scheduled', 'Scheduled'),
        ('posting', 'Posting...'),
        ('posted', 'Posted'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    PLATFORM_CHOICES = [
        ('pinterest', 'Pinterest'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ]

    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='social_posts')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    caption = models.TextField(help_text="Platform-optimized caption")
    hashtags = models.TextField(blank=True)
    image_url = models.URLField(max_length=500)
    utm_url = models.URLField(max_length=500, help_text="Article URL with UTM tracking")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_time = models.DateTimeField(null=True, blank=True, db_index=True)
    posted_time = models.DateTimeField(null=True, blank=True)

    platform_post_id = models.CharField(max_length=200, blank=True)
    post_url = models.URLField(max_length=500, blank=True)

    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)

    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    clicks_count = models.IntegerField(default=0)
    impressions_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'social_posts'
        ordering = ['-scheduled_time', '-created_at']
        verbose_name = 'Social Post'
        verbose_name_plural = 'Social Posts'
        indexes = [
            models.Index(fields=['status', 'scheduled_time'], name='social_post_queue_idx'),
            models.Index(fields=['platform', 'status'], name='social_post_platform_idx'),
            models.Index(fields=['blog_post', 'platform'], name='social_post_blog_plat_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['blog_post', 'platform'],
                condition=models.Q(status__in=['scheduled', 'posted', 'posting']),
                name='unique_active_post_per_platform'
            ),
        ]

    def __str__(self):
        return f"[{self.get_platform_display()}] {self.blog_post.title[:50]} ({self.get_status_display()})"

    @property
    def is_ready_to_post(self):
        return (
            self.status == 'scheduled'
            and self.scheduled_time
            and self.scheduled_time <= timezone.now()
        )

    @property
    def can_retry(self):
        return self.status == 'failed' and self.retry_count < self.max_retries


class PostingSchedule(models.Model):
    """Defines posting cadence for each platform."""
    PLATFORM_CHOICES = [
        ('pinterest', 'Pinterest'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    posts_per_day = models.IntegerField(default=1)
    posting_times = models.JSONField(
        default=list,
        help_text='UTC times, e.g. ["09:00", "14:00", "19:00"]'
    )
    days_of_week = models.JSONField(
        default=list,
        help_text='Day numbers (0=Mon, 6=Sun), e.g. [0,1,2,3,4,5,6]'
    )
    daily_limit = models.IntegerField(default=10, help_text="Hard daily rate limit")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posting_schedules'
        verbose_name = 'Posting Schedule'
        verbose_name_plural = 'Posting Schedules'

    def __str__(self):
        return f"{self.get_platform_display()} - {self.posts_per_day}/day"


class SocialPostLog(models.Model):
    """Audit trail for social posting operations."""
    LOG_TYPES = [
        ('generate', 'Queue Generation'),
        ('post', 'Post Execution'),
        ('refresh', 'Token Refresh'),
        ('metrics', 'Metrics Update'),
    ]

    STATUS_CHOICES = [
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial Success'),
    ]

    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    posts_processed = models.IntegerField(default=0)
    posts_succeeded = models.IntegerField(default=0)
    posts_failed = models.IntegerField(default=0)
    errors = models.JSONField(default=list, blank=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'social_post_logs'
        ordering = ['-started_at']
        verbose_name = 'Social Post Log'
        verbose_name_plural = 'Social Post Logs'

    def __str__(self):
        return f"{self.get_log_type_display()} - {self.status} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"

    def mark_complete(self, status='success'):
        self.status = status
        self.completed_at = timezone.now()
        self.save()

    def add_error(self, error_message):
        if not self.errors:
            self.errors = []
        self.errors.append({
            'message': str(error_message),
            'timestamp': timezone.now().isoformat()
        })
        self.posts_failed += 1
        self.save()
