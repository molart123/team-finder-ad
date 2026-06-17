from django.urls import path
from . import views

app_name = 'projects'


urlpatterns = [
    path('', views.projects_list, name='list'),
    path('projects/list', views.projects_list, name='list'),
    path('projects/<int:id>', views.project_detail, name='create'),
]