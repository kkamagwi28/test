from django.urls import path

from tasks.views import TaskAPIView, TaskDetailAPIView, SetFinishedTaskAPIView


urlpatterns = [
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view()),
    path('tasks/<int:id>/finished/', SetFinishedTaskAPIView.as_view()),
]
