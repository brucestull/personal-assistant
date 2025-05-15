# plan_it/urls.py

from django.urls import path

from . import views

app_name = "plan_it"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
