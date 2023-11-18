from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import SkillForm
from .models import BulletPoint, Skill


def home(request):
    """
    View function for the home page of the `career_organizerator` app.
    """
    return render(
        # Pass the `request` argument to the `render` function.
        request,
        # Specify the template to use.
        "career_organizerator/home.html",
        {
            # Specify some context variables to pass to the template.
            "the_site_name": THE_SITE_NAME,
            "page_title": "Career Organizerator Home",
        },
    )


class SkillListView(FormMixin, RegistrationAcceptedMixin, ListView):
    """
    `ListView` for the `Skill` model.
    """

    model = Skill
    form_class = SkillForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Skills",
    }
    success_url = "/career-organizerator/skills/"

    def post(self, request, *args, **kwargs):
        """
        Override the `post` method to add the current user to the form's
        `user` field.
        """
        form = self.get_form()
        form.instance.user = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        This method is here to override the `form_valid` method of the
        """
        form.save()
        return super().form_valid(form)


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
