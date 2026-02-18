from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.utils.text import Truncator

from .models import SocialAccount, SocialPost, PostingSchedule, SocialPostLog


# ---------------------------------------------------------------------------
# Platform badge helper shared across admins
# ---------------------------------------------------------------------------

PLATFORM_COLORS = {
    'pinterest': '#E60023',
    'facebook': '#1877F2',
    'instagram': '#C13584',
}

DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def _platform_badge(platform_value, platform_display=None):
    """Return a colored HTML badge for the given platform."""
    color = PLATFORM_COLORS.get(platform_value, '#666')
    label = platform_display or platform_value.title()
    return format_html(
        '<span style="background:{}; color:#fff; padding:3px 8px; '
        'border-radius:4px; font-size:11px; font-weight:600;">{}</span>',
        color,
        label,
    )


def _bool_badge(value, true_label='Active', false_label='Inactive'):
    """Return a green/red badge for boolean values."""
    if value:
        return format_html(
            '<span style="background:#28a745; color:#fff; padding:3px 8px; '
            'border-radius:4px; font-size:11px;">{}</span>',
            true_label,
        )
    return format_html(
        '<span style="background:#dc3545; color:#fff; padding:3px 8px; '
        'border-radius:4px; font-size:11px;">{}</span>',
        false_label,
    )


# ===========================================================================
# SocialAccount
# ===========================================================================

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = (
        'platform_badge',
        'account_name',
        'is_active_badge',
        'token_status',
        'last_used_at',
    )
    list_filter = ('platform', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'last_used_at')

    fieldsets = (
        ('Account Info', {
            'fields': ('platform', 'account_name', 'account_id', 'is_active'),
        }),
        ('Credentials', {
            'fields': (
                'access_token_encrypted',
                'refresh_token_encrypted',
                'token_expiry',
            ),
        }),
        ('Platform Config', {
            'fields': ('platform_metadata',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_used_at'),
        }),
    )

    # -- display helpers -----------------------------------------------------

    @admin.display(description='Platform', ordering='platform')
    def platform_badge(self, obj):
        return _platform_badge(obj.platform, obj.get_platform_display())

    @admin.display(description='Active', ordering='is_active', boolean=False)
    def is_active_badge(self, obj):
        return _bool_badge(obj.is_active, 'Active', 'Inactive')

    @admin.display(description='Token Status')
    def token_status(self, obj):
        if not obj.token_expiry:
            return format_html(
                '<span style="color:#888;">N/A</span>',
            )
        if obj.token_is_expired:
            return format_html(
                '<span style="background:#dc3545; color:#fff; padding:3px 8px; '
                'border-radius:4px; font-size:11px;">Expired</span>',
            )
        if obj.token_expires_soon:
            return format_html(
                '<span style="background:#ffc107; color:#000; padding:3px 8px; '
                'border-radius:4px; font-size:11px;">Expiring Soon</span>',
            )
        return format_html(
            '<span style="background:#28a745; color:#fff; padding:3px 8px; '
            'border-radius:4px; font-size:11px;">Valid</span>',
        )

    # Show encrypted tokens as masked text in the change form
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ('access_token_encrypted', 'refresh_token_encrypted'):
            field.help_text = '***encrypted*** \u2014 stored value is encrypted at rest.'
        return field


# ===========================================================================
# SocialPost
# ===========================================================================

STATUS_COLORS = {
    'draft': '#6c757d',
    'pending': '#17a2b8',
    'scheduled': '#1877F2',
    'posting': '#ffc107',
    'posted': '#28a745',
    'failed': '#dc3545',
    'cancelled': '#6c757d',
}

STATUS_TEXT_COLORS = {
    'posting': '#000',
}


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'platform_badge',
        'blog_post_title',
        'status_badge',
        'scheduled_time',
        'posted_time',
        'retry_count',
    )
    list_filter = ('platform', 'status', 'scheduled_time', 'created_at')
    search_fields = ('blog_post__title', 'caption', 'error_message')
    raw_id_fields = ('blog_post',)
    date_hierarchy = 'scheduled_time'
    readonly_fields = (
        'posted_time',
        'platform_post_id',
        'post_url',
        'error_message',
        'retry_count',
        'likes_count',
        'comments_count',
        'shares_count',
        'clicks_count',
        'impressions_count',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Content', {
            'fields': (
                'blog_post',
                'platform',
                'caption',
                'hashtags',
                'image_url',
                'utm_url',
            ),
        }),
        ('Scheduling', {
            'fields': ('status', 'scheduled_time', 'posted_time'),
        }),
        ('Platform Response', {
            'classes': ('collapse',),
            'fields': (
                'platform_post_id',
                'post_url',
                'error_message',
                'retry_count',
            ),
        }),
        ('Engagement', {
            'classes': ('collapse',),
            'fields': (
                'likes_count',
                'comments_count',
                'shares_count',
                'clicks_count',
                'impressions_count',
            ),
        }),
    )

    actions = ['schedule_posts', 'cancel_posts', 'retry_failed']

    # -- display helpers -----------------------------------------------------

    @admin.display(description='Platform', ordering='platform')
    def platform_badge(self, obj):
        return _platform_badge(obj.platform, obj.get_platform_display())

    @admin.display(description='Blog Post', ordering='blog_post__title')
    def blog_post_title(self, obj):
        return Truncator(obj.blog_post.title).chars(40)

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        bg = STATUS_COLORS.get(obj.status, '#666')
        fg = STATUS_TEXT_COLORS.get(obj.status, '#fff')
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; '
            'border-radius:4px; font-size:11px; font-weight:600;">{}</span>',
            bg,
            fg,
            obj.get_status_display(),
        )

    # -- bulk actions --------------------------------------------------------

    @admin.action(description='Schedule selected posts')
    def schedule_posts(self, request, queryset):
        updated = queryset.filter(status='draft').update(status='scheduled')
        self.message_user(request, f'{updated} post(s) set to scheduled.')

    @admin.action(description='Cancel selected posts')
    def cancel_posts(self, request, queryset):
        updated = queryset.exclude(status='posted').update(status='cancelled')
        self.message_user(request, f'{updated} post(s) cancelled.')

    @admin.action(description='Retry failed posts')
    def retry_failed(self, request, queryset):
        updated = queryset.filter(status='failed').update(
            status='scheduled',
            retry_count=0,
        )
        self.message_user(request, f'{updated} failed post(s) reset to scheduled.')


