# packing_list/urls.py

from django.urls import path

from . import views

app_name = "packing_list"
urlpatterns = [
    # Activities
    path("activities/", views.activity_list, name="activity_list"),
    path("activities/<int:pk>/", views.activity_detail, name="activity_detail"),
    path("activities/create/", views.activity_create, name="activity_create"),
    path("activities/<int:pk>/edit/", views.activity_update, name="activity_update"),
    path("activities/<int:pk>/delete/", views.activity_delete, name="activity_delete"),
    path("activities/<int:pk>/pdf/", views.activity_pdf, name="activity_pdf"),
    # Items
    path("items/", views.item_list, name="item_list"),
    path("items/<int:pk>/", views.item_detail, name="item_detail"),
    path("items/create/", views.item_create, name="item_create"),
    path("items/<int:pk>/edit/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
    # Tasks
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
]
