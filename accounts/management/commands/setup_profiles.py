# accounts/management/commands/setup_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creates user profiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for user: {user.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Profile already exists for user: {user.username}')
                )