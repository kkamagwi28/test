from django.shortcuts import render
from .models import Course


def python(request):
    courses = Course.objects.all()
    return render(request, "courses/python_index.html", {'courses': courses})
