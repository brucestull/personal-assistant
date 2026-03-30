# true_north/tests/test_tasks.py

from __future__ import annotations

from unittest.mock import patch

import pytest

from true_north.tests.factories import (
    CoreValueFactory,
    CustomUserFactory,
    GoalFactory,
    MilestoneFactory,
    ValueActionFactory,
)

pytestmark = pytest.mark.django_db


class TestSendCoreValueEmail:
    """Tests for true_north.tasks.send_core_value_email."""

    def test_returns_ok_and_sends_email(self):
        from true_north.tasks import send_core_value_email

        user = CustomUserFactory(email="test@example.com")
        core_value = CoreValueFactory(user=user, name="Integrity", definition="Be honest.")  # noqa: E501

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


class TestSendGoalEmail:
    """Tests for true_north.tasks.send_goal_email."""

    def test_returns_ok_and_sends_email(self):
        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="test@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user), title="Learn Python")

        with patch("true_north.tasks._send_email") as mock_send:
            result = send_goal_email(user.id, goal.id)

        assert result["ok"] is True
        assert result["goal_id"] == goal.id
        assert result["user_id"] == user.id
        mock_send.assert_called_once()
        subject, body, recipients = (
            mock_send.call_args[0][0],
            mock_send.call_args[0][1],
            mock_send.call_args[0][2],
        )
        assert "Learn Python" in subject
        assert "Learn Python" in body
        assert recipients == [user.email]

    def test_returns_error_when_user_not_found(self):
        from true_north.tasks import send_goal_email

        result = send_goal_email(99999, 1)

        assert result["ok"] is False
        assert result["reason"] == "user_not_found"

    def test_returns_error_when_user_has_no_email(self):
        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="")
        goal = GoalFactory(value=CoreValueFactory(user=user))

        result = send_goal_email(user.id, goal.id)

        assert result["ok"] is False
        assert result["reason"] == "no_user_email"

    def test_returns_error_when_goal_not_found_for_user(self):
        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="owner@example.com")
        other_user = CustomUserFactory(email="other@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=other_user))

        result = send_goal_email(user.id, goal.id)

        assert result["ok"] is False
        assert result["reason"] == "goal_not_found_for_user"

    def test_returns_error_when_goal_id_does_not_exist(self):
        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="owner@example.com")

        result = send_goal_email(user.id, 99999)

        assert result["ok"] is False
        assert result["reason"] == "goal_not_found_for_user"

    def test_email_body_contains_greeting(self):
        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="greet@example.com", username="greetuser")
        goal = GoalFactory(value=CoreValueFactory(user=user))

        with patch("true_north.tasks._send_email") as mock_send:
            send_goal_email(user.id, goal.id)

        body = mock_send.call_args[0][1]
        assert f"Hey {user.username}" in body

    def test_smtp_exception_is_reraised(self):
        import smtplib

        from true_north.tasks import send_goal_email

        user = CustomUserFactory(email="smtp@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user))

        with patch(
            "true_north.tasks._send_email",
            side_effect=smtplib.SMTPException("connection failed"),
        ):
            with pytest.raises(smtplib.SMTPException):
                send_goal_email(user.id, goal.id)


class TestSendMilestoneEmail:
    """Tests for true_north.tasks.send_milestone_email."""

    def test_returns_ok_and_sends_email(self):
        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="test@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal, description="First checkpoint")

        with patch("true_north.tasks._send_email") as mock_send:
            result = send_milestone_email(user.id, milestone.id)

        assert result["ok"] is True
        assert result["milestone_id"] == milestone.id
        assert result["user_id"] == user.id
        mock_send.assert_called_once()
        subject, body, recipients = (
            mock_send.call_args[0][0],
            mock_send.call_args[0][1],
            mock_send.call_args[0][2],
        )
        assert "First checkpoint" in subject
        assert "First checkpoint" in body
        assert recipients == [user.email]

    def test_returns_error_when_user_not_found(self):
        from true_north.tasks import send_milestone_email

        result = send_milestone_email(99999, 1)

        assert result["ok"] is False
        assert result["reason"] == "user_not_found"

    def test_returns_error_when_user_has_no_email(self):
        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)

        result = send_milestone_email(user.id, milestone.id)

        assert result["ok"] is False
        assert result["reason"] == "no_user_email"

    def test_returns_error_when_milestone_not_found_for_user(self):
        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="owner@example.com")
        other_user = CustomUserFactory(email="other@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=other_user))
        milestone = MilestoneFactory(goal=goal)

        result = send_milestone_email(user.id, milestone.id)

        assert result["ok"] is False
        assert result["reason"] == "milestone_not_found_for_user"

    def test_returns_error_when_milestone_id_does_not_exist(self):
        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="owner@example.com")

        result = send_milestone_email(user.id, 99999)

        assert result["ok"] is False
        assert result["reason"] == "milestone_not_found_for_user"

    def test_email_body_contains_greeting(self):
        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="greet@example.com", username="greetuser")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)

        with patch("true_north.tasks._send_email") as mock_send:
            send_milestone_email(user.id, milestone.id)

        body = mock_send.call_args[0][1]
        assert f"Hey {user.username}" in body

    def test_smtp_exception_is_reraised(self):
        import smtplib

        from true_north.tasks import send_milestone_email

        user = CustomUserFactory(email="smtp@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)

        with patch(
            "true_north.tasks._send_email",
            side_effect=smtplib.SMTPException("connection failed"),
        ):
            with pytest.raises(smtplib.SMTPException):
                send_milestone_email(user.id, milestone.id)


class TestSendValueActionEmail:
    """Tests for true_north.tasks.send_value_action_email."""

    def test_returns_ok_and_sends_email(self):
        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="test@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)
        value_action = ValueActionFactory(
            milestone=milestone, content="Practice daily meditation"
        )

        with patch("true_north.tasks._send_email") as mock_send:
            result = send_value_action_email(user.id, value_action.id)

        assert result["ok"] is True
        assert result["value_action_id"] == value_action.id
        assert result["user_id"] == user.id
        mock_send.assert_called_once()
        subject, body, recipients = (
            mock_send.call_args[0][0],
            mock_send.call_args[0][1],
            mock_send.call_args[0][2],
        )
        assert "Practice daily meditation" in subject
        assert "Practice daily meditation" in body
        assert recipients == [user.email]

    def test_returns_error_when_user_not_found(self):
        from true_north.tasks import send_value_action_email

        result = send_value_action_email(99999, 1)

        assert result["ok"] is False
        assert result["reason"] == "user_not_found"

    def test_returns_error_when_user_has_no_email(self):
        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)
        value_action = ValueActionFactory(milestone=milestone)

        result = send_value_action_email(user.id, value_action.id)

        assert result["ok"] is False
        assert result["reason"] == "no_user_email"

    def test_returns_error_when_value_action_not_found_for_user(self):
        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="owner@example.com")
        other_user = CustomUserFactory(email="other@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=other_user))
        milestone = MilestoneFactory(goal=goal)
        value_action = ValueActionFactory(milestone=milestone)

        result = send_value_action_email(user.id, value_action.id)

        assert result["ok"] is False
        assert result["reason"] == "value_action_not_found_for_user"

    def test_returns_error_when_value_action_id_does_not_exist(self):
        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="owner@example.com")

        result = send_value_action_email(user.id, 99999)

        assert result["ok"] is False
        assert result["reason"] == "value_action_not_found_for_user"

    def test_email_body_contains_greeting(self):
        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="greet@example.com", username="greetuser")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)
        value_action = ValueActionFactory(milestone=milestone)

        with patch("true_north.tasks._send_email") as mock_send:
            send_value_action_email(user.id, value_action.id)

        body = mock_send.call_args[0][1]
        assert f"Hey {user.username}" in body

    def test_smtp_exception_is_reraised(self):
        import smtplib

        from true_north.tasks import send_value_action_email

        user = CustomUserFactory(email="smtp@example.com")
        goal = GoalFactory(value=CoreValueFactory(user=user))
        milestone = MilestoneFactory(goal=goal)
        value_action = ValueActionFactory(milestone=milestone)

        with patch(
            "true_north.tasks._send_email",
            side_effect=smtplib.SMTPException("connection failed"),
        ):
            with pytest.raises(smtplib.SMTPException):
                send_value_action_email(user.id, value_action.id)
