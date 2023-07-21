
"""drivingschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
  # homepage
  path('', views.index, name='index'),

  # auth
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('profile', views.profile, name='profile'),

  # user schedule
  path('schedule', views.schedule, name='schedule'),
  path('api/appointments', views.getAppointments, name='getAppointments'),
  
  # pages for instructor minimum
  path('accounts', views.getAccounts, name='getAccounts'),
  path('accounts/new', views.newAccount, name='newAccount'),
  path('accounts/edit', views.newAccount, name='editAccount'),

  # pages for secretary minimum
  path('secretary/schedule', views.secretarySchedule, name='secretarySchedule'),

  # pages for admin minimum
]
