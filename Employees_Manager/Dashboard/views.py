from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .Forms import EmployeeForm, DepartmentForm, PositionForm, TypePrimeForm
from Auth.models import Employee, Department, Position, TypePrime

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

@login_required(login_url='login')
def get_department_form(request):
    id = request.GET.get('id', None)
    department = get_object_or_404(Department, pk=id) if id else None
    if department:
        form = DepartmentForm(instance=department)
    else: 
        form = DepartmentForm()
    return render(request, 'forms/Department.html', {'form': form, 'department': department})

@login_required(login_url='login')
def get_position_form(request):
    id = request.GET.get('id', None)
    position = get_object_or_404(Position, pk=id) if id else None
    if position:
        form = PositionForm(instance=position)
    else: 
        form = PositionForm()
    return render(request, 'forms/Position.html', {'form': form, 'position': position})

@login_required(login_url='login')
def get_typeprime_form(request):
    id = request.GET.get('id', None)
    typeprime = get_object_or_404(TypePrime, pk=id) if id else None
    if typeprime:
        form = TypePrimeForm(instance=typeprime)
    else: 
        form = TypePrimeForm()
    return render(request, 'forms/TypePrime.html', {'form': form, 'typeprime': typeprime})