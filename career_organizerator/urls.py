from django.urls import path

from .views import BulletPointListView

app_name = "career_organizerator"
urlpatterns = [
    path("bulletpoints/", BulletPointListView.as_view(), name="bulletpoint-list"),
]
