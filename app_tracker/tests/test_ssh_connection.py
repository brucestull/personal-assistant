# app_tracker/tests/test_ssh_connection.py
"""
Comprehensive tests for the SSHConnection model, admin, and views.
"""

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from app_tracker.admin import SSHConnectionAdmin, SSHClientConnectionInline, SSHServerConnectionInline
from app_tracker.models import Host, SSHConnection


def make_user(username="testuser", registration_accepted=True):
    user = CustomUser.objects.create_user(
        username=username,
        password="pass",
        registration_accepted=registration_accepted,
    )
    return user


def make_host(name, host_name, ip_address):
    return Host.objects.create(
        name=name,
        host_name=host_name,
        ip_address=ip_address,
    )


def make_ssh_connection(server, client, **kwargs):
    defaults = {
        "key_filename": "id_ed25519",
        "key_comment": "user@client",
        "encryption_algorithm": "ed25519",
        "passphrase_protected": False,
    }
    defaults.update(kwargs)
    return SSHConnection.objects.create(server=server, client=client, **defaults)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class SSHConnectionModelTest(TestCase):
    """
    Tests for the SSHConnection model.
    """

    @classmethod
    def setUpTestData(cls):
        cls.server = make_host("Server Host", "server-host", "192.168.1.1")
        cls.client_host = make_host("Client Host", "client-host", "192.168.1.2")
        cls.conn = make_ssh_connection(
            server=cls.server,
            client=cls.client_host,
            key_filename="id_ed25519",
            key_comment="user@client-host",
            encryption_algorithm="ed25519",
            passphrase_protected=True,
        )

    # --- Field verbose names ---

    def test_server_verbose_name(self):
        field = SSHConnection._meta.get_field("server")
        self.assertEqual(field.verbose_name, "Server")

    def test_client_verbose_name(self):
        field = SSHConnection._meta.get_field("client")
        self.assertEqual(field.verbose_name, "Client")

    def test_key_filename_verbose_name(self):
        field = SSHConnection._meta.get_field("key_filename")
        self.assertEqual(field.verbose_name, "Key Filename")

    def test_key_comment_verbose_name(self):
        field = SSHConnection._meta.get_field("key_comment")
        self.assertEqual(field.verbose_name, "Key Comment")

    def test_encryption_algorithm_verbose_name(self):
        field = SSHConnection._meta.get_field("encryption_algorithm")
        self.assertEqual(field.verbose_name, "Encryption Algorithm")

    def test_passphrase_protected_verbose_name(self):
        field = SSHConnection._meta.get_field("passphrase_protected")
        self.assertEqual(field.verbose_name, "Passphrase Protected")

    # --- Field help_texts ---

    def test_server_help_text(self):
        field = SSHConnection._meta.get_field("server")
        self.assertIn("server", field.help_text.lower())

    def test_client_help_text(self):
        field = SSHConnection._meta.get_field("client")
        self.assertIn("client", field.help_text.lower())

    def test_key_filename_help_text(self):
        field = SSHConnection._meta.get_field("key_filename")
        self.assertIn("key", field.help_text.lower())

    def test_key_comment_help_text(self):
        field = SSHConnection._meta.get_field("key_comment")
        self.assertIn("comment", field.help_text.lower())

    def test_encryption_algorithm_help_text(self):
        field = SSHConnection._meta.get_field("encryption_algorithm")
        self.assertIn("algorithm", field.help_text.lower())

    def test_passphrase_protected_help_text(self):
        field = SSHConnection._meta.get_field("passphrase_protected")
        self.assertIn("passphrase", field.help_text.lower())

    # --- Field nullability / blank ---

    def test_key_filename_blank_and_null(self):
        field = SSHConnection._meta.get_field("key_filename")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_key_comment_blank_and_null(self):
        field = SSHConnection._meta.get_field("key_comment")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_passphrase_protected_default_false(self):
        field = SSHConnection._meta.get_field("passphrase_protected")
        self.assertFalse(field.default)

    def test_encryption_algorithm_default_ed25519(self):
        field = SSHConnection._meta.get_field("encryption_algorithm")
        self.assertEqual(field.default, "ed25519")

    # --- __str__ ---

    def test_str_representation(self):
        expected = (
            f"{self.client_host} → {self.server}"
            f" ({self.conn.encryption_algorithm})"
        )
        self.assertEqual(str(self.conn), expected)

    # --- Meta ---

    def test_meta_verbose_name(self):
        self.assertEqual(SSHConnection._meta.verbose_name, "SSH Connection")

    def test_meta_verbose_name_plural(self):
        self.assertEqual(SSHConnection._meta.verbose_name_plural, "SSH Connections")

    def test_meta_ordering(self):
        self.assertEqual(SSHConnection._meta.ordering, ["server", "client"])

    # --- Encryption algorithm choices ---

    def test_encryption_algorithm_choices_include_ed25519(self):
        choices = dict(SSHConnection.ENCRYPTION_ALGORITHM_CHOICES)
        self.assertIn("ed25519", choices)

    def test_encryption_algorithm_choices_include_rsa(self):
        choices = dict(SSHConnection.ENCRYPTION_ALGORITHM_CHOICES)
        self.assertIn("rsa", choices)

    def test_encryption_algorithm_choices_include_ecdsa(self):
        choices = dict(SSHConnection.ENCRYPTION_ALGORITHM_CHOICES)
        self.assertIn("ecdsa", choices)

    def test_encryption_algorithm_choices_include_dsa(self):
        choices = dict(SSHConnection.ENCRYPTION_ALGORITHM_CHOICES)
        self.assertIn("dsa", choices)

    # --- Related names on Host ---

    def test_server_related_name(self):
        field = SSHConnection._meta.get_field("server")
        self.assertEqual(field.remote_field.related_name, "ssh_server_connections")

    def test_client_related_name(self):
        field = SSHConnection._meta.get_field("client")
        self.assertEqual(field.remote_field.related_name, "ssh_client_connections")

    # --- Cascade delete ---

    def test_delete_server_cascades_to_connection(self):
        server = make_host("TempServer", "temp-server", "10.0.0.1")
        client = make_host("TempClient", "temp-client", "10.0.0.2")
        conn = make_ssh_connection(server=server, client=client)
        conn_pk = conn.pk
        server.delete()
        self.assertFalse(SSHConnection.objects.filter(pk=conn_pk).exists())

    def test_delete_client_cascades_to_connection(self):
        server = make_host("TempServer2", "temp-server-2", "10.0.1.1")
        client = make_host("TempClient2", "temp-client-2", "10.0.1.2")
        conn = make_ssh_connection(server=server, client=client)
        conn_pk = conn.pk
        client.delete()
        self.assertFalse(SSHConnection.objects.filter(pk=conn_pk).exists())

    # --- Nullable fields creation ---

    def test_create_with_minimal_fields(self):
        server = make_host("MinServer", "min-server", "10.0.2.1")
        client = make_host("MinClient", "min-client", "10.0.2.2")
        conn = SSHConnection.objects.create(server=server, client=client)
        self.assertIsNone(conn.key_filename)
        self.assertIsNone(conn.key_comment)
        self.assertEqual(conn.encryption_algorithm, "ed25519")
        self.assertFalse(conn.passphrase_protected)


