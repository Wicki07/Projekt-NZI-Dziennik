# Generated by Django 3.1.4 on 2021-01-14 13:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0005_auto_20210114_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 14, 13, 55, 30, 308595, tzinfo=utc)),
        ),
    ]