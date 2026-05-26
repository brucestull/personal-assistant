# Base App Overview

The `base` Django app provides shared abstract models, view mixins, function-based view
decorators, DRF permissions, and management commands that are intended to be **reused
across all other apps** in the project.  Nothing in `base` has its own database table
(all models are `abstract = True`) unless a concrete child class is created elsewhere.

---

## Abstract Models (`base/models.py`)

### `CreatedUpdatedBase`

| Field | Type | Notes |
|---|---|---|
| `created` | `DateTimeField` | Auto-set on creation (`auto_now_add=True`) |
| `updated` | `DateTimeField` | Auto-updated on save (`auto_now=True`) |

**Purpose:** The root abstract model.  Every model that needs automatic `created` /
`updated` timestamps should inherit from this class (directly or via another abstract
child such as `Note`, `URL`, or `WorkspaceOwnedBase`).

**Usage in the project:** Nearly every concrete model in every app inherits from this
class, either directly or via one of the child abstracts below.

---

### `Note(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `title` | `CharField(255)` | Required |
| `content` | `TextField` | Optional (blank allowed) |
| `url` | `URLField` | Optional reference URL |
| `main_image` | `ImageField` | Optional image; `upload_to="test_uploads/"` |

**Key methods:**

| Method | Description |
|---|---|
| `display_content()` | Returns `content[:30]` with trailing `"..."` if truncated. Useful in admin list displays. |
| `__str__()` | Returns `"{title} - {content[:50]}..."` |

**Meta:** `abstract = True` — child classes must declare `verbose_name`,
`verbose_name_plural`, and `ordering`.

**Usage in the project:** Inherited by `story_line.StoryLineNote` and
`unimportant_notes.UnimportantNote` (which overrides `main_image` with its own
`upload_to` path).

---

### `URL(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `url` | `URLField(2000)` | Required |
| `label` | `CharField(100)` | Human-readable name |
| `description` | `TextField` | Optional |
| `url_type` | `CharField(20)` | Choices: `documentation`, `repository`, `api`, `demo`, `production`, `staging`, `development`, `tutorial`, `reference`, `other` |

**Key methods:**

| Method | Description |
|---|---|
| `__str__()` | Returns `"{label} ({url_type})"` |

**Meta:** `abstract = True`; default `ordering = ["label"]`.

**Usage in the project:** Inherited by `app_tracker.URL`, which adds a FK to
`app_tracker.Application`.

---

### `WorkspaceOwnedBase(CreatedUpdatedBase)`

| Field | Type | Notes |
|---|---|---|
| `workspace` | `ForeignKey("core.Workspace")` | Required; `CASCADE` on delete; `related_name="%(class)ss"` |

**Meta:** `abstract = True`.

**Usage in the project:** Prepared for a future `core` app with a `Workspace` model.
Not yet used by any concrete app.

---

## View Mixins (`base/mixins.py`)

All mixins are for Django **class-based views**.

### `UserQuerySetMixin`

```python
def get_queryset(self):
    return self.model.objects.filter(user=self.request.user)
```

**Purpose:** Restricts `ListView` / `DetailView` querysets to objects owned by the
currently logged-in user.  Drop-in for any CBV that has a `user` FK on its model.

---

### `UserAssignMixin`

```python
def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
```

**Purpose:** Automatically sets `form.instance.user` to the current user before saving
in `CreateView` / `UpdateView`, so the form does not need a user field.

---

### `RegistrationAcceptedMixin(AccessMixin)`

**Purpose:** Gate CBV access behind two checks:

1. User must be authenticated (redirects to login page on failure via `handle_no_permission()`).
2. `request.user.registration_accepted` must be `True` (raises `PermissionDenied` — HTTP 403 — on failure).

Used on virtually every CBV throughout the project to enforce the registration-accepted
workflow.

---

### `UserIsAuthorMixin(AccessMixin)`

**Purpose:** Raises `PermissionDenied` (HTTP 403) if `request.user != self.get_object().author`.
Used to prevent a user from editing or deleting another user's objects.

