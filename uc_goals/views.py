from django.shortcuts import render

from base.decorators import registration_accepted_required
from config.settings import THE_SITE_NAME
from uc_goals.models import Goal


@registration_accepted_required
def ultimate_concerns(request):
    """
    Goals which are ultimate concerns and owned by the user.
    """
    goals = Goal.objects.filter(is_ultimate_concern=True, user=request.user)
    return render(
        request,
        "uc_goals/goal_list.html",
        {
            "goals": goals,
            "the_site_name": THE_SITE_NAME,
            "page_title": "Ultimate Concerns",
        },
    )


@registration_accepted_required
def orphan_goals(request):
    """
    Goals which are not ultimate concerns but are owned by the user.
    """
    goals = Goal.objects.filter(
        is_ultimate_concern=False, parent__isnull=True, user=request.user
    )
    return render(request, "uc_goals/goal_list.html",
                  {
                      "goals": goals,
                      "the_site_name": THE_SITE_NAME,
                      "page_title": "Orphan Goals",
                  })
