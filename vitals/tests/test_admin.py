from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.urls import reverse

from vitals.admin import VitalsAdmin, PulseAdmin
from vitals.models import BloodPressure, Pulse
from accounts.models import CustomUser


class VitalsAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.blood_pressure = BloodPressure.objects.create(
            user=self.user,
            systolic=120,
            diastolic=80,
        )
        self.admin = VitalsAdmin(BloodPressure, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("user", "systolic", "diastolic", "created"),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            ("user", "created"),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("user__username", "systolic", "diastolic"),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("created", "updated"),
        )

    def test_fieldsets(self):
        self.assertEqual(
            self.admin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": ("user", "systolic", "diastolic"),
                    },
                ),
                (
                    "Dates/Metadata",
                    {
                        "fields": ("created", "updated"),
                    },
                ),
            ),
        )


class PulseAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.pulse = Pulse.objects.create(
            user=self.user,
            bpm=60,
        )
        self.admin = PulseAdmin(Pulse, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("user", "bpm", "created"),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            ("user", "created"),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("user__username", "bpm"),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("created", "updated"),
        )

    def test_fieldsets(self):
        self.assertEqual(
            self.admin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": ("user", "bpm"),
                    },
                ),
                (
                    "Dates",
                    {
                        "fields": ("created", "updated"),
                    },
                ),
            ),
        )