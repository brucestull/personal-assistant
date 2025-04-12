# Custom 403 Server Error Page

## Code Snippets

* [`templates/403.html`](../templates/403.html)

    ```html
    <h1>My Totally custom 403 page, NOICE!</h1>
        <p>Sorry, {{ user.username }}, you are not allowed to access this page.</p>
        <p>Perhaps, <a href="{% url 'login' %}">login</a> as a user who has their Registration Accepted, or contact the site administrator.</p>
    ```

* [`boosts/views.py`](../boosts/views.py)

    ```python
    from config.settings import THE_SITE_NAME


    class ForbiddenView(TemplateView):
        """
        View for the 403 Forbidden page.
        """

        # Define the template used by this view
        # This template is located at `templates/403.html`
        template_name = "403.html"

        # Override the `get_context_data` method to add the page title and the site name to the context:
        def get_context_data(self, **kwargs):
            """
            Add the page title and the site name to the context.
            """
            context = super().get_context_data(**kwargs)
            context["page_title"] = "Forbidden"
            context["the_site_name"] = THE_SITE_NAME
            return context
    ```

* [`boosts/urls.py`](../boosts/urls.py)

    ```python
    from django.urls import path

    from . import views

    # ...

    # Define the URL patterns for the `boosts` app:
    urlpatterns = [
        # ...
        path(
            '403/',
            views.ForbiddenView.as_view(),
            name='forbidden',
        ),
        # ...
    ]
    ```