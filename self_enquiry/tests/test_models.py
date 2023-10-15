from django.test import TestCase
from django.db import models as d_db_models

######################
# Can use either of these:
# from config.settings import AUTH_USER_MODEL
from accounts.models import CustomUser

######################
from self_enquiry.models import Journal
from self_enquiry.models import GrowthOpportunity


TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"
TEST_FIRST_NAME = "Test"

JOURNAL_AUTHOR_LABEL = "author"
JOURNAL_AUTHOR_RELATED_NAME = "journals"

JOURNAL_TITLE_VERBOSE_NAME = "Journal Title"
JOURNAL_TITLE_HELP_TEXT = "Optional - 100 characters or fewer"
JOURNAL_TITLE_MAX_LENGTH = 100
JOURNAL_TITLE = "Test Journal Title"

JOURNAL_CONTENT_VERBOSE_NAME = "Journal Content"
JOURNAL_CONTENT_HELP_TEXT = "Required"
JOURNAL_CONTENT_LESS_THAN_FIFTY = "Test Journal Content"
JOURNAL_CONTENT_MORE_THAN_FIFTY = (
    "Test Journal Content Test Journal Content "
    "Test Journal Content Test Journal Content "
    "Test Journal Content"
)

JOURNAL_CREATED_HELP_TEXT = "The date and time this object was created."

JOURNAL_UPDATED_HELP_TEXT = "The date and time this object was last updated."

GROWTH_OPPORTUNITY_VERBOSE_NAME = "Growth Opportunity"
GROWTH_OPPORTUNITY_VERBOSE_NAME_PLURAL = "Growth Opportunities"

GROWTH_OPPORTUNITY_AUTHOR_LABEL = "author"
GROWTH_OPPORTUNITY_AUTHOR_RELATED_NAME = "growth_opportunities"

GROWTH_OPPORTUNITY_QUESTION_VERBOSE_NAME = "Question"
GROWTH_OPPORTUNITY_QUESTION_HELP_TEXT = "Required"

GROWTH_OPPORTUNITY_CREATED_HELP_TEXT = "The date and time this object was created."

GROWTH_OPPORTUNITY_UPDATED_HELP_TEXT = "The date and time this object was last updated."

GROWTH_OPPORTUNITY_QUESTION_LESS_THAN_TWENTY_FOUR = "Growth Opportunity"
GROWTH_OPPORTUNITY_QUESTION_GREATER_THAN_TWENTY_FOUR = (
    "Test Growth Opportunity Question"
)


class JournalModelTest(TestCase):
    """
    Tests for the `Journal` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test `cls.user` and `cls.journal`.
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.journal = Journal.objects.create(
            author=cls.user,
            title=JOURNAL_TITLE,
            content=JOURNAL_CONTENT_LESS_THAN_FIFTY,
        )

    def test_author_label(self):
        """
        `Journal` model `author` field `label` should be `author`.
        """
        field = Journal._meta.get_field("author")
        self.assertEqual(field.verbose_name, JOURNAL_AUTHOR_LABEL)

    def test_author_uses_custom_user_model(self):
        """
        `Journal` model `author` field should use the custom cls.user model.
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
        journal = Journal.objects.get(id=self.journal.id)
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

    def test_content_verbose_name(self):
        """
        `Journal` model `content` field `verbose_name` should be
        `Journal Content`.
        """
        field = Journal._meta.get_field("content")
        self.assertEqual(field.verbose_name, JOURNAL_CONTENT_VERBOSE_NAME)

    def test_content_help_text(self):
        """
        `Journal` model `content` field `help_text` should be
        `Required`.
        """
        field = Journal._meta.get_field("content")
        self.assertEqual(field.help_text, JOURNAL_CONTENT_HELP_TEXT)

    def test_created_label(self):
        """
        `Journal` model `created` field `label` should be `created`.
        """
        field = Journal._meta.get_field("created")
        self.assertEqual(field.verbose_name, "Created")

    def test_created_help_text(self):
        """
        `Journal` model `created` field `help_text` should be
        `The date and time the journal was created.`.
        """
        field = Journal._meta.get_field("created")
        self.assertEqual(field.help_text, JOURNAL_CREATED_HELP_TEXT)

    def test_created_auto_now_add_true(self):
        """
        `Journal` model `created` field `auto_now_add` should be
        `True`.
        """
        field = Journal._meta.get_field("created")
        self.assertTrue(field.auto_now_add)

    def test_updated_label(self):
        """
        `Journal` model `updated` field `label` should be `updated`.
        """
        field = Journal._meta.get_field("updated")
        self.assertEqual(field.verbose_name, "Updated")

    def test_updated_help_text(self):
        """
        `Journal` model `updated` field `help_text` should be
        `The date and time the journal was last updated.`.
        """
        field = Journal._meta.get_field("updated")
        self.assertEqual(field.help_text, JOURNAL_UPDATED_HELP_TEXT)

    def test_updated_auto_now_true(self):
        """
        `Journal` model `updated` field `auto_now` should be
        `True`.
        """
        field = Journal._meta.get_field("updated")
        self.assertTrue(field.auto_now)

    def test_str_method(self):
        """
        `Journal` model `__str__` method should return something.
        """
        journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(
            str(journal), f"{TEST_USERNAME} : {journal.id} - {JOURNAL_TITLE[:24]}"
        )

    def test_get_absolute_url_method(self):
        """
        `Journal` model `get_absolute_url` method should return
        something.
        """
        journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(journal.get_absolute_url(), f"/journals/{journal.id}/detail/")

    def test_display_content_method_less_than_fifty_characters(self):
        """
        `Journal` model `display_content` method should return
        the first 50 characters of the content.
        """
        journal = Journal.objects.get(id=self.journal.id)
        self.assertEqual(
            journal.display_content(), JOURNAL_CONTENT_LESS_THAN_FIFTY[:50]
        )

    def test_display_content_method_more_than_fifty_characters(self):
        """
        `Journal` model `display_content` method should return
        the first 50 characters of the content.
        """
        journal = Journal.objects.get(id=self.journal.id)
        journal.content = JOURNAL_CONTENT_MORE_THAN_FIFTY
        self.assertEqual(
            journal.display_content(), JOURNAL_CONTENT_MORE_THAN_FIFTY[:50] + "..."
        )


