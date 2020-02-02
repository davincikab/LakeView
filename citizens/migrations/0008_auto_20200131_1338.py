# Generated by Django 3.0.2 on 2020-01-31 10:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0007_auto_20200131_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='date_completed',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 1, 31, 10, 38, 39, 881259, tzinfo=utc), verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sorted',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 38, 39, 877261, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teammembers',
            name='picture',
            field=models.ImageField(default='download.jpg', upload_to='teammembers'),
        ),
    ]