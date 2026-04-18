from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings

from accounts.models import CustomUser
from config.middleware import SuperuserMaintenanceMiddleware


class SuperuserMaintenanceMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="normal", password="pw", registration_accepted=True
        )
        self.superuser = CustomUser.objects.create_superuser(
            username="admin", email="admin@example.com", password="pw"
        )

    @override_settings(MAINTENANCE_MODE=True)
    def test_blocks_non_superuser_during_maintenance(self):
        middleware = SuperuserMaintenanceMiddleware(lambda request: HttpResponse("ok"))
        request = self.factory.get("/protected/")
        request.user = self.user

        response = middleware(request)
        self.assertEqual(response.status_code, 503)

    @override_settings(MAINTENANCE_MODE=True)
    def test_allows_superuser_during_maintenance(self):
        middleware = SuperuserMaintenanceMiddleware(lambda request: HttpResponse("ok"))
        request = self.factory.get("/protected/")
        request.user = self.superuser

        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MAINTENANCE_MODE=True)
    def test_allows_whitelisted_paths(self):
        middleware = SuperuserMaintenanceMiddleware(lambda request: HttpResponse("ok"))
        request = self.factory.get("/accounts/login/")
        request.user = self.user

        response = middleware(request)
        self.assertEqual(response.status_code, 200)
