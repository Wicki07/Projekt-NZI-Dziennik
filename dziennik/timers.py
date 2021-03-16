
#Timer
import time
import datetime
import pytz
from threading import Thread, Lock
from .models import User, Employee, Activity, Child, Attendance,EmailChange
from django.core.mail import EmailMessage

from django.template.loader import render_to_string



def removeChangeEmail():
    # usuwanie pracownika po 24h nieaktwowanego konta
    time=pytz.timezone('Europe/Warsaw')
    email = EmailChange.objects.filter()
    for us in email:
        if (us.change_date + datetime.timedelta(days=1)) < time.localize(datetime.datetime.now()):
            EmailChange.objects.filter(id=us.pk).delete()
            ##User.objects.filter(id=pr.user_id).delete()
def removeInactiveUsers():
    # usuwanie pracownika po 24h nieaktwowanego konta
    time=pytz.timezone('Europe/Warsaw')
    users = User.objects.filter(active=False)
    for us in users:
        if (us.creation_date + datetime.timedelta(days=1)) < time.localize(datetime.datetime.now()):
            print("User: "+ us.first_name +" "+ us.last_name  + " was deleted! - UserID: " + str(us.id))
            User.objects.filter(id=us.pk).delete()
            ##User.objects.filter(id=pr.user_id).delete()
