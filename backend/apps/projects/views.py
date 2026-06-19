import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from team_finder.constants import (
    PROJECT_PAGINATE_BY,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
)

from ..common.services import paginate_queryset
from .forms import ProjectForm
from .models import Project

logger = logging.getLogger(__name__)


def project_list(request):
    projects_qs = (
        Project.objects.filter(status=PROJECT_STATUS_OPEN)
        .select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )
    projects = paginate_queryset(projects_qs, request, PROJECT_PAGINATE_BY)
    return render(request, "projects/project_list.html", {"projects": projects})


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", id=project.id)
    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": False}
    )


@login_required
def edit_project(request, id):
    project = get_object_or_404(Project, id=id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:detail", id=project.id)
    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": True}
    )


@login_required
def complete_project(request, id):
    project = get_object_or_404(Project, id=id, owner=request.user)
    if project.status == PROJECT_STATUS_OPEN:
        project.status = PROJECT_STATUS_CLOSED
        project.save()
    return JsonResponse({"status": "ok", "project_status": project.status})


@login_required
def toggle_participate(request, id):
    project = get_object_or_404(Project, id=id)
    user = request.user

    is_participating = project.participants.filter(id=user.id).exists()

    if is_participating:
        project.participants.remove(user)
    else:
        project.participants.add(user)

    data = {
        "status": "ok",
        "is_participating": not is_participating,
        "participant": {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "avatar": user.avatar.url,
        }
        if not is_participating
        else None,
        "participants_count": project.participants.count(),
    }
    return JsonResponse(data)


@login_required
def toggle_favorite(request, id):
    project = get_object_or_404(Project, id=id)
    is_favorited = project.favorited_by.filter(id=request.user.id).exists()
    if is_favorited:
        project.favorited_by.remove(request.user)
    else:
        project.favorited_by.add(request.user)
    return JsonResponse({"status": "ok", "favorited": not is_favorited})


@login_required
def favorites_list(request):
    projects = (
        request.user.favorites.select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )
    return render(request, "projects/favorite_projects.html", {"projects": projects})
