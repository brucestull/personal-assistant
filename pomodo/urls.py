# pomodo/urls.py

from django.urls import path
from .views import timer_view

app_name = "pomodo"

urlpatterns = [
    path("", timer_view, name="timer"),
]
