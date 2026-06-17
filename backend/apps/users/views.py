from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import User
from .forms import *

# Create your views here.
def users_list(request):
    users = User.objects.all()
    return render(request, 'users/participants.html', {'users': users})

def users_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(name=form.cleaned_data['name'],
                                    surname = form.cleaned_data['surname'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, user)
            return redirect('projects:list')

    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect(request, 'projects:list')
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})