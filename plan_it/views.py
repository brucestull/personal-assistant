# plan_it/views.py

from django.shortcuts import render

from base.decorators import registration_accepted_required
from config.settings import THE_SITE_NAME

from .models import Activity, Item


@registration_accepted_required
def dashboard(request):
    activities = Activity.objects.order_by("due_date")[:10]
    items = Item.objects.all()[:10]
    return render(
        request,
        "plan_it/dashboard.html",
        {
            "activities": activities,
            "items": items,
            "page_title": "Plan It Dashboard",
            "the_site_name": THE_SITE_NAME,
        },
    )
