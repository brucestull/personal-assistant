from django.db import models

from config.settings import AUTH_USER_MODEL
from base.models import CreatedUpdatedBase


class OrganizationalConcept(CreatedUpdatedBase):
    """
    This model represents a single organizational concept that is being
    stored. (e.g. Repository Naming, 'TODO' Tags, 'LEARN' Tags, Important
    Best Practices, My Standards, etc.)

    Attributes:
        name (str): The name of the organizational concept.
        description (str): The description of the organizational concept.
        applications (list): Any application(s) that the organizational
        concept is associated with.
    """

    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the organizational concept.",
        max_length=50,
        # `unique=True` ensures that we can't create two organizational
        # concepts with the same name.
        unique=True,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the organizational concept.",
        # `null=True` allows us to create an organizational concept without
        # a description.
        null=True,
        # `blank=True` allows the create organizational concept form to be
        # submitted without a description.
        blank=True,
    )
    applications = models.ManyToManyField(
        "Application",
        verbose_name="Application(s)",
        help_text=(
            "The application(s) that the organizational concept is associated with."
        ),
        # `blank=True` allows the create organizational concept form to be
        # submitted without associating it with an application.
        blank=True,
    )

    def __str__(self):
        """
        Returns the string representation of the organizational concept.
        """
        return f"{self.name} | Applications Count: {self.applications.count()}"

    class Meta:
        verbose_name = "Organizational Concept"
        verbose_name_plural = "Organizational Concepts"


class LanguageFrameworkSystem(CreatedUpdatedBase):
    """
    This model represents a single language, framework, or system that is
    being tracked. (e.g. Python, Django, Docker, CSS, JavaScript, Vue.js,
    React.js, etc.)
    """

    # `name` is the name of the language, framework, or system.
    name = models.CharField(
        verbose_name="Name",
        help_text=(
            "The name of the language, framework, or system used in the application."
        ),
        max_length=30,
        unique=True,
    )

    def __str__(self):
        """
        Returns the string representation of the language, framework, or
        system.
        """
        return self.name

    class Meta:
        verbose_name_plural = "Language/Framework/Systems"


