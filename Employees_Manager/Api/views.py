from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from Auth.models import Employee, Department, Position, TypePrime, Prime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from Dashboard.Forms import EmployeeForm, DepartmentForm, PositionForm, TypePrimeForm
from datetime import date
from django.db import models
from django.db.models import Count

def responeObject(data):
    return {
        'status': 'success',
        'data': data
    }
def type_prime_obj(name):
    name = str(name)
    name = name.split(' ')
    for i in range(len(name)):
        # check if the name[i] is a number
        try:
            int(name[i])
            name[1] = int(name[i])
            break
        except ValueError:
            name[0] = name[0] + ' ' + name[i] if i > 0 else name[0]
        
    return {
        'name': name[0],
        'money': name[1]
    }
                
# Create your views here.
@login_required(login_url='login')
def index(request):
     # Total number of employees
    total_employees = Employee.objects.count()

    # Number of employees in each department
    department_counts = Department.objects.annotate(num_employees=Count('employee')).values('name', 'num_employees')

    # Number of employees in each position
    position_counts = Position.objects.annotate(num_employees=Count('employee')).values('name', 'num_employees')

    # Number of employees receiving primes today
    primes_today_count = Prime.objects.filter(date_creation=date.today()).count()

    # Total number of primes given
    total_primes_count = Prime.objects.count()

    # Average salary of all employees
    average_salary = Employee.objects.aggregate(avg_salary=models.Avg('salary'))['avg_salary']

    # Example: Fetching the latest 5 employees joined
    latest_employees = Employee.objects.order_by('-join_date')[:5]

    # Constructing the dashboard data dictionary
    dashboard_data = {
        'total_employees': total_employees,
        'department_counts': list(department_counts),
        'position_counts': list(position_counts),
        'primes_today_count': primes_today_count,
        'total_primes_count': total_primes_count,
        # show only two digits after the decimal point
        'average_salary': f'{average_salary:.2f}',
        'latest_employees': [{'fullname': emp.fullname, 'join_date': emp.join_date, 'department': emp.department.name, 'position': emp.position.name} for emp in latest_employees],
    }
    return render(request, 'dashboard.html', dashboard_data)

def isPrimeError(errors_list):
    if len(errors_list) == 1:
        for error in errors_list:
            err, msg = error
            return err == 'primes'
    return False
                
@login_required(login_url='login')
def employees(request):
    # create a new employee
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid() or ( not form.is_valid() and isPrimeError(form.errors.items()) ):
            employee = Employee(
                fullname=form.cleaned_data['fullname'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                birthday=form.cleaned_data['birthday'],
                address=form.cleaned_data['address'],
                salary=form.cleaned_data['salary'],
                department=form.cleaned_data['department'],
                position=form.cleaned_data['position'],
                join_date=form.cleaned_data['join_date'],
            )
            employee.save()
            
            if not isPrimeError(form.errors.items()):
                type_primes = form.cleaned_data['primes']
                for type_prime_name in type_primes:
                    type_prime_name = type_prime_obj(type_prime_name);
                    type_prime = TypePrime.objects.filter(name=type_prime_name['name'], money=type_prime_name['money']).first()
                    if type_prime is not None:
                        prime = Prime(
                            employee=employee,
                            type_prime=type_prime,
                            date=form.cleaned_data['join_date']
                        )
                        prime.save()
            messages.success(request, 'Employee created successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/employees') 
    
    # get the list of employees
    page_index = request.GET.get('page', 1)
    item_per_page = 6
    all_employees = Employee.objects.all()
    prime = Prime.objects.all()
    
    paginator = Paginator(all_employees, item_per_page)
    paginator.page_index = page_index
    if int(paginator.page_index) == 1 and int(paginator.num_pages) == 1:
        paginator.disable = 'both'
    elif int(paginator.page_index) >= int(paginator.num_pages):
        paginator.disable = 'next'
    elif int(paginator.page_index) <= 1:
        paginator.disable = 'prev'
    else:
        paginator.disable = None;
    try:
        employees = paginator.get_page(page_index)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        employees = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        employees = paginator.get_page(paginator.num_pages)    
    
    # add prime to employees
    for employee in employees:
        employee.prime = 0
        for p in prime:
            if employee.employee_id == p.employee.employee_id:
                employee.prime += p.type_prime.money
                
    return render(request, 'employees.html', {'employees': employees, 'paginator': paginator})

@login_required(login_url='login')
def employees_crud(request, id):    
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=id) if id else None
        if employee is None:
            return redirect('/employees')
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid() or ( not form.is_valid() and isPrimeError(form.errors.items()) ):
            employee.fullname = form.cleaned_data['fullname']
            employee.email = form.cleaned_data['email']
            employee.phone = form.cleaned_data['phone']
            employee.birthday = form.cleaned_data['birthday']
            employee.address = form.cleaned_data['address']
            employee.salary = form.cleaned_data['salary']
            employee.department = form.cleaned_data['department']
            employee.position = form.cleaned_data['position']
            employee.join_date = form.cleaned_data['join_date']
            employee.save()
            
            # delete all the prime and create a new one
            employee.prime_set.all().delete()
            if not isPrimeError(form.errors.items()):
                type_primes = form.cleaned_data['primes'];
                for type_prime_name in type_primes:
                    type_prime_name = type_prime_obj(type_prime_name);
                    print(f'\n\n{type_prime_name}\n\n\n')
                    type_prime = TypePrime.objects.filter(name=type_prime_name['name'], money=type_prime_name['money']).first()
                    if type_prime is not None:
                        prime = Prime(
                            employee=employee,
                            type_prime=type_prime,
                            date=form.cleaned_data['join_date']
                        )
                        prime.save() 
            messages.success(request, 'Employee updated successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/employees')
        
    elif request.method == 'DELETE':
        employee = Employee.objects.get(employee_id=id)
        employee.delete()
        return JsonResponse(responeObject({
            'employee': employee.fullname,
        }))
    return redirect('/employees')

