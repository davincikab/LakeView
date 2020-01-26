# Generated by Django 3.0.2 on 2020-01-26 15:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0011_auto_20200126_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupevents',
            name='attendants_count',
            field=models.IntegerField(default=0, verbose_name='Number of Attendants'),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 26, 15, 44, 7, 155480, tzinfo=utc), verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sorted',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 26, 15, 44, 7, 156480, tzinfo=utc)),
        ),
    ]
