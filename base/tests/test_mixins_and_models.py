from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.views import View

from base.mixins import (
    OrderableMixin,
    SiteContextMixin,
    UserAssignMixin,
    UserIsAuthorMixin,
    UserQuerySetMixin,
)
from base.models import Note, URL
from packing_list.models import Activity

User = get_user_model()


class BaseModelTests(TestCase):
    def test_note_display_content_and_str(self):
        class TestNote(Note):
            class Meta:
                app_label = "base"
                managed = False

        long_content = "x" * 60
        note = TestNote(title="My Title", content=long_content)
        self.assertEqual(note.display_content(), ("x" * 30) + "...")
        self.assertIn("...", str(note))

        short_note = TestNote(title="Short", content="small")
        self.assertEqual(short_note.display_content(), "small")
        self.assertEqual(str(short_note), "Short - small")

    def test_url_str(self):
        class TestURL(URL):
            class Meta:
                app_label = "base"
                managed = False

        model = TestURL(
            label="Docs", url="https://example.com", url_type="documentation"
        )
        self.assertEqual(str(model), "Docs (documentation)")


class BaseMixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="base-user", password="pw", registration_accepted=True
        )
        self.other_user = User.objects.create_user(
            username="other-user", password="pw", registration_accepted=True
        )
        self.activity = Activity.objects.create(name="Mine", user=self.user)
        Activity.objects.create(name="Other", user=self.other_user)

    def test_user_queryset_mixin_filters_by_request_user(self):
        class Dummy(UserQuerySetMixin):
            model = Activity

        view = Dummy()
        request = self.factory.get("/")
        request.user = self.user
        view.request = request
        self.assertEqual(list(view.get_queryset()), [self.activity])

    def test_user_assign_mixin_sets_user_on_form_instance(self):
        class Parent:
            def form_valid(self, form):
                return "ok"

        class Dummy(UserAssignMixin, Parent):
            pass

        view = Dummy()
        request = self.factory.post("/")
        request.user = self.user
        view.request = request
        form = SimpleNamespace(instance=SimpleNamespace(user=None))
        self.assertEqual(view.form_valid(form), "ok")
        self.assertEqual(form.instance.user, self.user)

    def test_user_is_author_mixin_denies_non_author(self):
        class TestView(UserIsAuthorMixin, View):
            desired_author = None

            def get_object(self):
                return SimpleNamespace(author=self.desired_author)

            def get(self, request, *args, **kwargs):
                return HttpResponse("ok")

        request = self.factory.get("/")
        request.user = self.other_user
        with self.assertRaises(PermissionDenied):
            TestView.as_view(desired_author=self.user)(request)

    def test_user_is_author_mixin_allows_author(self):
        class TestView(UserIsAuthorMixin, View):
            desired_author = None

            def get_object(self):
                return SimpleNamespace(author=self.desired_author)

            def get(self, request, *args, **kwargs):
                return HttpResponse("ok")

        request = self.factory.get("/")
        request.user = self.user
        response = TestView.as_view(desired_author=self.user)(request)
        self.assertEqual(response.status_code, 200)

    def test_orderable_mixin_reorder_all(self):
        saved = []

        class DummyItem:
            def __init__(self, order):
                self.order = order

            def save(self):
                saved.append(self.order)

        class DummyManager:
            def __init__(self, items):
                self._items = items

            def all(self):
                return self

            def order_by(self, *_):
                return sorted(self._items, key=lambda i: i.order)

        class Dummy(OrderableMixin):
            objects = DummyManager([DummyItem(10), DummyItem(3), DummyItem(7)])

        Dummy.reorder_all()
        self.assertEqual(saved, [0, 1, 2])

    @override_settings(THE_SITE_NAME="Site Name")
    def test_site_context_mixin_helpers(self):
        class Base:
            def get_context_data(self, **kwargs):
                return {"existing": True}

        class Dummy(SiteContextMixin, Base):
            page_title = None

        view = Dummy()
        self.assertEqual(view.get_site_name(), "Site Name")
        self.assertEqual(view.get_page_title(), "Dummy")
        context = view.get_context_data()
        self.assertEqual(context["the_site_name"], "Site Name")
        self.assertEqual(context["page_title"], "Dummy")
