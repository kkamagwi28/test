from django.db import models


class iFrame(models.Model):
    link = models.URLField()
    context = models.CharField(max_length = 2000, default='None')

    def __str__(self):
        return self.context


class Lesson(models.Model):
    title = models.CharField(max_length = 200)
    order = models.IntegerField()
    context = models.TextField(default=None)
    iframe = models.ForeignKey(iFrame, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


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
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name