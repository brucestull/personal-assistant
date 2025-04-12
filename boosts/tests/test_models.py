from django.db import models
from django.test import TestCase

from accounts.models import CustomUser
from boosts.models import Inspirational, InspirationalSent


class InspirationalModelTest(TestCase):
    """
    Tests for `Inspirational` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        author = CustomUser.objects.create(
            username="DezziKitten",
        )
        Inspirational.objects.create(
            author=author,
            body="Twenty-four  characters. or more...",
        )

    def test_body_help_text_attribute(self):
        """
        `Inspirational` `body` field `help_text` attribute should be `Required. 500
        characters or fewer.`.
        """
        inspirational = Inspirational.objects.get(id=1)
        help_text = inspirational._meta.get_field("body").help_text
        self.assertEqual(help_text, "Required.")

    def test_body_verbose_name_attribute(self):
        """
        `Inspirational` `body` field `verbose_name` attribute should be `Inspirational
        Body Text`.
        """
        inspirational = Inspirational.objects.get(id=1)
        verbose_name = inspirational._meta.get_field("body").verbose_name
        self.assertEqual(verbose_name, "Inspirational Body Text")

    def test_author_foreign_key(self):
        """
        `Inspirational` `author` should be a `ForeignKey` to `CustomUser`.
        """
        inspirational = Inspirational.objects.get(id=1)
        author = inspirational._meta.get_field("author").remote_field.model
        # Three ways to test the same thing:
        self.assertTrue(author is CustomUser)  # Tests identity (same object)
        self.assertIs(author, CustomUser)  # Tests identity (same object)
        self.assertEqual(author, CustomUser)  # Tests equality (same value)

    def test_author_on_delete_attribute(self):
        """
        `Inspirational` `author` field `on_delete` attribute should be `CASCADE`.
        """
        inspirational = Inspirational.objects.get(id=1)
        on_delete = inspirational._meta.get_field("author").remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_author_related_name(self):
        """
        `Inspirational` `author` field `related_name` attribute should be
        `inspirationals`.
        """
        inspirational = Inspirational.objects.get(id=1)
        related_name = inspirational._meta.get_field("author").related_query_name()
        self.assertEqual(related_name, "inspirationals")

    def test_created_auto_now_add_attribute(self):
        """
        `Inspirational` `created` field `auto_now_add` attribute should be `True`.
        """
        inspirational = Inspirational.objects.get(id=1)
        auto_now_add = inspirational._meta.get_field("created").auto_now_add
        self.assertTrue(auto_now_add)

    def test_str_method(self):
        """
        `Inspirational` `__str__` method should return `author.username + " : " +
        str(self.id) + " - " + self.body[:24]`.
        """
        test_body = "Twenty-four  characters."
        inspirational = Inspirational.objects.get(id=1)
        self.assertEqual(str(inspirational), "DezziKitten : 1 - " + test_body)


class InspirationalSentModelTest(TestCase):
    """
    Tests for `InspirationalSent` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        author = CustomUser.objects.create(
            username="DezziKitten",
        )
        beastie = CustomUser.objects.create(
            username="Beastie",
        )
        inspirational = Inspirational.objects.create(
            author=author,
            body="Twenty-four  characters. or more...",
        )
        InspirationalSent.objects.create(
            inspirational=inspirational,
            inspirational_text=inspirational.body,
            sender=author,
            beastie=beastie,
        )

    def test_inspirational_foreign_key(self):
        """
        `InspirationalSent` `inspirational` should be a `ForeignKey` to `Inspirational`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        inspirational = inspirational_sent._meta.get_field(
            "inspirational"
        ).remote_field.model
        # Three ways to test the same thing:
        self.assertTrue(inspirational is Inspirational)  # Tests identity (same object)
        self.assertIs(inspirational, Inspirational)  # Tests identity (same object)
        self.assertEqual(inspirational, Inspirational)  # Tests equality (same value)

    def test_inspirational_on_delete_attribute(self):
        """
        `InspirationalSent` `inspirational` field `on_delete` attribute should be
        `CASCADE`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        on_delete = inspirational_sent._meta.get_field(
            "inspirational"
        ).remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_inspirational_text_verbose_name_attribute(self):
        """
        `InspirationalSent` `inspirational_text` field `verbose_name` attribute should
        be `Inspirational Text Sent to Beastie`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        verbose_name = inspirational_sent._meta.get_field(
            "inspirational_text"
        ).verbose_name
        self.assertEqual(verbose_name, "Inspirational Text Sent to Beastie")

    def test_sender_foreign_key(self):
        """
        `InspirationalSent` `sender` should be a `ForeignKey` to `CustomUser`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        sender = inspirational_sent._meta.get_field("sender").remote_field.model
        # Three ways to test the same thing:
        self.assertTrue(sender is CustomUser)

    def test_sender_on_delete_attribute(self):
        """
        `InspirationalSent` `sender` field `on_delete` attribute should be `CASCADE`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        on_delete = inspirational_sent._meta.get_field("sender").remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_sender_related_name(self):
        """
        `InspirationalSent` `sender` field `related_name` attribute should be
        `inspirationals_sent`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        related_name = inspirational_sent._meta.get_field("sender").related_query_name()
        self.assertEqual(related_name, "inspirationals_sent")

    def test_beastie_foreign_key(self):
        """
        `InspirationalSent` `beastie` should be a `ForeignKey` to `CustomUser`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        beastie = inspirational_sent._meta.get_field("beastie").remote_field.model
        # Three ways to test the same thing:
        self.assertTrue(beastie is CustomUser)

    def test_beastie_on_delete_attribute(self):
        """
        `InspirationalSent` `beastie` field `on_delete` attribute should be `CASCADE`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        on_delete = inspirational_sent._meta.get_field("beastie").remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_sent_at_auto_now_add_attribute(self):
        """
        `InspirationalSent` `sent_at` field `auto_now_add` attribute should be `True`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        auto_now_add = inspirational_sent._meta.get_field("sent_at").auto_now_add
        self.assertTrue(auto_now_add)

    def test_str_method(self):
        """
        `InspirationalSent` `__str__` method should return `f"Inspiration
        #{self.inspirational.id} sent to Beastie #{self.beastie.id} at
        {self.sent_at.strftime('%Y-%m-%d %H:%M:%S')}"`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        self.assertEqual(
            str(inspirational_sent),
            "Inspiration #1 sent to Beastie #2 at "
            + inspirational_sent.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def test_meta_verbose_name_plural(self):
        """
        `InspirationalSent` `Meta` `verbose_name_plural` attribute should be
        `Inspirational Sent`.
        """
        inspirational_sent = InspirationalSent.objects.get(id=1)
        verbose_name_plural = inspirational_sent._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "Inspirationals Sent")
