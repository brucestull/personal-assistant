from django.db import models


class DateTimeBase(models.Model):
    """
    An abstract base class model that provides self-updating `created`
    and `updated` fields.
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


class LanguageFrameworkSystem(DateTimeBase):
    """
    This model represents a single language, framework, or system that is
    being tracked. (e.g. Python, Django, Docker, CSS, JavaScript, Vue.js,
    React.js, etc.)
    """

    # `name` is the name of the language, framework, or system.
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        """
        Returns the string representation of the language, framework, or system.
        """
        return self.name

    class Meta:
        verbose_name_plural = "Language/Framework/Systems"


class Application(DateTimeBase):
    """
    This model represents a single application that is being tracked.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="The name of the application.",
    )
    description = models.TextField(
        help_text="A description of the application.",
    )
    repository_url = models.URLField(
        help_text="The URL of the application's repository.",
    )
    has_custom_user = models.BooleanField(
        help_text="Whether or not the application has a custom user model.",
    )
    has_sticky_footer = models.BooleanField(
        help_text="Whether or not the application has a sticky footer.",
    )
    has_prod_deployment = models.BooleanField(
        help_text="Whether or not the application has a production deployment.",
    )
    # `TESTING_LEVEL_CHOICES` is a list of tuples that represent the
    # choices for the `testing_level` field.
    TESTING_LEVEL_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    # `testing_level` is the relative amount of testing coverage for the
    # application.
    testing_level = models.CharField(
        max_length=6,
        choices=TESTING_LEVEL_CHOICES,
        help_text="The relative amount of testing coverage for the application.",
    )
    # `language_framework_systems` is a many-to-many relationship with the
    # `LanguageFrameworkSystem` model.
    language_framework_systems = models.ManyToManyField(
        LanguageFrameworkSystem,
        # The related name for the `language_framework_systems` field is
        # `applications`. This allows us to access the applications for a
        # language, framework, or system by using
        # `language_framework_system.applications`.
        related_name="applications",
        help_text="The languages, frameworks, and systems used in the application.",
    )

    def __str__(self):
        """
        Returns the string representation of the application.
        """
        return self.name


class Note(DateTimeBase):
    """
    This model represents a single note that is being tracked.
    """

    # `title` is the title of the note.
    title = models.CharField(
        max_length=255,
        help_text="The title of the note.",
    )
    # `content` is the content of the note.
    content = models.TextField(
        help_text="The content of the note.",
    )
    # `application` is a foreign key to the `Application` model.
    application = models.ForeignKey(
        Application,
        # If the application is deleted, delete this note.
        on_delete=models.CASCADE,
        # The related name for the `application` field is `notes`.
        # This allows us to access the notes for an application by
        # using `application.notes`.
        related_name="notes",
    )

    def __str__(self):
        """
        Returns the string representation of the note.

        The string representation of the note is the title of the note
        followed by the name of the application that the note is associated
        with.
        """
        return f"{self.title} - {self.application.name}"


class DjangoModel(DateTimeBase):
    """
    This model represents a single Django model that is being tracked. This
    model can be a current model that is part of the application or a future
    model that is being considered for the application.
    """

    # `name` is the name of the Django model.
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="The name of the Django model.",
    )
    # `description` is a description of the Django model.
    description = models.TextField(
        help_text="The description of the Django model.",
    )
    # `is_current_model` is a boolean that indicates whether the Django model
    # is a current model or a future model.
    # If `is_current_model` is `True`, then the Django model is a current
    # model.
    # If `is_current_model` is `False`, then the Django model is a future
    # model.
    is_current_model = models.BooleanField(
        default=False,
        help_text=(
            "'True' if this model is currently used in the application, "
            "'False' if this model is not currently used in the application."
        ),
    )
    # `application` is a foreign key to the `Application` model.
    application = models.ForeignKey(
        Application,
        # If the application is deleted, delete this Django model.
        on_delete=models.CASCADE,
        # The related name for the `application` field is `django_models`.
        # This allows us to access the Django models for an application by
        # using `application.django_models`.
        related_name="django_models",
    )

    def __str__(self):
        """
        Returns the string representation of the Django model.
        """
        return self.name
