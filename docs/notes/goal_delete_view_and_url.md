# Goal DeleteView and URL

## Prompt

Here are my current urls:

```python
from django.urls import path

from . import views

app_name = "uc_goals"
urlpatterns = [
    path("create/", views.GoalCreateView.as_view(), name="goal_create"),
    path("<int:pk>/", views.GoalDetailView.as_view(), name="goal_detail"),
    path("<int:pk>/update/", views.GoalUpdateView.as_view(), name="goal_update"),
    path("ucs/", views.ultimate_concerns, name="uc_list"),
    path("orphans/", views.orphan_goals, name="orphan_list"),
]
```

Please help me create a class-based "GoalDeleteView" with a confirm reroute page, please?

## Response

Here's a `GoalDeleteView` using Django's `DeleteView`, which includes a confirmation page before deleting the goal. The user will be redirected to a success URL after deletion.

### 1. **Update `views.py`**
Add the `GoalDeleteView`:

```python
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Goal

class GoalDeleteView(DeleteView):
    model = Goal
    template_name = "uc_goals/goal_confirm_delete.html"
    success_url = reverse_lazy("uc_goals:uc_list")  # Redirect after deletion
```

- The `template_name` points to a confirmation page.
- The `success_url` redirects users to the `"uc_goals:uc_list"` after deletion.

---

### 2. **Update `urls.py`**
Add the new URL pattern for deleting a goal:

```python
urlpatterns += [
    path("<int:pk>/delete/", views.GoalDeleteView.as_view(), name="goal_delete"),
]
```

---

### 3. **Create the Confirmation Template (`goal_confirm_delete.html`)**
In your `uc_goals/templates/uc_goals/` directory, create a `goal_confirm_delete.html` file:

```html
{% extends "base.html" %}

{% block content %}
  <h2>Confirm Goal Deletion</h2>
  <p>Are you sure you want to delete the goal: "{{ object }}"?</p>

  <form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
    <a href="{% url 'uc_goals:goal_detail' object.pk %}">Cancel</a>
  </form>
{% endblock %}
```

---

This will:
- Show a confirmation page before deleting.
- Use a `POST` request to confirm deletion (preventing accidental deletion via GET requests).
- Redirect to the goal details page if the user cancels.

Would you like any modifications to the success redirection behavior? 🚀
