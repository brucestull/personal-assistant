from django.test import TestCase
from django.urls import reverse, resolve

from self_enquiry.models import Journal
from self_enquiry.views import JournalListView, JournalCreateView
from accounts.models import CustomUser


THE_SITE_NAME = "Health Activities"

A_TEST_USERNAME = "ACustomUser"
A_TEST_PASSWORD = "Apassword123"

JOURNAL_LIST_URL = "/journals/list/"
JOURNAL_LIST_VIEW_NAME = "self_enquiry:list"
JOURNAL_LIST_TEMPLATE = "self_enquiry/journal_list.html"
JOURNAL_LIST_PAGE_TITLE = "Journals"

JOURNAL_CREATE_URL = "/journals/create/"
JOURNAL_CREATE_VIEW_NAME = "self_enquiry:create"
JOURNAL_CREATE_TEMPLATE = "self_enquiry/journal_form.html"
JOURNAL_CREATE_PAGE_TITLE = "Create a Journal"

TEST_JOURNAL_TITLE = "Test Journal Title"
TEST_JOURNAL_CONTENT = "Test Journal Content"

NUMBER_OF_JOURNALS = 13
NUMBER_OF_JOURNALS_PER_PAGE = 10


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
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
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
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        `JournalListView` view should be accessible by name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        `JournalListView` view should use the correct template.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_LIST_TEMPLATE)

    def test_view_uses_correct_page_title(self):
        """
        `JournalListView` view should use the correct page title.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, f"<title>{THE_SITE_NAME} - {JOURNAL_LIST_PAGE_TITLE}</title>"
        )

    def test_view_pagination_is_ten(self):
        """
        `JournalListView` view should paginate by ten.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["journal_list"]) == 10)

    def test_view_returns_journal_ojects(self):
        """
        `JournalListView` view should return journal objects.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(
            len(response.context["journal_list"]) == NUMBER_OF_JOURNALS_PER_PAGE
        )
        for journal in response.context["journal_list"]:
            self.assertTrue(isinstance(journal, Journal))

    def test_view_pagination_is_correct(self):
        """
        `JournalListView` view should paginate correctly.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME) + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["journal_list"]) == 3)

    def test_view_returns_all_journals(self):
        """
        `JournalListView` view should return all journals.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response_page_one = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME))
        self.assertEqual(response_page_one.status_code, 200)
        self.assertTrue("is_paginated" in response_page_one.context)
        self.assertTrue(response_page_one.context["is_paginated"] == True)
        self.assertTrue(
            len(response_page_one.context["journal_list"])
            == NUMBER_OF_JOURNALS_PER_PAGE
        )
        response_page_two = self.client.get(reverse(JOURNAL_LIST_VIEW_NAME) + "?page=2")
        self.assertEqual(response_page_two.status_code, 200)
        self.assertTrue("is_paginated" in response_page_two.context)
        self.assertTrue(response_page_two.context["is_paginated"] == True)
        self.assertTrue(len(response_page_two.context["journal_list"]) == 3)


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
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )

    def test_journal_create_url_returns_200(self):
        """
        `JournalCreateView` view `url` should return a 200 response.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        `JournalCreateView` view should be accessible by name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        `JournalCreateView` view should use the correct template.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(reverse(JOURNAL_CREATE_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, JOURNAL_CREATE_TEMPLATE)

    def test_view_context_contains_page_title(self):
        """
        `JournalCreateView` view should use the correct page title.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("page_title" in response.context)
        self.assertEqual(response.context["page_title"], JOURNAL_CREATE_PAGE_TITLE)

    def test_view_context_contains_the_site_name(self):
        """
        `JournalCreateView` view should use the correct site name.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("the_site_name" in response.context)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)

    def test_view_has_proper_fields(self):
        """
        `JournalCreateView` view should have the proper fields.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        response = self.client.get(JOURNAL_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("title" in response.context["form"].fields)
        self.assertTrue("content" in response.context["form"].fields)

    def test_view_redirects_to_list_on_success(self):
        """
        `JournalCreateView` view should redirect to the list view on success.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
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
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
        self.client.post(
            JOURNAL_CREATE_URL,
            {
                "title": TEST_JOURNAL_TITLE,
                "content": TEST_JOURNAL_CONTENT,
            },
        )
        self.assertTrue(Journal.objects.filter(title=TEST_JOURNAL_TITLE).exists())

    def test_created_journal_is_owned_by_current_user(self):
        """
        `JournalCreateView` view should create a journal owned by the current user.
        """
        login = self.client.login(
            username=A_TEST_USERNAME,
            password=A_TEST_PASSWORD,
        )
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
            Journal.objects.filter(title=TEST_JOURNAL_TITLE).first().author
            == self.user,
        )
