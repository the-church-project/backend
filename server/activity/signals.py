from datetime import timedelta, date

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import ProtectedError
from . import models as activity_models
from django.conf import settings


@receiver(post_save, sender=activity_models.ActivityMain)
def edit_activity(sender, instance=None, created=False, **kwargs):
    if instance.end_date:
        dates = instance.get_occurance(instance.start_date,instance.end_date)
    else:
        temp_end_date = datetime.now() + timedelta(days=15)
        dates = instance.get_occurance(instance.start_date,temp_end_date)

    if created:
        for date in dates
            new_activities.append(activity_models.Activity(date=date, parent=instance))
        activity_models.Activity.objects.bulk_create(new_activities)
    elif instance.days_changed:        
        activities = activity_models.Activity.objects.filter(parent=instance)
        try:
            activities.delete()
        except Exception as exc:
            error = settings.ERROR_MODEL(description=exc.args, type=exc.args)
            error.save()
        new_activities = []
        for date in dates
            new_activities.append(activity_models.Activity(date=date, parent=instance))
        activity_models.Activity.objects.bulk_create(new_activities)