@login_required(login_url='login')
def departments(request):
    # create a new department
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/departments') 
    
    # get the list of departments
    page_index = request.GET.get('page', 1)
    item_per_page = 6
    all_departments = Department.objects.all()
    
    paginator = Paginator(all_departments, item_per_page)
    paginator.page_index = page_index
    if int(paginator.page_index) == 1 and int(paginator.num_pages) == 1:
        paginator.disable = 'both'
    elif int(paginator.page_index) >= int(paginator.num_pages):
        paginator.disable = 'next'
    elif int(paginator.page_index) <= 1:
        paginator.disable = 'prev'
    else:
        paginator.disable = None;
    try:
        departments = paginator.get_page(page_index)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        departments = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        departments = paginator.get_page(paginator.num_pages)    
                
    return render(request, 'departments.html', {'departments': departments, 'paginator': paginator})

@login_required(login_url='login')
def departments_crud(request, id):    
    if request.method == 'POST':
        department = get_object_or_404(Department, pk=id) if id else None
        if department is None:
            return redirect('/departments')
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/departments')
        
    elif request.method == 'DELETE':
        department = Department.objects.get(department_id=id)
        department.delete()
        return JsonResponse(responeObject({
            'department': department.name,
        }))
    return redirect('/departments')

@login_required(login_url='login')
def positions(request):
    # create a new position
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position created successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/positions') 
    
    # get the list of positions
    page_index = request.GET.get('page', 1)
    item_per_page = 6
    all_positions = Position.objects.all()
    
    paginator = Paginator(all_positions, item_per_page)
    paginator.page_index = page_index
    if int(paginator.page_index) == 1 and int(paginator.num_pages) == 1:
        paginator.disable = 'both'
    elif int(paginator.page_index) >= int(paginator.num_pages):
        paginator.disable = 'next'
    elif int(paginator.page_index) <= 1:
        paginator.disable = 'prev'
    else:
        paginator.disable = None;
    try:
        positions = paginator.get_page(page_index)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        positions = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        positions = paginator.get_page(paginator.num_pages)    
                
    return render(request, 'positions.html', {'positions': positions, 'paginator': paginator})

@login_required(login_url='login')
def positions_crud(request, id):    
    if request.method == 'POST':
        position = get_object_or_404(Position, pk=id) if id else None
        if position is None:
            return redirect('/positions')
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position updated successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/positions')
        
    elif request.method == 'DELETE':
        position = Position.objects.get(position_id=id)
        position.delete()
        return JsonResponse(responeObject({
            'position': position.name,
        }))
    return redirect('/positions')

@login_required(login_url='login')
def primes(request):
    # create a new typeprime
    if request.method == 'POST':
        form = TypePrimeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'TypePrime created successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/primes') 
    
    # get the list of typeprimes
    page_index = request.GET.get('page', 1)
    item_per_page = 6
    all_typeprimes = TypePrime.objects.all()
    
    paginator = Paginator(all_typeprimes, item_per_page)
    paginator.page_index = page_index
    if int(paginator.page_index) == 1 and int(paginator.num_pages) == 1:
        paginator.disable = 'both'
    elif int(paginator.page_index) >= int(paginator.num_pages):
        paginator.disable = 'next'
    elif int(paginator.page_index) <= 1:
        paginator.disable = 'prev'
    else:
        paginator.disable = None;
    try:
        typeprimes = paginator.get_page(page_index)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        typeprimes = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        typeprimes = paginator.get_page(paginator.num_pages)    
                
    return render(request, 'typeprimes.html', {'typeprimes': typeprimes, 'paginator': paginator})

@login_required(login_url='login')
def typeprimes_crud(request, id):    
    if request.method == 'POST':
        typeprime = get_object_or_404(TypePrime, pk=id) if id else None
        if typeprime is None:
            return redirect('/typeprimes')
        form = TypePrimeForm(request.POST, instance=typeprime)
        if form.is_valid():
            form.save()
            messages.success(request, 'TypePrime updated successfully!')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/primes')
        
    elif request.method == 'DELETE':
        typeprime = TypePrime.objects.get(type_prime_id=id)
        typeprime.delete()
        return JsonResponse(responeObject({
            'typeprime': typeprime.name,
        }))
    return redirect('/primes')

@login_required(login_url="login")
def error_page(request):
    return render(request, '404.html')
