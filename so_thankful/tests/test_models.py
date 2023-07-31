# Test so_thankful.models
# Path: so_thankful\tests\test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import models as d_db_models

from so_thankful.models import Strength, Gratitude, LovedOne

BLANK = ""

TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass123"
TEST_FIRST_NAME = "Test"

TEST_STRENGTH_DESCRIPTION = "Test Strength"
TEST_STRENGTH_DESCRIPTION_MAX_LENGTH = 200
TEST_STRENGTH_USER_RELATED_NAME = "strengths"

TEST_GRATITUDE_DESCRIPTION = "Test Gratitude"
TEST_GRATITUDE_DESCRIPTION_MAX_LENGTH = 200
TEST_GRATITUDE_USER_RELATED_NAME = "gratitudes"

TEST_LOVED_ONE_NAME = "Test Loved One"
TEST_LOVED_ONE_NAME_MAX_LENGTH = 200
TEST_LOVED_ONE_USER_RELATED_NAME = "loved_ones"


class StrengthModelTest(TestCase):
    """
    Test Strength model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for whole testcase.
        """
        cls.test_user = get_user_model().objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.test_strength = Strength.objects.create(
            description=TEST_STRENGTH_DESCRIPTION,
            user=cls.test_user,
        )

    def test_strength_description_label(self):
        """
        Test `Strength.description` label.
        """
        strength = Strength.objects.get(id=1)
        field_label = strength._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_strength_description_max_length(self):
        """
        Test `Strength.description` max_length.
        """
        strength = Strength.objects.get(id=1)
        max_length = strength._meta.get_field("description").max_length
        self.assertEqual(max_length, TEST_STRENGTH_DESCRIPTION_MAX_LENGTH)

    def test_strength_user_label(self):
        """
        Test `Strength.user` label.
        """
        strength = Strength.objects.get(id=self.test_strength.id)
        field_label = strength._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_strength_user_on_delete_cascade(self):
        """
        Test `Strength.user` on_delete CASCADE.
        """
        strength = Strength.objects.get(id=self.test_strength.id)
        on_delete = strength._meta.get_field("user").remote_field.on_delete
        self.assertEqual(on_delete, d_db_models.CASCADE)

    def test_strength_user_related_name(self):
        """
        Test `Strength.user` related_name.
        """
        strength = Strength.objects.get(id=self.test_strength.id)
        related_name = strength._meta.get_field("user").remote_field.related_name
        self.assertEqual(related_name, TEST_STRENGTH_USER_RELATED_NAME)

    def test_strength_dunder_str(self):
        """
        Test `Strength.__str__`.
        """
        strength = Strength.objects.get(id=self.test_strength.id)
        self.assertEqual(
            str(strength),
            f"{self.test_user.username} - {TEST_STRENGTH_DESCRIPTION}",
        )


class GratitudeModelTest(TestCase):
    """
    Test Gratitude model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for whole testcase.
        """
        cls.test_user = get_user_model().objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.test_gratitude = Gratitude.objects.create(
            description=TEST_GRATITUDE_DESCRIPTION,
            user=cls.test_user,
        )

    def test_gratitude_description_label(self):
        """
        Test `Gratitude.description` label.
        """
        gratitude = Gratitude.objects.get(id=1)
        field_label = gratitude._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_gratitude_description_max_length(self):
        """
        Test `Gratitude.description` max_length.
        """
        gratitude = Gratitude.objects.get(id=1)
        max_length = gratitude._meta.get_field("description").max_length
        self.assertEqual(max_length, TEST_GRATITUDE_DESCRIPTION_MAX_LENGTH)

    def test_gratitude_user_label(self):
        """
        Test `Gratitude.user` label.
        """
        gratitude = Gratitude.objects.get(id=self.test_gratitude.id)
        field_label = gratitude._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_gratitude_user_on_delete_cascade(self):
        """
        Test `Gratitude.user` on_delete CASCADE.
        """
        gratitude = Gratitude.objects.get(id=self.test_gratitude.id)
        on_delete = gratitude._meta.get_field("user").remote_field.on_delete
        self.assertEqual(on_delete, d_db_models.CASCADE)

    def test_gratitude_user_related_name(self):
        """
        Test `Gratitude.user` related_name.
        """
        gratitude = Gratitude.objects.get(id=self.test_gratitude.id)
        related_name = gratitude._meta.get_field("user").remote_field.related_name
        self.assertEqual(related_name, TEST_GRATITUDE_USER_RELATED_NAME)

    def test_gratitude_dunder_str(self):
        """
        Test `Gratitude.__str__`.
        """
        gratitude = Gratitude.objects.get(id=self.test_gratitude.id)
        self.assertEqual(
            str(gratitude),
            f"{self.test_user.username} - {TEST_GRATITUDE_DESCRIPTION}",
        )


class LovedOneModelTest(TestCase):
    """
    Test LovedOne model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for whole testcase.
        """
        cls.test_user = get_user_model().objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.test_loved_one = LovedOne.objects.create(
            name=TEST_LOVED_ONE_NAME,
            user=cls.test_user,
        )

    def test_loved_one_name_label(self):
        """
        Test `LovedOne.name` label.
        """
        loved_one = LovedOne.objects.get(id=1)
        field_label = loved_one._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_loved_one_name_max_length(self):
        """
        Test `LovedOne.name` max_length.
        """
        loved_one = LovedOne.objects.get(id=1)
        max_length = loved_one._meta.get_field("name").max_length
        self.assertEqual(max_length, TEST_LOVED_ONE_NAME_MAX_LENGTH)

    def test_loved_one_user_label(self):
        """
        Test `LovedOne.user` label.
        """
        loved_one = LovedOne.objects.get(id=self.test_loved_one.id)
        field_label = loved_one._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_loved_one_user_on_delete_cascade(self):
        """
        Test `LovedOne.user` on_delete CASCADE.
        """
        loved_one = LovedOne.objects.get(id=self.test_loved_one.id)
        on_delete = loved_one._meta.get_field("user").remote_field.on_delete
        self.assertEqual(on_delete, d_db_models.CASCADE)

    def test_loved_one_user_related_name(self):
        """
        Test `LovedOne.user` related_name.
        """
        loved_one = LovedOne.objects.get(id=self.test_loved_one.id)
        related_name = loved_one._meta.get_field("user").remote_field.related_name
        self.assertEqual(related_name, TEST_LOVED_ONE_USER_RELATED_NAME)

    def test_loved_one_dunder_str(self):
        """
        Test `LovedOne.__str__`.
        """
        loved_one = LovedOne.objects.get(id=self.test_loved_one.id)
        self.assertEqual(
            str(loved_one),
            f"{self.test_user.username} - {TEST_LOVED_ONE_NAME}",
        )

