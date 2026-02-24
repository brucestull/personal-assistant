# warcrafting/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import CharacterForm, CharacterProfessionForm
from .models import Character, CharacterProfession


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


class WarcraftingDashboardView(LoginRequiredMixin, TemplateView):
    """High-level overview: characters and their profession skill progress."""

    template_name = "warcrafting/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        characters = (
            Character.objects.filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related(
                "character_professions__profession_tier__profession",
                "assets",
            )
        )
        ctx["characters"] = characters
        ctx["character_count"] = characters.count()
        return ctx


# ---------------------------------------------------------------------------
# Character CRUD
# ---------------------------------------------------------------------------


class CharacterListView(LoginRequiredMixin, ListView):
    """'My characters' overview."""

    model = Character
    template_name = "warcrafting/character_list.html"
    context_object_name = "characters"
    paginate_by = 20

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related("character_professions__profession_tier__profession")
        )


class CharacterDetailView(LoginRequiredMixin, DetailView):
    """Per-character armory-style view."""

    model = Character
    template_name = "warcrafting/character_detail.html"
    context_object_name = "character"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related(
                "character_professions__profession_tier__profession",
                "assets",
            )
        )


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """Create a new WoW character."""

    model = Character
    form_class = CharacterForm
    template_name = "warcrafting/character_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "warcrafting:character_detail", kwargs={"pk": self.object.pk}
        )


class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing character owned by the logged-in user."""

    model = Character
    form_class = CharacterForm
    template_name = "warcrafting/character_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "warcrafting:character_detail", kwargs={"pk": self.object.pk}
        )


class CharacterDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a character owned by the logged-in user."""

    model = Character
    template_name = "warcrafting/character_confirm_delete.html"
    success_url = reverse_lazy("warcrafting:character_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# ---------------------------------------------------------------------------
# CharacterProfession CRUD
# ---------------------------------------------------------------------------


class CharacterProfessionCreateView(LoginRequiredMixin, CreateView):
    """Add a profession tier (with current skill) to a character."""

    model = CharacterProfession
    form_class = CharacterProfessionForm
    template_name = "warcrafting/characterprofession_form.html"

    def get_character(self):
        return get_object_or_404(
            Character, pk=self.kwargs["character_pk"], owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = self.get_character()
        return ctx

    def form_valid(self, form):
        form.instance.character = self.get_character()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "warcrafting:character_detail",
            kwargs={"pk": self.kwargs["character_pk"]},
        )


class CharacterProfessionUpdateView(LoginRequiredMixin, UpdateView):
    """Update the skill level of a character's profession tier."""

    model = CharacterProfession
    form_class = CharacterProfessionForm
    template_name = "warcrafting/characterprofession_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(character__owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = self.object.character
        return ctx

    def get_success_url(self):
        return reverse_lazy(
            "warcrafting:character_detail",
            kwargs={"pk": self.object.character.pk},
        )


class CharacterProfessionDeleteView(LoginRequiredMixin, DeleteView):
    """Remove a profession tier from a character."""

    model = CharacterProfession
    template_name = "warcrafting/characterprofession_confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(character__owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = self.object.character
        return ctx

    def get_success_url(self):
        return reverse_lazy(
            "warcrafting:character_detail",
            kwargs={"pk": self.object.character.pk},
        )
