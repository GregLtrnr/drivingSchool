from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as userLogin, logout as userLogout
from django.contrib.auth.models import User
from .models import Account, Appointment
from django.utils import timezone
from datetime import date, timedelta, datetime as dt

import datetime

# Create your views here.

def index(request):
  return renderTemplate(request, 'myapp/index.html')

def login(request):
  if(request.user.is_authenticated):
    return redirect('index')
  if(request.method == 'POST'):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      userLogin(request, user)
      return redirect('index')
    else:
      print('Invalid credentials')
      return renderTemplate(request, 'myapp/login.html', {'error': 'username or password is incorrect'})
  else:
    return renderTemplate(request, 'myapp/login.html')

def logout(request):
  userLogout(request)
  return redirect('index')

def profile(request):
  if not request.user.is_authenticated:
    return redirect('index')
  
  try:
    AccountUser = Account.objects.get(user=request.user)

    AccountUser.email = User.objects.get(id=AccountUser.user_id).email
    bookedLessons = Appointment.objects.filter(student=AccountUser).count()
    context = {
      'userInformations': AccountUser,
      'bookedLessons': bookedLessons,
      'paidLessonLeft': AccountUser.paid_hours - bookedLessons,
    }
    return renderTemplate(request, 'myapp/profile.html', context)

  except Account.DoesNotExist:
    return redirect('index')

def schedule(request):
  if not request.user.is_authenticated:
    return redirect('index')
  if (request.method == 'POST'):
    AccountUser = Account.objects.get(user=request.user)
    date_start = request.POST['date_start']
    date_format = "%Y-%m-%dT%H:%M"
    tempStart = date_start
    date_end =  dt.strptime(tempStart, date_format)+timedelta(hours=1)
    location = request.POST['location']
    student = Account.objects.get(user=request.POST['student'])
    Appointment.objects.create(
      date_start=date_start,
      date_end=date_end,
      location=location,
      instructor=AccountUser,
      student=student,
    )
    return redirect('schedule')
  AccountUser = Account.objects.get(user=request.user)
  now = timezone.now()
  accounts = Account.objects.filter(account_type='student')
  context = {
    'accounts': accounts,
  }
  print(accounts)
  return renderTemplate(request, 'myapp/schedule.html', context)

def getAppointments(request):
  AccountUser = Account.objects.get(user=request.user)
  if(AccountUser.account_type == 'student'):
    appointments = Appointment.objects.filter(student=AccountUser)
  else:
    appointments = Appointment.objects.filter(instructor=AccountUser)
  for appointment in appointments:
    appointment.studentInfo = Account.objects.get(id=appointment.student_id)
    
  return JsonResponse({'appointments': list(appointments.values())})

def book(request):
  return renderTemplate(request, 'myapp/book.html')


def secretarySchedule(request):
  return renderTemplate(request, 'myapp/secretarySchedule.html')

def dashboard(request):
  return renderTemplate(request, 'myapp/dashboard.html')

def getAccounts(request):
  if(request.user.is_authenticated):
    AccountUser = Account.objects.get(user=request.user)
    if AccountUser.account_type == 'students':
      return redirect('index')
    if (request.method == "DELETE"):
      match AccountUser.account_type:
        case 'admin':
          Account.objects.delete(id=request.POST['id'])
        case 'secretary':
          if(Account.objects.get(id=request.POST['id']).account_type != 'admin'):
            Account.objects.delete(id=request.POST['id'])
    match AccountUser.account_type:
      case 'admin':
        Accounts = Account.objects.all()
      case 'secretary':
        desired_types = ["instructor", "student"]
        Accounts = Account.objects.filter(account_type__in=desired_types)
      case _:
        Accounts = Account.objects.filter(account_type='student')
    for account in Accounts:
      account.email = User.objects.get(id=account.user.id).email
      account.username = User.objects.get(id=account.user.id).username
    context = {
      'accounts': Accounts,
    }

    return renderTemplate(request, 'myapp/accounts.html', context)
  return redirect('index')

def newAccount(request):
  context = {}
  AccountUser = Account.objects.get(user=request.user)
  if not request.user.is_authenticated or AccountUser.account_type == 'students' or AccountUser.account_type == 'instructors':
    return redirect('index')
  if(request.method == 'GET'):
    id = request.GET.get('id')
    if(id):
      try:
        account = Account.objects.get(id=id)
        account.email = User.objects.get(id=account.user_id).email
        context = {
          'account': account if account else None,
        }
      except Account.DoesNotExist:
        context = {}

    return renderTemplate(request, 'myapp/editAccount.html', context)
  elif(request.method == 'POST'):
    if(request.POST.get('id', False)):
      try:
        account = Account.objects.get(id=request.POST['id'])
        user = User.objects.get(id=account.user_id)
        account.first_name = request.POST['first_name'] if request.POST['first_name'] != '' else account.first_name
        account.last_name = request.POST['last_name'] if request.POST['last_name'] != '' else account.last_name
        account.date_of_birth = request.POST['date_of_birth'] if request.POST['date_of_birth'] != '' else account.date_of_birth
        account.account_type = request.POST['account_type'] if request.POST['account_type'] != '' else account.account_type
        account.address = request.POST['address'] if request.POST['address'] != '' else account.address
        account.paid_hours = request.POST['paid_hours'] if request.POST['paid_hours'] != '' else account.paid_hours
        user.email = request.POST['email'] if request.POST['email'] != '' else user.email
        if(request.POST['password'] and request.POST['password'] != '' and request.POST['confirm_password']): 
          user.set_password(request.POST['password'])
        user.save()
        account.save()
        return redirect('getAccounts')
      except Account.DoesNotExist:
        return renderTemplate(request, 'myapp/editAccount.html', {'error': 'account does not exist'})
    try:
      newUser = User.objects.create_user(
        username=request.POST['first_name']+request.POST['last_name'],
        email=request.POST['email'],
        password=request.POST['password'],
      )
      Account.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        date_of_birth=request.POST['date_of_birth'],
        account_type=request.POST['account_type'],
        address=request.POST['address'],
        paid_hours=request.POST['paid_hours'],
        user=newUser,
      )
      return redirect('getAccounts')
    except (KeyError):
      print(KeyError)
      return renderTemplate(request, 'myapp/editAccount.html', {'error': 'all fields are required for creation'})
  return renderTemplate(request, 'myapp/editAccount.html')

def renderTemplate(request, template, context={}):
  if(request.user.is_authenticated):
    try:
      AccountUser = Account.objects.get(user=request.user)
      context.update({'account_role': AccountUser.account_type if AccountUser else None})
    except:
      context.update({'account_role': None})
  return render(request, template, context)
