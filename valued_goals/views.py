from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponse


@user_passes_test(lambda u: u.is_staff)
def index(request):
    return HttpResponse(
        f"Hello, world. You're at the valued_goals index."
        f"<br>"
        f"<a href='/'>Home</a>"
        f"<br>"
        f"<a href='/admin/valued_goals/corevalue/'>Add Core Value</a>"
        f"<br>"
        f"<a href='/admin/valued_goals/valuedgoal/'>Add Valued Goal</a>"
        )
