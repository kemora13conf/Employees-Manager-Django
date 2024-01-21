from django.urls import path
from .views import index, employees, departments, positions, roles 

urlpatterns = [
    path('dashboard', index, name='index'),
    path('employees', employees, name='employees'),
    path('departments', departments, name='departments'),
    path('positions', positions, name='positions'),
    path('roles', roles, name='roles'),
]