# app_tracker/tests/test_full_coverage.py

import django
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

# NOTE: Adjust this if your settings module is different
# You only need these two lines if you want to run this module standalone
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_tracker.models import (
    Application,
    Label,
    LanguageFrameworkSystem,
    Note,
    OperatingSystem,
    OrganizationalConcept,
    Project,
    Server,
)
from app_tracker.views import home

User = get_user_model()


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user (for Project.owner M2M) and mark registration accepted if needed
        self.user = User.objects.create_user(username="tester", password="pass")
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

    def test_operating_system_str(self):
        os_obj = OperatingSystem.objects.create(name="Ubuntu 22.04")
        self.assertEqual(str(os_obj), "Ubuntu 22.04")

    def test_language_framework_system_str(self):
        lfs = LanguageFrameworkSystem.objects.create(name="Django")
        self.assertEqual(str(lfs), "Django")

    def test_organizational_concept_str_and_app_count(self):
        # Create one Application, attach it to OrganizationalConcept, then __str__()
        app = Application.objects.create(name="AppOne")
        oc = OrganizationalConcept.objects.create(name="Concept1", description="Desc")
        oc.applications.add(app)
        expected = "Concept1 | Applications Count: 1"
        self.assertEqual(str(oc), expected)

        # When no M2M, count should be zero
        oc2 = OrganizationalConcept.objects.create(name="Concept2", description="Desc2")
        self.assertEqual(str(oc2), "Concept2 | Applications Count: 0")

    def test_label_str_and_m2m(self):
        app = Application.objects.create(name="AppLabel")
        label = Label.objects.create(name="Bug", hue="#FF0000", description="Bug label")
        label.application.add(app)
        self.assertEqual(str(label), "Bug")
        self.assertIn(app, label.application.all())

    def test_note_str_with_and_without_application(self):
        # Without application
        note = Note.objects.create(title="Note1", content="Some content")
        self.assertEqual(str(note), "Note1 - No Application")

        # With application
        app = Application.objects.create(name="AppNote")
        note2 = Note.objects.create(
            title="Note2", content="Other content", application=app
        )
        self.assertEqual(str(note2), "Note2 - AppNote")

    def test_server_str_and_fields(self):
        os_obj = OperatingSystem.objects.create(name="CentOS 8")
        server = Server.objects.create(
            host_name="SERVER1",
            ip_address="192.168.1.10",
            environment="production",
            operating_system=os_obj,
            notes="Specs",
        )
        # __str__ should show "HOST_NAME (IP)" if IP is present
        self.assertEqual(str(server), "SERVER1 (192.168.1.10)")

        # If ip_address is None, it falls back to 'no IP'
        server_no_ip = Server.objects.create(host_name="SERVER2")
        self.assertEqual(str(server_no_ip), "SERVER2 (no IP)")

        # Test M2M applications on Server
        app_for_server = Application.objects.create(name="AppServer")
        server.applications.add(app_for_server)
        self.assertIn(app_for_server, server.applications.all())

    def test_project_str_and_owner_m2m(self):
        project = Project.objects.create(name="Proj1", description="ProjDesc")
        project.owner.add(self.user)
        self.assertEqual(str(project), "Proj1")
        self.assertIn(self.user, project.owner.all())

    def test_application_str_and_get_absolute_url_and_m2m(self):
        app = Application.objects.create(name="MyApp")

        # Test __str__
        self.assertEqual(str(app), "MyApp")

        # Test get_absolute_url
        expected_url = reverse("app_tracker:application_detail", kwargs={"pk": app.pk})
        self.assertEqual(app.get_absolute_url(), expected_url)

        # Test M2M on Application: project & language_framework_systems
        proj = Project.objects.create(name="ProjApp", description="Desc")
        lfs = LanguageFrameworkSystem.objects.create(name="Flask")
        app.project.add(proj)
        app.language_framework_systems.add(lfs)

        self.assertIn(proj, app.project.all())
        self.assertIn(lfs, app.language_framework_systems.all())

    def test_django_model_str_and_foreignkey(self):
        from app_tracker.models import DjangoModel

        app = Application.objects.create(name="AppDM")
        dm_obj = DjangoModel.objects.create(
            name="Model1", description="Desc", application=app
        )
        self.assertEqual(str(dm_obj), "Model1")
        self.assertEqual(dm_obj.application, app)


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # Create a registered user (RegistrationAcceptedMixin will check this field)
        self.user = User.objects.create_user(username="viewuser", password="pass")
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

        # Log in the client so RegistrationAcceptedMixin won’t redirect
        self.client.login(username="viewuser", password="pass")

        # Create one instance of each model so that detail/list views have something to return
        self.os_obj = OperatingSystem.objects.create(name="TestOS")
        self.lfs_obj = LanguageFrameworkSystem.objects.create(name="TestLFS")
        self.app_obj = Application.objects.create(name="TestApp")
        self.label_obj = Label.objects.create(name="TestLabel")
        self.label_obj.application.add(self.app_obj)
        self.note_obj = Note.objects.create(
            title="TestNote", content="C", application=self.app_obj
        )
        self.oc_obj = OrganizationalConcept.objects.create(
            name="TestOC", description="Desc"
        )
        self.oc_obj.applications.add(self.app_obj)
        self.project_obj = Project.objects.create(name="TestProj", description="Desc")
        self.project_obj.owner.add(self.user)
        self.server_obj = Server.objects.create(
            host_name="TestServer",
            ip_address="10.0.0.1",
            environment="test",
            operating_system=self.os_obj,
        )
        self.server_obj.applications.add(self.app_obj)

    def test_home_view(self):
        """
        The home() view should return status 200 and include
        both "the_site_name" and "page_title" in its context.
        """
        request = self.factory.get(reverse("app_tracker:home"))
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)
        # context_data is available because render(...) puts it there
        self.assertIn("the_site_name", response.context_data)
        self.assertEqual(response.context_data["page_title"], "App Tracker Home")

    def _test_crud_views_for_model(self, model, instance, form_fields, url_prefix):
        """
        Helper: For a given model, its existing instance, and the names of
        fields to include in a POST, exercise List, Detail, Create, Update, Delete.
        """
        # ——— List view ———
        list_url = reverse(f"app_tracker:{url_prefix}_list")
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(instance, resp.context["object_list"])

        # ——— Detail view ———
        detail_url = reverse(
            f"app_tracker:{url_prefix}_detail", kwargs={"pk": instance.pk}
        )
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["object"], instance)

        # ——— Create view ———
        create_url = reverse(f"app_tracker:{url_prefix}_create")
        # Build minimal valid POST data:
        post_data = {}
        if model == Application:
            post_data = {"name": "CreatedApp"}
        elif model == Label:
            post_data = {"name": "CreatedLabel"}
        elif model == LanguageFrameworkSystem:
            post_data = {"name": "CreatedLFS"}
        elif model == OperatingSystem:
            post_data = {"name": "CreatedOS"}
        elif model == OrganizationalConcept:
            post_data = {"name": "CreatedOC", "description": "D"}
        elif model == Project:
            post_data = {"name": "CreatedProj", "description": "D"}
        elif model == Note:
            # Needs a valid application FK:
            new_app = Application.objects.create(name="AppForNote")
            post_data = {
                "title": "CreatedNote",
                "content": "C",
                "application": new_app.pk,
            }
        elif model == Server:
            # Needs operating_system FK
            post_data = {
                "host_name": "CreatedServer",
                "ip_address": "192.168.0.50",
                "environment": "development",
                "operating_system": self.os_obj.pk,
            }

        resp = self.client.post(create_url, post_data)
        self.assertEqual(resp.status_code, 302)
        # The newly created object's PK is in the redirect URL:
        # e.g. /app_tracker/application/5/  →  pk=5
        new_pk = int(resp.url.rstrip("/").split("/")[-1])
        self.assertTrue(model.objects.filter(pk=new_pk).exists())

        # ——— Update view ———
        update_url = reverse(
            f"app_tracker:{url_prefix}_update", kwargs={"pk": instance.pk}
        )
        # Change just one field:
        modified_data = {}
        if model in (Application, Label, LanguageFrameworkSystem, OperatingSystem):
            # Those all have only a 'name' to update
            modified_data["name"] = getattr(instance, "name") + "_upd"
        elif model == OrganizationalConcept:
            modified_data = {
                "name": instance.name + "_upd",
                "description": instance.description,
            }
        elif model == Project:
            modified_data = {
                "name": instance.name + "_upd",
                "description": instance.description,
            }
        elif model == Note:
            modified_data = {
                "title": instance.title + "_upd",
                "content": instance.content,
                "application": instance.application.pk if instance.application else "",
            }
        elif model == Server:
            modified_data = {
                "host_name": instance.host_name + "_upd",
                "ip_address": instance.ip_address,
                "environment": instance.environment,
                "operating_system": (
                    instance.operating_system.pk if instance.operating_system else ""
                ),
            }

        resp = self.client.post(update_url, modified_data)
        self.assertEqual(resp.status_code, 302)
        instance.refresh_from_db()

        # Assert the field was updated
        if model in (Application, Label, LanguageFrameworkSystem, OperatingSystem):
            self.assertTrue(instance.name.endswith("_upd"))
        elif model in (OrganizationalConcept, Project):
            self.assertTrue(instance.name.endswith("_upd"))
        elif model == Note:
            self.assertTrue(instance.title.endswith("_upd"))
        elif model == Server:
            self.assertTrue(instance.host_name.endswith("_upd"))

        # ——— Delete view ———
        delete_url = reverse(
            f"app_tracker:{url_prefix}_delete", kwargs={"pk": instance.pk}
        )
        resp = self.client.post(delete_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(model.objects.filter(pk=instance.pk).exists())

    def test_application_crud(self):
        self._test_crud_views_for_model(
            Application, self.app_obj, ["name"], "application"
        )

    def test_label_crud(self):
        self._test_crud_views_for_model(Label, self.label_obj, ["name"], "label")

    def test_lfs_crud(self):
        self._test_crud_views_for_model(
            LanguageFrameworkSystem, self.lfs_obj, ["name"], "lfs"
        )

    def test_note_crud(self):
        self._test_crud_views_for_model(
            Note, self.note_obj, ["title", "content"], "note"
        )

    def test_operating_system_crud(self):
        self._test_crud_views_for_model(OperatingSystem, self.os_obj, ["name"], "os")

    def test_organizational_concept_crud(self):
        self._test_crud_views_for_model(
            OrganizationalConcept, self.oc_obj, ["name", "description"], "oc"
        )

    def test_project_crud(self):
        self._test_crud_views_for_model(
            Project, self.project_obj, ["name", "description"], "project"
        )

    def test_server_crud(self):
        self._test_crud_views_for_model(
            Server,
            self.server_obj,
            ["host_name", "ip_address", "environment", "operating_system"],
            "server",
        )
