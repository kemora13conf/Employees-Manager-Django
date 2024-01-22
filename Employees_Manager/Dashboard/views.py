from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .Forms import EmployeeForm
from Auth.models import Employee

@login_required(login_url='login')
def index(request, route=None):
    return render(request, 'base.html')

@login_required(login_url='login')
def get_employee_form(request):
    id = request.GET.get('id', None)
    employee = get_object_or_404(Employee, pk=id) if id else None
    if employee:
        form = EmployeeForm(instance=employee)
    else: 
        form = EmployeeForm()
    return render(request, 'forms/Employee.html', {'form': form, 'employee': employee})