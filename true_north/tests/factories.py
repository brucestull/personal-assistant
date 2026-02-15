# true_north/tests/factories.py

from __future__ import annotations

import factory

from accounts.models import CustomUser
from true_north.models import CoreValue, Goal, Milestone, ValueAction, GoalStatus, ValueActionStatus


class CustomUserFactory(factory.django.DjangoModelFactory):
    """
    Explicitly saves password in a post_generation hook so we don't depend on
    Factory Boy's changing default behavior.
    """

    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"tiny_user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """
        Usage:
          - CustomUserFactory() -> default password "password123"
          - CustomUserFactory(password="my-pass") -> sets given password
        """
        raw = extracted or "password123"
        self.set_password(raw)
        if create:
            self.save(update_fields=["password"])


class CoreValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CoreValue
        skip_postgeneration_save = True

    user = factory.SubFactory(CustomUserFactory)
    name = factory.Sequence(lambda n: f"Integrity_{n}")
    slug = ""  # force model to auto-generate unless overridden
    definition = "I do what I say I will do."
    is_active = True
    order = factory.Sequence(lambda n: n)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
        skip_postgeneration_save = True

    value = factory.SubFactory(CoreValueFactory)
    user = None  # let model sync from value unless overridden

    title = factory.Sequence(lambda n: f"Build grit habit_{n}")
    slug = ""  # force auto
    description = "Do small hard things daily."
    status = GoalStatus.ACTIVE
    is_active = True
    order = factory.Sequence(lambda n: n)


class MilestoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Milestone
        skip_postgeneration_save = True

    goal = factory.SubFactory(GoalFactory)
    user = None  # let model sync from goal unless overridden

    description = factory.Sequence(lambda n: f"Week {n} checkpoint")
    slug = ""  # force auto
    notes = "Notes go here."
    due_date = None
    is_completed = False
    completed_at = None
    order = factory.Sequence(lambda n: n)


class ValueActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ValueAction
        skip_postgeneration_save = True

    milestone = factory.SubFactory(MilestoneFactory)
    user = None  # let model sync from milestone in ValueAction.save()

    content = factory.Sequence(lambda n: f"ValueAction content line {n}")
    status = ValueActionStatus.TODO
    due_date = None
    is_completed = False
    completed_at = None
    order = factory.Sequence(lambda n: n)
