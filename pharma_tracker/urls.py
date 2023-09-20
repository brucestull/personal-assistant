from django.urls import path

from . import views


app_name = "pharma_tracker"
urlpatterns = [
    path(
        "",
        views.PharmaceuticalListView.as_view(),
        name="pharmaceutical-list",
    ),
]
