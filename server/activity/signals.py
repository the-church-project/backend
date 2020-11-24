from datetime import timedelta

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db.models.deletion import ProtectedError
from . import models as activity_models
from django.conf import settings
from django.utils.timezone import now


@receiver(m2m_changed, sender=activity_models.ActivityMain.days_in_week.through)
def edit_activity(sender, instance=None, created=False, **kwargs):
    if instance.is_recurring:
        action = kwargs.get('action')
        if action == 'pre_add' or action == 'pre_remove' or action == 'pre_clear':
            try:
                activities = activity_models.Activity.objects.filter(
                    parent=instance, date__gte=now())
                activities.delete()
            except Exception as exc:
                error = settings.ERROR_MODEL(
                    description=exc.args, type=exc.args)
                error.save()
        elif action == 'post_add' or action == 'post_remove':
            temp_end_date = now() + timedelta(days=15)
            dates = instance.get_occurance(
                start=instance.start_date, end=temp_end_date)
            new_activities = []
            for date in dates:
                new_activities.append(
                    activity_models.Activity(date=date, parent=instance))
            activity_models.Activity.objects.bulk_create(new_activities)
        # elif action == 'post_remove':
        #     activities = activity_models.Activity.objects.filter(
        #         parent=instance, date__gte=now())


@receiver(post_save, sender=activity_models.ActivityMain)
def make_activity(sender, instance=None, created=False, **kwargs):
    if created:
        new_activities = []
        if not instance.is_recurring:
            for num in range(0, instance.duration_days):
                new_activities.append(activity_models.Activity(
                    parent=instance, date=instance.start_date + timedelta(days=num)))
            activity_models.Activity.objects.bulk_create(new_activities)
    else:
        if not instance.is_recurring:
            new_activities = []
            try:
                activity = activity_models.Activity.objects.filter(
                    parent=instance, date__gte=now())
                activity.delete()
                for num in range(0, instance.duration_days):
                    new_activities.append(activity_models.Activity(
                        parent=instance, date=instance.start_date + timedelta(days=num)))         
                activity_models.Activity.objects.bulk_create(new_activities)
            except Exception as exc:
                error = settings.ERROR_MODEL(
                    description=f'{exc.args}', type=f'{exc.args}')
                error.save()
