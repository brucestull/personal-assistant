from django.db import models
from django.contrib.auth import get_user_model


class Strength(models.Model):
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='strengths',
    )

    def __str__(self):
        return f"{self.owner.username}: {self.description}"


class Gratitude(models.Model):
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='gratitudes',
    )

    def __str__(self):
        return f"{self.owner.username}: {self.description}"


class LovedOne(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='loved_ones',
    )

    def __str__(self):
        return f"{self.owner.username}: {self.name}"
