from django.shortcuts import render
from .models import indexPage


def index(request):
    index = indexPage.objects.all()
    return render(request, "base/index.html", {'index': index})

def webinars(request):
    return render(request, "base/webinars.html")


