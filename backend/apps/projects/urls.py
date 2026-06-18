from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("projects/list", views.project_list, name="list_full"),
    path("projects/<int:id>/", views.project_detail, name="detail"),
    path("projects/create-project", views.create_project, name="create"),
    path("projects/<int:id>/edit/", views.edit_project, name="edit"),
    path("projects/<int:id>/complete/", views.complete_project, name="complete"),
    path(
        "projects/<int:id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
    path(
        "projects/<int:id>/toggle-favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path("projects/favorites/", views.favorites_list, name="favorites"),
]
