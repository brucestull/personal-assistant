from django.urls import path

from .views import (BehavioralInterviewQuestionListView, BulletPointListView,
                    SkillListView, home)

app_name = "career_organizerator"
urlpatterns = [
    path("", home, name="home"),
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path(
        "behavioral-interview-questions/",
        BehavioralInterviewQuestionListView.as_view(),
        name="behavioral-interview-question-list",
    ),
    path("bulletpoints/", BulletPointListView.as_view(), name="bulletpoint-list"),
]
