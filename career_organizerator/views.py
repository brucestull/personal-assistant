from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from config.settings import THE_SITE_NAME

from .models import BulletPoint


class BulletPointListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    `ListView` for the `BulletPoint` model.
    """

    model = BulletPoint
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Bullet Points",
    }

    def test_func(self):
        """
        Override the `test_func` method to check if the current user has
        `registration_accepted` `True`.
        """
        return self.request.user.registration_accepted

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `BulletPoint` objects.
        """
        return BulletPoint.objects.filter(user=self.request.user)
