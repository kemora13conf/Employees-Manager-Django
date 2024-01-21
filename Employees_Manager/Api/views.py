from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    return HttpResponse('<h1>Dashboard</h1>')
@login_required(login_url='login')
def employees(request):
    return HttpResponse('<h1>Employees</h1>')

@login_required(login_url='login')
def departments(request):
    return HttpResponse('<h1>Departments</h1>')

@login_required(login_url='login')
def positions(request):
    return HttpResponse('<h1>Positions</h1>')

@login_required(login_url='login')
def roles(request):
    return HttpResponse('<h1>Salaries</h1>')
