from django.urls import path

from . import views

app_name = "uc_goals"
urlpatterns = [
    path("ucs/", views.ultimate_concerns, name="uc_list"),
    path("orphans/", views.orphan_goals, name="orphan_list"),
]
