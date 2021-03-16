from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views
from . import views
from django.conf.urls import url 
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_view
import dziennik.timers
urlpatterns = [
    path('', views.main, name='main'),
    #path('', include('django.contrib.auth.urls')),
    path('panel/admin/', include('smuggler.urls')),
    path('panel/admin/', admin.site.urls, name='panel_admin'),
    path('accounts/', include('allauth.urls')),
    path('login/',allauth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='base.html'), name='logout'),
    path('signup/person/', views.signup, name='signup'),
    path('signup/institution/', views.signup_institution, name='signup_institution'),
    path('create/employee/', views.create_employee, name='create_employee'),
    path('create/activity/', views.create_activity, name='create_activity'),
    path('create/child/', views.create_child, name='create_child'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),  
    path('schedule/week/',views.schedule_week, name='schedule_week'),
    path('view/children/',views.view_children, name='view_children') ,
    path('assign/child/',views.assign_child, name='assign_child'),
    path('view/assignments/',views.view_assignments, name='view_assignments'),
    path('view/settings/',views.view_settings, name='view_settings'),
    path('view/settings/change_email/',views.change_email, name='change_email'),
    path('view/settings/change_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.change_password, name='change_password'),
    path('view/settings/change_personal_data',views.name_surname_change, name='name_surname_change'),
    path('view/settings/change_institution_data',views.institution_change_about_us, name='institution_change_about_us'),
    path('confirmed_change_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.confirmed_change_email,name='confirmed_change_email'),
    path('view/settings/confirmed_change_password',views.confirmed_change_password,name='confirmed_change_password')
]