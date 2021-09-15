from django.db import models
import re, os

from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    destination_name = models.CharField(max_length=100)
    destination_url = models.URLField(max_length=255)
    destination_workbench = models.CharField(max_length=100)

    source_name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=255)
    source_workbench = models.CharField(max_length=100)
    folder = models.CharField(max_length=255, default='/repos')

    def __str__(self) -> str:
        return f'{self.destination_name}'


@receiver(post_save, sender=Project)
def repo_dir(sender, instance, **kwargs):
    project = Project.objects.get(pk=instance.pk)
    split = re.split('/', project.source_url)
    project_folder = split[-1][:-4]
    dirs = [name for name in os.listdir("repos/") if os.path.isdir(f'repos/{name}')]
    new_dir = project_folder
    while new_dir in dirs:
        new_dir = f'new_{new_dir}'
    cloned = [project.source_url for project in Project.objects.all()]
    if instance.source_url in cloned:
        new_dir = project_folder

    folder = f'repos/{project_folder}/{new_dir}'
    sender.objects.filter(pk=instance.pk).update(folder=folder)