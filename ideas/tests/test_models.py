# ideas/tests/test_models.py

from django.test import TestCase

from accounts.models import CustomUser
from ideas.models import Idea


class IdeaModelTest(TestCase):
    """
    Tests for the `Idea` model.
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

    def test_name_label(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        field_label = idea._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_name_max_length(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        max_length = idea._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_concept_label(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        field_label = idea._meta.get_field("concept").verbose_name
        self.assertEqual(field_label, "Concept")

    def test_author_foreign_key(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        self.assertEqual(idea.author, self.user)

    def test_author_on_delete_cascade(self):
        """
        Deleting the author should also delete the idea.
        """
        user_temp = CustomUser.objects.create_user(
            username="TempUser",
            email="tempuser@test.com",
            password="TempPass1234",
        )
        Idea.objects.create(
            name="Temp Idea",
            concept="Temp concept.",
            author=user_temp,
        )
        user_temp.delete()
        self.assertFalse(Idea.objects.filter(name="Temp Idea").exists())

    def test_str_method(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        self.assertEqual(str(idea), "Test Idea")

    def test_get_absolute_url(self):
        idea = Idea.objects.get(pk=self.idea.pk)
        self.assertEqual(idea.get_absolute_url(), f"/ideas/{idea.pk}/")

    def test_ordering(self):
        Idea.objects.create(name="A Idea", concept="AAA", author=self.user)
        Idea.objects.create(name="Z Idea", concept="ZZZ", author=self.user)
        ideas = list(Idea.objects.all())
        self.assertEqual(ideas[0].name, "A Idea")

    def test_verbose_name(self):
        self.assertEqual(Idea._meta.verbose_name, "Idea")

    def test_verbose_name_plural(self):
        self.assertEqual(Idea._meta.verbose_name_plural, "Ideas")
