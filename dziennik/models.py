from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
from django_mysql.models import JSONField, Model

import jsonfield

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in the New Manager to our Model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    first_name = models.CharField(max_length = 20,default=True)
    last_name = models.CharField(max_length = 20,default=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon musi być podany w formacie: '999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    role = models.CharField(max_length = 20,default='None')
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    objects = UserManager() ##### $$$$$$$$$$$$$$$$$$$$$############################################################################################BARDZO W      A   Ż  N  E   W   C  H  U  J 
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

#   python manage.py shell
#   from dziennik.models import Podglad
#   Podglad.objects.create(nazwa='test', data_rozpoczecia='2020-12-17', godzina_rozpoczecia='21:00',godzina_zakonczenia='21:30', prowadzacy='test')
'''class Podglad(models.Model):
    nazwa = models.CharField(max_length=200)
    data_rozpoczecia = models.DateField(blank=True, default=timezone.now)
    godzina_rozpoczecia = models.TimeField(blank=True, default=timezone.now)
    godzina_zakonczenia = models.TimeField(blank=True, default=timezone.now)
    prowadzacy = models.CharField(max_length=200)

    def __str__(self):
        return self.nazwa

    def publish(self):
        self.save()
'''

class Institution(models.Model):
    userid = models.IntegerField()
    email = models.CharField(max_length=200)
    nazwa = models.CharField(max_length=200)
    kategoria = models.CharField(max_length=200)
    profil = models.CharField(max_length=200)

    def __str__(self):
        return self.nazwa

    def publish(self):
        self.save()
        
class Employee(models.Model):
    institutionid = models.IntegerField(null=True)
    userid = models.IntegerField(null=True)
    email = models.CharField(max_length=200)
    specjalization = models.CharField(max_length = 20,default=True)
    active = models.BooleanField(default=False)
    first_name = models.CharField(max_length = 20,default=True)
    last_name = models.CharField(max_length = 20,default=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon musi być podany w formacie: '999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    role = models.CharField(max_length = 20,default='None')
    creation_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def publish(self):
        self.save()

#python manage.py shell
#from dziennik.models import Activity
#Activity.objects.create(instytucja='inst', nazwa='test', data_rozpoczecia='2020-12-17', godzina_rozpoczecia='21:00', godzina_zakonczenia='21:30', prowadzacy='test', uczniowie={'key1':'value1','key2':'value2'} ) 
class Activity(models.Model):
    nazwa = models.CharField(max_length=200)
    instytucja = models.CharField(blank=True, max_length=200) 
    data_rozpoczecia = models.DateField(blank=True, default=timezone.now)
    godzina_rozpoczecia = models.TimeField(blank=True, default=timezone.now)
    godzina_zakonczenia = models.TimeField(blank=True, default=timezone.now)
    cyklicznosc = models.IntegerField(null=True, default=0)
    prowadzacy = models.CharField(null=True,blank=True, max_length=200)
    uczniowie = jsonfield.JSONField(null=True)

    def __str__(self):
        return self.nazwa

    def publish(self):
        self.save()

class Child(models.Model):
    parentid = models.IntegerField(null=True)
    first_name = models.CharField(max_length = 20,default=True)
    last_name = models.CharField(max_length = 20,default=True)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def publish(self):
        self.save()