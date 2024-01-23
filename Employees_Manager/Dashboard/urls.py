from django.urls import path
from .views import index, get_employee_form, get_department_form, get_position_form, get_typeprime_form

urlpatterns = [
    path('', index, name='index'),
    path('get_employee_form', get_employee_form, name='get_employee_form'),
    path('get_department_form', get_department_form, name='get_department_form'),
    path('get_position_form', get_position_form, name='get_position_form'),
    path('get_typeprime_form', get_typeprime_form, name='get_typeprime_form'),
    path('<str:route>', index, name='redirect_to_home'),
]
