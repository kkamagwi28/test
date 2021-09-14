import requests
import asyncio
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProjectForm, PushForm
from .models import Project
from django.http import HttpResponseNotFound
from .scrypt import GitCloner
from django.contrib.auth.decorators import login_required


gitcloner = GitCloner()


@login_required
def get_repository_url(request):
    projects = Project.objects.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            if requests.codes.OK:
                gitcloner.clone_project(project.source_url, project.pk)
                return redirect('push_code', id=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'scrypt/project.html',
                  {'form': form,
                   'projects': projects})


@login_required
def push_to_repo(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        if requests.codes.OK:
            if project.source_url in Project.objects.all():
                gitcloner.updating_branch(project.source_url,
                                          project.source_workbench,
                                          project.pk,
                                          project.destination_workbench)
            else:
                gitcloner.creating_branch(project.source_url,
                                          project.source_workbench,
                                          project.destination_url,
                                          project.destination_workbench,
                                          project.pk)
                        
            form = PushForm(request.POST)
    else:
        form = PushForm()

    return render(request, 'scrypt/push.html',
                  {'form': form, 'project': project})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project_form = form.save(commit=False)
            project_form.save()
            return redirect('push_code', id=project_form.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'scrypt/project_edit.html', {'form': form})


@login_required
def delete_project(request, pk):
    try:
        project = Project.objects.get(id=pk)
        project.delete()
        return redirect('repos')
    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")


@login_required
def instructions(request):

    with open('/home/jellyfish/.ssh/id_rsa.pub', 'r') as f:
        rpub = f.read()

    return render(request, 'scrypt/instructions.html', {'file': rpub})

