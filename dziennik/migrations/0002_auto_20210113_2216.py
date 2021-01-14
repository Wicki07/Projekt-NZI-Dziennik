# Generated by Django 3.1.4 on 2021-01-13 21:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zgloszenie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('childid', models.IntegerField(null=True)),
                ('idinstytucji', models.IntegerField(null=True)),
                ('opis', models.CharField(default=True, max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 21, 16, 33, 361799, tzinfo=utc)),
        ),
    ]
