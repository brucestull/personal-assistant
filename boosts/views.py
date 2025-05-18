# boosts/views.py

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from accounts.models import CustomUser
from base.mixins import RegistrationAcceptedMixin
from base.decorators import registration_accepted_required
from boosts.forms import InspirationalForm
from boosts.models import Inspirational, InspirationalSent
from boosts.tasks import send_inspirational_to_beastie
from config.settings import THE_SITE_NAME


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
