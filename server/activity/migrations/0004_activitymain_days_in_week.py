# Generated by Django 3.1.2 on 2020-11-14 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activity", "0003_remove_activitymain_days_of_week"),
    ]

    operations = [
        migrations.AddField(
            model_name="activitymain",
            name="days_in_week",
            field=models.ManyToManyField(blank=True, to="activity.DaysOfTheWeek"),
        ),
    ]
