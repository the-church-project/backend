from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin

from . import models as activity_models

# Create your views here.

class ActivityListMixin(MultipleObjectMixin):
    queryset = activity_models.Activity.objects.filter(date__gte=now)
