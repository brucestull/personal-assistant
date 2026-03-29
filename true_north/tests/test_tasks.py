# true_north/tests/test_tasks.py

from __future__ import annotations

from unittest.mock import patch

import pytest

from true_north.tests.factories import CoreValueFactory, CustomUserFactory

pytestmark = pytest.mark.django_db


class TestSendCoreValueEmail:
    """Tests for true_north.tasks.send_core_value_email."""

    def test_returns_ok_and_sends_email(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="test@example.com")
        core_value = CoreValueFactory(user=user, name="Integrity", definition="Be honest.")

        with patch("true_north.tasks._send_email") as mock_send:
            result = send_core_value_email(user.id, core_value.id)

        assert result["ok"] is True
        assert result["core_value_id"] == core_value.id
        assert result["user_id"] == user.id
        mock_send.assert_called_once()
        subject, body, recipients = (
            mock_send.call_args[0][0],
            mock_send.call_args[0][1],
            mock_send.call_args[0][2],
        )
        assert "Integrity" in subject
        assert "Integrity" in body
        assert "Be honest." in body
        assert recipients == [user.email]

    def test_returns_error_when_user_not_found(self):
        from true_north.tasks import send_core_value_email

        result = send_core_value_email(99999, 1)

        assert result["ok"] is False
        assert result["reason"] == "user_not_found"

    def test_returns_error_when_user_has_no_email(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="")
        core_value = CoreValueFactory(user=user)

        result = send_core_value_email(user.id, core_value.id)

        assert result["ok"] is False
        assert result["reason"] == "no_user_email"

    def test_returns_error_when_core_value_not_found_for_user(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="owner@example.com")
        other_user = CustomUserFactory(email="other@example.com")
        core_value = CoreValueFactory(user=other_user)

        result = send_core_value_email(user.id, core_value.id)

        assert result["ok"] is False
        assert result["reason"] == "core_value_not_found_for_user"

    def test_returns_error_when_core_value_id_does_not_exist(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="owner@example.com")

        result = send_core_value_email(user.id, 99999)

        assert result["ok"] is False
        assert result["reason"] == "core_value_not_found_for_user"

    def test_email_body_contains_greeting(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="greet@example.com", username="greetuser")
        core_value = CoreValueFactory(user=user)

        with patch("true_north.tasks._send_email") as mock_send:
            send_core_value_email(user.id, core_value.id)

        body = mock_send.call_args[0][1]
        assert f"Hey {user.username}" in body

    def test_smtp_exception_is_reraised(self):
        import smtplib

        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="smtp@example.com")
        core_value = CoreValueFactory(user=user)

        with patch(
            "true_north.tasks._send_email",
            side_effect=smtplib.SMTPException("connection failed"),
        ):
            with pytest.raises(smtplib.SMTPException):
                send_core_value_email(user.id, core_value.id)
