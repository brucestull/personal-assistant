from django.urls import path

from . import views

urlpatterns = [
    path("", views.activity_list, name="activity_list"),
    path("<int:pk>/", views.activity_detail, name="activity_detail"),
    path("create/", views.activity_create, name="activity_create"),
    path("<int:pk>/edit/", views.activity_update, name="activity_update"),
    path("<int:pk>/delete/", views.activity_delete, name="activity_delete"),
]
