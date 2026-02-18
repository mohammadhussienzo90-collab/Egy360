"""
Data migration: create default PostingSchedule entries for Facebook
and Instagram (daily at 19:00 UTC = 9 PM Cairo time).
"""

from django.db import migrations


def create_schedules(apps, schema_editor):
    PostingSchedule = apps.get_model('social_poster', 'PostingSchedule')

    PostingSchedule.objects.update_or_create(
        platform='facebook',
        defaults={
            'posts_per_day': 1,
            'posting_times': ['19:00'],
            'days_of_week': [0, 1, 2, 3, 4, 5, 6],
            'daily_limit': 25,
            'is_active': True,
        },
    )

    PostingSchedule.objects.update_or_create(
        platform='instagram',
        defaults={
            'posts_per_day': 1,
            'posting_times': ['19:00'],
            'days_of_week': [0, 1, 2, 3, 4, 5, 6],
            'daily_limit': 10,
            'is_active': True,
        },
    )


def remove_schedules(apps, schema_editor):
    PostingSchedule = apps.get_model('social_poster', 'PostingSchedule')
    PostingSchedule.objects.filter(platform__in=['facebook', 'instagram']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('social_poster', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_schedules, remove_schedules),
    ]
