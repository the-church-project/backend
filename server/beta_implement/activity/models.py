from datetime import timedelta

from django import forms
from django.conf import settings
from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.text import slugify
from django.utils.timezone import datetime, now, utc

from . import models as core_models


class DaysOfTheWeek(models.Model):
    day = models.CharField(max_length=64)
    alias = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.day}"


class ActivityMain(models.Model):
    class ActivityType(models.IntegerChoices):
        Mass = 0
        Other = 1

    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=ActivityType.choices, default=0)
    slug = models.CharField(max_length=255, editable=False)
    is_recurring = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(default=now)
    days_in_week = models.ManyToManyField(DaysOfTheWeek)
    duration_days = models.PositiveSmallIntegerField(default=1)
    is_spc = models.BooleanField(default=False)

    # def __init__(self, *args, **kwargs):
    #     super(ActivityMain, self).__init__(*args, **kwargs)
    #     self.__important_fields = ['duration_days']
    #     for field in self.__important_fields:
    #         setattr(self, '__original_%s' % field, getattr(self, field))

    # def days_changed(self):
    #     for field in self.__important_fields:
    #         orig = '__original_%s' % field
    #         if getattr(self, orig) != getattr(self, field):
    #             return True
    #     return False

    def daterange(self, start_date, end_date):
        _list = []
        for n in range(int((end_date - start_date).days)):
            _list.append(start_date + timedelta(n))
        return _list

    def get_occurance(self, start, end):
        new_list = self.days_in_week.all().values_list("day")
        _list = []
        for a in range(len(new_list)):
            _list.append(new_list[a][0])
        dates = []
        # end.replace(tzinfo=timezone.utc)
        # print(start,end)
        if start < self.start_date:
            start_final = start
        else:
            start_final = self.start_date

        if not self.end_date or end < self.end_date:
            end_final = end
        else:
            end_final = self.end_date
        a = self.daterange(start_date=start_final, end_date=end_final)
        for day in a:
            print(DateFormat(day).l(), DateFormat(day).l() in _list)
            if DateFormat(day).l() in _list:
                dates.append(day)
        return dates

    def make_title(self):
        if self.is_recurring:
            _type = "recurring"
        else:
            _type = "one-time"
        th = DateFormat(self.start_date).S()
        mon = DateFormat(self.start_date).M()
        date = DateFormat(self.start_date).d()
        return f"{date}{th}/{mon} Activity {_type}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.make_title()
        if not self.is_recurring and not self.end_date:
            self.end_date = now()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Activity(models.Model):
    parent = models.ForeignKey(ActivityMain, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.time:
            self.time = self.parent.time
        super().save(*args, **kwargs)
