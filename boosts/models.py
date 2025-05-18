# boosts/models.py

from django.db import models

from config.settings import AUTH_USER_MODEL


class Inspirational(models.Model):
    body = models.TextField(
        help_text="Required.",
        verbose_name="Inspirational Body Text",
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inspirationals",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.author.username + " : " + str(self.id) + " - " + self.body[:24]


class InspirationalSent(models.Model):
    """
    Model for tracking when an inspirational was sent to a beastie.
    """

    # TODO: Add a field for the inspirational text so we can see what was sent, rather
    # than just the ID. The `Inspirational` model has a `body` field that we can use but
    # can change between the time the `Inspirational` is created and the time it is
    # sent. We should add a field to this model that stores the inspirational text at
    # the time it is sent.
    inspirational = models.ForeignKey(
        Inspirational,
        on_delete=models.CASCADE,
    )
    inspirational_text = models.TextField(
        verbose_name="Inspirational Text Sent to Beastie",
    )
    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inspirationals_sent",
    )
    beastie = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"Inspiration #{self.inspirational.id} sent to Beastie "
            f"#{self.beastie.id} at {self.sent_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    class Meta:
        verbose_name_plural = "Inspirationals Sent"
