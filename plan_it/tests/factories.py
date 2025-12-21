# plan_it/tests/factories.py

from datetime import date
import factory
from django.contrib.auth import get_user_model

from plan_it.models import (
    StorageLocation,
    ActivityLocation,
    Item,
    ActivityType,
    Activity,
)

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # avoids the FactoryBoy deprecation warning

    username = factory.Sequence(lambda n: f"user{n}")
    registration_accepted = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw_password = extracted or "testpass"
        self.set_password(raw_password)
        if create:
            self.save(update_fields=["password", "registration_accepted"])


class StorageLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StorageLocation

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Storage Location {n}")


class ActivityLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActivityLocation

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Activity Location {n}")


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Item {n}")
    storage_location = factory.SubFactory(
        StorageLocationFactory,
        user=factory.SelfAttribute("..user"),
    )


class ActivityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActivityType

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"ActivityType {n}")


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Activity {n}")

    type = factory.SubFactory(
        ActivityTypeFactory,
        user=factory.SelfAttribute("..user"),
    )
    target_item = factory.SubFactory(
        ItemFactory,
        user=factory.SelfAttribute("..user"),
    )
    activity_location = factory.SubFactory(
        ActivityLocationFactory,
        user=factory.SelfAttribute("..user"),
    )
    due_date = factory.LazyFunction(date.today)
