# Generated by Django 3.1.4 on 2021-01-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0003_auto_20210105_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='userid',
            field=models.IntegerField(null=True),
        ),
    ]