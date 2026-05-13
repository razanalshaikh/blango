from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from blango_auth.models import User


class Command(BaseCommand):
    help = "Delete inactive users whose activation expired"

    def handle(self, *args, **kwargs):
        expired_users = User.objects.filter(
            is_active=False,
            date_joined__lt=timezone.now() - timedelta(
                days=settings.ACCOUNT_ACTIVATION_DAYS
            )
        )

        count = expired_users.count()

        expired_users.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {count} inactive users."
            )
        )