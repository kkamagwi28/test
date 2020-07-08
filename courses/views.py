from django.shortcuts import render

def python(request):
    return render(request, "courses/python_index.html")
