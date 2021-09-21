import requests
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProjectForm, PushForm
from .models import Project
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
            gitcloner._get_reppo_url(project.source_url)
            project.save()
            if requests.codes.OK:
                gitcloner.clone_repo(project.id, projects, project.folder,
                                     project.source_url, project.source_workbench,
                                     project.destination_url, project.destination_workbench)
                return redirect('push_code', id=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'scrypt/project.html',
                  {'form': form,
                   'projects': projects})


@login_required
def push_to_repo(request, id):
    project = get_object_or_404(Project, pk=id)
    projects = Project.objects.all()
    gitcloner._get_reppo_url(project.source_url)

    if request.method == 'POST':
        if requests.codes.OK:
            if project.source_url in projects:
                gitcloner.update_repo(project.source_url,
                                          project.source_workbench,
                                          project.pk,
                                          project.destination_workbench)
            else:
                gitcloner.push_repo(project.source_url,
                                      projects, project.id,
                                      project.folder,
                                      project.source_workbench,
                                      project.destination_url,
                                      project.destination_workbench)
                        
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
        gitcloner.delete_repo(project.source_url)
        return redirect('repos')
    except Project.DoesNotExist:
        return redirect('repos')




@login_required
def instructions(request):

    with open('/usr/local/share/.ssh/id_rsa.pub', 'r') as f:
        rpub = f.read()

    return render(request, 'scrypt/instructions.html', {'file': rpub})

