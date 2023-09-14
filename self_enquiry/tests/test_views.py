from django.test import TestCase
from django.urls import reverse

from self_enquiry.models import Journal
from self_enquiry.views import (
    JournalUpdateView,
    JournalDeleteView,
)
from accounts.models import CustomUser


THE_SITE_NAME = "Personal Assistant"

TEST_USERNAME_ONE = "test_username_one"
TEST_PASSWORD_ONE = "test_password_one"

TEST_USERNAME_TWO = "test_username_two"
TEST_PASSWORD_TWO = "test_password_two"

JOURNAL_CREATE_URL = "/journals/create/"
JOURNAL_CREATE_VIEW_NAME = "self_enquiry:create"
JOURNAL_CREATE_TEMPLATE = "self_enquiry/journal_form.html"
JOURNAL_CREATE_PAGE_TITLE = "Create a Journal"

JOURNAL_LIST_URL = "/journals/list/"
JOURNAL_LIST_VIEW_NAME = "self_enquiry:list"
JOURNAL_LIST_TEMPLATE = "self_enquiry/journal_list.html"
JOURNAL_LIST_PAGE_TITLE = "Journals"

JOURNAL_DETAIL_URL = "/journals/1/"
JOURNAL_DETAIL_VIEW_NAME = "self_enquiry:detail"
JOURNAL_DETAIL_TEMPLATE = "self_enquiry/journal_detail.html"
JOURNAL_DETAIL_PAGE_TITLE = "Journal Detail"

JOURNAL_UPDATE_URL = "/journals/1/update/"
JOURNAL_UPDATE_VIEW_NAME = "self_enquiry:update"
JOURNAL_UPDATE_TEMPLATE = "self_enquiry/journal_form.html"
JOURNAL_UPDATE_PAGE_TITLE = "Update a Journal"
JOURNAL_UPDATE_FORM_BUTTON_TEXT = "Update your Journal!"

JOURNAL_CONFIRM_DELETE_URL = "/journals/1/confirm-delete/"
JOURNAL_CONFIRM_DELETE_VIEW_NAME = "self_enquiry:confirm-delete"
JOURNAL_CONFIRM_DELETE_TEMPLATE = "self_enquiry/journal_confirm_delete.html"
JOURNAL_CONFIRM_DELETE_PAGE_TITLE = "Delete a Journal"
JOURNAL_CONFIRM_DELETE_FORM_BUTTON_TEXT = "Confirm Delete your Journal!"

JOURNAL_DELETE_URL = "/journals/1/delete/"
JOURNAL_DELETE_VIEW_NAME = "self_enquiry:delete"
JOURNAL_DELETE_TEMPLATE = "self_enquiry/journal_confirm_delete.html"
JOURNAL_DELETE_PAGE_TITLE = "Delete a Journal"
JOURNAL_DELETE_FORM_BUTTON_TEXT = "Delete your Journal!"

TEST_JOURNAL_TITLE = "Test Journal Title"
TEST_JOURNAL_CONTENT = "Test Journal Content"

NUMBER_OF_JOURNALS = 13
NUMBER_OF_JOURNALS_PER_PAGE = 10


