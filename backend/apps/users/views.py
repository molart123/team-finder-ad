from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import RegisterForm, LoginForm, UpdateForm, CustomPasswordChangeForm


def users_list(request):
    users = User.objects.all()
    return render(request, 'users/participants.html', {'users': users})


def users_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('projects:list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)  # исправлено: username=email
            if user is not None:
                login(request, user)
                return redirect('projects:list')
            else:
                form.add_error(None, 'Неверный email или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def users_logout(request):
    logout(request)
    return redirect('projects:list')


def user_details(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "users/user-details.html", {'user': user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', id=request.user.id)
    else:
        form = UpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # чтобы не разлогинило
            return redirect('users:profile', id=request.user.id)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def projects_favorites(request):
    user = request.user
    projects = user.favorites_projects.all()
    return render(request, 'projects/favorite_projects.html', {'projects': projects})