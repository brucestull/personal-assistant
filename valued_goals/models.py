from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class TimestampBase(models.Model):
    """
    An abstract base class model that provides timestamp fields for created and updated.
    """

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        # This model will be an abstract base class model, which means that it will not be used to create any database tables.
        abstract = True


class ValuedGoal(TimestampBase):
    """
    A model that represents a valued goal, which is a goal that is aligned with one or more core values.
    """

    name = models.CharField(
        max_length=200,
    )
    # The description is a brief explanation of the valued goal.
    description = models.TextField(
        blank=True,
        null=True,
    )
    # The user is the person who created the valued goal.
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """
        String for representing the ValuedGoal object.
        """
        return self.name

class CoreValue(TimestampBase):
    """
    A model that represents a core value, which is a fundamental belief or principle that guides behavior and decision-making.
    """

    name = models.CharField(
        max_length=200,
    )
    # The description is a brief explanation of the core value.
    description = models.TextField(
        blank=True,
        null=True,
    )
    # The user is the person who created the core value.
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """
        String for representing the CoreValue object.
        """
        return self.name
