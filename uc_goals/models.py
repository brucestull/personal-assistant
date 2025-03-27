from django.db import models
from django.urls import reverse

from config.settings import AUTH_USER_MODEL


class Goal(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uc_goals",
        help_text="The user that set the goal.",
    )
    is_ultimate_concern = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_goals",
    )
    description = models.TextField(blank=True, null=True)
    character_strengths = models.ManyToManyField(
        "VIACharacterStrength",
        blank=True,
        related_name="goals",
        help_text="Select character strengths associated with this goal.",
    )
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def get_absolute_url(self):
        """
        Provides the URL to access a detail record for this goal. This is used in
        CreateView and UpdateView.
        """
        return reverse("uc_goals:goal_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"


class Virtue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class VIACharacterStrength(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    virtue = models.ForeignKey(
        Virtue, on_delete=models.CASCADE, related_name="character_strengths"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "VIA Character Strength"
        verbose_name_plural = "VIA Character Strengths"
