# true_north/urls.py

from django.urls import path

from true_north import views

app_name = "true_north"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
]
