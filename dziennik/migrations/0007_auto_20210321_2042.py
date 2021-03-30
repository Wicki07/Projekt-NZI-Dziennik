# Generated by Django 3.1.4 on 2021-03-21 19:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0006_auto_20210314_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailchange',
            name='change_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 19, 42, 9, 521529, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 19, 42, 9, 519528, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='institution',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 19, 42, 9, 519528, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 19, 42, 9, 509529, tzinfo=utc)),
        ),
    ]