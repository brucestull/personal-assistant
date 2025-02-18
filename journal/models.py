from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        help_text="The author of this entry.",
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("journal:entry_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.id} : {self.author.username} - {self.title}"

    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
