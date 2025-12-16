# base/models.py

from django.db import models


class CreatedUpdatedBase(models.Model):
    """
    An abstract base class model that provides self-updating `created` and
    `updated` fields.
    """

    created = models.DateTimeField(
        "Created",
        auto_now_add=True,
        help_text="The date and time this object was created.",
    )
    updated = models.DateTimeField(
        "Updated",
        auto_now=True,
        help_text="The date and time this object was last updated.",
    )

    class Meta:
        abstract = True


class Note(CreatedUpdatedBase):
    """
    A note.

    NOTE:
    This is an abstract base class for notes. If a `user` field is needed,
    it should be added in the child class. This class provides common fields
    and methods that can be reused in different note models.
    """

    title = models.CharField(
        "Title",
        max_length=255,
        help_text="The title of this note.",
    )
    content = models.TextField(
        "Content",
        help_text="The content of this note.",
        blank=True,
    )
    url = models.URLField(
        "URL",
        help_text="A reference URL for this note.",
        blank=True,
    )
    main_image = models.ImageField(
        verbose_name="Main Image",
        help_text="Add an image for the note.",
        # `upload_to` is a required argument for `ImageField`.
        # It specifies the path to which the uploaded file will be saved.
        upload_to="test_uploads/",
        blank=True,
        null=True,
    )

    def display_content(self):
        """
        This function returns a truncated version of the note's content.
        This can be used in the admin panel and other places where the full
        content is not needed.
        """
        return self.content[:30] + ("..." if len(self.content) > 30 else "")

    def __str__(self):
        return (
            f"{self.title} - {self.content[:50]}"
            f"{'...' if len(self.content) > 50 else ''}"
        )

    class Meta:
        # Use `abstract = True` to make this model an abstract base class which doesn't
        # have a model table created in the database.
        abstract = True
        # `verbose_name` and `verbose_name_plural` and `ordering` are declared in the
        # child class.


class URL(CreatedUpdatedBase):
    """
    An abstract base class model that provides a URL field with common attributes.

    This can be used as a base for URL-related models in different applications,
    providing a consistent structure for storing and categorizing URLs.

    Attributes:
        url: The actual URL string (required)
        label: A human-readable label/name for the URL
        description: An optional description of what the URL points to
        url_type: The type/category of the URL (e.g., 'documentation', 'api', 'demo')
    """

    URL_TYPE_CHOICES = [
        ("documentation", "Documentation"),
        ("repository", "Repository"),
        ("api", "API"),
        ("demo", "Demo/Preview"),
        ("production", "Production"),
        ("staging", "Staging"),
        ("development", "Development"),
        ("tutorial", "Tutorial"),
        ("reference", "Reference"),
        ("other", "Other"),
    ]

    url = models.URLField(
        verbose_name="URL",
        help_text="The URL address.",
        max_length=2000,
    )
    label = models.CharField(
        verbose_name="Label",
        help_text="A short label or name for this URL.",
        max_length=100,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="An optional description of this URL.",
        blank=True,
        null=True,
    )
    url_type = models.CharField(
        verbose_name="URL Type",
        help_text="The type or category of this URL.",
        max_length=20,
        choices=URL_TYPE_CHOICES,
        default="other",
    )

    def __str__(self):
        return f"{self.label} ({self.url_type})"

    class Meta:
        abstract = True
        ordering = ["label"]

class WorkspaceOwnedBase(CreatedUpdatedBase):
    workspace = models.ForeignKey(
        "core.Workspace", on_delete=models.CASCADE, related_name="%(class)ss"
    )

    class Meta:
        abstract = True