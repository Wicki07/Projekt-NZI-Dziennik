# Generated by Django 3.1.4 on 2021-01-18 21:16

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


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
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email address')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Telefon musi być podany w formacie: '999999999'.", regex='^\\+?1?\\d{9,15}$')])),
                ('role', models.CharField(default=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('start_time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('end_time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('periodicity', models.IntegerField(default=0, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('remind_employee', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('profile', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Institutions',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('specialization', models.CharField(default=True, max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('first_name', models.CharField(default=True, max_length=20)),
                ('last_name', models.CharField(default=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Telefon musi być podany w formacie: '999999999'.", regex='^\\+?1?\\d{9,15}$')])),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2021, 1, 18, 21, 16, 29, 582829, tzinfo=utc))),
                ('institution_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.institution')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=True, max_length=20)),
                ('last_name', models.CharField(default=True, max_length=20)),
                ('age', models.IntegerField(default=0)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presence', models.IntegerField(default=False)),
                ('remind_parent', models.BooleanField(default=False)),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.activity')),
                ('child_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.child')),
            ],
            options={
                'verbose_name_plural': 'Attendances',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=32)),
                ('child_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.child')),
                ('institution_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.institution')),
            ],
            options={
                'verbose_name_plural': 'Assignments',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.employee'),
        ),
        migrations.AddField(
            model_name='activity',
            name='isntitution_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dziennik.institution'),
        ),
    ]
