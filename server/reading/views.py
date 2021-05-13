from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic.list import MultipleObjectMixin
from . import models as reading_models
# Create your views here.

class DailyReadingMixin(MultipleObjectMixin):
    queryset = reading_models.Reading.objects.filter(date_time__lte=now, end_time__gte=now)
