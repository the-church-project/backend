# Generated by Django 3.1.2 on 2020-10-18 20:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='hash_number',
            field=models.PositiveIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
