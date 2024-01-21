from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('<str:route>', index, name='redirect_to_home'),
]
