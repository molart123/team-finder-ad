from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('users/list', views.users_list, name='list'),
    path('users/register/', views.users_register, name='register'),
    path('users/login/', views.users_login, name='login'),
]