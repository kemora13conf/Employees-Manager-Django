from django.urls import path
from .views import index, employees, employees_crud, departments, positions, primes

urlpatterns = [
    path('dashboard', index, name='index'),
    path('employees', employees, name='employees'),
    path('employees/<int:id>', employees_crud, name='employees_crud'),
    path('departments', departments, name='departments'),
    path('positions', positions, name='positions'),
    path('primes', primes, name='roles'),
]