"""
Management command: generate_social_posts

Populates the SocialPost queue from published BlogPost articles.
For each active platform schedule, generates captions and schedules
posts into the next available time slots.
"""

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogPost
from social_poster.content_generator import generate_caption
from social_poster.models import (
    PostingSchedule,
    SocialPost,
    SocialPostLog,
)
from social_poster.utm import build_utm_url


PLATFORMS = ['pinterest', 'facebook', 'instagram']


class Command(BaseCommand):
    help = (
        'Generate scheduled social posts from published blog articles. '
        'Creates SocialPost entries for each platform with available '
        'PostingSchedule, skipping articles that already have an active post.'
    )

    # ------------------------------------------------------------------
    # Arguments
    # ------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument(
            '--platform',
            type=str,
            choices=PLATFORMS,
            default=None,
            help='Limit generation to a single platform.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=15,
            help='Maximum number of posts to generate per platform (default: 15).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview what would be created without writing to the database.',
        )
        parser.add_argument(
            '--article-id',
            type=int,
            default=None,
            help='Generate posts for a single BlogPost by its primary key.',
        )

    # ------------------------------------------------------------------
    # Main handler
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        platform_filter = options['platform']
        limit = options['limit']
        dry_run = options['dry_run']
        article_id = options['article_id']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN -- no records will be created.\n'))

        # Determine which platforms to process
        platforms = [platform_filter] if platform_filter else PLATFORMS

        # Fetch published blog posts
        blog_qs = BlogPost.objects.filter(status='published').order_by('-published_at')
        if article_id:
            blog_qs = blog_qs.filter(pk=article_id)
            if not blog_qs.exists():
                self.stdout.write(self.style.ERROR(
                    f'BlogPost with id={article_id} not found or not published.'
                ))
                return

        # Create an audit log entry (unless dry-run)
        log = None
        if not dry_run:
            log = SocialPostLog.objects.create(
                log_type='generate',
                status='running',
                details={'platforms': platforms, 'limit': limit, 'article_id': article_id},
            )

        total_created = 0
        total_skipped = 0
        total_errors = 0
        summary_lines = []

        for platform in platforms:
            created, skipped, errors = self._process_platform(
                platform, blog_qs, limit, dry_run, log,
            )
            total_created += created
            total_skipped += skipped
            total_errors += errors
            summary_lines.append(
                f'  {platform}: {created} created, {skipped} skipped, {errors} errors'
            )

        # Finalise audit log
        if log:
            log.posts_processed = total_created + total_skipped
            log.posts_succeeded = total_created
            log.posts_failed = total_errors
            final_status = 'success'
            if total_errors and total_created:
                final_status = 'partial'
            elif total_errors and not total_created:
                final_status = 'failed'
            log.mark_complete(status=final_status)

        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Generation Summary ==='))
        for line in summary_lines:
            self.stdout.write(line)
        self.stdout.write(self.style.SUCCESS(
            f'Total: {total_created} created, {total_skipped} skipped, {total_errors} errors'
        ))

    # ------------------------------------------------------------------
    # Per-platform processing
    # ------------------------------------------------------------------
    def _process_platform(self, platform, blog_qs, limit, dry_run, log):
        """Generate posts for a single platform. Returns (created, skipped, errors)."""

        # Check for an active PostingSchedule
        try:
            schedule = PostingSchedule.objects.get(platform=platform, is_active=True)
        except PostingSchedule.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                f'[{platform}] No active PostingSchedule -- skipping.'
            ))
            return 0, 0, 0

        created = 0
        skipped = 0
        errors = 0

        # Pre-compute the set of blog_post ids that already have an active
        # SocialPost for this platform (scheduled / posting / posted).
        existing_ids = set(
            SocialPost.objects.filter(
                platform=platform,
                status__in=['scheduled', 'posting', 'posted'],
            ).values_list('blog_post_id', flat=True)
        )

        # Collect already-occupied scheduled_time slots so we can avoid
        # double-booking within the same run.
        occupied_slots = set(
            SocialPost.objects.filter(
                platform=platform,
                status__in=['scheduled', 'posting'],
                scheduled_time__isnull=False,
            ).values_list('scheduled_time', flat=True)
        )

        slot_generator = self._next_slot_generator(schedule, occupied_slots)

        for blog_post in blog_qs:
            if created >= limit:
                break

            if blog_post.pk in existing_ids:
                skipped += 1
                continue

            try:
                utm_url = build_utm_url(blog_post, platform)
                caption = generate_caption(blog_post, platform, utm_url)

                # Resolve image -- prefer image_url, fallback to get_image property
                image_url = blog_post.image_url or blog_post.get_image

                scheduled_time = next(slot_generator)

                if dry_run:
                    self.stdout.write(
                        f'  [DRY RUN] [{platform}] "{blog_post.title[:60]}" '
                        f'-> {scheduled_time:%Y-%m-%d %H:%M}'
                    )
                else:
                    SocialPost.objects.create(
                        blog_post=blog_post,
                        platform=platform,
                        caption=caption,
                        image_url=image_url,
                        utm_url=utm_url,
                        status='scheduled',
                        scheduled_time=scheduled_time,
                    )

                created += 1

            except Exception as exc:
                errors += 1
                msg = f'[{platform}] Error for BlogPost id={blog_post.pk}: {exc}'
                self.stdout.write(self.style.ERROR(msg))
                if log:
                    log.add_error(msg)

        self.stdout.write(self.style.SUCCESS(
            f'[{platform}] {created} posts {"would be " if dry_run else ""}created '
            f'({skipped} skipped, {errors} errors)'
        ))
        return created, skipped, errors

    # ------------------------------------------------------------------
    # Scheduling helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _next_slot_generator(schedule, occupied_slots):
        """Yield successive available datetime slots according to the
        PostingSchedule's ``posting_times`` and ``days_of_week``.

        ``occupied_slots`` is a set of datetimes that are already taken;
        the generator skips any slot that collides.
        """
        posting_times = sorted(schedule.posting_times or ['09:00'])
        days_of_week = set(schedule.days_of_week or list(range(7)))

        # Parse the time strings once
        time_objects = []
        for ts in posting_times:
            parts = ts.split(':')
            time_objects.append(datetime.time(int(parts[0]), int(parts[1])))

        now = timezone.now()
        current_date = now.date()

        # We scan up to 90 days into the future to avoid infinite loops
        end_date = current_date + datetime.timedelta(days=90)

        while current_date <= end_date:
            # Python weekday: Monday=0 .. Sunday=6 -- matches model convention
            if current_date.weekday() in days_of_week:
                for t in time_objects:
                    candidate = timezone.make_aware(
                        datetime.datetime.combine(current_date, t),
                        timezone=datetime.timezone.utc,
                    ) if timezone.is_naive(
                        datetime.datetime.combine(current_date, t)
                    ) else datetime.datetime.combine(current_date, t).replace(
                        tzinfo=datetime.timezone.utc
                    )

                    # Must be in the future and not already occupied
                    if candidate > now and candidate not in occupied_slots:
                        occupied_slots.add(candidate)
                        yield candidate

            current_date += datetime.timedelta(days=1)

        # If we exhaust 90 days, keep yielding hourly slots as a fallback
        fallback = timezone.now() + datetime.timedelta(days=91)
        while True:
            yield fallback
            fallback += datetime.timedelta(hours=1)
