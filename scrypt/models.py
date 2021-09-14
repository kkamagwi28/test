from django.db import models


class Project(models.Model):
    destination_name = models.CharField(max_length=100)
    destination_url = models.URLField(max_length=255)
    destination_workbench = models.CharField(max_length=100)

    source_name = models.CharField(max_length=100)
    source_url = models.URLField(max_length=255)
    source_workbench = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.destination_name}'
