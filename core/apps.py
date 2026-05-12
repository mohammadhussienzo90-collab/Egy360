from django.apps import AppConfig
from django.contrib.auth.models import User
import sys


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Run on Django startup - ensure admin exists"""
        try:
            user, created = User.objects.get_or_create(
                username='admin360',
                defaults={
                    'email': 'admin@360egy.com',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            user.set_password('Egy360Admin2026!')
            user.save(update_fields=['password', 'email', 'is_staff', 'is_superuser'])
            print(f"Admin360 ready: {'created' if created else 'reset'}", file=sys.stderr)
        except Exception as e:
            print(f"Admin setup in ready(): {e}", file=sys.stderr)
