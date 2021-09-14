from django.urls import path

from .views import push_to_repo

urlpatterns = [
    path('<int:id>/', push_to_repo)
]