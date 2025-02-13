from django.urls import path

from . import views

app_name = "uc_goals"
urlpatterns = [
    path("create/", views.GoalCreateView.as_view(), name="goal_create"),
    path("<int:pk>/", views.GoalDetailView.as_view(), name="goal_detail"),
    path("<int:pk>/update/", views.GoalUpdateView.as_view(), name="goal_update"),
    path("<int:pk>/delete/", views.GoalDeleteView.as_view(), name="goal_delete"),
    path("ucs/", views.ultimate_concerns, name="uc_list"),
    path("orphans/", views.orphan_goals, name="orphan_list"),
]
