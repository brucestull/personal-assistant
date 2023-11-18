from django.urls import path

from .views import BulletPointListView, SkillListView, home

app_name = "career_organizerator"
urlpatterns = [
    path("", home, name="home"),
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path("bulletpoints/", BulletPointListView.as_view(), name="bulletpoint-list"),
]
