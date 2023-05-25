from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse

from config.settings.common import THE_SITE_NAME
from .models import Journal

JOURNAL_LIST_PAGE_TITLE = "Journals"
JOURNAL_CREATE_PAGE_TITLE = "Create a Journal"


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

    def get_queryset(self) -> QuerySet[Any]:
        """
        Override the default queryset to only return journals that belong to the current user.
        """
        return super().get_queryset().filter(author=self.request.user)


class JournalCreateView(CreateView):
    """
    Create view for a new `self_enquiry.Journal`.
    """

    model = Journal
    fields = ["title", "content"]
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": JOURNAL_CREATE_PAGE_TITLE,
    }
    success_url = "/journals/list/"

    def form_valid(self, form):
        """
        Override the default form_valid method to add the current user to the `author` field.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)
