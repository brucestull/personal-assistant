from django.test import SimpleTestCase
from django.urls import reverse, resolve

from packing_list import views


class UrlsTest(SimpleTestCase):
    def test_activity_list_url(self):
        url = reverse("packing_list:activity_list")
        self.assertEqual(resolve(url).func, views.activity_list)

    def test_activity_detail_url(self):
        url = reverse("packing_list:activity_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.activity_detail)

    def test_activity_create_url(self):
        url = reverse("packing_list:activity_create")
        self.assertEqual(resolve(url).func, views.activity_create)

    def test_activity_update_url(self):
        url = reverse("packing_list:activity_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.activity_update)

    def test_activity_delete_url(self):
        url = reverse("packing_list:activity_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.activity_delete)

    def test_activity_pdf_url(self):
        url = reverse("packing_list:activity_pdf", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.activity_pdf)

    def test_item_list_url(self):
        url = reverse("packing_list:item_list")
        self.assertEqual(resolve(url).func, views.item_list)

    def test_item_detail_url(self):
        url = reverse("packing_list:item_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.item_detail)

    def test_item_create_url(self):
        url = reverse("packing_list:item_create")
        self.assertEqual(resolve(url).func, views.item_create)

    def test_item_update_url(self):
        url = reverse("packing_list:item_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.item_update)

    def test_item_delete_url(self):
        url = reverse("packing_list:item_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.item_delete)

    def test_task_list_url(self):
        url = reverse("packing_list:task_list")
        self.assertEqual(resolve(url).func, views.task_list)

    def test_task_detail_url(self):
        url = reverse("packing_list:task_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.task_detail)

    def test_task_create_url(self):
        url = reverse("packing_list:task_create")
        self.assertEqual(resolve(url).func, views.task_create)

    def test_task_update_url(self):
        url = reverse("packing_list:task_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.task_update)

    def test_task_delete_url(self):
        url = reverse("packing_list:task_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, views.task_delete)
