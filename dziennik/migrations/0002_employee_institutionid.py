# Generated by Django 3.1.4 on 2021-01-05 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='institutionid',
            field=models.IntegerField(null=True),
        ),
    ]