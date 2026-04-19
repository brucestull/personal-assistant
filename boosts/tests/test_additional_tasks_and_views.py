from unittest.mock import patch

from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser
from boosts.models import Inspirational, InspirationalSent, RandomInspirationalEmailSend
from boosts.tasks import (
    _send_email,
    send_inspirational_to_beastie,
    send_inspirational_to_self,
    send_random_inspirational_email,
    send_test_email,
)


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class BoostsAdditionalTaskTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="boost-user",
            password="pw",
            email="boost@example.com",
            registration_accepted=True,
        )
        self.beastie = CustomUser.objects.create_user(
            username="boost-beastie",
            password="pw",
            email="beastie@example.com",
            registration_accepted=True,
        )
        self.user.beastie = self.beastie
        self.user.save(update_fields=["beastie"])
        self.inspirational = Inspirational.objects.create(
            author=self.user, body="Keep going"
        )

    def test_send_email_helper_handles_empty_and_missing_sender(self):
        _send_email("s", "b", [])

        with patch("boosts.tasks.DEFAULT_FROM_EMAIL", None):
            with self.assertRaises(ValueError):
                _send_email("s", "b", ["to@example.com"], from_email=None)

    @patch("boosts.tasks._send_email")
    def test_send_random_inspirational_email_branches(self, mock_send_email):
        missing_user = send_random_inspirational_email.run(user_id=9999)
        self.assertEqual(missing_user["reason"], "user_not_found")

        no_quotes_user = CustomUser.objects.create_user(
            username="no-quotes",
            password="pw",
            email="no@example.com",
            registration_accepted=True,
        )
        no_quotes = send_random_inspirational_email.run(user_id=no_quotes_user.id)
        self.assertEqual(no_quotes["reason"], "no_inspirationals")

        random_send = RandomInspirationalEmailSend.objects.create(user=self.user)
        result = send_random_inspirational_email.run(
            user_id=self.user.id, random_send_id=random_send.id
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["user_id"], self.user.id)
        mock_send_email.assert_called_once()

        random_send.refresh_from_db()
        self.assertEqual(random_send.status, "sent")
        self.assertIsNotNone(random_send.inspirational_sent)

    def test_send_inspirational_to_beastie_requires_sender(self):
        with patch("boosts.tasks.DEFAULT_FROM_EMAIL", None):
            with self.assertRaises(ValueError):
                send_inspirational_to_beastie.run(
                    user_username="u",
                    user_email="",
                    user_beastie_email="b@example.com",
                    user_beastie_username="b",
                    message="m",
                )

    @patch("boosts.tasks._send_email")
    def test_send_inspirational_to_self_paths(self, mock_send_email):
        send_inspirational_to_self.run(user_id=9999)

        send_inspirational_to_self.run(
            user_id=self.user.id, inspirational_id=self.inspirational.id
        )
        mock_send_email.assert_called_once()

        no_email_user = CustomUser.objects.create_user(
            username="no-email", password="pw", email="", registration_accepted=True
        )
        Inspirational.objects.create(author=no_email_user, body="Body")
        send_inspirational_to_self.run(user_id=no_email_user.id)

    @patch("boosts.tasks._send_email")
    def test_send_test_email_paths(self, mock_send_email):
        send_test_email.run()
        self.assertTrue(mock_send_email.called)

        with patch("boosts.tasks.BOOSTS_TEST_EMAIL", None):
            with self.assertRaises(ValueError):
                send_test_email.run()


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
class BoostsAdditionalViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="view-user",
            password="pw",
            email="view@example.com",
            registration_accepted=True,
        )
        self.beastie = CustomUser.objects.create_user(
            username="view-beastie",
            password="pw",
            email="beastie@example.com",
            registration_accepted=True,
        )
        self.bret = CustomUser.objects.create_user(
            username="BretBeastie",
            password="pw",
            email="bret@example.com",
            registration_accepted=True,
        )
        self.user.beastie = self.beastie
        self.user.save(update_fields=["beastie"])
        self.inspirational = Inspirational.objects.create(
            author=self.user, body="Quote body"
        )

    @patch("boosts.views.send_inspirational_to_beastie.delay")
    def test_send_inspirational_success(self, mock_delay):
        self.client.login(username="view-user", password="pw")
        response = self.client.get(
            reverse("boosts:send-inspirational", kwargs={"pk": self.inspirational.pk})
        )
        self.assertRedirects(response, reverse("boosts:inspirational-list"))
        self.assertEqual(InspirationalSent.objects.count(), 1)
        mock_delay.assert_called_once()

    @patch(
        "boosts.views.InspirationalSent.objects.create",
        side_effect=ValidationError("bad"),
    )
    def test_send_inspirational_validation_error(self, _mock_create):
        self.client.login(username="view-user", password="pw")
        response = self.client.get(
            reverse("boosts:send-inspirational", kwargs={"pk": self.inspirational.pk})
        )
        self.assertRedirects(response, reverse("boosts:inspirational-list"))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any("bad" in msg for msg in messages))

    @patch(
        "boosts.views.send_inspirational_to_beastie.delay",
        side_effect=Exception("boom"),
    )
    def test_send_inspirational_generic_error(self, _mock_delay):
        self.client.login(username="view-user", password="pw")
        response = self.client.get(
            reverse("boosts:send-inspirational", kwargs={"pk": self.inspirational.pk})
        )
        self.assertRedirects(response, reverse("boosts:inspirational-list"))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any("An error occurred" in msg for msg in messages))

    def test_landing_view_routes_for_authenticated_and_unauthenticated(self):
        anonymous_response = self.client.get(reverse("boosts:landing"))
        self.assertEqual(anonymous_response.status_code, 200)
        self.assertEqual(anonymous_response.context["name_in_heading"], "BretBeastie")

        self.client.login(username="view-user", password="pw")
        auth_response = self.client.get(reverse("boosts:landing"))
        self.assertEqual(auth_response.status_code, 200)
        self.assertEqual(auth_response.context["name_in_heading"], "view-user")

    @patch("boosts.views.send_random_inspirational_email.delay")
    def test_random_send_crud_views(self, mock_delay):
        self.client.login(username="view-user", password="pw")
        own = RandomInspirationalEmailSend.objects.create(user=self.user)
        other_user = CustomUser.objects.create_user(
            username="other-view",
            password="pw",
            email="other@example.com",
            registration_accepted=True,
        )
        other = RandomInspirationalEmailSend.objects.create(user=other_user)

        list_response = self.client.get(reverse("boosts:random-send-list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list(list_response.context["object_list"]), [own])

        detail = self.client.get(
            reverse("boosts:random-send-detail", kwargs={"pk": own.pk})
        )
        self.assertEqual(detail.status_code, 200)
        forbidden_detail = self.client.get(
            reverse("boosts:random-send-detail", kwargs={"pk": other.pk})
        )
        self.assertEqual(forbidden_detail.status_code, 404)

        create = self.client.post(reverse("boosts:random-send-create"), {})
        self.assertEqual(create.status_code, 302)
        mock_delay.assert_called_once()

        update = self.client.post(
            reverse("boosts:random-send-update", kwargs={"pk": own.pk}),
            {"status": "failed", "error_message": "err"},
        )
        self.assertEqual(update.status_code, 302)

        forbidden_update = self.client.get(
            reverse("boosts:random-send-update", kwargs={"pk": other.pk})
        )
        self.assertEqual(forbidden_update.status_code, 404)

        delete_get = self.client.get(
            reverse("boosts:random-send-delete", kwargs={"pk": own.pk})
        )
        self.assertEqual(delete_get.status_code, 200)
        delete_post = self.client.post(
            reverse("boosts:random-send-delete", kwargs={"pk": own.pk})
        )
        self.assertEqual(delete_post.status_code, 302)
