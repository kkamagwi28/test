from django.db import models
import re, os


class Project(models.Model):
    destination_name = models.CharField(max_length=100)
    destination_url = models.URLField(max_length=255)
    destination_workbench = models.CharField(max_length=100)

    source_name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=255)
    source_workbench = models.CharField(max_length=100)

    @property
    def repo_dir(self):
        split = re.split('/', self.source_url)
        project_folder = split[-1][:-4]
        dirs = [name for name in os.listdir("repos/") if os.path.isdir(f'repos/{name}')]
        new_dir = project_folder
        while new_dir in dirs:
            new_dir = f'new_{new_dir}'

        return f'repos/{project_folder}/{new_dir}'

    def __str__(self) -> str:
        return f'{self.destination_name}'