# ===========================================================================
# PostingSchedule
# ===========================================================================

@admin.register(PostingSchedule)
class PostingScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'platform_badge',
        'posts_per_day',
        'posting_times_display',
        'days_display',
        'daily_limit',
        'is_active_badge',
    )

    # -- display helpers -----------------------------------------------------

    @admin.display(description='Platform', ordering='platform')
    def platform_badge(self, obj):
        return _platform_badge(obj.platform, obj.get_platform_display())

    @admin.display(description='Posting Times')
    def posting_times_display(self, obj):
        times = obj.posting_times
        if not times:
            return '-'
        return ', '.join(str(t) for t in times)

    @admin.display(description='Days')
    def days_display(self, obj):
        days = obj.days_of_week
        if not days:
            return '-'
        return ', '.join(DAY_NAMES[d] for d in days if 0 <= d <= 6)

    @admin.display(description='Active', ordering='is_active', boolean=False)
    def is_active_badge(self, obj):
        return _bool_badge(obj.is_active, 'Active', 'Inactive')


# ===========================================================================
# SocialPostLog
# ===========================================================================

LOG_STATUS_COLORS = {
    'running': '#17a2b8',
    'success': '#28a745',
    'failed': '#dc3545',
    'partial': '#ffc107',
}

LOG_STATUS_TEXT_COLORS = {
    'partial': '#000',
}


@admin.register(SocialPostLog)
class SocialPostLogAdmin(admin.ModelAdmin):
    list_display = (
        'log_type',
        'status_badge',
        'started_at',
        'completed_at',
        'posts_processed',
        'posts_succeeded',
        'posts_failed',
    )
    list_filter = ('log_type', 'status')
    readonly_fields = (
        'log_type',
        'status',
        'started_at',
        'completed_at',
        'posts_processed',
        'posts_succeeded',
        'posts_failed',
        'errors',
        'details',
    )
    date_hierarchy = 'started_at'

    # -- display helpers -----------------------------------------------------

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        bg = LOG_STATUS_COLORS.get(obj.status, '#666')
        fg = LOG_STATUS_TEXT_COLORS.get(obj.status, '#fff')
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; '
            'border-radius:4px; font-size:11px; font-weight:600;">{}</span>',
            bg,
            fg,
            obj.get_status_display(),
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
