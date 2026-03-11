# thoughts/tests/factories.py

from __future__ import annotations

import factory

from accounts.models import CustomUser
from thoughts.models import Thought


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"thought_user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    registration_accepted = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw = extracted or "password123"
        self.set_password(raw)
        if create:
            self.save(update_fields=["password"])


class ThoughtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thought
        skip_postgeneration_save = True

    user = factory.SubFactory(CustomUserFactory)
    text = factory.Sequence(lambda n: f"This is thought number {n}")
