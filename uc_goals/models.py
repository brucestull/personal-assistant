from django.db import models

from config.settings import AUTH_USER_MODEL


class Goal(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uc_goals",
        help_text="The user that set the goal.",
    )
    name = models.CharField(max_length=255)
    is_ultimate_concern = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_goals",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
