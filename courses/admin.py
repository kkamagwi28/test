from django.contrib import admin
from .models import Course, Lesson, iFrame


admin.site.register(Course)
admin.site.register(iFrame)
admin.site.register(Lesson)
