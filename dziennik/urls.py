from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views
from . import views
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('', views.main, name='main'),
    #path('', include('django.contrib.auth.urls')),
    path('panel/admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    #path('login/',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('login/',allauth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='base.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('newinstitution/', views.newinstitution, name='newinstitution'),
    path('newemployee/', views.newemployee, name='newemployee'),
    path('newactivity/', views.newactivity, name='newactivity'),
    path('newchild/', views.newchild, name='newchild'),
    #path('signup/', RegisterView.as_view(), name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),  
    path('week/',views.week_list, name='week_list') ,

    #path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    #path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    #path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete')

]



'''
mARCIN123@#
	
    {{form.username}}
    {{form.first_name}}
    {{form.last_name}}
    {{form.email}}
    {{form.password1}}
    {{form.password2}}  
    {{form.phone}}

'''


#Timer
import time
import datetime
import pytz
from threading import Thread, Lock
from .models import User, Employee, Activity,Child
from django.core.mail import EmailMessage

def tick():
    # usuwanie pracownika po 24h nieaktwowanego konta
    time=pytz.timezone('Europe/Warsaw')
    pracownicy = Employee.objects.filter(active=False)
    for pr in pracownicy:
        if (pr.creation_date + datetime.timedelta(days=1)) < time.localize(datetime.datetime.now()):
            print("Employee: "+ pr.first_name +" "+ pr.last_name  + " was deleted! - UserID: " + str(pr.userid))
            Employee.objects.filter(id=pr.pk).delete()
            User.objects.filter(id=pr.userid).delete()
    
    # powiadomienia o zajęciach
    zajecia = Activity.objects.all()
    for zaj in zajecia:
        # sprawdzenie daty
        start_zajec = datetime.datetime.strptime(str(zaj.data_rozpoczecia) + " " + str(zaj.godzina_rozpoczecia), '%Y-%m-%d %H:%M:%S')
        #print("zajecia: " + str(start_zajec - datetime.timedelta(days=1)))
        #print("teraz:   " + str(datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')))
        if (start_zajec - datetime.timedelta(days=1) == datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')):
            print("----------/ Powiadomienie o zajęciach /----------")
            print("Nazwa: "+str(zaj))
            # powiadomienie pracownika
            pracownik = Employee.objects.get(id=zaj.prowadzacy)  
            print("Prowadzący: "+str(pracownik))
            mail_subject = "Przypomnienie o zajeciach."
            message = render_to_string('email/powiadomienie_o_zajeciach.html', {
                'zajecia': zajecia,
                'user': pracownik,
            })
            to_email = pracownik.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            '''email.send()'''
            # powiadomienie podopiecznych
            podopieczni = Child.objects.filter(id=int(zaj.uczniowie)) 
            
            print("Podopieczni: "+str(podopieczni))
            for ucz in podopieczni:
                rodzic = User.objects.get(id=ucz.parentid)
                print("Wysłane do: "+str(rodzic))
                mail_subject = "Przypomnienie o zajeciach."
                message = render_to_string('email/powiadomienie_o_zajeciach.html', {
                    'zajecia': zajecia,
                    'user': rodzic,
                })
                to_email = rodzic.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                '''email.send()'''
            print("-------------------------------------------------")

def timer():
    while True:
        tick()
        time.sleep(60) # w sekundach (60 = 1 na minute)

t = Thread(target=timer, args=(), kwargs={})
t.setDaemon(True)
t.start()

#2021-01-12 12:41:09+00:00
#2021-01-11 13:54:22.916489