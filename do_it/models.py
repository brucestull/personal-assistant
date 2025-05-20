# do_it/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone  # noqa: F401

# This is useful since we have a custom user model `accounts.models.CustomUser`.
# We don't wantt to hardcode the user model from `cofnfig/settings.py`.
# This is the recommended way to get the user model in Django.
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="do_it_tags")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Cycle(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="do_it_cycles"
    )
    periodicity = models.CharField(
        max_length=50, help_text="e.g. 'daily', 'weekly', 'monthly'"
    )

    def __str__(self):
        return f"{self.name} [{self.periodicity}]"


class Task(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="do_it_tasks")
    description = models.TextField(blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    cycle = models.ForeignKey(
        Cycle, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    is_recurrent = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def schedule_next(self):
        """
        Stub for computing the next scheduled date based on self.cycle.periodicity.
        e.g. if periodicity == 'daily', return today + 1 day, etc.
        """
        # TODO: implement based on cycle.periodicity
        return None


# class TaskCompleted(models.Model):
#     pass


#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="do_it_completions"
#     )
#     task_repr = models.CharField(max_length=255)
#     date_scheduled = models.DateTimeField()
#     date_completed = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.task_repr} @ {self.date_completed:%Y-%m-%d}"
