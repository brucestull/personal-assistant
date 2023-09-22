# Forbidden Views

- A forbidden view can be specific to each application:
    - `accounts.views.forbidden_view`
    - `app_tracker.views.forbidden_view`
    - ...

Sample views:

```python
from django.http import HttpResponseForbidden

def forbidden_view(request):
    return HttpResponseForbidden()
```

```python
from django.views.generic import TemplateView

class ForbiddenView(TemplateView):
    """
    View for the 403 Forbidden page.
    """

    template_name = "403.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Forbidden"
        context["the_site_name"] = THE_SITE_NAME
        return context
```
