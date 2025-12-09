from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from app_tracker.models import (
    Application,
    Host,
    LanguageFrameworkSystem,
)


class HomeViewTest(TestCase):
    """
    Test the `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that the `home` view is rendered at "/app-tracker/".
        """
        response = self.client.get("/app-tracker/")
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that the `home` view is rendered at the desired location by
        "app_tracker:home".
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the `home` view uses the correct template "app_tracker/home.html".
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_tracker/home.html")

    def test_home_view_uses_correct_context(self):
        """
        Test that the `home` view uses the correct context.

        The context should contain the following:
        - the_site_name
        - page_title
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "App Tracker Home")


class DashboardViewTest(TestCase):
    """
    Test the `dashboard` view.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a test user with registration_accepted=True
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            registration_accepted=True,
        )
        # Create a language/framework/system for applications
        self.lfs = LanguageFrameworkSystem.objects.create(name="Python")

    def test_dashboard_requires_authentication(self):
        """
        Test that the dashboard view requires authentication.
        """
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_requires_registration_accepted(self):
        """
        Test that the dashboard view requires registration_accepted.
        """
        # Create a user without registration_accepted
        CustomUser.objects.create_user(
            username="unaccepteduser",
            password="testpass123",
            registration_accepted=False,
        )
        self.client.login(username="unaccepteduser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_url_accessible_by_name(self):
        """
        Test that the dashboard view is accessible when logged in.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """
        Test that the dashboard view is rendered at "/app-tracker/dashboard/".
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/app-tracker/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_uses_correct_template(self):
        """
        Test that the dashboard view uses the correct template.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_tracker/dashboard.html")

    def test_dashboard_uses_correct_context(self):
        """
        Test that the dashboard view uses the correct context.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "App Tracker Dashboard")
        # Check that all expected context variables are present
        self.assertIn("total_applications", response.context)
        self.assertIn("total_projects", response.context)
        self.assertIn("total_hosts", response.context)
        self.assertIn("total_lfs", response.context)
        self.assertIn("apps_with_production", response.context)
        self.assertIn("apps_with_cicd", response.context)
        self.assertIn("favorite_apps", response.context)
        self.assertIn("recent_apps", response.context)
        self.assertIn("testing_level_counts", response.context)
        self.assertIn("lfs_usage", response.context)
        self.assertIn("projects_overview", response.context)
        self.assertIn("hosts_by_environment", response.context)
        self.assertIn("pending_deployment_apps", response.context)

    def test_dashboard_displays_correct_counts(self):
        """
        Test that the dashboard displays correct counts for applications.
        """
        # Create some test applications
        app1 = Application.objects.create(
            name="Test App 1",
            has_prod_deployment=True,
            has_cicd=True,
            is_favorite=True,
        )
        app1.language_framework_systems.add(self.lfs)

        app2 = Application.objects.create(
            name="Test App 2",
            has_prod_deployment=False,
            has_cicd=False,
            is_favorite=False,
        )
        app2.language_framework_systems.add(self.lfs)

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_applications"], 2)
        self.assertEqual(response.context["apps_with_production"], 1)
        self.assertEqual(response.context["apps_with_cicd"], 1)

    def test_dashboard_displays_favorite_apps(self):
        """
        Test that the dashboard displays favorite applications.
        """
        # Create a favorite application
        app = Application.objects.create(
            name="Favorite App",
            is_favorite=True,
        )
        app.language_framework_systems.add(self.lfs)

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["favorite_apps"]), 1)
        self.assertEqual(response.context["favorite_apps"][0].name, "Favorite App")

    def test_dashboard_displays_pending_deployment_apps(self):
        """
        Test that the dashboard displays applications pending deployment.
        """
        # Create an application pending deployment
        app = Application.objects.create(
            name="Docker Engine",
            description="Container runtime engine",
            is_pending_deployment=True,
        )
        app.language_framework_systems.add(self.lfs)

        # Create a non-pending application
        app2 = Application.objects.create(
            name="Deployed App",
            is_pending_deployment=False,
        )
        app2.language_framework_systems.add(self.lfs)

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["pending_deployment_apps"]), 1)
        self.assertEqual(
            response.context["pending_deployment_apps"][0].name, "Docker Engine"
        )

    def test_dashboard_shows_only_active_hosts_by_default(self):
        """
        Test that the dashboard shows only ACTIVE hosts by default.
        """
        # Create hosts with different statuses
        Host.objects.create(
            name="Active Host 1",
            host_name="active-host-1",
            ip_address="192.168.1.10",
            status=Host.HostStatus.ACTIVE,
        )
        Host.objects.create(
            name="Active Host 2",
            host_name="active-host-2",
            ip_address="192.168.1.11",
            status=Host.HostStatus.ACTIVE,
        )
        Host.objects.create(
            name="Paused Host",
            host_name="paused-host",
            ip_address="192.168.1.20",
            status=Host.HostStatus.PAUSED,
        )
        Host.objects.create(
            name="Retired Host",
            host_name="retired-host",
            ip_address="192.168.1.30",
            status=Host.HostStatus.RETIRED,
        )

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_hosts"], 2)
        self.assertFalse(response.context["include_paused"])

    def test_dashboard_includes_paused_hosts_with_query_param(self):
        """
        Test that the dashboard includes PAUSED hosts when include_paused=1.
        """
        # Create hosts with different statuses
        Host.objects.create(
            name="Active Host",
            host_name="active-host",
            ip_address="192.168.1.10",
            status=Host.HostStatus.ACTIVE,
        )
        Host.objects.create(
            name="Paused Host",
            host_name="paused-host",
            ip_address="192.168.1.20",
            status=Host.HostStatus.PAUSED,
        )
        Host.objects.create(
            name="Retired Host",
            host_name="retired-host",
            ip_address="192.168.1.30",
            status=Host.HostStatus.RETIRED,
        )

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("app_tracker:dashboard") + "?include_paused=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_hosts"], 2)  # Active + Paused
        self.assertTrue(response.context["include_paused"])

    def test_dashboard_excludes_retired_hosts_always(self):
        """
        Test that the dashboard never includes RETIRED hosts.
        """
        # Create hosts with different statuses
        Host.objects.create(
            name="Active Host",
            host_name="active-host",
            ip_address="192.168.1.10",
            status=Host.HostStatus.ACTIVE,
        )
        Host.objects.create(
            name="Retired Host",
            host_name="retired-host",
            ip_address="192.168.1.30",
            status=Host.HostStatus.RETIRED,
        )

        self.client.login(username="testuser", password="testpass123")
        
        # Test without query param
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.context["total_hosts"], 1)
        
        # Test with include_paused=1 (should still exclude retired)
        response = self.client.get(
            reverse("app_tracker:dashboard") + "?include_paused=1"
        )
        self.assertEqual(response.context["total_hosts"], 1)

    def test_dashboard_context_includes_include_paused_flag(self):
        """
        Test that the dashboard context includes the include_paused flag.
        """
        self.client.login(username="testuser", password="testpass123")
        
        # Test without query param
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertIn("include_paused", response.context)
        self.assertFalse(response.context["include_paused"])
        
        # Test with include_paused=1
        response = self.client.get(
            reverse("app_tracker:dashboard") + "?include_paused=1"
        )
        self.assertIn("include_paused", response.context)
        self.assertTrue(response.context["include_paused"])


