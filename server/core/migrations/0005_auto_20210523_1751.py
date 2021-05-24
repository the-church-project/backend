# Generated by Django 3.1.2 on 2021-05-23 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201106_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familycard',
            name='expiry_date',
            field=models.DateField(blank=True, null=True, verbose_name='date of expiry'),
        ),
        migrations.AlterField(
            model_name='familycard',
            name='issue_date',
            field=models.DateField(blank=True, null=True, verbose_name='date of issue'),
        ),
        migrations.AlterUniqueTogether(
            name='family',
            unique_together={('family_name', 'hash_number')},
        ),
        migrations.RemoveField(
            model_name='family',
            name='username',
        ),
    ]