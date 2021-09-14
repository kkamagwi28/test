"""repo2repo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from scrypt.views import get_repository_url, push_to_repo, edit_project, delete_project, instructions
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', LoginView.as_view(), name="login"),
    path('source/', get_repository_url, name='repos'),
    path('push/<int:id>/', push_to_repo, name='push_code'),
    path('edit/<int:pk>/', edit_project, name='edit_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),

    path('instructions/', instructions, name='instructions'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('m/', include('scrypt.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
