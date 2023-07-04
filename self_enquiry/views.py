from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404

from config.settings.common import THE_SITE_NAME
from .models import Journal


JOURNAL_LIST_PAGE_TITLE = "Journals"
JOURNAL_CREATE_PAGE_TITLE = "Create a Journal"
JOURNAL_CREATE_FORM_BUTTON_TEXT = "Create your Journal!"
JOURNAL_UPDATE_PAGE_TITLE = "Update a Journal"
JOURNAL_UPDATE_FORM_BUTTON_TEXT = "Update your Journal!"
JOURNAL_DELETE_PAGE_TITLE = "Delete a Journal"
JOURNAL_DELETE_FORM_BUTTON_TEXT = "Delete your Journal!"
JOURNAL_DETAIL_PAGE_TITLE = "Journal Detail"


class JournalCreateView(CreateView):
    """
    Create view for a new `self_enquiry.Journal`.
    """

    model = Journal
    template_name = "self_enquiry/journal_form.html"
    fields = ["title", "content"]
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": JOURNAL_CREATE_PAGE_TITLE,
        "form_button_text": JOURNAL_CREATE_FORM_BUTTON_TEXT,
    }
    success_url = reverse_lazy("self_enquiry:list")

    def form_valid(self, form):
        """
        Override the default form_valid method to add the current user to the `author` field.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class JournalListView(ListView):
    """
    List view for all `self_enquiry.journals`.
    """

    model = Journal
    ordering = ["-created"]
    paginate_by = 10
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": JOURNAL_LIST_PAGE_TITLE,
    }

    def get_queryset(self):
        """
        Override the default queryset to only return journals that belong to the current user.
        """
        return super().get_queryset().filter(author=self.request.user)


class JournalDetailView(DetailView):
    """
    Detail view for a single `self_enquiry.Journal`.
    """

    model = Journal
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": JOURNAL_DETAIL_PAGE_TITLE,
    }


class JournalUpdateView(UpdateView):
    """
    Update view for a single `self_enquiry.Journal`.
    """

    model = Journal
    template_name = "self_enquiry/journal_form.html"
    fields = ["title", "content"]
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": JOURNAL_UPDATE_PAGE_TITLE,
        "form_button_text": JOURNAL_UPDATE_FORM_BUTTON_TEXT,
    }
    object = None

    def form_valid(self, form):
        """
        Override the default form_valid method to add the current user to the `author` field.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        """
        Override the default queryset to only return journals that belong to the current user.
        """
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        """
        Override the default `get_success_url` method to redirect to the journal detail page.
        """
        if self.object:
            # Assuming you pass the journal ID in the URL
            return reverse("self_enquiry:detail", kwargs={"pk": self.object.pk})
        else:
            # If the object doesn't exist, redirect to the journal list page
            return reverse("self_enquiry:list")


class JournalDeleteView(DeleteView):
    model = Journal
    # Template for the confirmation page
    template_name = "self_enquiry/journal_confirm_delete.html"

    # TODO: Add a `message` that the Journal was deleted successfully.

    def get_success_url(self):
        return reverse(
            "self_enquiry:list",
        )


class JournalConfirmDeleteView(View):
    """
    Confirm delete view for a single `self_enquiry.Journal`.
    """

    template_name = "self_enquiry/journal_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        # Assuming you pass the journal ID in the URL
        journal_id = kwargs["pk"]
        journal = get_object_or_404(Journal, pk=journal_id)
        context = {
            "journal": journal,
            "the_site_name": THE_SITE_NAME,
            "page_title": JOURNAL_DELETE_PAGE_TITLE,
        }
        return render(request, self.template_name, context)