class Project(CreatedUpdatedBase):
    """
    Model for a single `Project`.

    A `Project` can have multiple `owner`s (`CustomUser`s).
    """

    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the project.",
        max_length=255,
        unique=True,
    )
    # `owner` is a many-to-many relationship with the `CustomUser` model.
    owner = models.ManyToManyField(
        AUTH_USER_MODEL,
        verbose_name="Owner(s)",
        help_text="The owner(s) of the project.",
        # The related name for the `owner` field is `projects`.
        # This allows us to access the projects for a user by
        # using `user.projects`.
        related_name="projects",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the project.",
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        Returns the string representation of the project.
        """
        return self.name


class Application(CreatedUpdatedBase):
    """
    This model represents a single application that is being tracked.
    """

    project = models.ManyToManyField(
        Project,
        verbose_name="Project",
        help_text="The project(s) that the application is associated with.",
        # The related name for the `project` field is `applications`.
        # This allows us to access the applications for a project by
        # using `project.applications`.
        related_name="applications",
        # Use blank here so that we can create an application without
        # associating it with a project.
        blank=True,
    )
    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the application.",
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the application.",
        null=True,
        blank=True,
    )
    production_url = models.URLField(
        verbose_name="Production URL",
        help_text="The URL of the application's production deployment.",
        null=True,
        blank=True,
    )
    repository_url = models.URLField(
        verbose_name="Repository URL",
        help_text="The URL of the application's repository.",
        null=True,
        blank=True,
    )
    reference_repository_url = models.URLField(
        verbose_name="Reference Repository URL",
        help_text="The URL of the application's reference repository.",
        null=True,
        blank=True,
    )
    reference_url = models.URLField(
        verbose_name="Reference URL",
        help_text="The URL of the application's reference.",
        null=True,
        blank=True,
    )
    is_official_repository = models.BooleanField(
        verbose_name="Is Official Repository",
        help_text=(
            "Whether or not the application is a repository for an official "
            "app maintained by some other organization."
        ),
        default=False,
    )
    is_adapted_repository = models.BooleanField(
        verbose_name="Is Adapted Repository",
        help_text=(
            "Whether or not the application is a repository adapted from some "
            "other source."
        ),
        default=False,
    )
    is_archive_repository = models.BooleanField(
        verbose_name="Is Archive Repository",
        help_text=(
            "Whether or not the application is a repository for an archived "
            "app that is no longer maintained."
        ),
        default=False,
    )
    project_board_url = models.URLField(
        verbose_name="Project Board URL",
        help_text="The URL of the application's project board.",
        null=True,
        blank=True,
    )
    is_favorite = models.BooleanField(
        verbose_name="Is Favorite",
        help_text="Whether or not the application is a favorite.",
        default=False,
    )
    is_simple_example = models.BooleanField(
        verbose_name="Is Simple Example",
        help_text="Whether or not the application is a simple example.",
        default=False,
    )
    has_custom_user = models.BooleanField(
        verbose_name="Has Custom User",
        help_text="Whether or not the application has a custom user model.",
        default=False,
    )
    has_sticky_footer = models.BooleanField(
        verbose_name="Has Sticky Footer",
        help_text="Whether or not the application has a sticky footer.",
        default=False,
    )
    has_prod_deployment = models.BooleanField(
        verbose_name="Has Production Deployment",
        help_text=("Whether or not the application has a production deployment."),
        default=False,
    )
    has_cicd = models.BooleanField(
        verbose_name="Has CI/CD",
        help_text="Whether or not the application has CI/CD implemented.",
        default=False,
    )
    has_email_sending = models.BooleanField(
        verbose_name="Has Email Sending",
        help_text=("Whether or not the application has email sending capabilities."),
        default=False,
    )
    repository_is_public = models.BooleanField(
        verbose_name="Repository is Public",
        help_text="Whether or not the application's repository is public.",
        default=False,
    )
    settings_in_environment = models.BooleanField(
        verbose_name="Settings in Environment",
        help_text=("Whether or not the application's settings are in the environment."),
        default=False,
    )
    settings_in_dot_env_file = models.BooleanField(
        verbose_name="Settings in Environment File",
        help_text=(
            "Whether or not the application's settings are in an environment file."
        ),
        default=False,
    )
    settings_in_dot_yml_file = models.BooleanField(
        verbose_name="Settings in YAML File",
        help_text=("Whether or not the application's settings are in a YAML file."),
        default=False,
    )
    is_template_repository = models.BooleanField(
        verbose_name="Is Template Repository",
        help_text=(
            "Whether or not the application's repository is a template repository."
        ),
        default=False,
    )
    # `TESTING_LEVEL_CHOICES` is a list of tuples that represent the
    # choices for the `testing_level` field.
    TESTING_LEVEL_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
        ("none", "None"),
    ]
    # `testing_level` is the relative amount of testing coverage for the
    # application.
    testing_level = models.CharField(
        verbose_name="Testing Level",
        help_text=("The relative amount of testing coverage for the application."),
        max_length=6,
        choices=TESTING_LEVEL_CHOICES,
        null=True,
        blank=True,
    )
    all_tests_passing = models.BooleanField(
        verbose_name="All Tests Passing",
        help_text="Whether or not all tests are passing.",
        default=False,
    )
    # `language_framework_systems` is a many-to-many relationship with the
    # `LanguageFrameworkSystem` model.
    language_framework_systems = models.ManyToManyField(
        LanguageFrameworkSystem,
        verbose_name="Language/Framework/Systems",
        help_text=("The languages, frameworks, and systems used in the application."),
        # The related name for the `language_framework_systems` field is
        # `applications`. This allows us to access the applications for a
        # language, framework, or system by using
        # `language_framework_system.applications`.
        related_name="applications",
    )

    def __str__(self):
        """
        Returns the string representation of the application.
        """
        return self.name


class Label(CreatedUpdatedBase):
    """
    This model represents a single label that is being tracked. The label
    is used to tag applications in GitHub Issues and Pull Requests.
    """

    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the label.",
        max_length=50,
        unique=True,
    )
    hue = models.CharField(
        verbose_name="Hue",
        help_text=("The color of the label tag (e.g. '#2BDCC7', '#FF0000', 'ocre')."),
        max_length=25,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the label.",
        null=True,
        blank=True,
    )
    application = models.ManyToManyField(
        Application,
        verbose_name="Application(s)",
        help_text="The application(s) that the label is associated with.",
        blank=True,
    )

    def __str__(self):
        """
        Returns the string representation of the label.
        """
        return self.name


class Note(CreatedUpdatedBase):
    """
    This model represents a single note that is being tracked.
    """

    # `title` is the title of the note.
    title = models.CharField(
        help_text="The title of the note.",
        max_length=255,
    )
    # `content` is the content of the note.
    content = models.TextField(
        help_text="The content of the note.",
    )
    # `application` is a foreign key to the `Application` model.
    application = models.ForeignKey(
        Application,
        help_text="The application that the note is associated with.",
        # If the application is deleted, delete this note.
        on_delete=models.CASCADE,
        # The related name for the `application` field is `notes`.
        # This allows us to access the notes for an application by
        # using `application.notes`.
        related_name="notes",
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        Returns the string representation of the note.

        The string representation of the note is the title of the note
        followed by the name of the application that the note is associated
        with.
        """
        return f"{self.title} - {self.application.name}"


class DjangoModel(CreatedUpdatedBase):
    """
    This model represents a single Django model that is being tracked. This
    model can be a current model that is part of the application or a future
    model that is being considered for the application.
    """

    # `name` is the name of the Django model.
    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the Django model.",
        max_length=255,
        unique=True,
    )
    # `description` is a description of the Django model.
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the Django model.",
    )
    # `is_current_model` is a boolean that indicates whether the Django model
    # is a current model or a future model.
    # If `is_current_model` is `True`, then the Django model is a current
    # model.
    # If `is_current_model` is `False`, then the Django model is a future
    # model.
    is_current_model = models.BooleanField(
        verbose_name="Is Current Model",
        help_text=(
            "'True' if this model is currently used in the application, "
            "'False' if this model is not currently used in the application."
        ),
        default=False,
    )
    # `application` is a foreign key to the `Application` model.
    application = models.ForeignKey(
        Application,
        verbose_name="Application",
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
