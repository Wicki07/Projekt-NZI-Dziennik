from logging import error
from allauth import account
import calendar

import numpy as np
from django.db.models.functions.text import Length
from django.utils import timezone
from django.core.serializers import serialize
from django.utils.translation import gettext
from django.utils import translation
from django.core import serializers
from django.shortcuts import redirect ,render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import MailUpdateForm, RegisterForm, CreationForm ,RegisterCreation, NameAndSurnameChangeForm, AlternativeRegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.http import HttpResponse
from django.shortcuts import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, confirmed_change_email_token,confirmed_change_password_token
from django.core.mail import EmailMessage
from .models import Institution, Employee, Activity, Child, Assignment, Attendance, EmailChange 
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import datetime
import random
import string
from django.db.models.functions import Lower
from allauth.account.views import LoginView
from django.urls import resolve


def main(request):
    return render(request, 'main/main.html')

User = get_user_model() 
class CustomLoginView(LoginView):

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember'] 
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True     
        return super(CustomLoginView, self).form_valid(form)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.role = 'User'
            user.creation_date = datetime.datetime.now()
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta w serwisie Dziennik.'
            message = render_to_string('email/activation_email.html', {
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

            return render(request, 'signup/person/signup_person.html', {'form': form, 'message': 'Na podany email została wysłana wiadomośc z linkiem aktywującym konto.'})
    else:
        form = RegisterForm()
    return render(request, 'signup/person/signup_person.html', {'form': form})

def signup_institution(request):
    if request.method == 'POST':
        form = AlternativeRegisterForm(request.POST or None)
        print(form.is_valid())
        print(form)
        if form.is_valid():
            # Tworzenie konta instytucji
            user = form.save(commit=False)
            user.active = False
            user.role = 'Institution'
            user.last_name = '-'
            user.phone=form.data['phone']
            user.first_name=form.data['name']
            user.save()

            # Tworzenie profilu instytucji
            Institution.objects.create(user_id=user,email=user.email,name=form.data['name'],category=form.data['category'],profile=form.data['profile'])

            # Wysyłanie wiadomości aktywującej konto
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta w serwisie Dziennik.'
            message = render_to_string('email/activation_email.html', {
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

            return render(request, 'signup/institution/signup_institution.html', {'form': form, 'message': 'Na podany email została wysłana wiadomośc z linkiem aktywującym konto.'})
    else:
        form = AlternativeRegisterForm()
    return render(request, 'signup/institution/signup_institution.html', {'form': form})

def create_employee(request):
    if request.user.is_authenticated: # Czy zalogowany
        institution = Institution.objects.get(user_id=request.user)
        if request.method == 'POST':
            form = RegisterCreation(request.POST or None)
            if form.is_valid():
                # Tworzenie konta pracownika
                user = form.save(commit=False)
                user.active = False
                user.role = 'Employee'
                user.phone=form.data['phone']
                user.save()
                
                # Tworzenie profilu pracownika
                specialization=form.data['specjalization']
                phone=form.data['phone']
                Employee.objects.create(institution_id=institution,user_id=user,first_name=user.first_name,last_name=user.last_name,specialization=specialization,email=user.email,phone=phone,creation_date=datetime.datetime.now())
                print(Employee.objects.get(user_id=user))
                # Wysyłanie wiadomości aktywującej konto
                current_site = get_current_site(request)
                mail_subject = 'Aktywacja konta w serwisie Dziennik.'
                message = render_to_string('email/activation_email.html', {
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
                
                return render(request, 'create/employee/create_employee.html', {'form': form, 'message': 'Na podany email została wysłana wiadomośc z linkiem aktywującym konto.'})
        else:
            form = CreationForm()

    
    generated_password_size = 8
    generated_password_chars = string.ascii_uppercase + string.digits
    generated_password = ''.join(random.choice(generated_password_chars) for _ in range(generated_password_size))

    return render(request, 'create/employee/create_employee.html', {'generated_password': generated_password})

def create_activity(request):
    if request.user.is_authenticated: # Czy zalogowany
        institution = Institution.objects.get(user_id=request.user)
        if request.method == 'POST':
            # Dane z formularza
            data = request.POST.dict()
            employee_id = data.get('employee')
            name = data.get('name')
            date = data.get('date')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            periodicity = data.get('periodicity')

            employee = Employee.objects.get(id=employee_id)
            
            # Tworzenie nowego objektu Activity
            activity = Activity.objects.create(isntitution_id=institution, name=name, date=date, start_time=start_time, end_time=end_time, employee_id=employee,periodicity=periodicity ) 
            
            # Dopisywanie przypisania wybranych dzieci
            children = request.POST.getlist('children')
            print(children)
            for child in children:
                __child = Child.objects.get(id=child)
                print(__child)
                Attendance.objects.create(child_id=__child,activity_id=activity)


            return render(request, 'create/activity/create_activity.html', {'activity':activity})

        employees = Employee.objects.filter(institution_id=institution)
        assigned_children = Child.objects.none()
        institution = Institution.objects.get(user_id=request.user)
        assigements = Assignment.objects.filter(status="Accepted", institution_id=institution)
        for assigement in assigements:
            assigned_children |= Child.objects.filter(id=assigement.child_id.pk)

        return render(request, 'create/activity/create_activity.html', {'employees':employees,'children':assigned_children})
        
    return render(request, 'create/activity/create_activity.html', {})

def create_child(request):
    if request.user.is_authenticated: # Czy zalogowany
        if request.method == 'POST':
            data = request.POST.dict()
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            age = data.get('age')
            parent = request.user
            
            # Tworzenie nowego profilu dziecka
            child = Child.objects.create(parent_id=parent, first_name=first_name, last_name=last_name, age=age) 
            
            return render(request, 'create/child/create_child.html', {'parent': parent,'child':child})

    return render(request, 'create/child/create_child.html', {})

def activate(request, uidb64, token):  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.role == "Employee":
            employee = Employee.objects.get(user_id=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        employee = None

        if user.role == "Employee":
          employee = Employee.objects.get(user_id=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        if user.role == "Employee":
          employee = None

    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        if user.role == "Employee":
            employee.active=True
            employee.save()
        user.save()

        if user.role == "Employee":
          employee.active=True
          employee.save()

        # return redirect('home')
        return render(request, 'account/activate.html', {'title':"Dziękujemy za potwierdzenie emaila",'activation_message':" Twoje konto zostało aktywowane."})
    else:
        return render(request, 'account/activate.html', {'title':"Wystąpił błąd.",'activation_message':"Link aktywazyjny jest nieprawidłowy lub został już użyty!"})

# wyliczanie numeru tygodnia (wykorzystywne przy ustawianiu zajęć w odpowiednie tygodnie)
def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x==day)[0][0] + 1
    return(week_of_month)

def schedule(request, display_type='week'):
    # Tryp wyświetlania
    # 0 - day
    # 1 - week
    # 2 - month

    # Odsyłanie do default czyli week
    if(display_type != 'day' and display_type != 'week' and display_type != 'month'):
        display_type = 'week'
        return redirect(schedule,'week')

    # Polska translacja - konkretnie do dni tygodnia
    translation.activate('pl')
    shedule_title=''
    error_message = ''
    context = {}
    if request.user.is_authenticated: # Czy zalogowany
        # Przekazanie imion dzieci do danych zajęć (lista) w Dict
        children_in_activity = {} # [!] Jest tutaj bo musi byc widoczne
        remind = {} # [!] Jest tutaj bo musi byc widoczne

        # Przechwycenie formularzy
        data = request.POST.dict()

        # Ustalanie ram danego tygodnia
        some_day_last_week = timezone.now().date()
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        week_number = datetime.date(timezone.now().year,timezone.now().month,timezone.now().day).isocalendar()[1]
        datetime_object_day = datetime.datetime.strptime(str(timezone.now().day), "%d")
        datetime_object_month = datetime.datetime.strptime(str(timezone.now().month), "%m")

        # Ustawianie tytułu harmonogramu
        if(display_type=='day'):
            shedule_title = gettext(datetime_object_day.strftime("%d"))+" "+gettext(datetime_object_month.strftime("%B"))+", "+gettext(datetime_object_day.strftime("%A"))
        if(display_type=='week'):
            shedule_title = "Tydzień "+str(week_number)
        if(display_type=='month'):
            shedule_title = gettext(datetime_object_month.strftime("%B"))+ " "+ str(timezone.now().year) 

        # Przygotowanie tablicy z numerami dnia
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        this_week_days_numbers = []
        iterator = 0
        for day_number in week_days:
            __day_number = (monday_of_last_week + timedelta(days=iterator)).day
            iterator += 1
            this_week_days_numbers.append(__day_number)


        """
        # Pobieranie zajęć
        activities = Activity.objects.none()
        # Dla pracownika
        if request.user.role == "Employee":
            employee = Employee.objects.get(user_id=request.user)
            activities = Activity.objects.filter(employee_id=employee)

             # Interakcja z zajęciami (ustawienie przypomnień i wysylanie wiadomości)
            change_remind_activity = data.get('changeRemindActivity')
            send_mesage = data.get('sendMesage') 
            activityId = data.get('hiddenActivityId')
            message = data.get('hoverMessageToEmployee')# Hidden input aby forma odczytała
        """



        # Przechwycenie formularzy
        data = request.POST.dict()

        # Ustalanie ram danego tygodnia
        some_day_last_week = timezone.now().date()
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        
        # Zwiekszenie zasiegu dla podglądu miesiąca
        this_month_days = calendar.monthrange(timezone.now().year,timezone.now().month)[1]
        if(display_type=='month'):
            monday_of_this_week = monday_of_last_week + timedelta(days=this_month_days - timezone.now().day)
            monday_of_last_week = datetime.date(timezone.now().year,timezone.now().month,1)
        
        # Przygotowanie tablicy z numerami dnia
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        this_week_days_numbers = []
        iterator = 0
        for day_number in week_days:
            __day_number = (monday_of_last_week + timedelta(days=iterator)).day
            iterator += 1
            this_week_days_numbers.append(__day_number)

        # Pobieranie zajęć
        activities = Activity.objects.none()

        # Pojemnik na obecność dzieci
        childrenAttendence = {}

        # Dla pracownika
        if request.user.role == "Employee":
            employee = Employee.objects.get(user_id=request.user)
            activities = Activity.objects.filter(employee_id=employee)

             # Interakcja z zajęciami (ustawienie przypomnień i wysylanie wiadomości)
            change_remind_activity = data.get('changeRemindActivity')
            send_mesage = data.get('sendMesage') 
            activityId = data.get('hiddenActivityId')
            message = data.get('hoverMessageToEmployee')# Hidden input aby forma odczytała


            
            if change_remind_activity != 0:
                for activity in activities:
                    if change_remind_activity == '1':
                        activity.remind_employee = False
                        activity.save()
                        error_message = 'Włączono powiadomienie o zajęciach'
                    if change_remind_activity == '-1':
                        activity.remind_employee = True
                        activity.save()
                        error_message = 'Wyłączono powiadomienie o zajęciach'

            if send_mesage:
                activity = Activity.objects.get(id=activityId)
                # wysyłanie emaili
                attendances = Attendance.objects.filter(activity_id=activity)
                for attendance in attendances:
                    parent = User.objects.get(id=attendance.child_id.parent_id.pk)
                    mail_subject = "Powiadomienie od "+str(request.user)+" w sprawie zajęć "+str(activity.name)
                    message = render_to_string('email/announcement.html', {
                        'activity': activity,
                        'targetUser': parent,
                        'message': message,
                    })
                    to_email = parent.email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    
                activity.finished=True
                activity.save()
                error_message = 'Wysłano powiadomienie o odwołaniu zajęć'


            # Update listy obecności
            # Zmiana na obecne
            ch_attendence = Attendance.objects.none()
            children_present = request.POST.getlist('children_present')
            for ch_present in children_present:
                ch_attendence = Attendance.objects.get(id=int(ch_present))
                ch_attendence.presence = True
                ch_attendence.save()
            # Zmiana na nieobecne
            children_absent = request.POST.getlist('children_absent')
            for ch_absent in children_absent:
                ch_attendence = Attendance.objects.get(id=int(ch_absent))
                ch_attendence.presence = False
                ch_attendence.save()
            # W innym przypadku nie robimy nic

            activities = activities.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week)
            for activity in activities:
                date = str(activity.date)  
                remind[activity.pk] = activity.remind_employee
                
                # Pobranie informacji o obecności dzieci
                # umieszczamy w słowniku pod etykietą, o wartości id, queryset z wszystkimi obecnościami
                childrenAttendence[activity.pk] = Attendance.objects.filter(activity_id=activity)
                #
                week_day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
                setattr(activity,'day',week_day)
                if display_type == 'month':
                    data_temp = datetime.datetime.strptime(date, '%Y-%m-%d')
                    setattr(activity,'weekNumber',get_week_of_month(data_temp.year,data_temp.month,data_temp.day))
                

        ######## Wyświetlanie planu pracowników przez instytucje
        elif request.user.role == "Institution":
            serialized_activity = '[{}]'
            serialized_children = '[{}]'
            institution = Institution.objects.get(user_id=request.user)
            employees = Employee.objects.filter(institution_id=institution)
            activities = Activity.objects.none()
            for employee in employees :
                _activities = Activity.objects.filter(employee_id=employee)

                __activities = _activities.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week)
                activities |= __activities
            children = Attendance.objects.none()
            for a in activities:
                children |=  Attendance.objects.filter(activity_id = a)
                date = str(a.date)
                week_day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
                setattr(a,'day',week_day)
                if display_type == 'month':
                    data_temp = datetime.datetime.strptime(date, '%Y-%m-%d')
                    setattr(a,'weekNumber',get_week_of_month(data_temp.year,data_temp.month,data_temp.day))
            _children_list = Assignment.objects.filter(institution_id = institution)
            children_list = Child.objects.none()

            for assigement in _children_list:
                if assigement.status=='Accepted':
                    children_list |= Child.objects.filter(id=assigement.child_id.pk)
            

            # Usuwanie zajęć z panelu Instytucji
            if data.get("deleteActivityByInstitution"):
                Activity.objects.get(id=data.get('hiddenActivityIdToDelete')).delete() #usuwanie zajęć
                return render(request, 'schedule/schedule.html',{'display_type':display_type,'schedule_title':shedule_title,'thisWeek':this_week_days_numbers,'children_in_activity':children_in_activity,'remind':remind,'message':error_message,'activities':activities,'institutionActivitiesJSON':serialized_activity,'employees': employees,'childrenActivitiesJSON':serialized_children,'children':children_list,'message':'Usunięto zajęcia'})

            serialized_activity = serializers.serialize('json',activities)
            serialized_children = serializers.serialize('json',children)
            # Aktualizacja zajęć z panelu Instytucji
            if data.get("updateActivitySubmit"):
                activity_to_update = Activity.objects.get(id= data.get('idActivityToUpdate'))
                # Dane z formularza
                _employee_id = data.get('employee')
                activity_to_update.name = data.get('name')
                activity_to_update.date = data.get('date')
                activity_to_update.start_time = data.get('start_time')
                activity_to_update.end_time = data.get('end_time')
                activity_to_update.periodicity = data.get('periodicity')
                activity_to_update.employee_id = Employee.objects.get(id=_employee_id)
                activity_to_update.save()
                
                # Dopisywanie przypisania wybranych dzieci
                children = request.POST.getlist('children')
                try:
                    toDeleteAttendences = Attendance.objects.filter(activity_id=activity_to_update)
                    for xAttend in toDeleteAttendences:
                        xAttend.delete()
                except Attendance.DoesNotExist:
                    pass
                for child in children:
                    __child = Child.objects.get(id=child)
                    Attendance.objects.create(child_id=__child,activity_id=activity_to_update)
                return render(request, 'schedule/schedule.html',{'display_type':display_type,'schedule_title':shedule_title,'thisWeek':this_week_days_numbers,'children_in_activity':children_in_activity,'remind':remind,'message':error_message,'activities':activities,'institutionActivitiesJSON':serialized_activity,'employees': employees,'childrenActivitiesJSON':serialized_children,'children':children_list,'message':'Zaktualizowano zajęcia'})
            return render(request, 'schedule/schedule.html',{'display_type':display_type,'schedule_title':shedule_title,'thisWeek':this_week_days_numbers,'children_in_activity':children_in_activity,'remind':remind,'message':error_message,'activities':activities,'institutionActivitiesJSON':serialized_activity,'employees': employees,'childrenActivitiesJSON':serialized_children,'children':children_list})

        # Reszra użytkowników
        elif request.user.role == "User":
            #activities = []
            setattr(activities,'child',Child.objects.none())
            children = Child.objects.filter(parent_id=request.user.pk)

            # Interakcja z zajęciami (ustawienie przypomnień i wysylanie wiadomości)
            change_remind_activity = data.get('changeRemindActivity')
            send_mesage = data.get('sendMesage') 
            activityId = data.get('hiddenActivityId')
            message = data.get('hoverMessageToEmployee')# Hidden input aby forma odczytała

            
            if change_remind_activity != 0:
                for child in children:
                    attendances = Attendance.objects.filter(child_id=child,activity_id=activityId)
                    for attendance in attendances:
                        if change_remind_activity == '1':
                            attendance.remind_parent = False
                            attendance.save()
                            error_message = 'Wyłączono powiadomenie o zajęciach'
                        if change_remind_activity == '-1':
                            attendance.remind_parent = True
                            attendance.save()
                            error_message = 'Włączono powiadomenie o zajęciach'

            if send_mesage:
                activity = Activity.objects.get(id=activityId)
                # wysyłanie emaila
                mail_subject = "Powiadomienie od "+str(request.user)+" w sprawie zajęć "+str(activity.name)
                message = render_to_string('email/announcement.html', {
                    'activity': activity,
                    'targetUser': activity.employee_id,
                    'message': message,
                })
                to_email = activity.employee_id.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                error_message = 'Wysłano wiadomość do prowadzącego'

            for child in children:
                # Pobranie zajęć do jakich jest przypisane dane dziecko
                attendances = Attendance.objects.filter(child_id=child)
                for attendance in attendances:
                    remind[attendance.activity_id.pk] = False
                    if attendance.remind_parent:
                        remind[attendance.activity_id.pk] = attendance.remind_parent

                    # Dodanie zajęć do wyświetlenia
                        # Filtrowanie zajęć po dacie
                        # date_gte - Date Greater Than or Equal
                        # date_lt  - Date Less Than

                    __activities = Activity.objects.filter(id=attendance.activity_id.pk)

                    __activities = Activity.objects.filter(id=attendance.activity_id.id,date__gte=monday_of_last_week, date__lt=monday_of_this_week)

                    #setattr(__activity,'child',child)
                    #activities.extend(__activity)
                    activities |= __activities
                    
                    for __activity in __activities:
                        children_in_activity[(__activity.id,child.id)] = str(child)

            activities = activities.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week)

            for activity in activities:
                date= str(activity.date)
                day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
                week_day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
                setattr(activity,'day',week_day)
                if display_type == 'month':
                    data_temp = datetime.datetime.strptime(date, '%Y-%m-%d')
                    setattr(activity,'weekNumber',get_week_of_month(data_temp.year,data_temp.month,data_temp.day))

            print(activities)
        #print(error_message)

        return render(request, 'schedule/schedule.html',{'display_type':display_type,'schedule_title':shedule_title,'thisWeek':this_week_days_numbers,'children_in_activity':children_in_activity,'childrenAttendence':childrenAttendence,'remind':remind,'message':error_message,'activities':activities})
    print(error_message)
    return render(request, 'schedule/schedule.html',{'display_type':display_type})

def view_children(request):
    print(request.user)
    if request.user.is_authenticated: # Czy zalogowany
        message = ''
        children = Child.objects.filter(parent_id=request.user)

        data = request.POST.dict() # Dane z frontu do backendu w psotaci slownika
        childId = data.get('toDeleteHiddenChildID') # Odczytanie danych po etykiecie(name) z formularza który jest ukryty 'hiddenChildID'

        # USUWANIE DZIECKA
        childDelete = data.get('deleteChild') # Odczytanie czy chcemy usunąć dziecko
        if childDelete:
            Child.objects.filter(id=childId).delete()

        # EDYCJA DZIECKA
        childEdit = data.get('editChild')
        childIdEdit = data.get('toEditHiddenChildID')
        childToEdit = Child.objects.none()
        if childEdit:
            childToEdit = Child.objects.get(id=childIdEdit)
            childToEdit.first_name = data.get('first_name')
            childToEdit.last_name = data.get('last_name')
            childToEdit.age = data.get('age')
            childToEdit.save()
            message = "Poprawnie zmieniono dane profilu dziecka"


        institution_list = {}
        # Lista instytucji do których dziecko jest przypisane
        for child in children:
            assigments = Assignment.objects.filter(child_id=child)
            child_institution_list = {}
            for assigment in assigments:
                child_institution_list[assigment.id] = str(assigment.institution_id)
            institution_list[child.pk] = child_institution_list
        return render(request, 'view/children/view_children.html', {'children': children,'institution_list':institution_list,'childDelete':childDelete,'message':message})
    return render(request, 'view/children/view_children.html', {})


def assign_child(request):
    if request.user.is_authenticated: # Czy zalogowany
        institutions = Institution.objects.all()
        __child_id = 0
        institution_id = 0
        institution = Institution.objects.none()
        assignment = Assignment.objects.none()
        
        if request.method == 'POST':
            data = request.POST.dict() # Dane z frontu do backendu w psotaci slownika
            __child_id = data.get('hiddenChildID') # Odczytanie danych po etykiecie(name) z formularza który jest ukryty 'hiddenChildID'

            child = Child.objects.get(id=__child_id)
            if data.get('listaInstytucji'):
                institution_id = data.get('listaInstytucji')
                institution = Institution.objects.get(id=institution_id)
                assignment = Assignment.objects.create(child_id = child, institution_id = institution)
        return render(request, 'assign/child/assign_child.html',{'childID':__child_id,'institutions':institutions,'assignment':assignment})

    return render(request, 'assign/child/assign_child.html',{})

def view_assignments(request):
    if request.user.is_authenticated: # Czy zalogowany
        if request.method == 'POST':
            data = request.POST.dict()
            accept = data.get('accept')
            refuse = data.get('refuse')
            assignmentId = data.get('hiddenAssigmentID')
            assignment = Assignment.objects.get(id=assignmentId)
            if accept:
                assignment.status = "Accepted"
                assignment.save()
            if refuse:
                assignment.delete()
        
        institution = Institution.objects.get(user_id=request.user)
        assignments = Assignment.objects.filter(institution_id=institution,status="Pending") 
        for assignment in assignments:
            setattr(assignment,'parent',assignment.child_id.parent_id)

        return render(request, 'view/assignments/view_assignments.html',{'assignments':assignments})
    return render(request, 'view/assignments/view_assignments.html',{})

def view_settings(request):
    return render(request, 'view/settings/view_settings.html',{})


def name_surname_change(request):
    try:
        account = User.objects.get(id=request.user.pk)
    except User.DoesNotExist:
        return HttpResponse("coś się popsuło")
    context ={}
    if request.POST:
        form = NameAndSurnameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render (request,'view/settings/name_surname_change.html',{'message': 'Dane zostały zmienione'})
        else:
            form = NameAndSurnameChangeForm(request.POST, instance=request.user)
            context['form'] = form
            return render (request,'view/settings/name_surname_change.html',{'message': 'Coś poszło nie tak'})
    else:
        form = NameAndSurnameChangeForm(request.POST, instance=request.user)
                
        context['form'] = form
        return render(request, 'view/settings/name_surname_change.html',context)

def institution_change_about_us(request):
    if request.user.is_authenticated: # Czy zalogowany
        institution = Institution.objects.get(user_id = request.user)
        if request.POST:
            # pobierane dane z formularza 
            # i ustawione dane instytycji na dane z formularze
            data = request.POST.dict()
            # po get sa dane z formularza
            institution.name = data.get('name')
            user = institution.user_id
            user.first_name= data.get('name')
            user.save()
            institution.category = data.get('category')
            institution.profile = data.get('profile')
            institution.save()
            return render(request, 'view/settings/institution_change_about_us.html',{'institution':institution,'message': 'Poprawnie zmienione dane'})

        return render(request, 'view/settings/institution_change_about_us.html',{'institution':institution})
    return render(request, 'view/settings/institution_change_about_us.html',{})

def confirmed_change_email(request, uidb64, token):
    ############
    #jak activity 
    #odbieramy i  zz tamtego modelu odczytujemy i zmieniamy mail
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    email = EmailChange.objects.none()
    try:
        #sprawdzenie czy user to user
        if user.role == "User":
            email = EmailChange.objects.get(user_id=user)
        #Sprawdza czy user istnieje i token 
        if user is not None and confirmed_change_email_token.check_token(user, token):
            print(user.email)
            print(email.new_email)
            user.email = str(email.new_email)
            print(user.email)
            user.save()
            email.delete()
            current_site = get_current_site(request)
            mail_subject = 'Zmiana adresu e-mail.'
            #towrzenie massage
            message = render_to_string('email/change_email.html', {
                'user': request.user,
            })
            #email do kogo wysylamy
            to_email = user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            #wyslanie maila
            email.send()
            update_session_auth_hash(request, user_handler)
            return render(request, 'account/confirmed_change_email_activate.html', {'title':"Email został pomyślnie zmieniony",'activation_message':" Możesz sie teraz zalogować"})
        else:
            return render(request, 'account/confirmed_change_email_activate.html', {'title':"Wystąpił błąd.",'activation_message':"Link aktywacyjny jest nieprawidłowy lub został już użyty!"})
    except EmailChange.DoesNotExist:
        return render(request, 'account/confirmed_change_email_activate.html', {'title':"Wystąpił błąd.",'activation_message':"Link aktywacyjny jest nieprawidłowy lub został już użyty!"})

def change_email(request):
    try:
        account = User.objects.get(id=request.user.pk)
    except User.DoesNotExist:
        return HttpResponse("coś się popsuło")
        #return redirect('login')
    context ={}
    if request.POST:
        #dane
        data = request.POST.dict()
        new_email = data.get('email')
        print(new_email)
        old_email = request.user.email
        #try sprawdzajacy czy nie ma juz modelu przypisanego do modeli emailchange
        try:
            EmailChange.objects.get(user_id=account)
            form = MailUpdateForm(request.POST, instance=request.user)
            context['form'] = form
            return render (request,'view/settings/change_email.html',{'message': 'Podany adres email wysyłał już zmianę'})
        except EmailChange.DoesNotExist:
            form = MailUpdateForm(request.POST, instance=request.user)
            # warunek sprawdzajacy czy email nie jest juz w bazie 
            if  User.objects.filter(email=new_email):
                return render (request,'view/settings/change_email.html',{'message': 'Podany adres email jest już zajęty'})
            #sprawdzenie czy email nie jest taki sam jak request
            if  data.get('email') != request.user.email and data.get('email') != account.email :
                #przypisanie do modelu emailchange bo musimy gdizes zapisac te dane przed wyslaniem potwierdzenia
                EmailChange.objects.create(user_id=request.user,change_date=datetime.datetime.now(),old_email=old_email,new_email=new_email)
                #form.save()
                #wysylanie maila
                #zczytanie danych
                current_site = get_current_site(request)
                mail_subject = 'Potwierdź zmianę adresu e-mail.'
                #towrzenie massage
                message = render_to_string('email/confirmation_email.html', {
                    'user': request.user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token':account_activation_token.make_token(request.user),
                })
                #email do kogo wysylamy
                to_email = new_email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                #wyslanie maila
                email.send()
                return render (request,'view/settings/change_email.html',{'form':form ,'message': 'Na podany email została wysłana wiadomośc z linkiem potwierdzającym zmiane emailu.'})
            else:
                form = MailUpdateForm(request.POST, instance=request.user)
                context['form'] = form
                return render (request,'view/settings/change_email.html',{'message': 'Podany adres email jest już zajęty'})
    else:
        form = MailUpdateForm(request.POST, instance=request.user)
                
        context['form'] = form
        return render(request, 'view/settings/change_email.html',context)

def confirmed_change_password(request):
    try:
        account = User.objects.get(id=request.user.pk)
    except User.DoesNotExist:
        return HttpResponse("coś się popsuło")
        #return redirect('login')
    current_site = get_current_site(request)
    mail_subject = 'Potwierdź zmianę hasła.'
    #towrzenie massage
    message = render_to_string('email/confirmation_password.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token':account_activation_token.make_token(request.user),
    })
    #email do kogo wysylamy
    to_email = request.user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    #wyslanie maila
    email.send()
    return render (request,'view/settings/confirmed_change_password.html',{'message': 'Na podany email została wysłana wiadomośc z linkiem potwierdzającym zmiane hasła.'})
  

def change_password(request, uidb64, token):
    #jak activity 
    #odbieramy i  zz tamtego modelu odczytujemy i zmieniamy mail
    uid = force_text(urlsafe_base64_decode(uidb64))
    current_url = request.get_full_path_info()
    print("print")
    print(current_url)
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse("coś się popsuło")
        #return redirect('login')
    if request.method == 'POST':
        # Formularz z html zostaje przekazany, oraz user
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user_handler = form.save()
            # Linia 664 Jest Konieczna aby zaktualizować hasło
            # Wymagane jest zaktowalizowanie hasha w sesji
            update_session_auth_hash(request, user_handler)
            return render (request,'view/settings/change_password.html',{'message': 'Hasło zostało zmienione'})
        else:
            return render (request,'view/settings/change_password.html',{'message': 'Hasła się nie zgadzają'})
    else:
        form = PasswordChangeForm(request.user)
                
        return render(request, 'view/settings/change_password.html',{'form':form})
    

    
