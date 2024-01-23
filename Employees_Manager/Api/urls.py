from django.urls import path
from .views import index, employees, employees_crud, departments, departments_crud, positions, positions_crud, primes, typeprimes_crud, error_page

urlpatterns = [
    path('dashboard', index, name='index'),
    path('employees', employees, name='employees'),
    path('employees/<int:id>', employees_crud, name='employees_crud'),
    path('departments', departments, name='departments'),
    path('departments/<int:id>', departments_crud, name='departments_crud'),
    path('positions', positions, name='positions'),
    path('positions/<int:id>', positions_crud, name='positions_crud'),
    path('primes', primes, name='primes'),
    path('primes/<int:id>', typeprimes_crud, name='typeprimes_crud'),
    path('error_page', error_page, name='error_page'),
]