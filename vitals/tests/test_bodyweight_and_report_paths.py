from datetime import timedelta

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from vitals.models import BodyWeight, BloodPressure
from vitals.views import BloodPressureReportView


class BodyWeightViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="bw-user",
            password="pw",
            email="u@example.com",
            registration_accepted=True,
        )
        self.staff = CustomUser.objects.create_user(
            username="bw-staff",
            password="pw",
            email="s@example.com",
            registration_accepted=True,
            is_staff=True,
        )
        self.other = CustomUser.objects.create_user(
            username="bw-other",
            password="pw",
            email="o@example.com",
            registration_accepted=True,
        )
        self.mine = BodyWeight.objects.create(subject=self.user, measurement="180.50")
        self.other_weight = BodyWeight.objects.create(
            subject=self.other, measurement="160.00"
        )

    def test_bodyweight_list_filters_non_staff_and_searches(self):
        self.client.login(username="bw-user", password="pw")
        response = self.client.get(reverse("vitals:bodyweight_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["page_obj"].object_list), [self.mine])

        search = self.client.get(reverse("vitals:bodyweight_list") + "?q=180")
        self.assertEqual(list(search.context["page_obj"].object_list), [self.mine])

        self.client.login(username="bw-staff", password="pw")
        staff_response = self.client.get(reverse("vitals:bodyweight_list"))
        self.assertEqual(staff_response.status_code, 200)
        self.assertEqual(staff_response.context["page_obj"].paginator.count, 2)

    def test_bodyweight_detail_permissions(self):
        self.client.login(username="bw-user", password="pw")
        mine_response = self.client.get(
            reverse("vitals:bodyweight_detail", kwargs={"pk": self.mine.pk})
        )
        self.assertEqual(mine_response.status_code, 200)

        forbidden = self.client.get(
            reverse("vitals:bodyweight_detail", kwargs={"pk": self.other_weight.pk})
        )
        self.assertEqual(forbidden.status_code, 404)

        self.client.login(username="bw-staff", password="pw")
        staff_response = self.client.get(
            reverse("vitals:bodyweight_detail", kwargs={"pk": self.other_weight.pk})
        )
        self.assertEqual(staff_response.status_code, 200)

    def test_bodyweight_create_forces_subject_for_non_staff(self):
        self.client.login(username="bw-user", password="pw")
        get_response = self.client.get(reverse("vitals:bodyweight_create"))
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(get_response.context["force_subject"])

        post_response = self.client.post(
            reverse("vitals:bodyweight_create"),
            {"subject": self.other.pk, "measurement": "170.25"},
            follow=True,
        )
        created = BodyWeight.objects.exclude(pk=self.mine.pk).exclude(
            pk=self.other_weight.pk
        ).get()
        self.assertEqual(created.subject, self.user)
        self.assertRedirects(
            post_response,
            reverse("vitals:bodyweight_detail", kwargs={"pk": created.pk}),
        )

    def test_bodyweight_update_and_delete_enforce_permissions(self):
        self.client.login(username="bw-user", password="pw")
        forbidden_update = self.client.get(
            reverse("vitals:bodyweight_update", kwargs={"pk": self.other_weight.pk})
        )
        self.assertEqual(forbidden_update.status_code, 404)

        update_response = self.client.post(
            reverse("vitals:bodyweight_update", kwargs={"pk": self.mine.pk}),
            {"subject": self.other.pk, "measurement": "181.00"},
            follow=True,
        )
        self.mine.refresh_from_db()
        self.assertEqual(str(self.mine.measurement), "181.00")
        self.assertEqual(self.mine.subject, self.user)
        self.assertRedirects(
            update_response,
            reverse("vitals:bodyweight_detail", kwargs={"pk": self.mine.pk}),
        )

        get_delete = self.client.get(
            reverse("vitals:bodyweight_delete", kwargs={"pk": self.mine.pk})
        )
        self.assertEqual(get_delete.status_code, 200)
        delete_response = self.client.post(
            reverse("vitals:bodyweight_delete", kwargs={"pk": self.mine.pk}),
            follow=True,
        )
        self.assertFalse(BodyWeight.objects.filter(pk=self.mine.pk).exists())
        self.assertRedirects(delete_response, reverse("vitals:bodyweight_list"))


class BloodPressureExtraPathTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="bp-user", password="pw", registration_accepted=True
        )
        self.client.login(username="bp-user", password="pw")

    def test_create_view_sets_user_and_list_per_page_fallbacks(self):
        create_response = self.client.post(
            reverse("vitals:bloodpressure-create"),
            {"systolic": 120, "diastolic": 80, "pulse": 70, "note": "note"},
            follow=True,
        )
        created = BloodPressure.objects.get()
        self.assertEqual(created.user, self.user)
        self.assertRedirects(create_response, reverse("vitals:bloodpressure-list"))

        invalid_per_page = self.client.get(
            reverse("vitals:bloodpressure-list") + "?per_page=bogus"
        )
        self.assertEqual(invalid_per_page.status_code, 200)
        self.assertEqual(invalid_per_page.context["current_per_page"], 10)

    def test_report_view_month_and_custom_windows(self):
        now = timezone.now()
        recent = BloodPressure.objects.create(
            user=self.user, systolic=121, diastolic=79, pulse=72
        )
        old = BloodPressure.objects.create(user=self.user, systolic=110, diastolic=70, pulse=65)
        old.created = now - timedelta(days=40)
        old.save(update_fields=["created"])

        month = self.client.get(
            reverse("vitals:bloodpressure-report")
            + f"?period=month&month={timezone.localdate():%Y-%m}"
        )
        self.assertEqual(month.status_code, 200)
        self.assertEqual(month.context["period_choice"], "month")

        # Intentionally pass start > end so the view exercises its swap branch.
        custom = self.client.get(
            reverse("vitals:bloodpressure-report")
            + f"?period=custom&start={timezone.localdate():%Y-%m-%d}"
            + f"&end={(timezone.localdate() - timedelta(days=1)):%Y-%m-%d}"
        )
        self.assertEqual(custom.status_code, 200)
        self.assertEqual(custom.context["period_choice"], "custom")
        self.assertEqual(
            custom.context["period_start"], timezone.localdate() - timedelta(days=1)
        )
        self.assertEqual(custom.context["period_end"], timezone.localdate())
        self.assertTrue(custom.context["period_start"] <= custom.context["period_end"])
        self.assertEqual(custom.context["bp_summary"]["count"], 1)
        self.assertEqual(custom.context["latest_bp"].pk, recent.pk)

        all_time = self.client.get(reverse("vitals:bloodpressure-report") + "?period=all")
        self.assertEqual(all_time.status_code, 200)
        self.assertEqual(all_time.context["period_choice"], "all")
        self.assertEqual(all_time.context["bp_summary"]["count"], 2)


class ReportParserUnitTests(TestCase):
    def test_week_and_month_parsers_handle_bad_values(self):
        view = BloodPressureReportView()
        self.assertEqual(view._parse_week_value(""), (None, None))
        self.assertEqual(view._parse_week_value("bad"), (None, None))
        self.assertEqual(view._parse_month_value(""), (None, None))
        self.assertEqual(view._parse_month_value("bad"), (None, None))

    def test_compute_window_custom_single_date(self):
        class Form:
            cleaned_data = {"period": "custom", "start": timezone.localdate(), "end": None}

        view = BloodPressureReportView()
        start, end, label, period = view._compute_window(Form())
        self.assertEqual(start, end)
        self.assertIn(str(start.year), label)
        self.assertEqual(period, "custom")

    def test_compute_window_defaults_for_invalid_month(self):
        class Form:
            cleaned_data = {"period": "month", "month": "bogus"}

        view = BloodPressureReportView()
        start, end, label, period = view._compute_window(Form())
        self.assertIsNotNone(start)
        self.assertIsNotNone(end)
        self.assertEqual(period, "month")
        self.assertIn(start.strftime("%B"), label)
