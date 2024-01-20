from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return HttpResponse('<a href="/auth/logout">Logout</a>')