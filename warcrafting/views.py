# warcrafting/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Character


class CharacterListView(LoginRequiredMixin, ListView):
    """
    Simple 'my characters' overview.
    """

    model = Character
    template_name = "warcrafting/character_list.html"
    context_object_name = "characters"
    paginate_by = 20

    def get_queryset(self):
        # Only show the logged-in user's characters
        qs = super().get_queryset()
        return (
            qs.filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related("professions", "assets")
        )


class CharacterDetailView(LoginRequiredMixin, DetailView):
    """
    Simple per-character armory-style view.
    """

    model = Character
    template_name = "warcrafting/character_detail.html"
    context_object_name = "character"

    def get_queryset(self):
        # Lock detail view down to the logged-in user's characters
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related("professions", "assets")
        )
