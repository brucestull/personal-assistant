# ideas/tests/test_views.py

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from ideas.models import Idea


class IdeaListViewTest(TestCase):
    """
    Tests for the `IdeaListView`.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="TestUser",
            email="testuser@test.com",
            password="TestPass1234",
        )
        cls.user.registration_accepted = True
        cls.user.save()
        cls.idea = Idea.objects.create(
            name="Test Idea",
            concept="This is a test idea concept.",
            author=cls.user,
        )

    def test_list_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get("/ideas/")
        self.assertEqual(response.status_code, 200)

    def test_list_view_url_accessible_by_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertTemplateUsed(response, "ideas/idea_list.html")

    def test_list_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/ideas/",
            status_code=302,
            target_status_code=200,
        )

    def test_list_view_returns_only_ideas_owned_by_user(self):
        other_user = CustomUser.objects.create_user(
            username="OtherUser",
            email="otheruser@test.com",
            password="OtherPass1234",
        )
        other_user.registration_accepted = True
        other_user.save()
        Idea.objects.create(
            name="Other Idea",
            concept="Other concept.",
            author=other_user,
        )
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.context["object_list"][0].name, "Test Idea")

    def test_list_view_context_contains_site_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertIn("the_site_name", response.context)

    def test_list_view_context_contains_page_title(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_list"))
        self.assertEqual(response.context["page_title"], "Ideas")


class IdeaDetailViewTest(TestCase):
    """
    Tests for the `IdeaDetailView`.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="TestUser",
            email="testuser@test.com",
            password="TestPass1234",
        )
        cls.user.registration_accepted = True
        cls.user.save()
        cls.idea = Idea.objects.create(
            name="Test Idea",
            concept="This is a test idea concept.",
            author=cls.user,
        )

    def test_detail_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(f"/ideas/{self.idea.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_detail_view_url_accessible_by_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_detail", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_detail", kwargs={"pk": self.idea.pk})
        )
        self.assertTemplateUsed(response, "ideas/idea_detail.html")

    def test_detail_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(
            reverse("ideas:idea_detail", kwargs={"pk": self.idea.pk})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/ideas/{self.idea.pk}/",
            status_code=302,
            target_status_code=200,
        )

    def test_detail_view_returns_403_for_non_author(self):
        other_user = CustomUser.objects.create_user(
            username="OtherUser",
            email="otheruser@test.com",
            password="OtherPass1234",
        )
        other_user.registration_accepted = True
        other_user.save()
        self.client.login(username="OtherUser", password="OtherPass1234")
        response = self.client.get(
            reverse("ideas:idea_detail", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 403)


class IdeaCreateViewTest(TestCase):
    """
    Tests for the `IdeaCreateView`.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="TestUser",
            email="testuser@test.com",
            password="TestPass1234",
        )
        cls.user.registration_accepted = True
        cls.user.save()

    def test_create_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get("/ideas/create/")
        self.assertEqual(response.status_code, 200)

    def test_create_view_url_accessible_by_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_create"))
        self.assertTemplateUsed(response, "ideas/idea_form.html")

    def test_create_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(reverse("ideas:idea_create"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/ideas/create/",
            status_code=302,
            target_status_code=200,
        )

    def test_create_view_creates_idea_with_correct_author(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.post(
            reverse("ideas:idea_create"),
            {"name": "New Idea", "concept": "New concept."},
        )
        self.assertRedirects(response, reverse("ideas:idea_list"))
        idea = Idea.objects.get(name="New Idea")
        self.assertEqual(idea.author, self.user)

    def test_create_view_context_mode_is_create(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(reverse("ideas:idea_create"))
        self.assertEqual(response.context["mode"], "create")


class IdeaUpdateViewTest(TestCase):
    """
    Tests for the `IdeaUpdateView`.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="TestUser",
            email="testuser@test.com",
            password="TestPass1234",
        )
        cls.user.registration_accepted = True
        cls.user.save()
        cls.idea = Idea.objects.create(
            name="Test Idea",
            concept="This is a test idea concept.",
            author=cls.user,
        )

    def test_update_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(f"/ideas/{self.idea.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_update_view_url_accessible_by_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk})
        )
        self.assertTemplateUsed(response, "ideas/idea_form.html")

    def test_update_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/ideas/{self.idea.pk}/update/",
            status_code=302,
            target_status_code=200,
        )

    def test_update_view_returns_403_for_non_author(self):
        other_user = CustomUser.objects.create_user(
            username="OtherUser",
            email="otheruser@test.com",
            password="OtherPass1234",
        )
        other_user.registration_accepted = True
        other_user.save()
        self.client.login(username="OtherUser", password="OtherPass1234")
        response = self.client.get(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_updates_idea(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.post(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk}),
            {"name": "Updated Idea", "concept": "Updated concept."},
        )
        self.assertRedirects(
            response,
            reverse("ideas:idea_detail", kwargs={"pk": self.idea.pk}),
        )
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.name, "Updated Idea")

    def test_update_view_context_mode_is_update(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_update", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.context["mode"], "update")


class IdeaDeleteViewTest(TestCase):
    """
    Tests for the `IdeaDeleteView`.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="TestUser",
            email="testuser@test.com",
            password="TestPass1234",
        )
        cls.user.registration_accepted = True
        cls.user.save()

    def setUp(self):
        self.idea = Idea.objects.create(
            name="Test Idea",
            concept="This is a test idea concept.",
            author=self.user,
        )

    def test_delete_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(f"/ideas/{self.idea.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_view_url_accessible_by_name(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_delete", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_view_uses_correct_template(self):
        self.client.login(username="TestUser", password="TestPass1234")
        response = self.client.get(
            reverse("ideas:idea_delete", kwargs={"pk": self.idea.pk})
        )
        self.assertTemplateUsed(response, "ideas/idea_confirm_delete.html")

    def test_delete_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(
            reverse("ideas:idea_delete", kwargs={"pk": self.idea.pk})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/ideas/{self.idea.pk}/delete/",
            status_code=302,
            target_status_code=200,
        )

    def test_delete_view_returns_403_for_non_author(self):
        other_user = CustomUser.objects.create_user(
            username="OtherUser",
            email="otheruser@test.com",
            password="OtherPass1234",
        )
        other_user.registration_accepted = True
        other_user.save()
        self.client.login(username="OtherUser", password="OtherPass1234")
        response = self.client.get(
            reverse("ideas:idea_delete", kwargs={"pk": self.idea.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_view_deletes_idea(self):
        self.client.login(username="TestUser", password="TestPass1234")
        idea_pk = self.idea.pk
        response = self.client.post(
            reverse("ideas:idea_delete", kwargs={"pk": idea_pk})
        )
        self.assertRedirects(response, reverse("ideas:idea_list"))
        self.assertFalse(Idea.objects.filter(pk=idea_pk).exists())
