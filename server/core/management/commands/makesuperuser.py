import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(phone_number=settings.ADMIN_PHONE).exists():
            User.objects.create_superuser(
                phone_number=settings.ADMIN_PHONE, first_name=settings.ADMIN_NAME, password=settings.ADMIN_PASS)
            self.stdout.write(self.style.SUCCESS('Admin user has created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))
