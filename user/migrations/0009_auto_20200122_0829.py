# Generated by Django 3.0.2 on 2020-01-22 05:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200121_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 22, 5, 29, 15, 846059, tzinfo=utc), verbose_name='Date of Birth'),
        ),
    ]