# ---------------------------------------------------------------------------
# Admin tests
# ---------------------------------------------------------------------------


class SSHConnectionAdminTest(TestCase):
    """
    Tests for SSHConnectionAdmin registration and configuration.
    """

    def test_list_display(self):
        self.assertEqual(
            SSHConnectionAdmin.list_display,
            (
                "server",
                "client",
                "encryption_algorithm",
                "key_filename",
                "key_comment",
                "passphrase_protected",
                "created",
            ),
        )

    def test_list_filter(self):
        self.assertEqual(
            SSHConnectionAdmin.list_filter,
            ("encryption_algorithm", "passphrase_protected"),
        )

    def test_date_hierarchy(self):
        self.assertEqual(SSHConnectionAdmin.date_hierarchy, "created")

    def test_search_fields(self):
        self.assertEqual(
            SSHConnectionAdmin.search_fields,
            (
                "server__host_name",
                "client__host_name",
                "key_filename",
                "key_comment",
            ),
        )

    def test_ordering(self):
        self.assertEqual(SSHConnectionAdmin.ordering, ("server", "client"))

    def test_readonly_fields(self):
        self.assertEqual(
            SSHConnectionAdmin.readonly_fields,
            ("created", "updated"),
        )


class SSHServerConnectionInlineTest(TestCase):
    """
    Tests for SSHServerConnectionInline.
    """

    def test_model(self):
        self.assertEqual(SSHServerConnectionInline.model, SSHConnection)

    def test_fk_name(self):
        self.assertEqual(SSHServerConnectionInline.fk_name, "server")

    def test_fields(self):
        self.assertIn("client", SSHServerConnectionInline.fields)
        self.assertIn("encryption_algorithm", SSHServerConnectionInline.fields)
        self.assertIn("passphrase_protected", SSHServerConnectionInline.fields)


