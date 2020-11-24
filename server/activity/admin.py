from django.contrib import admin
from . import models
# register your models here.


class ActivityMainAdmin(admin.ModelAdmin):
    filter_horizontal = ('days_in_week',)


admin.site.register(models.Activity)
admin.site.register(models.DaysOfTheWeek)
admin.site.register(models.ActivityMain, ActivityMainAdmin)
