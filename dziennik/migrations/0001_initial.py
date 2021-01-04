# Generated by Django 3.1.4 on 2020-12-19 17:54

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default=True, max_length=20)),
                ('last_name', models.CharField(default=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('role', models.CharField(default='None', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('nazwa', models.CharField(max_length=200)),
                ('kategoria', models.CharField(max_length=200)),
                ('profil', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Podglad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200)),
                ('data_rozpoczecia', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('godzina_rozpoczecia', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('godzina_zakonczenia', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('prowadzacy', models.CharField(max_length=200)),
            ],
        ),
    ]