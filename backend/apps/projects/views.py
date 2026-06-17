from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project
from .forms import ProjectForm

def project_list(request):
    projects = Project.objects.filter(status='open').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project-details.html', {'project': project})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})

@login_required
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status == 'open':
        project.status = 'closed'
        project.save()
    return JsonResponse({'status': 'ok', 'project_status': project.status})

@login_required
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return redirect('projects:detail', pk=project.pk)

@login_required
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.favorited_by.all():
        project.favorited_by.remove(request.user)
        favorited = False
    else:
        project.favorited_by.add(request.user)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})

@login_required
def favorites_list(request):
    projects = request.user.favorites.all().order_by('-created_at')
    return render(request, 'projects/favorite_projects.html', {'projects': projects})