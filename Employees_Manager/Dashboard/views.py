from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required(login_url='login')
def index(request, route=None):
    return render(request, 'base.html')