class JournalCreateViewTest(TestCase):
    """
    Tests for `JournalCreateView`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user.
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )

    def test_journal_create_url_returns_200(self):
        """
        `JournalCreateView` view `url` should return a 200 response.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        `JournalCreateView` view should be accessible by name.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        `JournalCreateView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_CREATE_TEMPLATE)

    def test_view_context_contains_page_title(self):
        """
        `JournalCreateView` view should use the correct page title.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("page_title" in response.context)
        self.assertEqual(
            response.context["page_title"], JOURNAL_CREATE_PAGE_TITLE)

    def test_view_context_contains_the_site_name(self):
        """
        `JournalCreateView` view should use the correct site name.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("the_site_name" in response.context)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)

    def test_view_has_proper_fields(self):
        """
        `JournalCreateView` view should have the proper fields.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("title" in response.context["form"].fields)
        self.assertTrue("content" in response.context["form"].fields)

    def test_view_redirects_to_list_on_success(self):
        """
        `JournalCreateView` view should redirect to the list view on success.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.post(
            JOURNAL_CREATE_URL,
            {
                "title": TEST_JOURNAL_TITLE,
                "content": TEST_JOURNAL_CONTENT,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(JOURNAL_LIST_VIEW_NAME))

    def test_view_creates_journal_on_success(self):
        """
        `JournalCreateView` view should create a journal on success.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        self.client.post(
            JOURNAL_CREATE_URL,
            {
                "title": TEST_JOURNAL_TITLE,
                "content": TEST_JOURNAL_CONTENT,
            },
        )
        self.assertTrue(Journal.objects.filter(
            title=TEST_JOURNAL_TITLE).exists())

    def test_created_journal_is_owned_by_current_user(self):
        """
        `JournalCreateView` view should create a journal owned by the current
        user.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        self.client.post(
            JOURNAL_CREATE_URL,
            {
                "title": TEST_JOURNAL_TITLE,
                "content": TEST_JOURNAL_CONTENT,
            },
        )
        self.assertTrue(
            Journal.objects.filter(title=TEST_JOURNAL_TITLE).exists(),
        )
        self.assertTrue(
            Journal.objects.filter(
                title=TEST_JOURNAL_TITLE).first().author == self.user,
        )


class JournalListViewTest(TestCase):
    """
    Tests for the `JournalListView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        # Create 13 journals for pagination tests.
        number_of_journals = 13
        cls.all_the_journals = []
        for journal_num in range(number_of_journals):
            journal = Journal.objects.create(
                author=cls.user,
                title=f"Test Journal Title: {journal_num}",
                content=f"Test Journal Content: {journal_num}",
            )
            cls.all_the_journals.append(journal)
        pass

    def test_the_test_worked(self):
        """
        Sanity check.
        """
        self.assertEqual(1 + 1, 2)

    def test_journal_list_url_returns_200(self):
        """
        `JournalListView` view `url` should return a 200 response.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(JOURNAL_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        `JournalListView` view should be accessible by name.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        `JournalListView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_LIST_TEMPLATE)

    def test_view_uses_correct_page_title(self):
        """
        `JournalListView` view should use the correct page title.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f"<title>{THE_SITE_NAME} - {JOURNAL_LIST_PAGE_TITLE}</title>",
        )

    def test_view_pagination_is_ten(self):
        """
        `JournalListView` view should paginate by ten.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["journal_list"]) == 10)

    def test_view_returns_journal_ojects(self):
        """
        `JournalListView` view should return journal objects.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(
            len(response.context["journal_list"]
                ) == NUMBER_OF_JOURNALS_PER_PAGE
        )
        for journal in response.context["journal_list"]:
            self.assertTrue(isinstance(journal, Journal))

    def test_view_pagination_is_correct(self):
        """
        `JournalListView` view should paginate correctly.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME) + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["journal_list"]) == 3)

    def test_view_returns_all_journals(self):
        """
        `JournalListView` view should return all journals.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response_page_one = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response_page_one.status_code, 200)
        self.assertTrue("is_paginated" in response_page_one.context)
        self.assertTrue(response_page_one.context["is_paginated"])
        self.assertTrue(
            len(
                response_page_one.context["journal_list"]
            ) == NUMBER_OF_JOURNALS_PER_PAGE
        )
        response_page_two = self.client.get(
            reverse(JOURNAL_LIST_VIEW_NAME) + "?page=2")
        self.assertEqual(response_page_two.status_code, 200)
        self.assertTrue("is_paginated" in response_page_two.context)
        self.assertTrue(response_page_two.context["is_paginated"])
        self.assertTrue(len(response_page_two.context["journal_list"]) == 3)


