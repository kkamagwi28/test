from django.shortcuts import render


def index(request):
    return render(request, "base/index.html")

def webinars(request):
    return render(request, "base/video.html")
