from django.urls import path
from .views import index, get_employee_form

urlpatterns = [
    path('', index, name='index'),
    path('get_employee_form', get_employee_form, name='get_employee_form'),
    path('<str:route>', index, name='redirect_to_home'),
]
