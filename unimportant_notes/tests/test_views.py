from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from unimportant_notes.models import NoteTag


class NoteTagDetailViewTest(TestCase):
    """
    Tests for the `NoteTagDetailView`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data for the `NoteTagDetailView` tests.
        """
        cls.user_dezzi = CustomUser.objects.create_user(
            username="DezziKitten",
            email="dezzi.kitten@purr.scratch",
            password="PurrMachine1234",
        )
        # Update `registration_accepted` to `True`.
        cls.user_dezzi.registration_accepted = True
        cls.user_dezzi.save()
        cls.note_tag = NoteTag.objects.create(
            name="Dezzi's Note Tag",
            author=cls.user_dezzi,
        )

    def test_note_tag_detail_view_url_exists_at_desired_location(self):
        """
        Test that the `NoteTagDetailView` is rendered at "/unimportant-notes/tags/1/".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(f"/unimportant-notes/tag/{self.note_tag.id}/")
        self.assertEqual(response.status_code, 200)

    def test_note_tag_detail_view_url_accessible_by_name(self):
        """
        Test that the `NoteTagDetailView` is rendered at the desired location by
        "unimportant_notes:tag_detail".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_note_tag_detail_view_uses_correct_template(self):
        """
        Test that the `NoteTagDetailView` uses the correct template
        "unimportant_notes/notetag_detail.html".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "unimportant_notes/notetag_detail.html")

    def test_note_tag_detail_view_uses_correct_context(self):
        """
        Test that the `NoteTagDetailView` uses the correct context.

        The context should contain the following:
        - the_site_name
        - page_title
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Note Tag")

    def test_note_tag_detail_view_redirects_for_unauthenticated_user(self):
        """
        Test that the `NoteTagDetailView` redirects an unauthenticated user to the
        login page.
        """
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/unimportant-notes/tag/{self.note_tag.id}/",
            status_code=302,
            target_status_code=200,
        )

    def test_note_tag_detail_view_can_be_seen_by_author_only(self):
        """
        Test that the `NoteTagDetailView` can be seen by the author only.
        """
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        # Create a new user.
        knot_dezzi = CustomUser.objects.create_user(
            username="KnotDezzi",
            email="KnotDezzi@purr.scratch",
            password="PurrMachine12345",
        )
        # Set `registration_accepted` to `True`.
        knot_dezzi.registration_accepted = True
        knot_dezzi.save()
        login = self.client.login(username="KnotDezzi", password="PurrMachine12345")
        self.assertTrue(login)
        response = self.client.get(
            reverse("unimportant_notes:tag_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 403)


class NoteTagListViewTest(TestCase):
    """
    Tests for the `NoteTagListView`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data for the `NoteTagListView` tests.
        """
        cls.user_dezzi = CustomUser.objects.create_user(
            username="DezziKitten",
            email="DezziKitten@purr.scratch",
            password="PurrMachine1234",
        )
        # Update `registration_accepted` to `True`.
        cls.user_dezzi.registration_accepted = True
        cls.user_dezzi.save()
        cls.note_tag = NoteTag.objects.create(
            name="Dezzi's Note Tag",
            author=cls.user_dezzi,
        )

    def test_note_tag_list_view_url_exists_at_desired_location(self):
        """
        Test that the `NoteTagListView` is rendered at "/unimportant-notes/tags/".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get("/unimportant-notes/tags/")
        self.assertEqual(response.status_code, 200)

    def test_note_tag_list_view_url_accessible_by_name(self):
        """
        Test that the `NoteTagListView` is rendered at the desired location by
        "unimportant_notes:tag_list".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertEqual(response.status_code, 200)

    def test_note_tag_list_view_uses_correct_template(self):
        """
        Test that the `NoteTagListView` uses the correct template
        "unimportant_notes/notetag_list.html".
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "unimportant_notes/notetag_list.html")

    def test_note_tag_list_view_uses_correct_context(self):
        """
        Test that the `NoteTagListView` uses the correct context.

        The context should contain the following:
        - the_site_name
        - page_title
        """
        # Log in the user.
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Note Tags")

    def test_note_tag_list_view_redirects_for_unauthenticated_user(self):
        """
        Test that the `NoteTagListView` redirects an unauthenticated user to the
        login page.
        """
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/unimportant-notes/tags/",
            status_code=302,
            target_status_code=200,
        )

    def test_note_tag_list_view_returns_only_tags_owned_by_user(self):
        """
        Test that the `NoteTagListView` returns only the tags owned by the user.
        """
        login = self.client.login(username="DezziKitten", password="PurrMachine1234")
        self.assertTrue(login)
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.context["object_list"][0].name, "Dezzi's Note Tag")
        # Create a new user.
        knot_dezzi = CustomUser.objects.create_user(
            username="KnotDezzi",
            email="KnotDezzi@purr.scratch",
            password="PurrMachine12345",
        )
        # Set `registration_accepted` to `True`.
        knot_dezzi.registration_accepted = True
        knot_dezzi.save()
        login = self.client.login(username="KnotDezzi", password="PurrMachine12345")
        self.assertTrue(login)
        response = self.client.get(reverse("unimportant_notes:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
