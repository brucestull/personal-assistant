"""URL configuration for the successes app."""

from django.urls import path

from successes import views

app_name = "successes"
urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Success URLs
    path("successes/", views.SuccessListView.as_view(), name="success_list"),
    path("successes/add/", views.SuccessCreateView.as_view(), name="success_create"),
    path(
        "successes/<int:pk>/", views.SuccessDetailView.as_view(), name="success_detail"
    ),
    path(
        "successes/<int:pk>/edit/",
        views.SuccessUpdateView.as_view(),
        name="success_update",
    ),
    path(
        "successes/<int:pk>/delete/",
        views.SuccessDeleteView.as_view(),
        name="success_delete",
    ),
    # What Went Well URLs
    path(
        "what-went-well/",
        views.WhatWentWellListView.as_view(),
        name="whatwentwell_list",
    ),
    path(
        "what-went-well/add/",
        views.WhatWentWellCreateView.as_view(),
        name="whatwentwell_create",
    ),
    path(
        "what-went-well/<int:pk>/",
        views.WhatWentWellDetailView.as_view(),
        name="whatwentwell_detail",
    ),
    path(
        "what-went-well/<int:pk>/edit/",
        views.WhatWentWellUpdateView.as_view(),
        name="whatwentwell_update",
    ),
    path(
        "what-went-well/<int:pk>/delete/",
        views.WhatWentWellDeleteView.as_view(),
        name="whatwentwell_delete",
    ),
]
