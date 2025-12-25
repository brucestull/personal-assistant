from django.test import TestCase

from config.utils import get_database_config_variables


class TestUtils(TestCase):
    """
    Tests for the `get_database_config_variables` function.
    """

    def test_get_database_config_variables(self):
        """
        `get_database_config_variables` function should return the
        correct dictionary for a valid `DATABASE_URL`.
        """
        test_url = "postgres://username:password@localhost:5432/mydatabase"

        expected_output = {
            "DATABASE_USER": "username",
            "DATABASE_PASSWORD": "password",
            "DATABASE_HOST": "localhost",
            "DATABASE_PORT": "5432",
            "DATABASE_NAME": "mydatabase",
        }

        self.assertEqual(
            get_database_config_variables(test_url),
            expected_output,
        )

    def test_get_database_config_variables_postgresql_scheme(self):
        """
        `get_database_config_variables` should handle postgresql:// scheme.
        """
        test_url = "postgresql://username:password@localhost:5432/mydatabase"

        expected_output = {
            "DATABASE_USER": "username",
            "DATABASE_PASSWORD": "password",
            "DATABASE_HOST": "localhost",
            "DATABASE_PORT": "5432",
            "DATABASE_NAME": "mydatabase",
        }

        self.assertEqual(
            get_database_config_variables(test_url),
            expected_output,
        )

    def test_get_database_config_variables_with_special_chars(self):
        """
        `get_database_config_variables` should handle percent-encoded
        special characters in username and password.
        """
        # password is "p@ss:word"
        test_url = "postgres://user:p%40ss%3Aword@localhost:5432/mydatabase"
        result = get_database_config_variables(test_url)
        self.assertEqual(result["DATABASE_USER"], "user")
        self.assertEqual(result["DATABASE_PASSWORD"], "p@ss:word")
        self.assertEqual(result["DATABASE_HOST"], "localhost")
        self.assertEqual(result["DATABASE_PORT"], "5432")
        self.assertEqual(result["DATABASE_NAME"], "mydatabase")

    def test_get_database_config_variables_with_query_params(self):
        """
        `get_database_config_variables` should handle query parameters
        like ?sslmode=require.
        """
        test_url = "postgres://user:pass@localhost:5432/mydatabase?sslmode=require"
        result = get_database_config_variables(test_url)
        self.assertEqual(result["DATABASE_USER"], "user")
        self.assertEqual(result["DATABASE_PASSWORD"], "pass")
        self.assertEqual(result["DATABASE_HOST"], "localhost")
        self.assertEqual(result["DATABASE_PORT"], "5432")
        self.assertEqual(result["DATABASE_NAME"], "mydatabase")
        self.assertIn("OPTIONS", result)
        self.assertEqual(result["OPTIONS"]["sslmode"], ["require"])

    def test_get_database_config_variables_default_port(self):
        """
        `get_database_config_variables` should default to port 5432
        when not specified.
        """
        test_url = "postgres://username:password@localhost/mydatabase"
        result = get_database_config_variables(test_url)
        self.assertEqual(result["DATABASE_PORT"], "5432")

    def test_get_database_config_variables_empty_url(self):
        """
        `get_database_config_variables` should raise ValueError
        for an empty URL.
        """
        with self.assertRaises(ValueError) as cm:
            get_database_config_variables("")
        self.assertIn("database_url is required", str(cm.exception))

    def test_get_database_config_variables_invalid_scheme(self):
        """
        `get_database_config_variables` should raise ValueError
        for unsupported database schemes.
        """
        test_url = "mysql://username:password@localhost:3306/mydatabase"
        with self.assertRaises(ValueError) as cm:
            get_database_config_variables(test_url)
        self.assertIn("Unsupported database scheme", str(cm.exception))

    def test_get_database_config_variables_missing_dbname(self):
        """
        `get_database_config_variables` should raise ValueError
        when database name is missing.
        """
        test_url = "postgres://username:password@localhost:5432/"
        with self.assertRaises(ValueError) as cm:
            get_database_config_variables(test_url)
        self.assertIn("missing database name", str(cm.exception))

    # Add more edge cases or invalid inputs here
