from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from .models import SocialPost, SocialPostLog


@require_GET
def queue_status(request):
    """Return current social posting queue status."""
    today = timezone.now().date()
    return JsonResponse({
        'queue': {
            'scheduled': SocialPost.objects.filter(status='scheduled').count(),
            'posting': SocialPost.objects.filter(status='posting').count(),
            'posted_today': SocialPost.objects.filter(
                status='posted', posted_time__date=today
            ).count(),
            'failed': SocialPost.objects.filter(status='failed').count(),
            'total_posted': SocialPost.objects.filter(status='posted').count(),
        },
        'by_platform': {
            platform: {
                'scheduled': SocialPost.objects.filter(platform=platform, status='scheduled').count(),
                'posted_today': SocialPost.objects.filter(
                    platform=platform, status='posted', posted_time__date=today
                ).count(),
                'total_posted': SocialPost.objects.filter(platform=platform, status='posted').count(),
            }
            for platform in ['pinterest', 'facebook', 'instagram']
        },
        'last_run': _last_run_info(),
    })


def _last_run_info():
    log = SocialPostLog.objects.filter(log_type='post').first()
    if not log:
        return None
    return {
        'status': log.status,
        'started_at': log.started_at.isoformat(),
        'posts_succeeded': log.posts_succeeded,
        'posts_failed': log.posts_failed,
    }


@require_GET
def trigger_generation(request):
    """Trigger social post generation (admin only)."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    from django.core.management import call_command
    from io import StringIO

    out = StringIO()
    call_command('generate_social_posts', '--limit', '15', stdout=out)
    return JsonResponse({
        'status': 'ok',
        'output': out.getvalue(),
    })
