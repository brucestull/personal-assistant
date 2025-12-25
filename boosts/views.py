# boosts/views.py

import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from accounts.models import CustomUser
from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from boosts.forms import InspirationalForm, RandomInspirationalEmailSendForm
from boosts.models import Inspirational, InspirationalSent, RandomInspirationalEmailSend
from boosts.tasks import send_inspirational_to_beastie, send_random_inspirational_email
from django.conf import settings

THE_SITE_NAME = settings.THE_SITE_NAME


class InspirationalListView(RegistrationAcceptedMixin, ListView):
    """
    ListView for the Inspirational model.

    This view is only accessible to users who have `registration_accepted=True`.
    This is controlled by the `UserPassesTestMixin` and the `test_func` method.

    Mixins:
        LoginRequiredMixin: Ensures that the user is logged in. If not, they
        are redirected to the login page.
        UserPassesTestMixin: Ensures that the user has `registration_accepted=True`.
        If not, they are prompted to login.

    Attributes:
        paginate_by (int): The number of objects to display per page.

    Methods:
        test_func: Test if user has `registration_accepted=True`. Only users
        who pass this test can access this view.
        get_queryset: Get the queryset for the view. Only the `Inspirational`
        objects for the current user are returned.
        get_context_data: Override the `get_context_data` method to add the
        page title and the site name to the context.
    """

    paginate_by = 10
    queryset = None

    # We are not using 'model = Inspirational' attribute since we want only
    # the `Inspirationals` for the current user.
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Inspirational.objects.filter(
                author=self.request.user,
            ).order_by("-created")
            return queryset
        else:
            queryset = Inspirational.objects.none()
            return queryset

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add `page_title`,
        `the_site_name`, and `name_in_heading` to the context.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Inspirationals"
        context["the_site_name"] = THE_SITE_NAME
        context["name_in_heading"] = self.request.user.username
        return context


class InspirationalCreateView(RegistrationAcceptedMixin, CreateView):
    """
    CreateView for the Inspirational model.
    """

    form_class = InspirationalForm
    template_name = "boosts/inspirational_form.html"
    success_url = reverse_lazy("boosts:inspirational-list")

    def form_valid(self, form):
        """
        Override `form_valid` to set the author of the Inspirational to the current
        user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add the page title and the site name
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create an Inspirational"
        context["the_site_name"] = THE_SITE_NAME
        # Hide the "Create Inspirational" link in the navbar since we are
        # already on the page.
        context["hide_inspirational_create_link"] = True
        return context


# TODO: Possible refactor permissions for this view, using decorators.
@registration_accepted_required
def send_inspirational(request, pk):
    """
    Send an inspirational quote to the User's Beastie (a User which has
    been designated as the User's Beastie).
    """
    try:
        # Get the inspirational quote from the pk sent in the URL:
        inspirational = get_object_or_404(Inspirational, pk=pk)
        # Get the current site domain. This will resolve to a localhost in DEV
        # and to the production domain in PROD:
        current_site = get_current_site(request)
        plain_text_body = (
            f"{inspirational.created.strftime('%y-%m-%d')} - {request.user.username}:\n\n"  # noqa E501
            f"{inspirational.body}\n\n"
            f"Sent from https://{current_site.domain} by {request.user.username} "
            f"({request.user.email})."
        )
        # Extract the necessary information from the request object
        user_username = request.user.username
        user_email = request.user.email
        user_beastie_email = request.user.beastie.email
        user_beastie_username = request.user.beastie.username

        # Use Celery to send the email:
        # Pass only this serializable data to the task
        send_inspirational_to_beastie.delay(
            user_username,
            user_email,
            user_beastie_email,
            user_beastie_username,
            plain_text_body,
        )

        inspirational_sent = InspirationalSent.objects.create(
            inspirational=inspirational,
            inspirational_text=inspirational.body,
            sender=request.user,
            beastie=request.user.beastie,
        )
        print(f"inspirational_sent: {inspirational_sent}")
        messages.success(
            request,
            f"Sent '{inspirational.body[:20]}...' to your Beastie: "
            f"{request.user.beastie.username}!",
        )
        return redirect("boosts:inspirational-list")
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect("boosts:inspirational-list")
    except Exception as e:
        messages.error(
            request, f"An error occurred while sending the inspirational quote: {e}"
        )
        return redirect("boosts:inspirational-list")


@login_required
@require_POST
def send_random_inspirational_to_self(request):
    """
    Pick a random Inspirational authored by the logged-in user,
    email its body to them, and record that in InspirationalSent.
    """

    user = request.user

    # Only pick from the logged-in author's inspirationals
    qs = Inspirational.objects.filter(author=user)

    count = qs.count()
    if count == 0:
        messages.error(
            request,
            "You don't have any Inspirationals yet. Create one before sending.",
        )
        return redirect("boosts:inspirational-list")  # adjust if your name is different

    # More efficient than order_by('?') for larger tables
    random_index = random.randint(0, count - 1)
    inspirational = qs[random_index]

    if not user.email:
        messages.error(
            request,
            "Your account has no email address set, so I can't send this to you.",
        )
        return redirect("boosts:inspirational-list")

    subject = "Your random Inspirational ✨"
    body_text = (
        f"{inspirational.created.strftime('%y-%m-%d')} - {user.username}:\n\n"
        f"{inspirational.body}"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    # Send the email
    send_mail(
        subject,
        body_text,
        from_email,
        [user.email],
        fail_silently=False,
    )

    # Log what was sent (snapshot of the text at send time)
    InspirationalSent.objects.create(
        inspirational=inspirational,
        inspirational_text=body_text,
        sender=user,
        beastie=user,  # treat the logged-in user as the beastie/recipient
    )

    messages.success(
        request, "A random Inspirational has been emailed to you. Check your inbox!"
    )

    return redirect("boosts:inspirational-list")


class BretBeastieInspirationalListView(ListView):
    """
    ListView to show a sample of `Inspirational`s for the example user named
    "BretBeastie".

    This view is accessible to users who are not logged in.
    """

    paginate_by = 10
    username = "BretBeastie"

    # We are not using 'model = Inspirational' attribute since we want only
    # the `Inspirationals` for the example user.
    def get_queryset(self):
        """
        Override the `get_queryset` method to return only the `Inspirational`s for the
        example user named "BretBeastie".
        """
        demo_example_user = CustomUser.objects.get(username=self.username)
        queryset = Inspirational.objects.filter(
            author=demo_example_user,
        ).order_by("-created")
        return queryset

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add the page title and the site name
        to the context.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Inspirationals"
        context["the_site_name"] = THE_SITE_NAME
        context["name_in_heading"] = self.username
        return context


def landing_view(request):
    """
    This view checks is the user is authenticated.

    If they are, they are routed to their own `InspirationalListView`.

    If they are not, they are routed to the `BretBeastieInspirationalListView`.
    """
    if request.user.is_authenticated and request.user.registration_accepted:
        return InspirationalListView.as_view()(request)
    else:
        return BretBeastieInspirationalListView.as_view()(request)


# --- RandomInspirationalEmailSend CRUD Views ---


class RandomInspirationalEmailSendListView(RegistrationAcceptedMixin, ListView):
    """
    ListView for RandomInspirationalEmailSend model.
    Shows all random inspirational email send requests for the current user.
    """

    model = RandomInspirationalEmailSend
    paginate_by = 10

    def get_queryset(self):
        """Only show the current user's send requests."""
        if self.request.user.is_authenticated:
            return RandomInspirationalEmailSend.objects.filter(
                user=self.request.user
            ).order_by("-created")
        return RandomInspirationalEmailSend.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Random Inspirational Email Sends"
        context["the_site_name"] = THE_SITE_NAME
        return context


