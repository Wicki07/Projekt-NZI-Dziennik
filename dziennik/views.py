from django.db.models.functions.text import Length
from django.utils import timezone
from django.shortcuts import redirect ,render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RegisterForm, CreationForm ,RegisterCreation
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Institution, Employee,Activity,Child, Zgloszenie
from django.utils import timezone
from datetime import timedelta
import datetime
import random
from django.db.models import Q 
#A Q object (django.db.models.Q) is an object 
#used to encapsulate a collection of keyword arguments. These keyword arguments are specified as in “Field lookups” above.
from django.db.models.functions import Lower


def main(request):
    return render(request, 'main/main.html')

User = get_user_model() 
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.role = 'User'
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('email/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'signup/signup.html', {'form': form, 'message': 'Please confirm your email address to complete the registration'})
    else:
        form = RegisterForm()
    return render(request, 'signup/signup.html', {'form': form})

def newinstitution(request):
    if request.method == 'POST':
        form = CreationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.role = 'Institution'
            user.phone=form.data['phone']
            user.save()
            Institution.objects.create(userid=user.pk,email=user.email,nazwa=user.first_name,kategoria=form.data['kategoria'],profil=form.data['profil'])
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('email/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'newinstitution/newinstitution.html', {'form': form, 'message': 'Please confirm your email address to complete the registration'})
    else:
        form = CreationForm()
    return render(request, 'newinstitution/newinstitution.html', {'form': form})

def newemployee(request):
    if request.method == 'POST':
        form = RegisterCreation(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.role = 'Employee'
            user.phone=form.data['phone']
            user.save()
            #zamienic user na instytucje
            dane = request.POST.dict()
            instytucja = dane.get('instytucja')
            Employee.objects.create(institutionid=instytucja,userid=user.pk,first_name=user.first_name,last_name=user.last_name,specjalization=form.data['specjalization'],email=user.email,phone=form.data['phone'],creation_date=datetime.datetime.now())
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('email/acc_active_email.html', {
                'pass': form.data['password1'],
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'newemployee/newemployee.html', {'form': form, 'message': 'Please confirm your email address to complete the registration'})
    else:

        form = CreationForm()
    

    wyghaslo = random.randrange(10000, 1000000)   
    return render(request, 'newemployee/newemployee.html', {'form': form , 'wyghaslo': wyghaslo})

def newactivity(request):
    if request.method == 'POST':
        #if form.is_valid():
            #Institution.objects.create(email=user.email,nazwa=user.first_name,kategoria=form.data['kategoria'],profil=form.data['profil'])
            
        dane = request.POST.dict()
        instytucja = dane.get('instytucja')
        nazwa = dane.get('name')
        data_rozpoczecia = dane.get('data_rozpoczecia')
        godzina_rozpoczecia = dane.get('godzina_rozpoczecia')
        godzina_zakonczenia = dane.get('godzina_zakonczenia')
        prowadzacy = dane.get('prowadzacy')
        uczniowie = dane.get('uczniowie')
        Activity.objects.create(instytucja=instytucja, nazwa=nazwa, data_rozpoczecia=data_rozpoczecia, godzina_rozpoczecia=godzina_rozpoczecia, godzina_zakonczenia=godzina_zakonczenia, prowadzacy=prowadzacy, uczniowie=uczniowie ) 
        return render(request, 'newactivity/newactivity.html', {'instytucja': instytucja,'nazwa':nazwa,'data_rozpoczecia':data_rozpoczecia,'godzina_rozpoczecia':godzina_rozpoczecia,'godzina_zakonczenia':godzina_zakonczenia,'prowadzacy':prowadzacy,'uczniowie':uczniowie})

    pracownicy = Employee.objects.filter(institutionid=request.user.pk)
    #print(pracownicy)
    return render(request, 'newactivity/newactivity.html', {'pracownicy':pracownicy})

def newchild(request):
    if request.method == 'POST':
        #if form.is_valid():
            #Institution.objects.create(email=user.email,nazwa=user.first_name,kategoria=form.data['kategoria'],profil=form.data['profil'])
            
        dane = request.POST.dict()
        parentid = dane.get('rodzic')
        first_name = dane.get('first_name')
        last_name = dane.get('last_name')
        age = dane.get('age')
        
        Child.objects.create(parentid=parentid, first_name=first_name, last_name=last_name, age=age) 
        return render(request, 'newchild/newchild.html', {'parentid': parentid,'first_name':first_name,'last_name':last_name,'age':age})

    return render(request, 'newchild/newchild.html', {})

def newactivity(request):
    if request.method == 'POST':
        #if form.is_valid():
            #Institution.objects.create(email=user.email,nazwa=user.first_name,kategoria=form.data['kategoria'],profil=form.data['profil'])
            
        dane = request.POST.dict()
        instytucja = dane.get('instytucja')
        nazwa = dane.get('name')
        data_rozpoczecia = dane.get('data_rozpoczecia')
        godzina_rozpoczecia = dane.get('godzina_rozpoczecia')
        godzina_zakonczenia = dane.get('godzina_zakonczenia')
        prowadzacy = dane.get('prowadzacy')
        uczniowie = dane.get('uczniowie')
        Activity.objects.create(instytucja=instytucja, nazwa=nazwa, data_rozpoczecia=data_rozpoczecia, godzina_rozpoczecia=godzina_rozpoczecia, godzina_zakonczenia=godzina_zakonczenia, prowadzacy=prowadzacy, uczniowie=uczniowie ) 
        return render(request, 'newactivity/newactivity.html', {'instytucja': instytucja,'nazwa':nazwa,'data_rozpoczecia':data_rozpoczecia,'godzina_rozpoczecia':godzina_rozpoczecia,'godzina_zakonczenia':godzina_zakonczenia,'prowadzacy':prowadzacy,'uczniowie':uczniowie})

    pracownicy = Employee.objects.filter(institutionid=request.user.pk)
    #print(pracownicy)
    return render(request, 'newactivity/newactivity.html', {'pracownicy':pracownicy})

def newchild(request):
    if request.method == 'POST':
        #if form.is_valid():
            #Institution.objects.create(email=user.email,nazwa=user.first_name,kategoria=form.data['kategoria'],profil=form.data['profil'])
            
        dane = request.POST.dict()
        parentid = dane.get('rodzic')
        first_name = dane.get('first_name')
        last_name = dane.get('last_name')
        age = dane.get('age')
        
        Child.objects.create(parentid=parentid, first_name=first_name, last_name=last_name, age=age) 
        return render(request, 'newchild/newchild.html', {'parentid': parentid,'first_name':first_name,'last_name':last_name,'age':age})

    return render(request, 'newchild/newchild.html', {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.role == "Employee":
          employee = Employee.objects.get(userid=user.pk)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        if user.role == "Employee":
          employee = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        if user.role == "Employee":
          employee.active=True
          employee.save()
        
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def week_list(request):
    #lte=Less than or equal to
    #podglad = Activity.objects.filter(uczniowie=request.user.pk) # zamienić na dziecko
    podglad = Activity.objects.none()
    dzieci = Child.objects.filter(parentid=request.user.pk)
    for dziecko in dzieci:
        podglad |= Activity.objects.filter(uczniowie=dziecko.pk)

    some_day_last_week = timezone.now().date()
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    filtr = podglad.filter(data_rozpoczecia__gte=monday_of_last_week, data_rozpoczecia__lt=monday_of_this_week)
    for podgla in filtr:
        date= str(podgla.data_rozpoczecia)
        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        da = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        setattr(podgla,'day',da)
        child = Child.objects.get(parentid=request.user.pk,id=podgla.uczniowie)
        if child:
            setattr(podgla,'child',child)
    return render(request, 'week/week.html',{'filtr':filtr})

def list_pupils(request):
    dzieci = Child.objects.filter(parentid=request.user.pk)
    return render(request, 'list_pupils/list_pupils.html', {'dzieci': dzieci})

def find_institution(request):
    tempChildid = 0
    institutionid = 0
    if request.method == 'POST':
        dane = request.POST.dict()#Dane z frontu do backendu w psotaci slownika
        tempChildid = int(dane.get('ukrytyPatryk'))#Odczytanie danych po etykiecie(name) z formularza który jest ukryty
        if dane.get('listaInstytucji'):
            institutionid = dane.get('listaInstytucji')
            Zgloszenie.objects.create(childid = tempChildid, idinstytucji = institutionid, opis = "Zgloszenie")

    if request.method =='GET':
        query = str(request.GET.get('searchBar'))
        dane = request.GET.dict()#Dane z frontu do backendu w psotaci slownika
        tempChildid = int(dane.get('ukrytyPatryk2'))#Odczytanie danych po etykiecie(name) z formularza który jest ukryty
        object_list = Institution.objects.filter(
            Q(nazwa__icontains=query)
        )
        return render(request,'find_institution/find_institution.html',{'object_list':object_list,'childid':tempChildid})

    institution = Institution.objects.all()
    return render(request, 'find_institution/find_institution.html',{'childid':tempChildid,'institution':institution})
