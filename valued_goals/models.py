from django.db import models


class TimestampBase(models.Model):
    """
    An abstract base class model that provides timestamp fields for created and updated.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        # This model will be an abstract base class model, which means that it will not be used to create any database tables.
        abstract = True


class ValuedGoal(TimestampBase):
    """
    A model that represents a valued goal, which is a goal that is aligned with one or more core values.
    """
    name = models.CharField(max_length=200)
    # The description is a brief explanation of the valued goal.
    description = models.TextField()
    # The target date is the date by which the valued goal should be completed.
    target_date = models.DateField()
    # The completed field indicates whether the valued goal has been completed.
    completed = models.BooleanField(default=False)
    # The completed date is the date on which the valued goal was completed.
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        String for representing the ValuedGoal object.
        """
        return self.name


class CoreValue(TimestampBase):
    """
    A model that represents a core value, which is a fundamental belief or principle that guides behavior and decision-making.
    """
    name = models.CharField(max_length=200)
    # The description is a brief explanation of the core value.
    description = models.TextField()

    def __str__(self):
        """
        String for representing the CoreValue object.
        """
        return f"{self.name} - {self.description}"
