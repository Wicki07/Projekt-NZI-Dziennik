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
from django.shortcuts import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Institution, Employee, Activity, Child, Assignment, Attendance
from django.utils import timezone
from datetime import timedelta
import datetime
import random
import string
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
            user.creation_date = datetime.datetime.now()
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
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
        form = CreationForm(request.POST or None)
        if form.is_valid():
            # Tworzenie konta instytucji
            user = form.save(commit=False)
            user.active = False
            user.role = 'Institution'
            user.last_name = '-'
            user.phone=form.data['phone']
            user.save()

            # Tworzenie profilu instytucji
            Institution.objects.create(user_id=user,email=user.email,name=user.first_name,category=form.data['category'],profile=form.data['profile'])

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
        form = CreationForm()
    return render(request, 'signup/institution/signup_institution.html', {'form': form})

def create_employee(request):
    if request.user != "": # Czy zalogowany
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

    return render(request, 'create/employee/create_employee.html', {})
    
    generated_password_size = 8
    generated_password_chars = string.ascii_uppercase + string.digits
    generated_password = ''.join(random.choice(generated_password_chars) for _ in range(generated_password_size))

    return render(request, 'create/employee/create_employee.html', {'form': form , 'generated_password': generated_password})

def create_activity(request):
    if request.user != "": # Czy zalogowany
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
    if request.user != "": # Czy zalogowany
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

def schedule_week(request):
    if request.user != "": # Czy zalogowany
        # Przekazanie imion dzieci do danych zajęć (lista) w Dict
        children_in_activity = {} # [!] Jest tutaj bo musi byc widoczne
        remind = {} # [!] Jest tutaj bo musi byc widoczne

        # Przechwycenie formularzy
        data = request.POST.dict()

        # Ustalanie ram danego tygodnia
        some_day_last_week = timezone.now().date()
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)

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
                    if change_remind_activity == '-1':
                        activity.remind_employee = True
                        activity.save()

            if send_mesage:
                '''activity = Activity.objects.get(id=activityId)
                # wysyłanie emaila
                mail_subject = "Powiadomienie od "+str(request.user)+" w sprawie zajęć "+str(activity.name)
                message = render_to_string('email/announcement.html', {
                    'activity': activity,
                    'employee': activity.employee_id,
                    'message': message,
                })
                to_email = activity.employee_id.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()'''

            activities = activities.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week)
            for activity in activities:
                remind[activity.pk] = activity.remind_employee

            for activity in activities:
                date = str(activity.date)  
                day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
                week_day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
                setattr(activity,'day',week_day) 

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
                        if change_remind_activity == '-1':
                            attendance.remind_parent = True
                            attendance.save()

            if send_mesage:
                activity = Activity.objects.get(id=activityId)
                # wysyłanie emaila
                mail_subject = "Powiadomienie od "+str(request.user)+" w sprawie zajęć "+str(activity.name)
                message = render_to_string('email/announcement.html', {
                    'activity': activity,
                    'employee': activity.employee_id,
                    'message': message,
                })
                to_email = activity.employee_id.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

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
                    __activities = Activity.objects.filter(id=attendance.activity_id.id,date__gte=monday_of_last_week, date__lt=monday_of_this_week)
                    #setattr(__activity,'child',child)
                    #activities.extend(__activity)
                    activities |= __activities
                    
                    for __activity in __activities:
                        children_in_activity[(__activity.id,child.id)] = str(child)

            for activity in activities:
                date= str(activity.date)
                day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
                week_day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
                setattr(activity,'day',week_day)

        print(activities)

        return render(request, 'schedule/week/week.html',{'activities':activities,'thisWeek':this_week_days_numbers,'children_in_activity':children_in_activity,'remind':remind})

    return render(request, 'schedule/week/week.html',{})

def view_children(request):
    if request.user != "": # Czy zalogowany
        children = Child.objects.filter(parent_id=request.user)

        data = request.POST.dict() # Dane z frontu do backendu w psotaci slownika
        childDelete = data.get('deleteChild') # Odczytanie czy chcemy usunąć dziecko
        childId = data.get('toDeleteHiddenChildID') # Odczytanie danych po etykiecie(name) z formularza który jest ukryty 'hiddenChildID'
        
        if childDelete:
            Child.objects.filter(id=childId).delete()

        institution_list = {}
        # Lista instytucji do których dziecko jest przypisane
        for child in children:
            assigments = Assignment.objects.filter(child_id=child)
            child_institution_list = {}
            for assigment in assigments:
                child_institution_list[assigment.id] = str(assigment.institution_id)
            institution_list[child.pk] = child_institution_list
        return render(request, 'view/children/view_children.html', {'children': children,'institution_list':institution_list,'childDelete':childDelete})
    return render(request, 'view/children/view_children.html', {})


def assign_child(request):
    if request.user != "": # Czy zalogowany
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
    if request.user != "": # Czy zalogowany
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
