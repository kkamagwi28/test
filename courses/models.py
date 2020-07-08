from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 200)
    silabus = models.CharField(max_length = 2000)
    certificate_example = models.CharField(max_length = 2000)
    date_of_start = models.DateField()
    author = models.CharField(max_length = 200)
    goal = models.CharField(max_length = 2000)
    tasks = models.CharField(max_length = 2000)
    slag = models.CharField(max_length = 2000)
    reviews = models.CharField(max_length = 2000)

    def __str__(self):
        return self.name