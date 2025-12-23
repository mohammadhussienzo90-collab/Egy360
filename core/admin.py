"""
Admin configuration for Core app
Affiliate tracking and analytics
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import AffiliateClick, DailyRevenueSummary


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'platform_badge',
        'item_type',
        'content_object_link',
        'user_display',
        'device_type',
        'estimated_commission_display',
        'converted_badge',
        'clicked_at',
    ]
    list_filter = [
        'platform',
        'item_type',
        'device_type',
        'converted',
        'clicked_at',
    ]
    search_fields = [
        'affiliate_url',
        'user__username',
        'user__email',
        'ip_address',
    ]
    readonly_fields = [
        'user',
        'session_key',
        'platform',
        'item_type',
        'content_type',
        'object_id',
        'affiliate_url',
        'referrer_url',
        'ip_address',
        'user_agent',
        'country',
        'device_type',
        'clicked_at',
    ]
    date_hierarchy = 'clicked_at'
    ordering = ['-clicked_at']

    fieldsets = (
        ('Click Details', {
            'fields': ('platform', 'item_type', 'content_type', 'object_id', 'affiliate_url')
        }),
        ('User Info', {
            'fields': ('user', 'session_key', 'ip_address', 'user_agent', 'device_type', 'country')
        }),
        ('Revenue', {
            'fields': ('estimated_commission', 'converted', 'conversion_value', 'converted_at')
        }),
        ('Timestamps', {
            'fields': ('clicked_at', 'referrer_url')
        }),
    )

    def platform_badge(self, obj):
        colors = {
            'booking_com': '#003580',
            'viator': '#00AA6C',
            'getyourguide': '#FF5533',
            'hotellook': '#FF6B00',
            'agoda': '#5392F9',
        }
        color = colors.get(obj.platform, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_platform_display()
        )
    platform_badge.short_description = 'Platform'

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anonymous ({obj.session_key[:8]}...)" if obj.session_key else "Unknown"
    user_display.short_description = 'User'

    def content_object_link(self, obj):
        if obj.content_object:
            return str(obj.content_object)[:50]
        return f"ID: {obj.object_id}"
    content_object_link.short_description = 'Item'

    def estimated_commission_display(self, obj):
        if obj.estimated_commission:
            return format_html(
                '<span style="color: green;">${:.2f}</span>',
                obj.estimated_commission
            )
        return '-'
    estimated_commission_display.short_description = 'Est. Commission'

    def converted_badge(self, obj):
        if obj.converted:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px;">Yes</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 2px 6px; border-radius: 3px;">No</span>'
        )
    converted_badge.short_description = 'Converted'

    def changelist_view(self, request, extra_context=None):
        # Add summary statistics to the top of the list
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        extra_context = extra_context or {}

        # Today's stats
        today_clicks = AffiliateClick.objects.filter(clicked_at__date=today)
        extra_context['today_clicks'] = today_clicks.count()
        extra_context['today_revenue'] = today_clicks.aggregate(
            total=Sum('estimated_commission')
        )['total'] or 0

        # This week's stats
        week_clicks = AffiliateClick.objects.filter(clicked_at__date__gte=week_ago)
        extra_context['week_clicks'] = week_clicks.count()
        extra_context['week_revenue'] = week_clicks.aggregate(
            total=Sum('estimated_commission')
        )['total'] or 0

        # This month's stats
        month_clicks = AffiliateClick.objects.filter(clicked_at__date__gte=month_ago)
        extra_context['month_clicks'] = month_clicks.count()
        extra_context['month_revenue'] = month_clicks.aggregate(
            total=Sum('estimated_commission')
        )['total'] or 0

        # Platform breakdown
        platform_stats = AffiliateClick.objects.filter(
            clicked_at__date__gte=week_ago
        ).values('platform').annotate(
            count=Count('id'),
            revenue=Sum('estimated_commission')
        ).order_by('-count')
        extra_context['platform_stats'] = platform_stats

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DailyRevenueSummary)
class DailyRevenueSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'total_clicks',
        'accommodation_clicks',
        'tour_clicks',
        'estimated_revenue_display',
        'confirmed_revenue_display',
        'conversion_rate_display',
        'unique_visitors',
    ]
    list_filter = ['date']
    date_hierarchy = 'date'
    ordering = ['-date']
    readonly_fields = ['date', 'created_at', 'updated_at']

    def estimated_revenue_display(self, obj):
        return format_html('<span style="color: #17a2b8;">${:.2f}</span>', obj.estimated_revenue)
    estimated_revenue_display.short_description = 'Est. Revenue'

    def confirmed_revenue_display(self, obj):
        return format_html('<span style="color: #28a745;">${:.2f}</span>', obj.confirmed_revenue)
    confirmed_revenue_display.short_description = 'Confirmed'

    def conversion_rate_display(self, obj):
        color = '#28a745' if obj.conversion_rate >= 5 else '#ffc107' if obj.conversion_rate >= 2 else '#dc3545'
        return format_html('<span style="color: {};">{:.1f}%</span>', color, obj.conversion_rate)
    conversion_rate_display.short_description = 'Conv. Rate'
