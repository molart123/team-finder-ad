from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("users/list", views.users_list, name="list"),
    path("users/register/", views.users_register, name="register"),
    path("users/login/", views.users_login, name="login"),
    path("users/logout/", views.users_logout, name="logout"),
    path("users/<int:id>/", views.user_details, name="profile"),
    path("users/update/", views.user_details, name="update"),
    path("users/edit-profile/", views.profile_edit, name="edit"),
    path("users/change-password/", views.change_password, name="change_password"),
]
