# Generated by Django 3.0.2 on 2020-02-13 04:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0008_auto_20200131_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('physical_address', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.AlterField(
            model_name='college',
            name='date_completed',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 2, 13, 4, 38, 54, 425906, tzinfo=utc), verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sorted',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 13, 4, 38, 54, 420910, tzinfo=utc)),
        ),
    ]