from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Course, Lesson
from django.http import HttpResponse
from django.http import HttpResponse
from .forms import LessonForm



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

def lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    #for course in courses:
       # url = 'courses/' + str(course.name) + str(course.lesson.order) + '.html'

    #return render(request, url, {'lessons': lessons})
    return render(request, "courses/python/1.html", {'course': course})

def lesson_new(request):
    form = LessonForm(request.POST)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.save()
    return render(request, 'courses/lessons/new.html', {'form': form})