class HostUpdateViewTest(TestCase):
    """
    Test the HostUpdateView.
    """

    def setUp(self):
        """
        Set up test data.
        """
        from app_tracker.models import Host, OperatingSystem

        # Create a test user with registration_accepted=True
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            registration_accepted=True,
        )

        # Create operating systems in non-alphabetical order
        self.os_ubuntu = OperatingSystem.objects.create(name="Ubuntu 22.04")
        self.os_debian = OperatingSystem.objects.create(name="Debian 11")
        self.os_centos = OperatingSystem.objects.create(name="CentOS 7")
        self.os_alpine = OperatingSystem.objects.create(name="Alpine Linux")

        # Create a test host
        self.host = Host.objects.create(
            name="Test Host",
            host_name="test-host",
            operating_system=self.os_ubuntu,
        )

    def test_host_update_view_operating_system_sorted(self):
        """
        Test that the operating system field is sorted by name.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("app_tracker:host_update", kwargs={"pk": self.host.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Get the form from the response
        form = response.context["form"]
        os_field = form.fields["operating_system"]

        # Get the queryset and convert to list
        os_list = list(os_field.queryset.values_list("name", flat=True))

        # Check that the list is sorted alphabetically
        self.assertEqual(
            os_list,
            ["Alpine Linux", "CentOS 7", "Debian 11", "Ubuntu 22.04"],
        )

    def test_host_update_view_template_has_search_input(self):
        """
        Test that the template includes a search input for operating system.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("app_tracker:host_update", kwargs={"pk": self.host.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Check that the search input is in the rendered HTML
        self.assertContains(response, 'id="os-search"')
        self.assertContains(response, "Search operating systems...")


class HostCreateViewTest(TestCase):
    """
    Test the HostCreateView.
    """

    def setUp(self):
        """
        Set up test data.
        """
        from app_tracker.models import OperatingSystem

        # Create a test user with registration_accepted=True
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            registration_accepted=True,
        )

        # Create operating systems in non-alphabetical order
        self.os_ubuntu = OperatingSystem.objects.create(name="Ubuntu 22.04")
        self.os_debian = OperatingSystem.objects.create(name="Debian 11")
        self.os_centos = OperatingSystem.objects.create(name="CentOS 7")

    def test_host_create_view_operating_system_sorted(self):
        """
        Test that the operating system field is sorted by name in create view.
        """
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("app_tracker:host_create"))
        self.assertEqual(response.status_code, 200)

        # Get the form from the response
        form = response.context["form"]
        os_field = form.fields["operating_system"]

        # Get the queryset and convert to list
        os_list = list(os_field.queryset.values_list("name", flat=True))

        # Check that the list is sorted alphabetically
        self.assertEqual(
            os_list,
            ["CentOS 7", "Debian 11", "Ubuntu 22.04"],
        )
