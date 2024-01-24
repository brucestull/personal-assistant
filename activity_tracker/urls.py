from django.urls import path

from . import views

app_name = "activity_tracker"
urlpatterns = [
    path("jsr/", views.json_response, name="json-response"),
]
