from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from Auth.models import Employee, Department, Position, TypePrime, Prime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from Dashboard.Forms import EmployeeForm

def responeObject(data):
    return {
        'status': 'success',
        'data': data
    }

# Create your views here.
@login_required(login_url='login')
def index(request):
    return HttpResponse('<h1>Dashboard</h1>')

@login_required(login_url='login')
def employees(request):
    # create a new employee
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
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
            
            type_primes = form.cleaned_data['primes']
            for type_prime_name in type_primes:
                type_prime = TypePrime.objects.filter(name=type_prime_name).first()
                if type_prime is not None:
                    prime = Prime(
                        employee=employee,
                        type_prime=type_prime,
                        date=form.cleaned_data['join_date']
                    )
                    prime.save()  
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error in {field}: {error}')
        
        return redirect('/employees') 
    
    # get the list of employees
    page_index = request.GET.get('page', 1)
    item_per_page = 5
    all_employees = Employee.objects.all()
    prime = Prime.objects.all()
    
    paginator = Paginator(all_employees, item_per_page)
    paginator.page_index = page_index
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
    if request.method == 'GET':
        employee = Employee.objects.get(employee_id=id)
        return JsonResponse(responeObject({
            'employee': employee.toJson(),
        }))
    
    elif request.method == 'POST':
        employee = get_object_or_404(Employee, pk=id) if id else None
        if employee is None:
            return redirect('/employees')
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
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
            type_primes = form.cleaned_data['primes'];
            for type_prime_name in type_primes:
                type_prime = TypePrime.objects.filter(name=type_prime_name).first()
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

@login_required(login_url='login')
def departments(request):
    return HttpResponse('<h1>Departments</h1>')

@login_required(login_url='login')
def positions(request):
    return HttpResponse('<h1>Positions</h1>')

@login_required(login_url='login')
def primes(request):
    return HttpResponse('<h1>Primes</h1>')