---

### `OrderableMixin`

```python
@classmethod
def reorder_all(cls, queryset=None, **scope_filters):
    ...
```

**Purpose:** Adds a `reorder_all()` class method to any model with an integer `order`
field.  Calling it re-numbers all matching rows (`0, 1, 2, …`) in `order` / `pk` order,
fixing gaps created by deletions.  Accepts optional `scope_filters` kwargs (e.g.
`user_id=…`) to narrow the reorder to a single owner.

**Usage in the project:** Inherited by `true_north.CoreValue`, `true_north.Goal`,
`true_north.Milestone`, and `true_north.ValueAction`.

---

### `SiteContextMixin`

| Attribute / Method | Description |
|---|---|
| `page_title: str \| None` | Class attribute — override to set a custom page title |
| `get_page_title()` | Returns `page_title` or the class name with `"View"` stripped |
| `get_site_name()` | Returns `settings.THE_SITE_NAME` (falls back to `"Personal Assistant"`) |
| `get_context_data(**kwargs)` | Injects `the_site_name` and `page_title` into template context via `setdefault` |

**Purpose:** Ensures every CBV automatically passes `the_site_name` and `page_title` to
its template without requiring repetitive `get_context_data` overrides.

---

## Decorators (`base/decorators.py`)

### `@registration_accepted_required`

```python
def registration_accepted_required(view_func):
    ...
```

**Purpose:** Function-based-view (FBV) equivalent of `RegistrationAcceptedMixin`.
Wraps an FBV and checks:

1. User must be authenticated — returns `render(request, "403.html", …, status=403)` on failure.
2. `request.user.registration_accepted` must be `True` — returns the same 403 response on failure.

**Use this decorator on FBVs; use `RegistrationAcceptedMixin` on CBVs.**

---

## DRF Permission (`base/permissions.py`)

### `RegistrationAcceptedPermission(BasePermission)`

```python
def has_permission(self, request, view):
    return (
        request.user.is_authenticated
        and getattr(request.user, "registration_accepted", False)
    )
```

**Purpose:** Django REST Framework permission class.  Apply to API views that should
only be accessible to users whose registration has been accepted.

---

## Management Commands (`base/management/commands/`)

### `max_pk`

```bash
python manage.py max_pk app_label.ModelName
# or
python manage.py max_pk app_label ModelName
```

**Purpose:** Prints the highest primary-key value for any model.  Useful for
diagnosing ID gaps (e.g. after bulk deletes) or verifying data after migrations.

---

## Summary Table

| Component | Location | Type | Purpose |
|---|---|---|---|
| `CreatedUpdatedBase` | `base/models.py` | Abstract model | `created` / `updated` timestamps |
| `Note` | `base/models.py` | Abstract model | Reusable note with title, content, URL, image |
| `URL` | `base/models.py` | Abstract model | Reusable typed URL record |
| `WorkspaceOwnedBase` | `base/models.py` | Abstract model | Workspace FK (future use) |
| `UserQuerySetMixin` | `base/mixins.py` | CBV mixin | Filter queryset to current user |
| `UserAssignMixin` | `base/mixins.py` | CBV mixin | Auto-assign current user on save |
| `RegistrationAcceptedMixin` | `base/mixins.py` | CBV mixin | Enforce registration-accepted check |
| `UserIsAuthorMixin` | `base/mixins.py` | CBV mixin | Enforce author-only access |
| `OrderableMixin` | `base/mixins.py` | Model + CBV mixin | `reorder_all()` for orderable models |
| `SiteContextMixin` | `base/mixins.py` | CBV mixin | Inject site name + page title into context |
| `registration_accepted_required` | `base/decorators.py` | FBV decorator | Enforce registration-accepted check (FBV) |
| `RegistrationAcceptedPermission` | `base/permissions.py` | DRF permission | Enforce registration-accepted check (API) |
| `max_pk` | `base/management/commands/max_pk.py` | Management command | Print max PK for any model |
