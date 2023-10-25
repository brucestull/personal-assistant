from django.contrib import admin
from django.test import RequestFactory, TestCase

from accounts.models import CustomUser
from vitals.admin import PulseAdmin, TemperatureAdmin, VitalsAdmin, BodyWeightAdmin
from vitals.models import BloodPressure, Pulse, Temperature, BodyWeight


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
            pulse=72,
        )
        self.admin = VitalsAdmin(BloodPressure, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("user", "systolic", "diastolic", "pulse", "created"),
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
            ("user__username", "systolic", "diastolic", "pulse"),
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
                        "fields": ("user", "systolic", "diastolic", "pulse"),
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


class TemperatureAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@email.app",
            password="testpassword",
        )
        self.temperature = Temperature.objects.create(
            subject=self.user,
            measurement=98.6,
        )
        self.admin = TemperatureAdmin(Temperature, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("subject", "measurement", "created"),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            ("subject", "created"),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("subject__username", "measurement"),
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
                        "fields": ("subject", "measurement"),
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


class BodyWeightAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = BodyWeightAdmin(BodyWeight, admin.site)

    def test_list_display(self):
        """
        `list_display` should contains the following fields:

        - subject
        - measurement
        - created
        """
        self.assertEqual(
            self.admin.list_display,
            ("subject", "measurement", "created"),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        """
        `list_filter` should contains the following fields:

        - subject
        - created
        """
        self.assertEqual(
            self.admin.list_filter,
            ("subject", "created"),
        )

    def test_search_fields(self):
        """
        `search_fields` should contains the following fields:

        - subject__username
        - measurement
        """
        self.assertEqual(
            self.admin.search_fields,
            ("subject__username", "measurement"),
        )

    def test_readonly_fields(self):
        """
        `readonly_fields` should contains the following fields:

        - created
        - updated
        """
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
                        "fields": ("subject", "measurement"),
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
