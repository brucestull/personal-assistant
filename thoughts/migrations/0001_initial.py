# thoughts/migrations/0001_initial.py

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Thought",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time this object was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The date and time this object was last updated.",
                        verbose_name="Updated",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Your thought.",
                        verbose_name="Thought",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="The user who created this thought.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="thoughts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Thought",
                "verbose_name_plural": "Thoughts",
                "ordering": ["-created"],
            },
        ),
    ]
