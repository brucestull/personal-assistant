# thoughts/tests/test_models.py

import pytest

from thoughts.models import Thought
from thoughts.tests.factories import CustomUserFactory, ThoughtFactory

pytestmark = pytest.mark.django_db


def test_thought_str_truncates_at_50_chars():
    long_text = "A" * 60
    thought = ThoughtFactory(text=long_text)
    assert str(thought) == "A" * 50


def test_thought_str_short_text():
    thought = ThoughtFactory(text="Hello world")
    assert str(thought) == "Hello world"


def test_thought_belongs_to_user():
    user = CustomUserFactory()
    thought = ThoughtFactory(user=user)
    assert thought.user == user


def test_thought_ordering_newest_first():
    user = CustomUserFactory()
    t1 = ThoughtFactory(user=user)
    t2 = ThoughtFactory(user=user)
    thoughts = list(Thought.objects.filter(user=user))
    assert thoughts[0] == t2
    assert thoughts[1] == t1


def test_thought_has_created_and_updated_timestamps():
    thought = ThoughtFactory()
    assert thought.created is not None
    assert thought.updated is not None


def test_thought_user_cascade_delete():
    user = CustomUserFactory()
    ThoughtFactory(user=user)
    user_pk = user.pk
    assert Thought.objects.filter(user_id=user_pk).count() == 1
    user.delete()
    assert Thought.objects.filter(user_id=user_pk).count() == 0
