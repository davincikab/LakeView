# Generated by Django 3.0.2 on 2020-01-21 04:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200121_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 21, 4, 58, 50, 187109, tzinfo=utc), verbose_name='Date of Birth'),
        ),
    ]
