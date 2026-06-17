from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.users_list, name='list'),
    path('<int:pk>/', views.user_detail, name='detail'),
    path('register/', views.users_register, name='register'),
    path('login/', views.users_login, name='login'),
    path('logout/', views.users_logout, name='logout'),
    path('edit/', views.profile_edit, name='edit'),
    path('change-password/', views.change_password, name='change_password'),
]