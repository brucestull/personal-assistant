from django.urls import path

from .views import temporary_http_response

app_name = "project_manager"
urlpatterns = [
    path("", temporary_http_response, name="temporary_http_response"),
]
