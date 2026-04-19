from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from uc_goals.forms import GoalForm
from uc_goals.models import Goal, VIACharacterStrength, Virtue

User = get_user_model()


class UcGoalsModelFormAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="goal-user", password="pw", registration_accepted=True
        )
        self.virtue = Virtue.objects.create(name="Wisdom", description="Wise desc")
        self.strength = VIACharacterStrength.objects.create(
            name="Curiosity", description="Curious desc", virtue=self.virtue
        )
        self.goal = Goal.objects.create(user=self.user, name="Read")
        self.goal.character_strengths.add(self.strength)

    def test_models_and_get_absolute_url(self):
        self.assertEqual(str(self.goal), "Read")
        self.assertEqual(str(self.virtue), "Wisdom")
        self.assertEqual(str(self.strength), "Curiosity")
        self.assertEqual(
            self.goal.get_absolute_url(),
            reverse("uc_goals:goal_detail", kwargs={"pk": self.goal.pk}),
        )

    def test_form_filters_parent_and_sets_initial_strengths(self):
        parent = Goal.objects.create(user=self.user, name="Parent")
        form = GoalForm(instance=self.goal)
        parent_qs = form.fields["parent"].queryset
        self.assertIn(parent, parent_qs)
        self.assertNotIn(self.goal, parent_qs)
        self.assertEqual(
            list(form.fields["character_strengths"].initial),
            [self.strength],
        )

    def test_admin_config_and_helper_methods(self):
        goal_admin = site._registry[Goal]
        virtue_admin = site._registry[Virtue]
        strength_admin = site._registry[VIACharacterStrength]

        self.assertIn("display_character_strengths", goal_admin.list_display)
        self.assertEqual(
            goal_admin.display_character_strengths(self.goal),
            "Curiosity",
        )

        long_desc = "x" * 80
        self.virtue.description = long_desc
        self.virtue.save()
        self.assertTrue(virtue_admin.short_description(self.virtue).endswith("..."))
        self.assertEqual(
            strength_admin.short_description(self.strength),
            "Curious desc",
        )


class UcGoalsAdditionalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="accepted-goal", password="pw", registration_accepted=True
        )
        self.other = User.objects.create_user(
            username="other-goal", password="pw", registration_accepted=True
        )
        self.client.login(username="accepted-goal", password="pw")
        self.parent = Goal.objects.create(
            user=self.user, name="Parent", is_ultimate_concern=True
        )
        self.goal = Goal.objects.create(
            user=self.user, name="Child", parent=self.parent
        )
        self.other_uc = Goal.objects.create(
            user=self.other, name="Other UC", is_ultimate_concern=True
        )
        Goal.objects.create(
            user=self.other, name="Other Orphan", is_ultimate_concern=False
        )

    def test_create_view_prefills_parent_and_sets_user(self):
        response = self.client.get(
            reverse("uc_goals:goal_create") + f"?parent={self.parent.pk}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["mode"], "create")
        self.assertEqual(
            response.context["form"].initial["parent"], str(self.parent.pk)
        )

        post_response = self.client.post(
            reverse("uc_goals:goal_create"),
            {
                "parent": self.parent.pk,
                "name": "New Goal",
                "is_ultimate_concern": False,
                "description": "desc",
                "completed": False,
                "is_archived": False,
                "character_strengths": [],
            },
        )
        created = Goal.objects.get(name="New Goal")
        self.assertEqual(created.user, self.user)
        self.assertRedirects(
            post_response,
            reverse("uc_goals:goal_detail", kwargs={"pk": created.pk}),
        )

    def test_update_view_filters_queryset_and_context(self):
        response = self.client.get(
            reverse("uc_goals:goal_update", kwargs={"pk": self.goal.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["mode"], "update")
        self.assertIn("Edit:", response.context["page_title"])

        forbidden = self.client.get(
            reverse("uc_goals:goal_update", kwargs={"pk": self.other_uc.pk})
        )
        self.assertEqual(forbidden.status_code, 404)

    def test_ultimate_concerns_and_orphan_goals_filter_to_user(self):
        uc_response = self.client.get(reverse("uc_goals:uc_list"))
        self.assertEqual(uc_response.status_code, 200)
        self.assertEqual(list(uc_response.context["goals"]), [self.parent])

        orphan = Goal.objects.create(
            user=self.user, name="Orphan", is_ultimate_concern=False
        )
        orphan_response = self.client.get(reverse("uc_goals:orphan_list"))
        self.assertEqual(orphan_response.status_code, 200)
        self.assertEqual(list(orphan_response.context["goals"]), [orphan])
