from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserAdmin

def mprint(obj):
    print(f'\n\n\n {obj} \n\n\n')
# Create your views here.
def login_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('/')
    
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            if UserAdmin.objects.filter(email=username).exists():
                context.clear()
                context['password'] = 'The password is incorrect.'
            else:
                context.clear()
                context['username'] = 'The username does not exist.'
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')