# ideas/urls.py

from django.urls import path

from . import views

app_name = "ideas"
urlpatterns = [
    path("", views.IdeaListView.as_view(), name="idea_list"),
    path("create/", views.IdeaCreateView.as_view(), name="idea_create"),
    path("<int:pk>/", views.IdeaDetailView.as_view(), name="idea_detail"),
    path("<int:pk>/update/", views.IdeaUpdateView.as_view(), name="idea_update"),
    path("<int:pk>/delete/", views.IdeaDeleteView.as_view(), name="idea_delete"),
]
