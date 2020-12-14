from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views
from . import views
from .views import  RegisterView
from rest_framework import routers  
urlpatterns = [
    path('', views.main, name='main'),
    #path('', include('django.contrib.auth.urls')),
    path('panel/admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    #path('login/',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('login/',allauth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='base.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    #path('signup/', RegisterView.as_view(), name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),  
    path('week/',views.week_list, name='week_list') 
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