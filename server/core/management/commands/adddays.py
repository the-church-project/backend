import os
from datetime import timedelta

from activity import models as activity_models
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dates import WEEKDAYS, WEEKDAYS_ABBR
from django.utils.timezone import now


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-d", "--del", action="store_true", help="del the db")

    def handle(self, *args, **options):
        model = activity_models.DaysOfTheWeek
        _del = options.get("del")
        if _del:
            model.objects.all().delete()
        if not model.objects.filter(day="Sunday").exists():
            days = []
            for i in range(0, len(WEEKDAYS)):
                days.append(model(day=WEEKDAYS.get(i), alias=WEEKDAYS_ABBR.get(i)))
            model.objects.bulk_create(days)
            self.stdout.write(self.style.SUCCESS("Days added to DB"))
        else:
            self.stdout.write(self.style.WARNING("Already exist in DB"))
