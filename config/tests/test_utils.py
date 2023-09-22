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

    def test_get_database_config_variables_invalid_url(self):
        """
        `get_database_config_variables` function should raise an
        `IndexError` for an invalid `DATABASE_URL`.
        """
        test_url = "invalid_url"

        with self.assertRaises(IndexError):
            get_database_config_variables(test_url)

    # Add more edge cases or invalid inputs here