class SSHClientConnectionInlineTest(TestCase):
    """
    Tests for SSHClientConnectionInline.
    """

    def test_model(self):
        self.assertEqual(SSHClientConnectionInline.model, SSHConnection)

    def test_fk_name(self):
        self.assertEqual(SSHClientConnectionInline.fk_name, "client")

    def test_fields(self):
        self.assertIn("server", SSHClientConnectionInline.fields)
        self.assertIn("encryption_algorithm", SSHClientConnectionInline.fields)
        self.assertIn("passphrase_protected", SSHClientConnectionInline.fields)


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------


class SSHConnectionViewTestBase(TestCase):
    """
    Base class for SSH connection view tests.
    """

    def setUp(self):
        self.user = make_user()
        self.server = make_host("Server", "server-host", "192.168.10.1")
        self.client_host = make_host("Client", "client-host", "192.168.10.2")
        self.conn = make_ssh_connection(
            server=self.server,
            client=self.client_host,
        )

    def login(self):
        self.client.login(username="testuser", password="pass")


class SSHConnectionListViewTest(SSHConnectionViewTestBase):
    """
    Tests for SSHConnectionListView.
    """

    def test_requires_authentication(self):
        # RegistrationAcceptedMixin redirects unauthenticated users to login
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertEqual(response.status_code, 302)

    def test_requires_registration_accepted(self):
        unaccepted = make_user("unaccepted", registration_accepted=False)
        self.client.login(username="unaccepted", password="pass")
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertEqual(response.status_code, 403)

    def test_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get("/app-tracker/ssh-connections/")
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertTemplateUsed(response, "app_tracker/sshconnection_list.html")

    def test_shows_connections_in_context(self):
        self.login()
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertIn(self.conn, response.context["object_list"])

    def test_empty_list_renders(self):
        self.login()
        SSHConnection.objects.all().delete()
        response = self.client.get(reverse("app_tracker:ssh_connection_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)


class SSHConnectionDetailViewTest(SSHConnectionViewTestBase):
    """
    Tests for SSHConnectionDetailView.
    """

    def test_requires_authentication(self):
        # RegistrationAcceptedMixin redirects unauthenticated users to login
        response = self.client.get(
            reverse("app_tracker:ssh_connection_detail", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_url_accessible_by_name(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_detail", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_desired_location(self):
        self.login()
        response = self.client.get(f"/app-tracker/ssh-connections/{self.conn.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_detail", args=[self.conn.pk])
        )
        self.assertTemplateUsed(response, "app_tracker/sshconnection_detail.html")

    def test_shows_object_in_context(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_detail", args=[self.conn.pk])
        )
        self.assertEqual(response.context["object"], self.conn)

    def test_404_for_nonexistent(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_detail", args=[99999])
        )
        self.assertEqual(response.status_code, 404)


class SSHConnectionCreateViewTest(SSHConnectionViewTestBase):
    """
    Tests for SSHConnectionCreateView.
    """

    def test_requires_authentication(self):
        # RegistrationAcceptedMixin redirects unauthenticated users to login
        response = self.client.get(reverse("app_tracker:ssh_connection_create"))
        self.assertEqual(response.status_code, 302)

    def test_url_accessible_by_name(self):
        self.login()
        response = self.client.get(reverse("app_tracker:ssh_connection_create"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.login()
        response = self.client.get(reverse("app_tracker:ssh_connection_create"))
        self.assertTemplateUsed(response, "app_tracker/sshconnection_form.html")

    def test_post_creates_connection(self):
        self.login()
        server2 = make_host("Server2", "server2", "10.1.1.1")
        client2 = make_host("Client2", "client2", "10.1.1.2")
        count_before = SSHConnection.objects.count()
        response = self.client.post(
            reverse("app_tracker:ssh_connection_create"),
            {
                "server": server2.pk,
                "client": client2.pk,
                "key_filename": "id_rsa",
                "key_comment": "test@host",
                "encryption_algorithm": "rsa",
                "passphrase_protected": False,
            },
        )
        self.assertEqual(SSHConnection.objects.count(), count_before + 1)
        self.assertRedirects(response, reverse("app_tracker:ssh_connection_list"))

    def test_post_invalid_data_does_not_create(self):
        self.login()
        count_before = SSHConnection.objects.count()
        response = self.client.post(
            reverse("app_tracker:ssh_connection_create"),
            {
                "server": "",
                "client": "",
                "encryption_algorithm": "ed25519",
            },
        )
        # Should re-render form with errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SSHConnection.objects.count(), count_before)


class SSHConnectionUpdateViewTest(SSHConnectionViewTestBase):
    """
    Tests for SSHConnectionUpdateView.
    """

    def test_requires_authentication(self):
        # RegistrationAcceptedMixin redirects unauthenticated users to login
        response = self.client.get(
            reverse("app_tracker:ssh_connection_update", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_url_accessible_by_name(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_update", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_update", args=[self.conn.pk])
        )
        self.assertTemplateUsed(response, "app_tracker/sshconnection_form.html")

    def test_post_updates_connection(self):
        self.login()
        response = self.client.post(
            reverse("app_tracker:ssh_connection_update", args=[self.conn.pk]),
            {
                "server": self.server.pk,
                "client": self.client_host.pk,
                "key_filename": "id_ecdsa",
                "key_comment": "updated@host",
                "encryption_algorithm": "ecdsa",
                "passphrase_protected": True,
            },
        )
        self.assertRedirects(response, reverse("app_tracker:ssh_connection_list"))
        self.conn.refresh_from_db()
        self.assertEqual(self.conn.encryption_algorithm, "ecdsa")
        self.assertEqual(self.conn.key_filename, "id_ecdsa")
        self.assertTrue(self.conn.passphrase_protected)


class SSHConnectionDeleteViewTest(SSHConnectionViewTestBase):
    """
    Tests for SSHConnectionDeleteView.
    """

    def test_requires_authentication(self):
        # RegistrationAcceptedMixin redirects unauthenticated users to login
        response = self.client.get(
            reverse("app_tracker:ssh_connection_delete", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_url_accessible_by_name(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_delete", args=[self.conn.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.login()
        response = self.client.get(
            reverse("app_tracker:ssh_connection_delete", args=[self.conn.pk])
        )
        self.assertTemplateUsed(
            response, "app_tracker/sshconnection_confirm_delete.html"
        )

    def test_post_deletes_connection(self):
        self.login()
        conn_pk = self.conn.pk
        response = self.client.post(
            reverse("app_tracker:ssh_connection_delete", args=[self.conn.pk])
        )
        self.assertRedirects(response, reverse("app_tracker:ssh_connection_list"))
        self.assertFalse(SSHConnection.objects.filter(pk=conn_pk).exists())


# ---------------------------------------------------------------------------
# Dashboard integration tests
# ---------------------------------------------------------------------------


class DashboardSSHConnectionTest(SSHConnectionViewTestBase):
    """
    Tests for SSH connection data on the dashboard.
    """

    def test_dashboard_has_total_ssh_connections_context(self):
        self.login()
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertIn("total_ssh_connections", response.context)

    def test_dashboard_total_ssh_connections_count(self):
        self.login()
        # setUp already created 1 connection
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.context["total_ssh_connections"], 1)

    def test_dashboard_total_ssh_connections_reflects_new(self):
        self.login()
        server2 = make_host("Server3", "server3", "10.2.2.1")
        client2 = make_host("Client3", "client3", "10.2.2.2")
        make_ssh_connection(server=server2, client=client2)
        response = self.client.get(reverse("app_tracker:dashboard"))
        self.assertEqual(response.context["total_ssh_connections"], 2)


# ---------------------------------------------------------------------------
# Host detail integration tests
# ---------------------------------------------------------------------------


class HostDetailSSHConnectionTest(SSHConnectionViewTestBase):
    """
    Tests for SSH connections shown on the host detail view.
    """

    def test_host_detail_shows_incoming_connections(self):
        """Server's detail page should list connections where it's the server."""
        self.login()
        response = self.client.get(
            reverse("app_tracker:host_detail", args=[self.server.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "client-host")

    def test_host_detail_shows_outgoing_connections(self):
        """Client's detail page should list connections where it's the client."""
        self.login()
        response = self.client.get(
            reverse("app_tracker:host_detail", args=[self.client_host.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "server-host")
