from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import datetime
from core import models as core_models
from django import forms
class ActivityMain(models.Model):

    class ActivityType(models.IntegerChoices):
        One_time = 1
        Recursive = 2

    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, editable=False)
    type = models.PositiveSmallIntegerField(
        choices=ActivityType.choices, default=1)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)


    def make_title(self):
        return f'{self.date_time} Activity {self.type}'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.make_title()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class ActivitySub(models.Model):
    activity_main = models.ForeignKey(ActivityMain, on_delete=models.CASCADE)
    time = models.TimeField(default=datetime.now)
    days = models.



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
