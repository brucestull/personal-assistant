# app_tracker/models.py

from django.db import models
from django.urls import reverse

from base.models import URL as BaseURL
from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class OperatingSystem(models.Model):
    """
    Represents a known host operating system (e.g., Ubuntu Server 22.04).
    """

    name = models.CharField(
        verbose_name="Operating System Name",
        help_text="The name and version of the operating system.",
        max_length=100,
        unique=True,
    )
    code_name = models.CharField(
        verbose_name="Code Name",
        help_text="The code name of the operating system (e.g., Jammy Jellyfish).",
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = "operating_systems"
        verbose_name = "Operating System"
        verbose_name_plural = "Operating Systems"


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
        "Application",
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
        "Application",
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
        return f"{self.title} - {self.application.name if self.application else 'No Application'}"  # noqa: E501


class URL(BaseURL):
    """
    A URL associated with an application in the app_tracker.

    Inherits from the abstract URL base class and adds a relationship
    to the Application model.
    """

    application = models.ForeignKey(
        "Application",
        verbose_name="Application",
        help_text="The application that this URL is associated with.",
        on_delete=models.CASCADE,
        related_name="urls",
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("app_tracker:url_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"
        ordering = ["label"]


class HostQuerySet(models.QuerySet):
    """
    Custom queryset for Host model with filtering methods.
    """

    def visible_on_dashboard(self):
        """
        Returns only hosts with ACTIVE status that should be visible on the dashboard.
        """
        return self.filter(status=Host.HostStatus.ACTIVE)


class Host(CreatedUpdatedBase):
    """
    Represents a physical or virtual host where applications are hosted.
    """

    class HostStatus(models.TextChoices):
        """
        Status choices for Host visibility and lifecycle management.
        """

        ACTIVE = "ACTIVE", "Active"
        PAUSED = "PAUSED", "Paused"
        RETIRED = "RETIRED", "Retired"

    FORM_FACTOR_CHOICES = [
        # Raspberry Pi 5 variants
        ("Pi5-8GB", "Raspberry Pi 5 - 8GB"),
        ("Pi5-4GB", "Raspberry Pi 5 - 4GB"),
        ("Pi5-2GB", "Raspberry Pi 5 - 2GB"),
        # Raspberry Pi 4 variants
        ("Pi4-8GB", "Raspberry Pi 4 - 8GB"),
        ("Pi4-4GB", "Raspberry Pi 4 - 4GB"),
        ("Pi4-2GB", "Raspberry Pi 4 - 2GB"),
        ("Pi4-1GB", "Raspberry Pi 4 - 1GB"),
        # Raspberry Pi 3 variants
        ("Pi3B+", "Raspberry Pi 3 Model B+"),
        ("Pi3B", "Raspberry Pi 3 Model B"),
        ("Pi3A+", "Raspberry Pi 3 Model A+"),
        # Raspberry Pi Zero variants
        ("PiZero2W", "Raspberry Pi Zero 2 W"),
        ("PiZeroW", "Raspberry Pi Zero W"),
        ("PiZero", "Raspberry Pi Zero"),
        # Raspberry Pi Pico variants
        ("PiPico2W", "Raspberry Pi Pico 2 W"),
        ("PiPico2", "Raspberry Pi Pico 2"),
        ("PiPicoW", "Raspberry Pi Pico W"),
        ("PiPico", "Raspberry Pi Pico"),
        # Traditional form factors
        ("Desktop", "Desktop"),
        ("Laptop", "Laptop"),
        ("Server", "Server"),
        ("Headless", "Headless Server"),
        # Network devices
        ("SwitchEth", "Switch - Ethernet"),
        ("SwitchPOE", "Switch - Ethernet POE"),
        ("Router", "Router"),
        ("AccessPt", "Access Point"),
        # IoT and embedded devices
        ("IoT", "IoT - General"),
        ("Camera", "Camera"),
        ("Sensor", "Sensor"),
        # Virtual and cloud
        ("VM", "Virtual Machine"),
        ("Container", "Container"),
        ("Cloud", "Cloud Instance"),
        # Other
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    operating_system = models.ForeignKey(
        OperatingSystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Operating System",
        help_text="The OS running on this host.",
    )
    host_name = models.CharField(
        verbose_name="Host Name",
        help_text="A unique host name for the host.",
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        help_text="Format: XX:XX:XX:XX:XX:XX",
        blank=True,
        null=True,
    )
    ram = models.CharField(
        max_length=50,
        help_text="e.g., 500MB, .5GB, 2GB, 4GB, 8GB",
        blank=True,
        null=True,
    )
    form_factor = models.CharField(
        max_length=20, choices=FORM_FACTOR_CHOICES, blank=True, null=True
    )

    ip_address = models.GenericIPAddressField(
        verbose_name="IP Address",
        help_text="The IP address of the host.",
        protocol="both",
        null=True,
        blank=True,
    )
    environment = models.CharField(
        verbose_name="Environment",
        help_text="The environment this host belongs to (e.g., production, staging, test).",  # noqa: E501
        max_length=50,
        choices=[
            ("production", "Production"),
            ("staging", "Staging"),
            ("test", "Test"),
            ("development", "Development"),
        ],
        null=True,
        blank=True,
    )
    notes = models.TextField(
        verbose_name="Notes",
        help_text="Optional notes about the host (e.g., hardware specs, roles, etc.).",  # noqa: E501
        blank=True,
        null=True,
    )
    applications = models.ManyToManyField(
        "Application",
        verbose_name="Applications",
        help_text="Applications hosted on this host.",
        related_name="hosts",
        blank=True,
    )
    status = models.CharField(
        verbose_name="Status",
        help_text="The current status of the host (Active, Paused, or Retired).",
        max_length=10,
        choices=HostStatus.choices,
        default=HostStatus.ACTIVE,
    )
    archived_at = models.DateTimeField(
        verbose_name="Archived At",
        help_text="The date and time when the host was paused or retired.",
        null=True,
        blank=True,
    )

    # Attach custom queryset as the default manager
    objects = HostQuerySet.as_manager()

    def __str__(self):
        return f"{self.host_name} ({self.ip_address or 'no IP'})"

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosts"
        ordering = ["host_name"]


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
    is_pending_deployment = models.BooleanField(
        verbose_name="Is Pending Deployment",
        help_text=(
            "Whether or not the application is pending deployment to a server "
            "(e.g., packages like DuckDNS, Docker Engine, or Jenkins yet to be "
            "implemented on a server)."
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

    def get_absolute_url(self):
        return reverse("app_tracker:application_detail", kwargs={"pk": self.pk})

    def __str__(self):
        """
        Returns the string representation of the application.
        """
        return self.name


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
        "Application",
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
