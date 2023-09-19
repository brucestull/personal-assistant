from django.urls import path

from . import views


app_name = "pharma_tracker"
urlpatterns = [
    path("", views.temp_index, name="temp-index")
]
