from datetime import timedelta, date

from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import datetime
from . import models as core_models
from django import forms
from django.utils.dateformat import DateFormat


class DaysOfTheWeek(models.Model):
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
    time = models.TimeField(default=datetime.now)
    days_of_week = models.ManyToManyField(DaysOfTheWeek)
    duration_days = models.PositiveSmallIntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super(ActivityMain, self).__init__(*args, **kwargs)
        self.__important_fields = ['days_of_week', 'duration_days']
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

    def days_changed(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True
        return False


    def daterange(start_date, end_date):
        _list = []
        for n in range(int((end_date - start_date).days)):
            _list.append(start_date + timedelta(n))
        return _list

    def get_occurance(self, start, end):
        _list = self.days_of_week.all().values_list('day')
        dates = []
        if start < self.start_date:
            start_final = start
        else:
            start_final = self.start_date

        if end < self.end_date:
            end_final = end
        else:
            end_final = self.end_date

        for day in self.daterange(start_final,end_final):
            if DateFormat(day).l() in _list:
                dates.append(day)
        return dates

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

    # class Meta:
    #     pass


class Activity(models.Model):
    parent = models.ForeignKey(ActivityMain, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=False)
    date = models.DateField()
    time = models.TimeField(blank=True, null=False)

    def save(self):
        if not self.time:
            self.time = self.parent.time
        super().save()