from django.urls import path
from .consumers import WSConsumer


ws_urlspatterns = [
    path('ws/', WSConsumer.as_asgi())
]