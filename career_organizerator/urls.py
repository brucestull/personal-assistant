from django.urls import path

from .views import BulletPointListView, home

app_name = "career_organizerator"
urlpatterns = [
    path("", home, name="home"),
    path("bulletpoints/", BulletPointListView.as_view(), name="bulletpoint-list"),
]
