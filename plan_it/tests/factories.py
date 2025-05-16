import factory
from django.contrib.auth import get_user_model
from plan_it.models import StorageLocation, Item, ActivityType, Activity
from datetime import date


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass")


class StorageLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StorageLocation

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Location {n}")


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Item {n}")
    storage_location = factory.SubFactory(StorageLocationFactory)


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
    type = factory.SubFactory(ActivityTypeFactory)
    due_date = factory.LazyFunction(date.today)
