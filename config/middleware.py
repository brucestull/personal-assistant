# config/middleware.py
from django.conf import settings
from django.shortcuts import render


class SuperuserMaintenanceMiddleware:
    """
    If MAINTENANCE_MODE is on, only allow Django superusers to access.
    Everybody else gets a 503 with a maintenance page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass for:
        #  - staff logged in via admin (superusers are staff + is_superuser)
        #  - any URL you want always public (e.g. health checks)
        always_allowed = [
            "/accounts/login/",  # e.g. "/accounts/login/"
            "/accounts/logout/",  # e.g. "/accounts/logout/"
            "/admin/login/",  # admin login form
            "/admin/logout/",  # admin logout
            "/health-check/",
            "/static/",
            "/favicon.ico",
        ]
        path = request.path_info
        if settings.MAINTENANCE_MODE and not any(
            path.startswith(u) for u in always_allowed
        ):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated and user.is_superuser):
                # Option A: return a simple text response
                # return HttpResponseServiceUnavailable("Site is under maintenance", content_type="text/plain") # noqa E501

                # Option B: render a nice maintenance template
                return render(request, "503_maintenance.html", status=503)

        return self.get_response(request)
