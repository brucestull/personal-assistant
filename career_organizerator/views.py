from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView

from base.mixins import RegistrationAcceptedMixin
from base.decorators import registration_accepted_required
from config.settings import THE_SITE_NAME

from .forms import (
    BehavioralInterviewQuestionForm,
    BulletPointForm,
    PurposeForm,
    QuestionResponseForm,
    SkillForm,
)
from .models import (
    BehavioralInterviewQuestion,
    BulletPoint,
    Purpose,
    QuestionResponse,
    Skill,
)


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


class PurposeListView(FormMixin, RegistrationAcceptedMixin, ListView):
    """
    `ListView` for the `Purpose` model.
    """

    model = Purpose
    form_class = PurposeForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Purposes",
    }
    success_url = reverse_lazy("career_organizerator:purpose-list")

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

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `Purpose` objects.
        """
        return Purpose.objects.filter(user=self.request.user).order_by("-created")


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
    success_url = reverse_lazy("career_organizerator:skill-list")

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

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `Skill` objects.
        """
        return Skill.objects.filter(user=self.request.user).order_by("order")


# TODO: Implement the `move_up` view function for any model.
# def move_up(request, model, model_id):
#     """
#     View function to move a `model` object up in the list.
#     """
#     model = get_object_or_404(model, id=model_id)
#     previous_model = model.objects.filter(order__lt=model.order).last()

#     if previous_model:
#         model.order, previous_model.order = previous_model.order, model.order
#         model.save()
#         previous_model.save()
#         model.reorder_all()

#     return redirect(f"{model.__name__.lower()}-list")


@registration_accepted_required
def skill_move_up(request, skill_id):
    """
    View function to move a `Skill` object up in the list.
    """
    with transaction.atomic():
        skill = get_object_or_404(Skill, id=skill_id)
        previous_skill = (
            Skill.objects.filter(order__lt=skill.order).order_by("-order").first()
        )

        if previous_skill:
            skill.order, previous_skill.order = previous_skill.order, skill.order
            skill.save()
            previous_skill.save()

    return redirect("career_organizerator:skill-list")


@registration_accepted_required
def skill_move_down(request, skill_id):
    """
    View function to move a `Skill` object down in the list.
    """
    with transaction.atomic():
        skill = get_object_or_404(Skill, id=skill_id)
        # Find the next skill in the list (i.e., with the next higher order value)
        next_skill = (
            Skill.objects.filter(order__gt=skill.order).order_by("order").first()
        )

        if next_skill:
            # Swap the order values of the current skill and the next skill
            skill.order, next_skill.order = next_skill.order, skill.order
            skill.save()
            next_skill.save()

    # Redirect to the skill list page, adjust the URL name as necessary
    return redirect("career_organizerator:skill-list")


@registration_accepted_required
def skill_delete(request, skill_id):
    """
    View function to delete a `Skill` object.
    """
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    Skill.reorder_all()
    return redirect("career_organizerator:skill-list")


class BehavioralInterviewQuestionListView(
    FormMixin, RegistrationAcceptedMixin, ListView
):
    """
    `ListView` for the `BehavioralInterviewQuestion` model.
    """

    model = BehavioralInterviewQuestion
    form_class = BehavioralInterviewQuestionForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Behavioral Interview Questions",
    }
    # We don't use a hard-coded URL here because we would need to change every
    # occurrence of the URL in the code if we changed the URL.
    # success_url = "/career-organizerator/behavioral-interview-questions/"
    # Instead, we use the `reverse_lazy` function to reverse the URL. It uses the
    # application namespace and the URL name to reverse the URL.
    success_url = reverse_lazy(
        "career_organizerator:behavioral-interview-question-list"
    )

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

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `BehavioralInterviewQuestion` objects.
        """
        return BehavioralInterviewQuestion.objects.filter(
            user=self.request.user
        ).order_by("-created")


class QuestionResponseListView(FormMixin, RegistrationAcceptedMixin, ListView):
    """
    `ListView` for the `QuestionResponse` model.
    """

    template_name = "career_organizerator/questionresponse_list.html"
    form_class = QuestionResponseForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Question Responses",
    }
    success_url = reverse_lazy("career_organizerator:question-response-list")

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

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `QuestionResponse` objects.
        """
        return BehavioralInterviewQuestion.objects.filter(
            user=self.request.user
        ).order_by("-created")


class QuestionResponseCreateView(RegistrationAcceptedMixin, CreateView):
    """
    `CreateView` for the `QuestionResponse` model.
    """

    model = QuestionResponse
    form_class = QuestionResponseForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Question Response",
    }
    success_url = reverse_lazy("career_organizerator:question-response-list")

    def get(self, request, *args, **kwargs):
        """
        Override the `get` method to add the `question` field to the form's
        `initial` data.
        """
        self.initial["question"] = BehavioralInterviewQuestion.objects.get(
            pk=kwargs["question_id"]
        )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Override the `form_valid` method to add the current user to the form's
        `user` field.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionResponseUpdateView(RegistrationAcceptedMixin, UpdateView):
    """
    `UpdateView` for the `QuestionResponse` model.
    """

    model = QuestionResponse
    form_class = QuestionResponseForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Update Question Response",
    }
    success_url = reverse_lazy("career_organizerator:question-response-list")


class BulletPointListView(FormMixin, RegistrationAcceptedMixin, ListView):
    """
    `ListView` and `create` form for the `BulletPoint` model.
    """

    model = BulletPoint
    form_class = BulletPointForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Bullet Points",
    }
    success_url = reverse_lazy("career_organizerator:bulletpoint-list")

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

    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the current user's
        `BulletPoint` objects.
        """
        return BulletPoint.objects.filter(user=self.request.user).order_by("-created")
