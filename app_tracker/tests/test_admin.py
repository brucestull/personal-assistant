from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser

from app_tracker.models import LanguageFrameworkSystem, Application, Note, DjangoModel


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            is_staff=True,
        )
        cls.client.login(username='testuser', password='testpass')
        cls.lfs = LanguageFrameworkSystem.objects.create(name='Test LFS')
        cls.app = Application.objects.create(
            name='Test App',
            description='Test Description',
            repository_url='https://github.com/testuser/testrepo',
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level='UNIT',
        )
        cls.note = Note.objects.create(
            title='Test Note',
            content='Test Content',
            application=cls.app,
        )
        cls.model = DjangoModel.objects.create(
            name='Test Model',
            description='Test Description',
            is_current_model=True,
            application=cls.app,
        )

    def test_language_framework_system_admin(self):
        response = self.client.get(reverse('admin:app_tracker_languageframeworksystem_change', args=[self.lfs.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test LFS')

    def test_application_admin(self):
        response = self.client.get(reverse('admin:app_tracker_application_change', args=[self.app.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test App')

    def test_note_admin(self):
        response = self.client.get(reverse('admin:app_tracker_note_change', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'Test Content')

    def test_django_model_admin(self):
        response = self.client.get(reverse('admin:app_tracker_djangomodel_change', args=[self.model.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Model')