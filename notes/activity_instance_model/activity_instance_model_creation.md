# ActivityInstance Model Creation

- [ActivityInstance Model Creation - Private ChatGPT](https://chatgpt.com/c/682a7a85-7574-8002-82d2-82420818067c)

I have an `Activity` Django model. Create an `ActivityInstance` to record when an `Activity` has been completed. The `ActivityInstance` should record the current (at time of completion) actual string values of the `Activity,name`, `Activity.type.name`, `Activity.target_item.name`, `Activity.activity_location.name`, and the time the activity is completed.

```python
# plan_it/models.py

from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class StorageLocation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="storage_locations"
    )
    name = models.CharField(max_length=100)
    parent_location = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="sublocations",
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("plan_it:storage_location_list")

    def __str__(self):
        return (
            self.name
            if not self.parent_location
            else f"{self.parent_location} > {self.name}"
        )


class ActivityLocation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_locations"
    )
    name = models.CharField(max_length=100)
    parent_location = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="sublocations",
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("plan_it:activity_location_list")

    def __str__(self):
        return (
            self.name
            if not self.parent_location
            else f"{self.parent_location} > {self.name}"
        )

    @property
    def depth(self):
        level = 0
        current = self.parent_location
        while current:
            level += 1
            current = current.parent_location
        return level


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("plan_it:item_list")

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="plan_it_activity_types"
    )
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("plan_it:activity_type_list")

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="plan_it_activities"
    )
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    target_item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.CASCADE
    )
    activity_location = models.ForeignKey(
        ActivityLocation, null=True, blank=True, on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    last_completed = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("plan_it:activity_list")

    def __str__(self):
        return f"{self.name}[{self.activity_location}]"

    def due_status(self):
        if not self.due_date:
            return "none"
        today = date.today()
        if self.due_date < today:
            return "overdue"
        elif self.due_date == today:
            return "today"
        else:
            return "upcoming"

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
```

`plan_it/templates/plan_it/activity_list.html`:

```html
{% extends "plan_it/plan_it_base.html" %}

{% block title %}
    {{ page_title }}
    -
    {{ the_site_name }}
{% endblock title %}

{% block content %}
<div class="container py-4">
    <h1 class="mb-4">Activities</h1>

    <div class="mb-3">
        <a href="{% url 'plan_it:activity_add' %}" class="btn btn-primary">➕ Add Activity</a>
    </div>

    {% if object_list %}
        <ul class="list-group">
            {% for activity in object_list %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    {{ activity }}{% if activity.due_date %} - Due: {{ activity.due_date }}{% endif %}
                    <div>
                        <a href="{% url 'plan_it:activity_edit' activity.pk %}" class="btn btn-sm btn-outline-secondary">Edit</a>
                        <a href="{% url 'plan_it:activity_delete' activity.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
                    </div>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p class="text-muted">No activities found.</p>
    {% endif %}
</div>
{% endblock %}
```

```python
# plan_it/views.py

from collections import defaultdict
from datetime import date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .models import Activity, ActivityLocation, ActivityType, Item, StorageLocation


@registration_accepted_required
def dashboard(request):
    today = date.today()

    all_activities = (
        Activity.objects.filter(user=request.user)
        .select_related("activity_location", "target_item")
        .order_by("due_date")
    )

    grouped_activities = defaultdict(list)
    for activity in all_activities:
        loc = activity.activity_location
        grouped_activities[loc].append(activity)

    top_locations = ActivityLocation.objects.filter(
        user=request.user, parent_location__isnull=True
    ).prefetch_related("sublocations")

    items = Item.objects.filter(user=request.user).select_related("storage_location")[
        :10
    ]

    return render(
        request,
        "plan_it/dashboard.html",
        {
            "grouped_activities": grouped_activities,
            "top_locations": top_locations,
            "items": items,
            "today": today,
            "page_title": "Plan It Dashboard",
            "the_site_name": THE_SITE_NAME,
        },
    )


# Generic mixins
class UserQuerySetMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserAssignMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ---- StorageLocation Views ----
class StorageLocationListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = StorageLocation
    extra_context = {
        "page_title": "Storage Locations",
        "the_site_name": THE_SITE_NAME,
    }


class StorageLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = StorageLocation
    fields = ["name", "parent_location"]
    extra_context = {
        "page_title": "Create Storage Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class StorageLocationUpdateView(StorageLocationCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Storage Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


class StorageLocationDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = StorageLocation
    success_url = reverse_lazy("plan_it:storage_location_list")


# ---- ActivityLocation Views ----
class ActivityLocationListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityLocation
    extra_context = {
        "page_title": "Activity Locations",
        "the_site_name": THE_SITE_NAME,
    }


class ActivityLocationCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityLocation
    fields = ["name", "parent_location"]
    extra_context = {
        "page_title": "Create Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["parent_location"].queryset = ActivityLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityLocationUpdateView(ActivityLocationCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


class ActivityLocationDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = ActivityLocation
    extra_context = {
        "page_title": "Delete Activity Location",
        "the_site_name": THE_SITE_NAME,
        "mode": "delete",
    }
    success_url = reverse_lazy("plan_it:activity_location_list")


# ---- Item Views ----
class ItemListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Item
    extra_context = {
        "page_title": "Items",
        "the_site_name": THE_SITE_NAME,
    }


class ItemCreateView(RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView):
    model = Item
    fields = ["name", "storage_location", "description"]
    extra_context = {
        "page_title": "Create Item",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["storage_location"].queryset = StorageLocation.objects.filter(
            user=self.request.user
        )
        return form


class ItemUpdateView(ItemCreateView, generic.UpdateView):
    extra_context = {
        "page_title": "Update Item",
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }


class ItemDeleteView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy("plan_it:item_list")


# ---- ActivityType Views ----
class ActivityTypeListView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView
):
    model = ActivityType
    extra_context = {
        "page_title": "Activity Types",
        "the_site_name": THE_SITE_NAME,
    }


class ActivityTypeCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = ActivityType
    fields = ["name"]
    extra_context = {
        "page_title": "Create Activity Type",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }


class ActivityTypeUpdateView(ActivityTypeCreateView, generic.UpdateView):
    pass


class ActivityTypeDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = ActivityType
    success_url = reverse_lazy("plan_it:activity_type_list")


# ---- Activity Views ----
class ActivityListView(RegistrationAcceptedMixin, UserQuerySetMixin, generic.ListView):
    model = Activity
    extra_context = {
        "page_title": "Activities",
        "the_site_name": THE_SITE_NAME,
    }


class ActivityCreateView(
    RegistrationAcceptedMixin, UserAssignMixin, generic.CreateView
):
    model = Activity
    fields = [
        "name",
        "type",
        "target_item",
        "activity_location",
        "description",
        "due_date",
        "is_recurring",
        "last_completed",
    ]
    extra_context = {
        "page_title": "Create Activity",
        "the_site_name": THE_SITE_NAME,
        "mode": "create",
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["type"].queryset = ActivityType.objects.filter(
            user=self.request.user
        )
        form.fields["target_item"].queryset = Item.objects.filter(
            user=self.request.user
        )
        form.fields["activity_location"].queryset = ActivityLocation.objects.filter(
            user=self.request.user
        )
        return form


class ActivityUpdateView(ActivityCreateView, generic.UpdateView):
    pass


class ActivityDeleteView(
    RegistrationAcceptedMixin, UserQuerySetMixin, generic.DeleteView
):
    model = Activity
    extra_context = {
        "page_title": "Delete Activity",
        "the_site_name": THE_SITE_NAME,
        "mode": "delete",
    }
    success_url = reverse_lazy("plan_it:activity_list")
```

To track when an `Activity` is completed and to record a snapshot of its details at that time, you can add an `ActivityInstance` model like this:

---

### ✅ Add `ActivityInstance` model

```python
# plan_it/models.py (add at the bottom)

from django.utils.timezone import now

class ActivityInstance(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_instances"
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="instances", help_text="Reference to original activity"
    )
    name_snapshot = models.CharField(max_length=100)
    type_name_snapshot = models.CharField(max_length=50)
    target_item_name_snapshot = models.CharField(max_length=100, blank=True)
    activity_location_name_snapshot = models.CharField(max_length=100, blank=True)
    completed_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name_snapshot} @ {self.completed_at.strftime('%Y-%m-%d %H:%M')}"
```

---

### ✅ Create a method to record an instance

In `Activity`, you can add:

```python
# inside Activity model
def record_completion(self, user):
    from .models import ActivityInstance  # avoid circular import

    instance = ActivityInstance.objects.create(
        user=user,
        activity=self,
        name_snapshot=self.name,
        type_name_snapshot=self.type.name,
        target_item_name_snapshot=self.target_item.name if self.target_item else "",
        activity_location_name_snapshot=self.activity_location.name if self.activity_location else "",
    )
    self.last_completed = instance.completed_at.date()
    self.save(update_fields=["last_completed"])
    return instance
```

---

### ✅ Run migration

```bash
python manage.py makemigrations plan_it
python manage.py migrate
```

---

### ✅ Optional: Add admin panel support

```python
# plan_it/admin.py

from .models import ActivityInstance

@admin.register(ActivityInstance)
class ActivityInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "name_snapshot",
        "type_name_snapshot",
        "target_item_name_snapshot",
        "activity_location_name_snapshot",
        "completed_at",
    )
    list_filter = ("completed_at",)
    search_fields = ("name_snapshot", "type_name_snapshot")
```

---

Let me know if you’d like:

* A button in the UI to “mark activity as completed”
* Auto-refresh of dashboard stats after completion
* Display of recent completions in the dashboard

Why do you note `# avoid circular import` here:

```python
# plan_it/models.py
# ...
def record_completion(self, user):
    from .models import ActivityInstance  # avoid circular import
#...
```

Great question.

You see this comment:

```python
from .models import ActivityInstance  # avoid circular import
```

inside the `record_completion` method of the `Activity` model. It's **intentional** and necessary **to avoid a circular import error**, which would happen if we moved that import to the top of the file.

---

### 🔄 Why would a circular import happen?

If you define the `ActivityInstance` class **below** the `Activity` class in the same `models.py` file, and at the top you write:

```python
from .models import ActivityInstance
```

Python will try to import `ActivityInstance` *before it's been defined*, because Python executes the file from top to bottom. Since `ActivityInstance` hasn’t been reached yet, and you’re referencing it from inside the definition of `Activity`, it results in an `ImportError` or `NameError`.

---

### ✅ Solution: Import it locally inside the method

By doing:

```python
def record_completion(self, user):
    from .models import ActivityInstance
    ...
```

you delay the import until **after the file is fully loaded and all models are defined**. This avoids the circular reference and works fine as long as `record_completion` isn’t called during model class definition (which it isn’t).

---

### 🧠 TL;DR

* ✅ Local import is used to **defer evaluation**.
* 🔁 Circular import would occur if you imported `ActivityInstance` at the top while it hasn't been defined yet.
* 🛠 This trick is common in Django apps when methods in one model depend on other models in the same file.

---

Let me know if you'd rather move `ActivityInstance` to a separate file (`models/activity_instance.py`) and import it cleanly at the top — that’s also a clean and scalable alternative.

Why not put `Activity` above `ActivityInstance` and only put import at top?

Excellent instinct — and yes, in theory, **you *can*** define `Activity` *before* `ActivityInstance` and import normally from the top of the file like:

```python
from .models import ActivityInstance
```

However, here’s why that approach is *not always the best choice* and why I suggested the local import instead:

---

### ✅ Yes, you *can* avoid circular import by ordering classes

If you do this:

```python
class Activity(models.Model):
    ...
    def record_completion(self, user):
        from .models import ActivityInstance
```

➡️ You avoid the circular import *without* worrying about model order.

But you might say:

> “Why not just move `Activity` above `ActivityInstance` and avoid the whole issue?”

You can, but…

---

### ⚠️ Why we *don’t always* just move `Activity` above `ActivityInstance`

#### 1. **Readability and Logical Grouping**

* `ActivityInstance` is conceptually a *log* or *history* of `Activity`, not its peer.
* Keeping it grouped *below* the core model makes it easier to read and maintain.

#### 2. **File Organization**

* Moving models around based solely on import order breaks logical flow. It’s better to structure models by domain logic and avoid reordering everything for one import.

#### 3. **Scalability**

* As the app grows, you're more likely to split models into multiple files. At that point, local imports avoid reshuffling large files or creating hidden circular dependencies.

#### 4. **Future-Proofing**

* If `ActivityInstance` ever grows to depend on `Activity` again (which it might via `ForeignKey` or signals), moving `Activity` above may no longer prevent circular issues.

---

### 🧠 Best Practice Rule of Thumb

> Use **top-level imports when safe and clean**, but prefer **local imports** inside methods when:
>
> * You're working within the same file.
> * The model you're importing comes *after* in the same file.
> * You want to avoid reshuffling model order just for imports.

---

### ✅ Summary

| Strategy                                                 | Pros                                    | Cons                                                  |
| -------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------- |
| Move `Activity` above `ActivityInstance`                 | Cleaner import at top                   | Breaks logical grouping; fragile if structure changes |
| Use `from .models import ActivityInstance` inside method | Safe, avoids reordering, works reliably | Slightly less elegant, but pragmatic                  |

Let me know if you’d like to split the models into separate files for cleaner imports — that’s a great way to scale.

Add:

* A button in the UI to “mark activity as completed”
* Auto-refresh of dashboard stats after completion
* Display of recent completions in the dashboard

Here's how to implement your requested enhancements step by step:

---

## ✅ 1. Add “Mark as Completed” button in activity list

Update `plan_it/templates/plan_it/activity_list.html`:

```html
<div>
    <a href="{% url 'plan_it:activity_edit' activity.pk %}" class="btn btn-sm btn-outline-secondary">Edit</a>
    <a href="{% url 'plan_it:activity_delete' activity.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
    <form action="{% url 'plan_it:activity_complete' activity.pk %}" method="post" style="display: inline;">
        {% csrf_token %}
        <button type="submit" class="btn btn-sm btn-outline-success">✅ Complete</button>
    </form>
</div>
```

---

## ✅ 2. Add view to handle completion

In `plan_it/views.py`:

```python
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

@registration_accepted_required
def mark_activity_completed(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    if request.method == "POST":
        instance = activity.record_completion(user=request.user)
        messages.success(request, f"Activity '{activity.name}' marked as completed.")
        return redirect("plan_it:dashboard")

    return redirect("plan_it:activity_list")
```

---

## ✅ 3. Add route for the new view

In `plan_it/urls.py`:

```python
from . import views

urlpatterns = [
    # existing patterns...
    path("activities/<int:pk>/complete/", views.mark_activity_completed, name="activity_complete"),
]
```

---

## ✅ 4. Show recent completions in the dashboard

Update the `dashboard` view:

```python
from .models import ActivityInstance

@registration_accepted_required
def dashboard(request):
    today = date.today()

    all_activities = (
        Activity.objects.filter(user=request.user)
        .select_related("activity_location", "target_item")
        .order_by("due_date")
    )

    grouped_activities = defaultdict(list)
    for activity in all_activities:
        loc = activity.activity_location
        grouped_activities[loc].append(activity)

    top_locations = ActivityLocation.objects.filter(
        user=request.user, parent_location__isnull=True
    ).prefetch_related("sublocations")

    items = Item.objects.filter(user=request.user).select_related("storage_location")[:10]

    recent_completions = ActivityInstance.objects.filter(user=request.user).order_by("-completed_at")[:5]

    return render(
        request,
        "plan_it/dashboard.html",
        {
            "grouped_activities": grouped_activities,
            "top_locations": top_locations,
            "items": items,
            "recent_completions": recent_completions,
            "today": today,
            "page_title": "Plan It Dashboard",
            "the_site_name": THE_SITE_NAME,
        },
    )
```

---

## ✅ 5. Update dashboard template to show completions

In `plan_it/templates/plan_it/dashboard.html`, add:

```html
<h2 class="mt-5">✅ Recently Completed</h2>
<ul class="list-group mb-4">
    {% for instance in recent_completions %}
        <li class="list-group-item">
            {{ instance.name_snapshot }} @ {{ instance.completed_at|date:"Y-m-d H:i" }}
        </li>
    {% empty %}
        <li class="list-group-item text-muted">No completions yet.</li>
    {% endfor %}
</ul>
```

---

## ✅ 6. Auto-refresh dashboard (optional JS)

Add this at the bottom of `dashboard.html` to refresh every 90 seconds:

```html
<script>
    setTimeout(() => window.location.reload(), 90000);
</script>
```

(You can later replace this with AJAX/WebSocket if you prefer a smoother UX.)

---

Let me know if you'd like to:

* Include a modal confirmation before marking completed
* Filter recent completions by today/this week
* Add color-coded badges for recent completions

