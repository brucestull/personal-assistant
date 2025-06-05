# app_tracker/tests/test_full_coverage.py

import django
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

# Ensure Django settings are loaded if you run this module directly
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
        # Create a user for M2M relationships
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
        app = Application.objects.create(name="AppOne")
        oc = OrganizationalConcept.objects.create(name="Concept1", description="Desc")
        oc.applications.add(app)
        self.assertEqual(str(oc), "Concept1 | Applications Count: 1")

        oc2 = OrganizationalConcept.objects.create(name="Concept2", description="Desc2")
        self.assertEqual(str(oc2), "Concept2 | Applications Count: 0")

    def test_label_str_and_m2m(self):
        app = Application.objects.create(name="AppLabel")
        label = Label.objects.create(name="Bug", hue="#FF0000", description="Bug label")
        label.application.add(app)
        self.assertEqual(str(label), "Bug")
        self.assertIn(app, label.application.all())

    def test_note_str_with_and_without_application(self):
        note = Note.objects.create(title="Note1", content="Some content")
        self.assertEqual(str(note), "Note1 - No Application")

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
        self.assertEqual(str(server), "SERVER1 (192.168.1.10)")

        server_no_ip = Server.objects.create(host_name="SERVER2")
        self.assertEqual(str(server_no_ip), "SERVER2 (no IP)")

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
        self.assertEqual(str(app), "MyApp")

        expected_url = reverse("app_tracker:application_detail", kwargs={"pk": app.pk})
        self.assertEqual(app.get_absolute_url(), expected_url)

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
        self.client = Client()
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username="viewuser", password="pass")
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

        self.client.login(username="viewuser", password="pass")

        # Create one instance of each model so list/detail have data
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

    def test_home_view_render(self):
        """
        Confirm that the home() view returns 200 and includes the expected title.
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "App Tracker Home")

    def _test_crud_views_for_model(self, model, instance, url_prefix, create_data):
        """
        For a given model and instance, test:
         - GET list, GET detail
         - POST create → redirect to list, object created
         - POST update → redirect to list, object updated
         - POST delete → redirect to list, object deleted
        `create_data` is a dict of the minimal fields needed to create a fresh instance.
        """
        # List view
        list_url = reverse(f"app_tracker:{url_prefix}_list")
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(instance, resp.context["object_list"])

        # Detail view
        detail_url = reverse(
            f"app_tracker:{url_prefix}_detail", kwargs={"pk": instance.pk}
        )
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["object"], instance)

        # Create view (POST)
        create_url = reverse(f"app_tracker:{url_prefix}_create")
        resp = self.client.post(create_url, create_data)
        self.assertRedirects(resp, list_url)

        # Verify new object exists
        for field, value in create_data.items():
            self.assertTrue(model.objects.filter(**{field: value}).exists())

        # Update view (POST)
        update_url = reverse(
            f"app_tracker:{url_prefix}_update", kwargs={"pk": instance.pk}
        )
        modified_data = create_data.copy()
        first_field = list(modified_data.keys())[0]
        original_value = getattr(instance, first_field)
        if isinstance(original_value, str):
            modified_data[first_field] = original_value + "_upd"
        else:
            # For ForeignKey fields (e.g. 'application', 'operating_system'), reuse existing PK
            modified_data[first_field] = getattr(instance, first_field).pk

        resp = self.client.post(update_url, modified_data)
        self.assertRedirects(resp, list_url)
        instance.refresh_from_db()
        if isinstance(getattr(instance, first_field), str):
            self.assertTrue(getattr(instance, first_field).endswith("_upd"))

        # Delete view (POST)
        delete_url = reverse(
            f"app_tracker:{url_prefix}_delete", kwargs={"pk": instance.pk}
        )
        resp = self.client.post(delete_url)
        self.assertRedirects(resp, list_url)
        self.assertFalse(model.objects.filter(pk=instance.pk).exists())

    def test_application_crud(self):
        self._test_crud_views_for_model(
            Application, self.app_obj, "application", {"name": "CreatedApp"}
        )

    def test_label_crud(self):
        self._test_crud_views_for_model(
            Label, self.label_obj, "label", {"name": "CreatedLabel"}
        )

    def test_lfs_crud(self):
        self._test_crud_views_for_model(
            LanguageFrameworkSystem, self.lfs_obj, "lfs", {"name": "CreatedLFS"}
        )

    def test_note_crud(self):
        new_app = Application.objects.create(name="ForNote")
        self._test_crud_views_for_model(
            Note,
            self.note_obj,
            "note",
            {"title": "CreatedNote", "content": "C", "application": new_app.pk},
        )

    def test_operating_system_crud(self):
        self._test_crud_views_for_model(
            OperatingSystem, self.os_obj, "os", {"name": "CreatedOS"}
        )

    def test_organizational_concept_crud(self):
        self._test_crud_views_for_model(
            OrganizationalConcept,
            self.oc_obj,
            "oc",
            {"name": "CreatedOC", "description": "Desc"},
        )

    def test_project_crud(self):
        self._test_crud_views_for_model(
            Project,
            self.project_obj,
            "project",
            {"name": "CreatedProj", "description": "Desc"},
        )

    def test_server_crud(self):
        self._test_crud_views_for_model(
            Server,
            self.server_obj,
            "server",
            {
                "host_name": "CreatedServer",
                "ip_address": "192.168.0.50",
                "environment": "development",
                "operating_system": self.os_obj.pk,
            },
        )


class URLTests(TestCase):
    def test_reverse_list_and_create_urls(self):
        self.assertEqual(reverse("app_tracker:home"), "/")
        self.assertEqual(reverse("app_tracker:application_list"), "/applications/")
        self.assertEqual(
            reverse("app_tracker:application_create"), "/applications/create/"
        )
        self.assertEqual(reverse("app_tracker:label_list"), "/labels/")
        self.assertEqual(reverse("app_tracker:label_create"), "/labels/create/")
        self.assertEqual(reverse("app_tracker:lfs_list"), "/lfss/")
        self.assertEqual(reverse("app_tracker:lfs_create"), "/lfss/create/")
        self.assertEqual(reverse("app_tracker:note_list"), "/notes/")
        self.assertEqual(reverse("app_tracker:note_create"), "/notes/create/")
        self.assertEqual(reverse("app_tracker:os_list"), "/oses/")
        self.assertEqual(reverse("app_tracker:os_create"), "/oses/create/")
        self.assertEqual(reverse("app_tracker:oc_list"), "/oces/")
        self.assertEqual(reverse("app_tracker:oc_create"), "/oces/create/")
        self.assertEqual(reverse("app_tracker:project_list"), "/projects/")
        self.assertEqual(reverse("app_tracker:project_create"), "/projects/create/")
        self.assertEqual(reverse("app_tracker:server_list"), "/servers/")
        self.assertEqual(reverse("app_tracker:server_create"), "/servers/create/")

    def test_reverse_detail_update_delete_urls(self):
        pk = 42
        self.assertEqual(
            reverse("app_tracker:application_detail", kwargs={"pk": pk}),
            f"/applications/{pk}/",
        )
        self.assertEqual(
            reverse("app_tracker:application_update", kwargs={"pk": pk}),
            f"/applications/{pk}/update/",
        )
        self.assertEqual(
            reverse("app_tracker:application_delete", kwargs={"pk": pk}),
            f"/applications/{pk}/delete/",
        )

        self.assertEqual(
            reverse("app_tracker:label_detail", kwargs={"pk": pk}), f"/labels/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:label_update", kwargs={"pk": pk}),
            f"/labels/{pk}/update/",
        )
        self.assertEqual(
            reverse("app_tracker:label_delete", kwargs={"pk": pk}),
            f"/labels/{pk}/delete/",
        )

        self.assertEqual(
            reverse("app_tracker:lfs_detail", kwargs={"pk": pk}), f"/lfss/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:lfs_update", kwargs={"pk": pk}), f"/lfss/{pk}/update/"
        )
        self.assertEqual(
            reverse("app_tracker:lfs_delete", kwargs={"pk": pk}), f"/lfss/{pk}/delete/"
        )

        self.assertEqual(
            reverse("app_tracker:note_detail", kwargs={"pk": pk}), f"/notes/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:note_update", kwargs={"pk": pk}),
            f"/notes/{pk}/update/",
        )
        self.assertEqual(
            reverse("app_tracker:note_delete", kwargs={"pk": pk}),
            f"/notes/{pk}/delete/",
        )

        self.assertEqual(
            reverse("app_tracker:os_detail", kwargs={"pk": pk}), f"/oses/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:os_update", kwargs={"pk": pk}), f"/oses/{pk}/update/"
        )
        self.assertEqual(
            reverse("app_tracker:os_delete", kwargs={"pk": pk}), f"/oses/{pk}/delete/"
        )

        self.assertEqual(
            reverse("app_tracker:oc_detail", kwargs={"pk": pk}), f"/oces/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:oc_update", kwargs={"pk": pk}), f"/oces/{pk}/update/"
        )
        self.assertEqual(
            reverse("app_tracker:oc_delete", kwargs={"pk": pk}), f"/oces/{pk}/delete/"
        )

        self.assertEqual(
            reverse("app_tracker:project_detail", kwargs={"pk": pk}), f"/projects/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:project_update", kwargs={"pk": pk}),
            f"/projects/{pk}/update/",
        )
        self.assertEqual(
            reverse("app_tracker:project_delete", kwargs={"pk": pk}),
            f"/projects/{pk}/delete/",
        )

        self.assertEqual(
            reverse("app_tracker:server_detail", kwargs={"pk": pk}), f"/servers/{pk}/"
        )
        self.assertEqual(
            reverse("app_tracker:server_update", kwargs={"pk": pk}),
            f"/servers/{pk}/update/",
        )
        self.assertEqual(
            reverse("app_tracker:server_delete", kwargs={"pk": pk}),
            f"/servers/{pk}/delete/",
        )
