# Generated by Django 3.0.2 on 2020-01-31 10:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200131_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 31, 10, 38, 39, 873264, tzinfo=utc), verbose_name='Date of Birth'),
        ),
    ]