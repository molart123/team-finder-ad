from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('project/list/', views.project_list, name='list_full'),
    path('projects/<int:pk>/', views.project_detail, name='detail'),
    path('projects/create/', views.create_project, name='create'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit'),
    path('projects/<int:pk>/complete/', views.complete_project, name='complete'),
    path('projects/<int:pk>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('projects/<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('projects/favorites/', views.favorites_list, name='favorites'),
]