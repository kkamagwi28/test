from django.db import models


class indexPage(models.Model):
    title = models.CharField(max_length=500)
    page_context = models.TextField()

    def __str__(self):
        return self.title
