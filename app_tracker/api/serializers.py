# app_tracker/api/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app_tracker.models import (
    Application,
    DjangoModel,
    Host,
    Label,
    LanguageFrameworkSystem,
    Note,
    OperatingSystem,
    OrganizationalConcept,
    Project,
    URL,
)

User = get_user_model()


class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ["id", "name", "code_name"]


class LanguageFrameworkSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageFrameworkSystem
        fields = ["id", "name", "created", "updated"]


class OrganizationalConceptSerializer(serializers.ModelSerializer):
    applications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Application.objects.all(), required=False
    )

    class Meta:
        model = OrganizationalConcept
        fields = ["id", "name", "description", "applications", "created", "updated"]


class LabelSerializer(serializers.ModelSerializer):
    application = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Application.objects.all(), required=False
    )

    class Meta:
        model = Label
        fields = ["id", "name", "hue", "description", "application", "created", "updated"]


class NoteSerializer(serializers.ModelSerializer):
    application = serializers.PrimaryKeyRelatedField(
        queryset=Application.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Note
        fields = ["id", "title", "content", "application", "created", "updated"]


class URLSerializer(serializers.ModelSerializer):
    application = serializers.PrimaryKeyRelatedField(
        queryset=Application.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = URL
        fields = [
            "id",
            "url",
            "label",
            "description",
            "url_type",
            "application",
            "created",
            "updated",
        ]


class HostSerializer(serializers.ModelSerializer):
    operating_system = serializers.PrimaryKeyRelatedField(
        queryset=OperatingSystem.objects.all(), allow_null=True, required=False
    )
    applications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Application.objects.all(), required=False
    )

    class Meta:
        model = Host
        fields = [
            "id",
            "name",
            "description",
            "operating_system",
            "host_name",
            "mac_address",
            "ram",
            "form_factor",
            "ip_address",
            "environment",
            "notes",
            "applications",
            "status",
            "archived_at",
            "created",
            "updated",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ["id", "name", "owner", "description", "created", "updated"]


class ApplicationSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Project.objects.all(), required=False
    )
    language_framework_systems = serializers.PrimaryKeyRelatedField(
        many=True, queryset=LanguageFrameworkSystem.objects.all()
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "project",
            "name",
            "description",
            "production_url",
            "repository_url",
            "reference_repository_url",
            "reference_url",
            "is_official_repository",
            "is_adapted_repository",
            "is_archive_repository",
            "project_board_url",
            "is_favorite",
            "is_simple_example",
            "has_custom_user",
            "has_sticky_footer",
            "has_prod_deployment",
            "has_cicd",
            "has_email_sending",
            "repository_is_public",
            "settings_in_environment",
            "settings_in_dot_env_file",
            "settings_in_dot_yml_file",
            "is_template_repository",
            "is_pending_deployment",
            "testing_level",
            "all_tests_passing",
            "language_framework_systems",
            "created",
            "updated",
        ]


class DjangoModelSerializer(serializers.ModelSerializer):
    application = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())

    class Meta:
        model = DjangoModel
        fields = [
            "id",
            "name",
            "description",
            "is_current_model",
            "application",
            "created",
            "updated",
        ]
