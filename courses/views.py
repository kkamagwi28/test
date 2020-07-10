from django.shortcuts import render
from django.template import loader
from .models import Course, Lesson
from django.http import HttpResponse
from django.http import HttpResponse



def courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, "base/courses.html", context)


def course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    
    for course in courses:
        url = 'courses/' + str(course.name) 
        html_url = url + '.html'
        url = '/courses/' + str(course.name) + '/'
    return render(request, html_url, context)

def lessons(request, order):
    courses = Course.objects.all()
    #for course in courses:
       # url = 'courses/' + str(course.name) + str(course.lesson.order) + '.html'

    #return render(request, url, {'lessons': lessons})
    return HttpResponse(str(order))
