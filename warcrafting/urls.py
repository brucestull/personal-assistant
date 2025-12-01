# warcrafting/urls.py

from django.urls import path

from . import views

app_name = "warcrafting"

urlpatterns = [
    path("characters/", views.CharacterListView.as_view(), name="character_list"),
    path(
        "characters/<int:pk>/",
        views.CharacterDetailView.as_view(),
        name="character_detail",
    ),
]