def remindEmployee():
    # powiadomienia o pracownika zajęciach
    activities = Activity.objects.filter(finished=False,remind_employee=True)
    for activity in activities:
        # sprawdzenie daty
        activity_start_time = datetime.datetime.strptime(str(activity.date) + " " + str(activity.start_time), '%Y-%m-%d %H:%M:%S')
        if (activity_start_time - datetime.timedelta(days=1) == datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')):
            print("----------/ Powiadomienie o zajęciach /----------")
            print("Nazwa: "+str(activity))

            # wysyłanie emaila

            employee =activity.employee_id

            employee = Employee.objects.get(id=activity.employee_id)  

            print("Prowadzący: "+str(employee))
            mail_subject = "Przypomnienie o zajeciach."
            message = render_to_string('email/remind.html', {
                'activity': activity,
                'user': employee,
            })
            to_email = employee.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            print("-------------------------------------------------")
            
def remindParent():
    # powiadomienie rodziców
    activities = Activity.objects.filter(finished=False)
    for activity in activities: 
        attendances = Attendance.objects.filter(remind_parent=True,activity_id=activity)
        for attendance in attendances:
            child = attendance.child_id
            parent = child.parent_id # Objekt rodzica
            activity_start_time = datetime.datetime.strptime(str(activity.date) + " " + str(activity.start_time), '%Y-%m-%d %H:%M:%S')
            if (activity_start_time - datetime.timedelta(days=1) == datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')):
                print("----------/ Powiadomienie o zajęciach /----------")

        for attendance in attendances:
            child = Child.objects.get(id=attendance.child_id.pk)
            parent = child.parent_id # Objekt rodzica
            activity_start_time = datetime.datetime.strptime(str(activity.date) + " " + str(activity.start_time), '%Y-%m-%d %H:%M:%S')
            if (activity_start_time - datetime.timedelta(days=1) == datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')):

                print("Wysłane do: "+str(parent))
                mail_subject = "Przypomnienie o zajeciach."
                message = render_to_string('email/remind.html', {
                    'child': str(child),
                    'activity': activity,
                    'user': parent,
                })
                to_email = parent.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                print("-------------------------------------------------")

def refreshPeriodicity():
    # Odświerze cykliczności zajęć
    # Jeżeli zajęcia się zakończą (i mają ustawioną cykliczność) to zostaną przesunięte (lub sklonowane) o ustalony czas 
    activities = Activity.objects.filter(finished=False)
    for activity in activities:
        if activity.periodicity:
            # Sprawdzanie czy zajęcia się już odbyły
            activity_end = datetime.datetime.strptime(str(activity.date) + " " + str(activity.end_time), '%Y-%m-%d %H:%M:%S')
            actual_date =  datetime.datetime.strptime(str(datetime.datetime.now())[0:16], '%Y-%m-%d %H:%M')

            if activity_end < actual_date:
                # Odchaczenie zajęć ze zostały skończone (aby ich ponownie nie przedlozac)
                activity.finished = True
                activity.save()

                periodicity = activity.periodicity
                if periodicity:
                    # Klonowanie zajęć
                    Activity.objects.create(
                        employee_id = activity.employee_id,
                        isntitution_id = activity.isntitution_id,
                        name = activity.name,
                        date = activity.date + datetime.timedelta(days=activity.periodicity),
                        start_time = activity.start_time,
                        end_time = activity.end_time,
                        periodicity = activity.periodicity
                    )
                    # Klonowanie listy uczniów
                    attendences = Attendance.objects.filter(activity_id=activity)
                    for attendance in attendences:
                        # presence - jest ustawiany domyslnie (aby była czysta lista obecności)
                        Attendance.objects.create(
                            activity_id = activity,
                            child_id = attendance.child_id,
                            remind_parent = attendance.remind_parent,
                            remind = attendance.remind
                        )
            


# URUCHAMIANIE TIMERÓW
def timeFormater(seconds):
    return str(datetime.time(seconds // 3600, (seconds % 3600) // 60, seconds % 60))


def removeInactiveUsersTimer():
    time_span = 3600 # w sekundach (60 = 1 na minute)
    print("Uruchomiono sprawdzanie kont urzytkownków (usuwanie nieaktywych po 24h), Freq: "+ timeFormater(time_span))
    while True:
        print("Usuwanie nieaktywnych kont urzytkownków które istnieja ponad 24h...")
        removeInactiveUsers()
        time.sleep(time_span) 

t2 = Thread(target=removeInactiveUsersTimer, args=(), kwargs={})
t2.setDaemon(True)
t2.start()

def remindEmployeeTimer():
    time_span = 60 # w sekundach (60 = 1 na minute)
    print("Uruchomiono powiadamianie pracowników o zajęciach, Freq: "+ timeFormater(time_span))
    while True:
        print("Wysyłanie przypomnień do pracowników...")
        remindEmployee()
        time.sleep(time_span) 

t3 = Thread(target=remindEmployeeTimer, args=(), kwargs={})
t3.setDaemon(True)

t3.start()

# t2.start()

def remindParentTimer():
    time_span = 60 # w sekundach (60 = 1 na minute)
    print("Uruchomiono powiadamianie rodziców o zajęciach, Freq: "+ timeFormater(time_span))
    while True:
        print("Wysyłanie przypomnień do rodziców...")
        remindParent()
        time.sleep(time_span) 

t4 = Thread(target=remindParentTimer, args=(), kwargs={})
t4.setDaemon(True)
t4.start()


def refreshPeriodicityTimer():
    time_span = 60 # w sekundach (60 = 1 na minute)
    print("Uruchomiono obsługę cykliczności zajęć (automatyczne tworzenie kolejnych), Freq: "+ timeFormater(time_span))
    while True:
        print("Przedłużanie zajęć cyklicznych...")
        refreshPeriodicity()
        time.sleep(time_span) 

t5 = Thread(target=refreshPeriodicityTimer, args=(), kwargs={})
t5.setDaemon(True)
t5.start()

def removeChangeEmailTimer():
    time_span = 60 # w sekundach (60 = 1 na minute)
    print("Uruchomiono sprawdzanie zmian emaili (usuwanie nieaktywych po 24h), Freq: "+ timeFormater(time_span))
    while True:
        print("Usuwanie nieaktywnych modeli")
        removeChangeEmail()
        time.sleep(time_span) 

t6 = Thread(target=removeChangeEmailTimer, args=(), kwargs={})
t6.setDaemon(True)
t6.start()
