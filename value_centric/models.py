from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class PersonalValue(models.Model):
    name = models.CharField(
        verbose_name="Identifier for the Personal Value", max_length=100
    )
    description = models.TextField(verbose_name="Description of the Personal Value")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Value: {self.name}"

    def get_absolute_url(self):
        return reverse("value_centric:personal-value-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Personal Value"
        verbose_name_plural = "Personal Values"
