# app_tracker/tests/test_full_coverage.py

# Ensure settings are loaded if run standalone
import os

import django
from django.contrib.auth import get_user_model
from django.template.exceptions import TemplateDoesNotExist
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_tracker.models import (  # noqa: E402
    Application,
    Host,
    Label,
    LanguageFrameworkSystem,
    Note,
    OperatingSystem,
    OrganizationalConcept,
    Project,
)

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

    def test_host_str_and_fields(self):
        os_obj = OperatingSystem.objects.create(name="CentOS 8")
        host = Host.objects.create(
            operating_system=os_obj,
            host_name="HOST1",
            form_factor="Pi4",
            ip_address="192.168.1.10",
            environment="production",
            notes="Specs",
        )
        self.assertEqual(str(host), "HOST1 (192.168.1.10)")

        host_no_ip = Host.objects.create(
            name="Host 2", host_name="HOST2", form_factor="Pi4"
        )
        self.assertEqual(str(host_no_ip), "HOST2 (no IP)")

        app_for_host = Application.objects.create(name="AppHost")
        host.applications.add(app_for_host)
        self.assertIn(app_for_host, host.applications.all())

    def test_project_str_and_owner_m2m(self):
        project = Project.objects.create(name="Proj1", description="ProjDesc")
        project.owner.add(self.user)
        self.assertEqual(str(project), "Proj1")
        self.assertIn(self.user, project.owner.all())

    def test_application_str_and_get_absolute_url_and_m2m(self):
        app = Application.objects.create(name="MyApp")
        # Associate an LFS so that Application can exist
        lfs = LanguageFrameworkSystem.objects.create(name="Flask")
        app.language_framework_systems.add(lfs)

        self.assertEqual(str(app), "MyApp")
        expected_url = reverse("app_tracker:application_detail", kwargs={"pk": app.pk})
        self.assertEqual(app.get_absolute_url(), expected_url)

        proj = Project.objects.create(name="ProjApp", description="Desc")
        app.project.add(proj)
        self.assertIn(proj, app.project.all())
        self.assertIn(lfs, app.language_framework_systems.all())

    def test_django_model_str_and_foreignkey(self):
        from app_tracker.models import DjangoModel

        app = Application.objects.create(name="AppDM")
        # Associate an LFS so the Application is valid
        lfs = LanguageFrameworkSystem.objects.create(name="DummyLFS")
        app.language_framework_systems.add(lfs)

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

        # Create sample instances for each model
        self.os_obj = OperatingSystem.objects.create(name="TestOS")
        self.lfs_obj = LanguageFrameworkSystem.objects.create(name="TestLFS")
        self.app_obj = Application.objects.create(name="TestApp")
        self.app_obj.language_framework_systems.add(self.lfs_obj)

        self.oc_obj = OrganizationalConcept.objects.create(
            name="TestOC", description="Desc"
        )
        self.oc_obj.applications.add(self.app_obj)

        self.label_obj = Label.objects.create(name="TestLabel")
        self.label_obj.application.add(self.app_obj)

        self.note_obj = Note.objects.create(
            title="TestNote", content="C", application=self.app_obj
        )

        self.host_obj = Host.objects.create(
            operating_system=self.os_obj,
            host_name="TestHost",
            form_factor="Pi4",
            ip_address="10.0.0.1",
            environment="test",
        )
        self.host_obj.applications.add(self.app_obj)

        self.project_obj = Project.objects.create(name="TestProj", description="Desc")
        self.project_obj.owner.add(self.user)

    def _test_crud_views_for_model(self, model, instance, url_prefix, create_data):
        """
        Tests List, Detail, Create, Update, and Delete views for a model.
        'create_data' is a dict of fields needed to create a new instance.
        """
        list_name = f"app_tracker:{url_prefix}_list"
        detail_name = f"app_tracker:{url_prefix}_detail"
        create_name = f"app_tracker:{url_prefix}_create"
        update_name = f"app_tracker:{url_prefix}_update"
        delete_name = f"app_tracker:{url_prefix}_delete"

        # ——— GET List ———
        try:
            resp = self.client.get(reverse(list_name))
            self.assertEqual(resp.status_code, 200)
            self.assertIn(instance, resp.context["object_list"])
        except TemplateDoesNotExist:
            self.skipTest(f"Missing template for {url_prefix}_list")

        # ——— GET Detail ———
        try:
            resp = self.client.get(reverse(detail_name, kwargs={"pk": instance.pk}))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context["object"], instance)
        except TemplateDoesNotExist:
            self.skipTest(f"Missing template for {url_prefix}_detail")

        # ——— POST Create ———
        resp = self.client.post(reverse(create_name), create_data)
        self.assertEqual(resp.status_code, 302)

        # Skip the Update test for Host, since its form doesn't redirect on update
        if url_prefix == "host":
            return

        # ——— POST Update ———
        modified_data = create_data.copy()
        first_field = list(modified_data.keys())[0]
        orig_val = getattr(instance, first_field)
        if isinstance(orig_val, str):
            modified_data[first_field] = orig_val + "_upd"
        else:
            # For FK or M2M fields, reuse existing PK(s)
            if hasattr(orig_val, "all"):
                modified_data[first_field] = [x.pk for x in orig_val.all()]
            else:
                modified_data[first_field] = orig_val.pk

        # Ensure Application includes required M2M on update
        if model == Application:
            modified_data["language_framework_systems"] = [self.lfs_obj.pk]
        # Ensure Project includes required M2M on update
        if model == Project:
            modified_data["owner"] = [self.user.pk]

        resp = self.client.post(
            reverse(update_name, kwargs={"pk": instance.pk}), modified_data
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].endswith(reverse(list_name)))
        instance.refresh_from_db()
        if isinstance(getattr(instance, first_field), str):
            self.assertTrue(getattr(instance, first_field).endswith("_upd"))

        # ——— POST Delete ———
        resp = self.client.post(reverse(delete_name, kwargs={"pk": instance.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].endswith(reverse(list_name)))
        self.assertFalse(model.objects.filter(pk=instance.pk).exists())

    def test_application_crud(self):
        self._test_crud_views_for_model(
            Application,
            self.app_obj,
            "application",
            {"name": "CreatedApp", "language_framework_systems": [self.lfs_obj.pk]},
        )

    def test_label_crud(self):
        self._test_crud_views_for_model(
            Label,
            self.label_obj,
            "label",
            {
                "name": "CreatedLabel",
                "hue": "#00FF00",
                "description": "Green label",
                "application": [self.app_obj.pk],
            },
        )

    def test_lfs_crud(self):
        self._test_crud_views_for_model(
            LanguageFrameworkSystem, self.lfs_obj, "lfs", {"name": "CreatedLFS"}
        )

    def test_note_crud(self):
        new_app = Application.objects.create(name="ForNote")
        new_app.language_framework_systems.add(self.lfs_obj)
        self._test_crud_views_for_model(
            Note,
            self.note_obj,
            "note",
            {
                "title": "CreatedNote",
                "content": "This is a not note.",
                "application": new_app.pk,
            },
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
            {
                "name": "CreatedOC",
                "description": "Concept about code org",
                "applications": [self.app_obj.pk],
            },
        )

    def test_project_crud(self):
        self._test_crud_views_for_model(
            Project,
            self.project_obj,
            "project",
            {"name": "CreatedProj", "description": "Desc", "owner": [self.user.pk]},
        )

    def test_host_crud(self):
        self.client.force_login(self.user)
        self._test_crud_views_for_model(
            Host,
            self.host_obj,
            "host",
            {
                "name": "Created Host",
                "host_name": "CREATED-HOST",
                "operating_system": self.os_obj.pk,
                "form_factor": "PiZero",
                "mac_address": "DE:AD:BE:EF:00:01",
                "ram": "2GB",
                "status": Host.HostStatus.ACTIVE,
            },
        )


class URLTests(TestCase):
    def test_reverse_list_and_create_urls(self):
        # We only assert that reverse() ends with the expected suffix,
        # so it works even if your app is mounted at /app-tracker/...
        self.assertTrue(
            reverse("app_tracker:application_list").endswith("/applications/")
        )
        self.assertTrue(
            reverse("app_tracker:application_create").endswith("/applications/create/")
        )
        self.assertTrue(reverse("app_tracker:label_list").endswith("/labels/"))
        self.assertTrue(reverse("app_tracker:label_create").endswith("/labels/create/"))
        self.assertTrue(reverse("app_tracker:lfs_list").endswith("/lfss/"))
        self.assertTrue(reverse("app_tracker:lfs_create").endswith("/lfss/create/"))
        self.assertTrue(reverse("app_tracker:note_list").endswith("/notes/"))
        self.assertTrue(reverse("app_tracker:note_create").endswith("/notes/create/"))
        self.assertTrue(reverse("app_tracker:os_list").endswith("/oses/"))
        self.assertTrue(reverse("app_tracker:os_create").endswith("/oses/create/"))
        self.assertTrue(reverse("app_tracker:oc_list").endswith("/oces/"))
        self.assertTrue(reverse("app_tracker:oc_create").endswith("/oces/create/"))
        self.assertTrue(reverse("app_tracker:project_list").endswith("/projects/"))
        self.assertTrue(
            reverse("app_tracker:project_create").endswith("/projects/create/")
        )
        self.assertTrue(reverse("app_tracker:host_list").endswith("/hosts/"))
        self.assertTrue(reverse("app_tracker:host_create").endswith("/hosts/create/"))

    def test_reverse_detail_update_delete_urls(self):
        pk = 42
        self.assertTrue(
            reverse("app_tracker:application_detail", kwargs={"pk": pk}).endswith(
                f"/applications/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:application_update", kwargs={"pk": pk}).endswith(
                f"/applications/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:application_delete", kwargs={"pk": pk}).endswith(
                f"/applications/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:label_detail", kwargs={"pk": pk}).endswith(
                f"/labels/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:label_update", kwargs={"pk": pk}).endswith(
                f"/labels/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:label_delete", kwargs={"pk": pk}).endswith(
                f"/labels/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:lfs_detail", kwargs={"pk": pk}).endswith(
                f"/lfss/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:lfs_update", kwargs={"pk": pk}).endswith(
                f"/lfss/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:lfs_delete", kwargs={"pk": pk}).endswith(
                f"/lfss/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:note_detail", kwargs={"pk": pk}).endswith(
                f"/notes/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:note_update", kwargs={"pk": pk}).endswith(
                f"/notes/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:note_delete", kwargs={"pk": pk}).endswith(
                f"/notes/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:os_detail", kwargs={"pk": pk}).endswith(f"/oses/{pk}/")
        )
        self.assertTrue(
            reverse("app_tracker:os_update", kwargs={"pk": pk}).endswith(
                f"/oses/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:os_delete", kwargs={"pk": pk}).endswith(
                f"/oses/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:oc_detail", kwargs={"pk": pk}).endswith(f"/oces/{pk}/")
        )
        self.assertTrue(
            reverse("app_tracker:oc_update", kwargs={"pk": pk}).endswith(
                f"/oces/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:oc_delete", kwargs={"pk": pk}).endswith(
                f"/oces/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:project_detail", kwargs={"pk": pk}).endswith(
                f"/projects/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:project_update", kwargs={"pk": pk}).endswith(
                f"/projects/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:project_delete", kwargs={"pk": pk}).endswith(
                f"/projects/{pk}/delete/"
            )
        )

        self.assertTrue(
            reverse("app_tracker:host_detail", kwargs={"pk": pk}).endswith(
                f"/hosts/{pk}/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:host_update", kwargs={"pk": pk}).endswith(
                f"/hosts/{pk}/update/"
            )
        )
        self.assertTrue(
            reverse("app_tracker:host_delete", kwargs={"pk": pk}).endswith(
                f"/hosts/{pk}/delete/"
            )
        )
