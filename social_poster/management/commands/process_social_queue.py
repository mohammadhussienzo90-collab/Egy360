"""
Management command: process_social_queue

Processes the social post queue -- publishes posts whose scheduled_time
has arrived and retries eligible failed posts.
"""

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from social_poster.models import (
    PostingSchedule,
    SocialAccount,
    SocialPost,
    SocialPostLog,
)
from social_poster.platforms import get_client


PLATFORMS = ['pinterest', 'facebook', 'instagram']
RETRY_DELAY_MINUTES = 30


class Command(BaseCommand):
    help = (
        'Process the social post queue. Publishes scheduled posts whose '
        'scheduled_time <= now and retries eligible failed posts.'
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
            help='Limit processing to a single platform.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which posts would be processed without publishing.',
        )
        parser.add_argument(
            '--no-log',
            action='store_true',
            help='Do not create a SocialPostLog audit entry.',
        )

    # ------------------------------------------------------------------
    # Main handler
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        platform_filter = options['platform']
        dry_run = options['dry_run']
        no_log = options['no_log']
        now = timezone.now()

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN -- nothing will be published.\n'))

        # Create audit log
        log = None
        if not dry_run and not no_log:
            log = SocialPostLog.objects.create(
                log_type='post',
                status='running',
                details={'platform': platform_filter},
            )

        # ----- Scheduled posts ready to publish -----
        ready_qs = SocialPost.objects.filter(
            status='scheduled',
            scheduled_time__lte=now,
        ).order_by('scheduled_time')

        if platform_filter:
            ready_qs = ready_qs.filter(platform=platform_filter)

        # ----- Retryable failed posts -----
        # We filter by status='failed' here and use the model's
        # ``can_retry`` property in the loop to honour max_retries.
        retry_qs = SocialPost.objects.filter(status='failed').order_by('scheduled_time')
        if platform_filter:
            retry_qs = retry_qs.filter(platform=platform_filter)

        # Combine the two querysets for processing
        all_posts = list(ready_qs) + [p for p in retry_qs if p.can_retry]

        total_processed = 0
        total_succeeded = 0
        total_failed = 0

        for post in all_posts:
            success = self._process_post(post, now, dry_run, log)
            total_processed += 1
            if success:
                total_succeeded += 1
            else:
                total_failed += 1

        # Finalise audit log
        if log:
            log.posts_processed = total_processed
            log.posts_succeeded = total_succeeded
            log.posts_failed = total_failed
            final_status = 'success'
            if total_failed and total_succeeded:
                final_status = 'partial'
            elif total_failed and not total_succeeded:
                final_status = 'failed'
            log.mark_complete(status=final_status)

        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Queue Processing Summary ==='))
        self.stdout.write(f'  Processed: {total_processed}')
        self.stdout.write(self.style.SUCCESS(f'  Succeeded: {total_succeeded}'))
        if total_failed:
            self.stdout.write(self.style.ERROR(f'  Failed:    {total_failed}'))
        else:
            self.stdout.write(f'  Failed:    {total_failed}')

    # ------------------------------------------------------------------
    # Process a single post
    # ------------------------------------------------------------------
    def _process_post(self, post, now, dry_run, log):
        """Attempt to publish a single SocialPost. Returns True on success."""

        platform = post.platform

        # --- Check daily limit ---
        try:
            schedule = PostingSchedule.objects.get(platform=platform, is_active=True)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_count = SocialPost.objects.filter(
                platform=platform,
                status='posted',
                posted_time__gte=today_start,
            ).count()

            if today_count >= schedule.daily_limit:
                self.stdout.write(self.style.WARNING(
                    f'[{platform}] Daily limit ({schedule.daily_limit}) reached -- '
                    f'skipping post id={post.pk}.'
                ))
                return False
        except PostingSchedule.DoesNotExist:
            # No schedule means no enforced daily limit; proceed anyway.
            pass

        if dry_run:
            self.stdout.write(
                f'  [DRY RUN] [{platform}] Would publish post id={post.pk} '
                f'"{post.blog_post.title[:50]}" (scheduled {post.scheduled_time})'
            )
            return True

        # --- Mark as posting ---
        post.status = 'posting'
        post.save(update_fields=['status', 'updated_at'])

        # --- Get account and client ---
        try:
            account = SocialAccount.objects.get(platform=platform, is_active=True)
        except SocialAccount.DoesNotExist:
            msg = f'[{platform}] No active SocialAccount found.'
            self.stdout.write(self.style.ERROR(msg))
            post.status = 'failed'
            post.error_message = msg
            post.retry_count += 1
            if post.retry_count >= post.max_retries:
                post.status = 'failed'
            else:
                post.status = 'scheduled'
                post.scheduled_time = now + datetime.timedelta(minutes=RETRY_DELAY_MINUTES)
            post.save()
            if log:
                log.add_error(msg)
            return False

        try:
            client = get_client(account)
        except Exception as exc:
            msg = f'[{platform}] Failed to create platform client: {exc}'
            self.stdout.write(self.style.ERROR(msg))
            post.status = 'failed'
            post.error_message = msg
            post.save()
            if log:
                log.add_error(msg)
            return False

        # --- Publish ---
        try:
            full_caption = post.caption
            if post.hashtags:
                full_caption = post.caption + '\n\n' + post.hashtags

            result = client.publish_with_retry(
                caption=full_caption,
                image_url=post.image_url,
                link_url=post.utm_url,
            )

            # Success
            post.status = 'posted'
            post.posted_time = timezone.now()
            post.platform_post_id = result.get('post_id', '') if isinstance(result, dict) else str(result or '')
            post.post_url = result.get('post_url', '') if isinstance(result, dict) else ''
            post.error_message = ''
            post.save()

            # Update account last_used_at
            account.last_used_at = timezone.now()
            account.save(update_fields=['last_used_at', 'updated_at'])

            self.stdout.write(self.style.SUCCESS(
                f'[{platform}] Posted id={post.pk} "{post.blog_post.title[:50]}"'
            ))
            return True

        except Exception as exc:
            post.retry_count += 1
            post.error_message = str(exc)

            if post.retry_count >= post.max_retries:
                post.status = 'failed'
                self.stdout.write(self.style.ERROR(
                    f'[{platform}] FAILED (max retries) id={post.pk}: {exc}'
                ))
            else:
                post.status = 'scheduled'
                post.scheduled_time = now + datetime.timedelta(minutes=RETRY_DELAY_MINUTES)
                self.stdout.write(self.style.WARNING(
                    f'[{platform}] Retry {post.retry_count}/{post.max_retries} '
                    f'id={post.pk}: {exc} -- rescheduled +{RETRY_DELAY_MINUTES}min'
                ))

            post.save()
            if log:
                log.add_error(f'[{platform}] Post id={post.pk}: {exc}')
            return False
