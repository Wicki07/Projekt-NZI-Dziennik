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

# Model Użytkownika
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # Tworzy i zapisuje Użytkownika z podanym email'em i hasłem
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        # Tworzy i zapisuje Użytkownika (STAFF) z podanym email'em i hasłem
        user = self.create_user(
            email,
            password=password,
        )

        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # Tworzy i zapisuje Użytkownika (SuperUser) z podanym email'em i hasłem
        user = self.create_user(
            email,
            password=password,
        )

        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# Definiowanie na nowo noewgo Modelu Użytkownika (Custom)
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # Definiuje czy konto jest Admin'em - nie SuperUser'em
    admin = models.BooleanField(default=False) # Definiuje czy konto jest SuperUser'em
    first_name = models.CharField(max_length = 20, default='')
    last_name = models.CharField(max_length = 20, default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon musi być podany w formacie: '999999999'.") # Sprawdza format numeru telefonu
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role = models.CharField(max_length = 20, default=True)
    creation_date = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Pola email i hasło są ustawione jak wymagane domyslne
    objects = UserManager() # Istotne - ustawia Manager'owie atrybut 'get_by_natural_key'
    
    def get_full_name(self):
        # Użytkownik jest identyfikowany poprzez adress email
        return self.email

    def get_short_name(self):
        # Użytkownik jest identyfikowany poprzez adress email
        return self.email

    def __str__(self):
        if self.role == 'Institution':
            return self.first_name
        else:
            return self.first_name+" "+self.last_name

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

    class Meta:
        verbose_name_plural = "Users"

class Institution(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    profile = models.CharField(max_length=200)
    creation_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    def publish(self):
        self.save()
        
    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Institutions"

class Employee(models.Model):
    institution_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    specialization = models.CharField(max_length = 20,default=True)
    active = models.BooleanField(default=False)
    first_name = models.CharField(max_length = 20,default=True)
    last_name = models.CharField(max_length = 20,default=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon musi być podany w formacie: '999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    creation_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "Employees"

class Activity(models.Model):
    isntitution_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    employee_id = models.ForeignKey('Employee', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateField(blank=True, default=timezone.now)
    start_time = models.TimeField(blank=True, default=timezone.now)
    end_time = models.TimeField(blank=True, default=timezone.now)
    periodicity = models.IntegerField(null=True, default=0)
    finished = models.BooleanField(default=False)
    remind_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "Activities"

class Child(models.Model):
    parent_id = models.ForeignKey('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20,default=True)
    last_name = models.CharField(max_length = 20,default=True)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "Children"

class Assignment(models.Model):
    child_id = models.ForeignKey('Child', on_delete=models.CASCADE)
    institution_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    status = models.CharField(max_length=32,default='Pending')

    def __str__(self):
        return str(self.child_id)+" -> "+str(self.institution_id)+" ["+str(self.status)+"]"

    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "Assignments"
        
class Attendance(models.Model):
    child_id = models.ForeignKey('Child', on_delete=models.CASCADE)
    activity_id = models.ForeignKey('Activity', on_delete=models.CASCADE)
    presence = models.IntegerField(default=False)
    remind_parent = models.BooleanField(default=False)

    def __str__(self):
            return str(self.child_id)+" -> "+str(self.activity_id)+" ["+str(self.presence)+"]"


    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "Attendances"
        