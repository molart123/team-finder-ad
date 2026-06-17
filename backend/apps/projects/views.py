from django.shortcuts import render
from .models import Project


# Create your views here.
def projects_list(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})