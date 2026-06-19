from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from team_finder.constants import USERS_PAGINATE_BY

from ..common.services import paginate_queryset
from ..users.forms import (
    CustomPasswordChangeForm,
    LoginForm,
    RegisterForm,
    UpdateForm,
)

User = get_user_model()


def users_list(request):
    users_qs = User.objects.all().order_by("id")
    filter_type = request.GET.get("filter")

    if request.user.is_authenticated and filter_type:
        if filter_type == "owners-of-favorite-projects":
            users_qs = User.objects.filter(
                owned_projects__in=request.user.favorites_projects.all()
            ).distinct()
        elif filter_type == "owners-of-participating-projects":
            users_qs = User.objects.filter(
                owned_projects__in=request.user.participated_projects.all()
            ).distinct()
        elif filter_type == "interested-in-my-projects":
            users_qs = User.objects.filter(
                favorites_projects__in=request.user.owned_projects.all()
            ).distinct()
        elif filter_type == "participants-of-my-projects":
            users_qs = User.objects.filter(
                participated_projects__in=request.user.owned_projects.all()
            ).distinct()

    users = paginate_queryset(users_qs, request, USERS_PAGINATE_BY)

    return render(
        request,
        "users/participants.html",
        {
            "participants": users,
            "active_filter": filter_type if request.user.is_authenticated else None,
        },
    )


def users_register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        login(request, user)
        return redirect("projects:list")
    return render(request, "users/register.html", {"form": form})


def users_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("projects:list")
        form.add_error(None, "Неверный email или пароль")
    return render(request, "users/login.html", {"form": form})


def users_logout(request):
    logout(request)
    return redirect("projects:list")


def user_details(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "users/user-details.html", {"user": user})


@login_required
def profile_edit(request):
    form = UpdateForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect("users:profile", id=request.user.id)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("users:profile", id=request.user.id)
    return render(request, "users/change_password.html", {"form": form})
