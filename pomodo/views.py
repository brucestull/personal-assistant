# pomodo/views.py

from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def timer_view(request):
    logger.info("Pomodoro timer loaded by user %s", request.user)
    return render(request, "pomodo/timer.html")
