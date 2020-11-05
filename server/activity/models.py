from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import datetime
from core import models as core_models
from django import forms


class DaysOFTheWeek(models.Model):
    day = models.CharField(max_length=64)
    alias = models.CharField(max_length=16)

    def __str__(self):
        return self.day


class ActivityMain(models.Model):

    class ActivityType(models.IntegerChoices):
        Mass = 0

    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(
        choices=ActivityType.choices, default=0)
    slug = models.CharField(max_length=255, editable=False)
    is_recurring = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def make_title(self):
        if self.is_recurring:
            _type = 'recurring'
        else:
            _type = 'one-time'
        return f'{self.date_time} Activity {_type}'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.make_title()
        if not self.is_recurring:
            self.end_date = datetime.now
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        pass


class ActivitySchedule(models.Model):
    activity_main = models.ForeignKey(ActivityMain, on_delete=models.CASCADE)
    added_description = models.TextField(null=True, blank=False)
    time = models.TimeField(default=datetime.now)
    duration_days = models.PositiveSmallIntegerField(default=1)
    days_of_week = models.ForeignKey(DaysOFTheWeek, on_delete=models.PROTECT)


class Mass(Activity):

    def make_title(self):
        return f'{self.date_time} Mass'

    class Meta:
        verbose_name = "Mass details"


class MasIntentionDescription(models.Model):
    class IntnetionType(models.IntegerChoices):
        Thanksgiving = 0
        Late = 1
        other = 2

    type = models.PositiveSmallIntegerField(
        choices=IntnetionType.choices, default=0)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Massintentions(MasIntentionDescription):
    mass = models.ForeignKey(EucCelb, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payments, on_delete=models.PROTECT)
    by = models.TextField()
