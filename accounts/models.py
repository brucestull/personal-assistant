# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    A `CustomUser` so we can add our own functionality for site users.
    """

    registration_accepted = models.BooleanField(
        default=False,
        help_text=("Designates whether this user's registration has been accepted."),
    )
    beastie = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username
