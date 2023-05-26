from django.test import TestCase
from django.urls import reverse
from django.db import models as d_db_models

######################
# Can use either of these:
# from config.settings.common import AUTH_USER_MODEL
from accounts.models import CustomUser
######################
from self_enquiry.models import Journal


A_TEST_USERNAME = "ACustomUser"

JOURNAL_AUTHOR_LABEL = "author"
JOURNAL_AUTHOR_RELATED_NAME = "journals"

JOURNAL_TITLE_VERBOSE_NAME = "Journal Title"
JOURNAL_TITLE_HELP_TEXT = "Optional - 100 characters or fewer"
JOURNAL_TITLE_MAX_LENGTH = 100
JOURNAL_TITLE = "Test Journal Title"

JOURNAL_CONTENT_VERBOSE_NAME = "Journal Content"
JOURNAL_CONTENT_HELP_TEXT = "Required"
JOURNAL_CONTENT = "Test Journal Content"

JOURNAL_CREATED_HELP_TEXT = "The date and time the journal was created."

JOURNAL_UPDATED_HELP_TEXT = "The date and time the journal was last updated."


class JournalModelTest(TestCase):
    """
    Tests for the `Journal` model.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        journal = Journal.objects.create(
            author=user,
            title=JOURNAL_TITLE,
            content=JOURNAL_CONTENT,
        )

    def test_author_label(self):
        """
        `Journal` model `author` field `label` should be `author`.
        """
        field = Journal._meta.get_field("author")
        self.assertEqual(field.verbose_name, JOURNAL_AUTHOR_LABEL)

    def test_author_uses_custom_user_model(self):
        """
        `Journal` model `author` field should use the custom user model.
        """
        field = Journal._meta.get_field("author")
        self.assertEqual(field.related_model, CustomUser)

    def test_author_on_delete_cascade(self):
        """
        `Journal` model `author` field `on_delete` should be `CASCADE`.
        """
        field = Journal._meta.get_field("author")
        self.assertEqual(field.remote_field.on_delete, d_db_models.CASCADE)

    def test_author_related_name(self):
        """
        `Journal` model `author` field `related_name` should be
        `journals`.
        """
        journal = Journal.objects.get(id=1)
        related_name = journal._meta.get_field("author").related_query_name()
        self.assertEqual(related_name, JOURNAL_AUTHOR_RELATED_NAME)

    def test_title_verbose_name(self):
        """
        `Journal` model `title` field `verbose_name` should be
        `Journal Title`.
        """
        field = Journal._meta.get_field("title")
        self.assertEqual(field.verbose_name, JOURNAL_TITLE_VERBOSE_NAME)

    def test_title_help_text(self):
        """
        `Journal` model `title` field `help_text` should be
        `Optional - 100 characters or fewer`.
        """
        field = Journal._meta.get_field("title")
        self.assertEqual(field.help_text, JOURNAL_TITLE_HELP_TEXT)

    def test_title_max_length(self):
        """
        `Journal` model `title` field `max_length` should be `100`.
        """
        field = Journal._meta.get_field("title")
        self.assertEqual(field.max_length, JOURNAL_TITLE_MAX_LENGTH)

    def test_title_null_true(self):
        """
        `Journal` model `title` field `null` should be `True`.
        """
        field = Journal._meta.get_field("title")
        self.assertTrue(field.null)

    def test_title_blank_true(self):
        """
        `Journal` model `title` field `blank` should be `True`.
        """
        field = Journal._meta.get_field("title")
        self.assertTrue(field.blank)


