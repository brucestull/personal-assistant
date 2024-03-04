from django.urls import path

from .views import (
    BehavioralInterviewQuestionListView,
    BulletPointListView,
    PurposeListView,
    QuestionResponseCreateView,
    QuestionResponseListView,
    QuestionResponseUpdateView,
    SkillListView,
    skill_move_up,
    skill_delete,
    home,
)

app_name = "career_organizerator"
urlpatterns = [
    path("", home, name="home"),
    path("purposes/", PurposeListView.as_view(), name="purpose-list"),
    path("skills/", SkillListView.as_view(), name="skill-list"),
    path("skills/<int:skill_id>/move-up/", skill_move_up, name="move_skill_up"),
    path("skills/<int:skill_id>/delete/", skill_delete, name="delete_skill"),
    path(
        "behavioral-interview-questions/",
        BehavioralInterviewQuestionListView.as_view(),
        name="behavioral-interview-question-list",
    ),
    path(
        "question-responses/",
        QuestionResponseListView.as_view(),
        name="question-response-list",
    ),
    path(
        "question-responses/create/<int:question_id>/",
        QuestionResponseCreateView.as_view(),
        name="question-response-create",
    ),
    path(
        "question-responses/<int:pk>/update/",
        QuestionResponseUpdateView.as_view(),
        name="question-response-update",
    ),
    path("bulletpoints/", BulletPointListView.as_view(), name="bulletpoint-list"),
]