class RandomInspirationalEmailSendDetailView(RegistrationAcceptedMixin, DetailView):
    """
    DetailView for RandomInspirationalEmailSend model.
    Shows details of a specific send request.
    """

    model = RandomInspirationalEmailSend

    def get_queryset(self):
        """Only allow users to view their own send requests."""
        return RandomInspirationalEmailSend.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Email Send Details"
        context["the_site_name"] = THE_SITE_NAME
        return context


class RandomInspirationalEmailSendCreateView(RegistrationAcceptedMixin, CreateView):
    """
    CreateView for RandomInspirationalEmailSend model.
    Creates a new send request and triggers the Celery task.
    """

    model = RandomInspirationalEmailSend
    form_class = RandomInspirationalEmailSendForm
    success_url = reverse_lazy("boosts:random-send-list")

    def form_valid(self, form):
        """Set the user and trigger the Celery task to send the email."""
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Trigger the Celery task to send the random inspirational email
        # Pass the RandomInspirationalEmailSend ID so the task can update it
        send_random_inspirational_email.delay(
            self.request.user.id, random_send_id=self.object.id
        )

        messages.success(
            self.request,
            "Your random inspirational email send has been queued! "
            "Check your email inbox soon.",
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Send Random Inspirational Email"
        context["the_site_name"] = THE_SITE_NAME
        return context


class RandomInspirationalEmailSendUpdateView(RegistrationAcceptedMixin, UpdateView):
    """
    UpdateView for RandomInspirationalEmailSend model.
    Allows updating the status or error message of a send request.
    """

    model = RandomInspirationalEmailSend
    fields = ["status", "error_message"]
    success_url = reverse_lazy("boosts:random-send-list")

    def get_queryset(self):
        """Only allow users to update their own send requests."""
        return RandomInspirationalEmailSend.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Email Send"
        context["the_site_name"] = THE_SITE_NAME
        return context


class RandomInspirationalEmailSendDeleteView(RegistrationAcceptedMixin, DeleteView):
    """
    DeleteView for RandomInspirationalEmailSend model.
    Allows deleting a send request record.
    """

    model = RandomInspirationalEmailSend
    success_url = reverse_lazy("boosts:random-send-list")

    def get_queryset(self):
        """Only allow users to delete their own send requests."""
        return RandomInspirationalEmailSend.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Email Send"
        context["the_site_name"] = THE_SITE_NAME
        return context
