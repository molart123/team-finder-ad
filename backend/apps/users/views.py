from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import RegisterForm, LoginForm, ProfileEditForm, CustomPasswordChangeForm

def users_list(request):
    users = User.objects.all().order_by('id')
    filter_type = request.GET.get('filter')
    if request.user.is_authenticated and filter_type:
        if filter_type == 'favorite_authors':
            users = User.objects.filter(owned_projects__in=request.user.favorites.all()).distinct()
        elif filter_type == 'my_project_authors':
            users = User.objects.filter(owned_projects__in=request.user.participated_projects.all()).distinct()
        elif filter_type == 'project_fans':
            users = User.objects.filter(favorites__in=request.user.owned_projects.all()).distinct()
        elif filter_type == 'my_project_participants':
            users = User.objects.filter(participated_projects__in=request.user.owned_projects.all()).distinct()
    return render(request, 'users/participants.html', {'participants': users, 'active_filter': filter_type})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': user})

def users_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('projects:list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def users_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
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

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})