class JournalDetailViewTest(TestCase):
    """
    Test `JournalDetailView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        cls.user_one = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        cls.user_two = CustomUser.objects.create_user(
            username=TEST_USERNAME_TWO,
            password=TEST_PASSWORD_TWO,
        )
        cls.journal = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )

    def test_journal_detail_url_returns_200(self):
        """
        `JournalDetailView` view `url` should return a 200 response.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(self.journal.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        `JournalDetailView` view should be accessible by name.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DETAIL_VIEW_NAME, args=[self.journal.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        `JournalDetailView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DETAIL_VIEW_NAME, args=[self.journal.id]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_DETAIL_TEMPLATE)

    def test_view_uses_correct_page_title(self):
        """
        `JournalDetailView` view should use the correct page title.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DETAIL_VIEW_NAME, args=[self.journal.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f"<title>{THE_SITE_NAME} - {JOURNAL_DETAIL_PAGE_TITLE}</title>",
        )

    def test_view_accessible_by_user(self):
        """
        `JournalDetailView` view should be accessible by the user who created
        the journal.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DETAIL_VIEW_NAME, args=[self.journal.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_inaccessible_by_another_user(self):
        """
        `JournalDetailView` view should be inaccessible by another user.
        """
        login = self.client.login(
            username=TEST_USERNAME_TWO,
            password=TEST_PASSWORD_TWO,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DETAIL_VIEW_NAME, args=[self.journal.id])
        )
        self.assertEqual(response.status_code, 403)


class JournalUpdateViewTest(TestCase):
    """
    Test `JournalUpdateView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        cls.user_one = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        cls.user_two = CustomUser.objects.create_user(
            username=TEST_USERNAME_TWO,
            password=TEST_PASSWORD_TWO,
        )
        cls.journal_one = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )

    def test_uses_correct_model(self):
        """
        `JournalUpdateView` view should use the correct model.
        """
        self.assertEqual(JournalUpdateView.model, Journal)

    def test_uses_correct_template(self):
        """
        `JournalUpdateView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_UPDATE_TEMPLATE)

    def test_has_correct_fields(self):
        """
        View should have only `title` and `content` fields.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Title")
        self.assertContains(response, "Content")
        self.assertNotContains(response, "Author")

    def test_has_correct_extra_context(self):
        """
        View should have correct extra context.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(
            response.context["page_title"], JOURNAL_UPDATE_PAGE_TITLE)
        self.assertEqual(
            response.context["form_button_text"],
            JOURNAL_UPDATE_FORM_BUTTON_TEXT,
        )

    def test_form_valid_method(self):
        """
        `form_valid` method should set the `author` field of the journal to
        the current user.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.post(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id]),
            data={
                "title": TEST_JOURNAL_TITLE,
                "content": TEST_JOURNAL_CONTENT,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Journal.objects.get(id=self.journal_one.id).author, self.user_one
        )

    def test_view_accessible_by_user(self):
        """
        `JournalUpdateView` view should be accessible by the user who created
        the journal.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_inaccessible_by_another_user(self):
        """
        `JournalUpdateView` view should be inaccessible by another user.
        """
        login = self.client.login(
            username=TEST_USERNAME_TWO,
            password=TEST_PASSWORD_TWO,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_UPDATE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 403)


class JournalConfirmDeleteViewTest(TestCase):
    """
    Test for `JournalConfirmDeleteView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        cls.user_one = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        cls.journal_one = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )
        cls.journal_two = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )

    def test_uses_correct_template(self):
        """
        `JournalConfirmDeleteView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_CONFIRM_DELETE_VIEW_NAME,
                    args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_CONFIRM_DELETE_TEMPLATE)

    def test_get_method(self):
        """
        `JournalConfirmDeleteView` view should return a confirmation page.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_CONFIRM_DELETE_VIEW_NAME,
                    args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["journal"], self.journal_one)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(
            response.context["page_title"], JOURNAL_CONFIRM_DELETE_PAGE_TITLE)
        # TODO: Fix this test.
        # self.assertEqual(
        #     response.context["form_button_text"],
        #     JOURNAL_CONFIRM_DELETE_FORM_BUTTON_TEXT,
        # )


class JournalDeleteViewTest(TestCase):
    """
    Test `JournalDeleteView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and journal.
        """
        cls.user_one = CustomUser.objects.create_user(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        cls.journal_one = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )
        cls.journal_two = Journal.objects.create(
            author=cls.user_one,
            title=TEST_JOURNAL_TITLE,
            content=TEST_JOURNAL_CONTENT,
        )

    def test_uses_correct_model(self):
        """
        `JournalDeleteView` view should use the correct model.
        """
        self.assertEqual(JournalDeleteView.model, Journal)

    def test_uses_correct_template(self):
        """
        `JournalDeleteView` view should use the correct template.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.get(
            reverse(JOURNAL_DELETE_VIEW_NAME, args=[self.journal_one.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_DELETE_TEMPLATE)

    def test_get_success_url_method(self):
        """
        `get_success_url` method should return the Journal List page.
        """
        login = self.client.login(
            username=TEST_USERNAME_ONE,
            password=TEST_PASSWORD_ONE,
        )
        self.assertTrue(login)
        response = self.client.post(
            reverse(JOURNAL_DELETE_VIEW_NAME, args=[self.journal_one.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(JOURNAL_LIST_VIEW_NAME))