class GrowthOpportunityModelTest(TestCase):
    """
    Tests for the `GrowthOpportunity` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test `cls.user`, `cls.growth_opportunity_greater_than_24`,
        and `cls.growth_opportunity_less_than_24`.
        """

        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.growth_opportunity_less_than_24 = GrowthOpportunity.objects.create(
            author=cls.user,
            question=GROWTH_OPPORTUNITY_QUESTION_LESS_THAN_TWENTY_FOUR,
        )
        cls.growth_opportunity_greater_than_24 = GrowthOpportunity.objects.create(
            author=cls.user,
            question=GROWTH_OPPORTUNITY_QUESTION_GREATER_THAN_TWENTY_FOUR,
        )

    def test_author_label(self):
        """
        `GrowthOpportunity` model `author` field `label` should be
        `author`.
        """
        field = GrowthOpportunity._meta.get_field("author")
        self.assertEqual(field.verbose_name, GROWTH_OPPORTUNITY_AUTHOR_LABEL)

    def test_author_uses_custom_user_model(self):
        """
        `GrowthOpportunity` model `author` field should use the
        `CustomUser` model.
        """
        field = GrowthOpportunity._meta.get_field("author")
        self.assertEqual(field.related_model, CustomUser)

    def test_author_on_delete_cascade(self):
        """
        `GrowthOpportunity` model `author` field `on_delete` should be
        `CASCADE`.
        """
        field = GrowthOpportunity._meta.get_field("author")
        self.assertEqual(field.remote_field.on_delete, d_db_models.CASCADE)

    def test_author_related_name(self):
        """
        `GrowthOpportunity` model `author` field `related_name` should be
        `growth_opportunities`.
        """
        growth_opportunity_less_than_24 = GrowthOpportunity.objects.get(
            id=self.growth_opportunity_less_than_24.id
        )
        related_name = growth_opportunity_less_than_24._meta.get_field(
            "author"
        ).related_query_name()
        self.assertEqual(related_name, GROWTH_OPPORTUNITY_AUTHOR_RELATED_NAME)

    def test_question_verbose_name(self):
        """
        `GrowthOpportunity` model `question` field `verbose_name` should be
        `question`.
        """
        field = GrowthOpportunity._meta.get_field("question")
        self.assertEqual(field.verbose_name, GROWTH_OPPORTUNITY_QUESTION_VERBOSE_NAME)

    def test_question_help_text(self):
        """
        `GrowthOpportunity` model `question` field `help_text` should be
        `The question for the growth opportunity.`.
        """
        field = GrowthOpportunity._meta.get_field("question")
        self.assertEqual(field.help_text, GROWTH_OPPORTUNITY_QUESTION_HELP_TEXT)

    def test_created_help_text(self):
        """
        `GrowthOpportunity` model `created` field `help_text` should be
        `The date and time the growth opportunity was created.`.
        """
        field = GrowthOpportunity._meta.get_field("created")
        self.assertEqual(field.help_text, GROWTH_OPPORTUNITY_CREATED_HELP_TEXT)

    def test_created_auto_now_add_true(self):
        """
        `GrowthOpportunity` model `created` field `auto_now_add` should be
        `True`.
        """
        field = GrowthOpportunity._meta.get_field("created")
        self.assertTrue(field.auto_now_add)

    def test_updated_help_text(self):
        """
        `GrowthOpportunity` model `updated` field `help_text` should be
        `The date and time the growth opportunity was last updated.`.
        """
        field = GrowthOpportunity._meta.get_field("updated")
        self.assertEqual(field.help_text, GROWTH_OPPORTUNITY_UPDATED_HELP_TEXT)

    def test_updated_auto_now_true(self):
        """
        `GrowthOpportunity` model `updated` field `auto_now` should be
        `True`.
        """
        field = GrowthOpportunity._meta.get_field("updated")
        self.assertTrue(field.auto_now)

    def test_dunder_string_method(self):
        """
        `GrowthOpportunity` model `__str__` method should return
        something.
        """
        growth_opportunity = GrowthOpportunity.objects.get(
            id=self.growth_opportunity_less_than_24.id
        )
        self.assertEqual(
            str(growth_opportunity),
            f"{growth_opportunity.question}",
        )
        growth_opportunity = GrowthOpportunity.objects.get(
            id=self.growth_opportunity_greater_than_24.id
        )
        self.assertEqual(
            str(growth_opportunity),
            f"{growth_opportunity.question[:24]}...",
        )
