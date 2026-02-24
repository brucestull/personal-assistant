# warcrafting/urls.py

from django.urls import path

from . import views

app_name = "warcrafting"

urlpatterns = [
    # Dashboard
    path("", views.WarcraftingDashboardView.as_view(), name="dashboard"),
    # Character CRUD
    path("characters/", views.CharacterListView.as_view(), name="character_list"),
    path(
        "characters/create/",
        views.CharacterCreateView.as_view(),
        name="character_create",
    ),
    path(
        "characters/<int:pk>/",
        views.CharacterDetailView.as_view(),
        name="character_detail",
    ),
    path(
        "characters/<int:pk>/edit/",
        views.CharacterUpdateView.as_view(),
        name="character_update",
    ),
    path(
        "characters/<int:pk>/delete/",
        views.CharacterDeleteView.as_view(),
        name="character_delete",
    ),
    # CharacterProfession CRUD (nested under character)
    path(
        "characters/<int:character_pk>/professions/add/",
        views.CharacterProfessionCreateView.as_view(),
        name="characterprofession_create",
    ),
    path(
        "professions/<int:pk>/edit/",
        views.CharacterProfessionUpdateView.as_view(),
        name="characterprofession_update",
    ),
    path(
        "professions/<int:pk>/delete/",
        views.CharacterProfessionDeleteView.as_view(),
        name="characterprofession_delete",
    ),
]
