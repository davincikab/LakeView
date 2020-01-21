# Generated by Django 3.0.2 on 2020-01-21 04:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0006_auto_20200121_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 21, 4, 58, 50, 189107, tzinfo=utc), verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='phone_number',
            field=models.CharField(blank=True, default='0704893840', max_length=12, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sorted',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 21, 4, 58, 50, 190106, tzinfo=utc)),
        ),
    ]
