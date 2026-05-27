# Refactoring Recommendations

This document lists recommended code refactors for the **Personal Assistant** project.
No code changes are included here — these are observations and suggestions only.

---

## 1. Consolidate Timestamp Abstract Models

### Problem

`warcrafting` defines its own `TimeStampedModel` with `created` / `updated` fields that
is identical in purpose to `base.CreatedUpdatedBase`.  `kanban_cabinet.StockItem` also
uses its own raw `created_at` / `updated_at` fields instead of inheriting from
`base.CreatedUpdatedBase`.

### Recommendation

Replace the local `TimeStampedModel` in `warcrafting/models.py` and the bare timestamp
fields in `kanban_cabinet/models.py` with `base.CreatedUpdatedBase`.  This removes
duplication, ensures consistent field names (`created` / `updated`), and means those
models automatically benefit from any future enhancements to `CreatedUpdatedBase`.

---

## 2. Standardise User Field FK Declaration

### Problem

Different apps reference the current user model in inconsistent ways:

- Some use `from config.settings import AUTH_USER_MODEL` and then `AUTH_USER_MODEL` as
  the FK target string.
- Others use `from django.conf import settings` and `settings.AUTH_USER_MODEL`.
- A few use `from django.contrib.auth import get_user_model; User = get_user_model()` and
  then pass the class directly.

### Recommendation

Standardise on `settings.AUTH_USER_MODEL` (the string) passed as the `to` argument to
`ForeignKey`.  Using the string avoids circular import risks and is the Django-recommended
approach.  Update all apps to import `settings` from `django.conf` and use
`settings.AUTH_USER_MODEL` consistently.

---

## 3. Move `decide.Decision` Timestamps to `CreatedUpdatedBase`

### Problem

`decide.Decision` uses `created_at` (manually defined) while the project convention is
`created` / `updated` via `base.CreatedUpdatedBase`.  `decide.Prompt` and
`decide.DecisionResponse` use `answered_at` etc. but do not inherit from
`CreatedUpdatedBase`.

### Recommendation

Make `decide.Decision`, `decide.Prompt`, and `decide.DecisionResponse` inherit from
`base.CreatedUpdatedBase` and remove hand-rolled timestamp fields.  This aligns them
with the rest of the project.

---

## 4. Promote `true_north.UserOwnedBase` to `base`

### Problem

`true_north/models.py` defines a local `UserOwnedBase(CreatedUpdatedBase)` abstract
model that ties an object to a user via `AUTH_USER_MODEL`.  This pattern (user FK +
timestamps) is repeated manually in many other apps (`bus_drive`, `thoughts`,
`item_location`, `thing_thought_reminder`, etc.).

### Recommendation

Move `UserOwnedBase` to `base/models.py` (perhaps renamed `UserOwnedBase` or
`UserBase`).  Other apps can then inherit from it instead of declaring their own `user`
FK, reducing repetition and providing a single place to update the field definition if
needed.

---

## 5. Unify the "Thought" Model Naming

### Problem

Three separate apps each define a model called `Thought` for capturing free-form text:

- `thoughts.Thought` — `text` field, `related_name="thoughts"`
- `bus_drive.Thought` — `text` field, `related_name="bus_drive_thoughts"`
- `thing_thought_reminder.Thought` — `name` + `content` + `realm` fields, `related_name="ttr_thoughts"`

### Recommendation

Either:

1. Merge `thoughts.Thought` and `bus_drive.Thought` into a single app (since they are
   structurally almost identical), or
2. Add a `context` or `source` field to a shared model to distinguish the capture
   context (commute, general, etc.).

The `thing_thought_reminder.Thought` is richer (name, content, realm) and could remain
separate or be the canonical model that the simpler thought apps inherit from.

---

## 6. Extract `RegistrationAcceptedMixin` to `accounts` App

### Problem

`base/mixins.py` references `request.user.registration_accepted`, a field that is
specific to `accounts.CustomUser`.  The `base` app is intended to be a generic,
reusable layer that should not have knowledge of app-specific user fields.

### Recommendation

Move `RegistrationAcceptedMixin`, `RegistrationAcceptedPermission`, and
`registration_accepted_required` to `accounts/` (e.g.
`accounts/mixins.py`, `accounts/permissions.py`, `accounts/decorators.py`).  Update all
imports throughout the project accordingly.  This makes `base` truly generic and keeps
registration-specific logic inside the `accounts` domain.

---

## 7. Adopt `django.contrib.auth.get_user_model()` in Model Definitions

### Problem

Some models import and store the user model string at module level
(`from config.settings import AUTH_USER_MODEL`) then reference it later.  Others use
`get_user_model()` which returns a class.  Using `get_user_model()` at class definition
time (outside of `AppConfig.ready()`) can cause `AppRegistryNotReady` errors in some
contexts.

### Recommendation

Use the **string** form `settings.AUTH_USER_MODEL` consistently in all FK / M2M
`to` arguments, which is the officially documented Django approach for ForeignKey targets
and never triggers registry issues.  Reserve `get_user_model()` for use inside method
bodies (forms, views, tasks) where the app registry is guaranteed to be ready.

---

## 8. Eliminate Magic Constants in Settings

### Problem

`config/settings.py` contains a hardcoded insecure `SECRET_KEY` fallback:

```python
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-mm8cx0al6wo$$0hhv3&eevzsst9dbw&(5p$#9k(1rx%e@j+=$l",
)
```

Even though this is only active in non-production environments, it risks accidental
production exposure if the environment variable is ever unset.

### Recommendation

Remove the fallback default entirely.  In development, ensure the `SECRET_KEY` is
always present in `.env`.  If a truly safe default is needed for test/CI, generate a
random one at startup:

```python
from django.core.management.utils import get_random_secret_key
SECRET_KEY = os.environ.get("SECRET_KEY") or get_random_secret_key()
```

---

## 9. Separate Settings Modules for Each Environment

### Problem

`config/settings.py` interleaves development and production configuration in a single
file using `if ENVIRONMENT == "production"` branching.  This makes the file hard to
read and risks accidentally mixing configuration values.

### Recommendation

Adopt a split-settings pattern:

```
config/
    settings/
        __init__.py      # imports from base
        base.py          # shared settings
        development.py   # dev overrides
        production.py    # prod overrides
        test.py          # test overrides
```

Point `DJANGO_SETTINGS_MODULE` to the appropriate module for each environment.  This is
a well-established pattern that removes all `if ENVIRONMENT == …` branching and makes
each environment's config explicit.

---

## 10. Remove Stale `notes` and `dicts` Directories

### Problem

The project root contains `notes/` and `dicts/` directories that appear to be developer
notes, not Django apps or Python packages.  They exist alongside actual Django app
directories which may cause confusion.

### Recommendation

Move developer note directories out of the project root (e.g. into `docs/` or a
separate repository wiki) so that the root only contains Django apps and standard project
files.

---

## 11. Use `TextChoices` / `IntegerChoices` Consistently

### Problem

Choice fields across the project use a mix of:

- Plain `list` of 2-tuples (e.g. `QUADRANT_CHOICES`, `FREQUENCY_CHOICES`).
- `models.TextChoices` subclasses (e.g. `warcrafting.Character.WowClass`,
  `app_tracker.Host.HostStatus`).

### Recommendation

Standardise on `models.TextChoices` (or `models.IntegerChoices`) for all choice fields.
The enum approach provides named constants, IDE auto-completion, and avoids magic string
literals spread throughout queries and templates.

---

## 12. Use `select_related` / `prefetch_related` in QuerySets

### Problem

`UserQuerySetMixin.get_queryset()` returns a bare `filter(user=…)` queryset without any
`select_related` hints.  Many list views likely trigger N+1 queries when templates
access related objects.

### Recommendation

Override `get_queryset()` in individual CBVs (or define `queryset` on the view) with
appropriate `select_related` / `prefetch_related` calls for the known related fields in
each view.  Consider adding `select_related("user")` in `UserQuerySetMixin` as a
sensible default.

---

## 13. Consolidate Email-Reminder Pattern

### Problem

Two separate apps (`true_north` and `thing_thought_reminder`) implement a very similar
recurring-email-reminder pattern with their own models (`CoreValueEmailSchedule`,
`ReminderSchedule`), Celery tasks, and `compute_next_send()` logic.

### Recommendation

Extract a shared abstract model (e.g. `base.ReminderScheduleBase`) that encapsulates
the common fields (`user`, `frequency`, `is_active`, `next_send`, `last_sent`) and the
`compute_next_send()` algorithm.  App-specific child classes then only need to define
the target FK and the `get_subject()` / `get_content()` methods.  The Celery task can
also be generalised to process any model inheriting from the abstract base.

---

## 14. Add `db_index=True` to Frequently Filtered Fields

### Problem

Several FK and boolean fields used heavily in querysets lack explicit indexes:

- `boosts.Inspirational.author`
- `unimportant_notes.UnimportantNote.author`
- `decide.Decision.user`
- `thing_thought_reminder.ReminderSchedule.is_active` + `next_send`
- `true_north.CoreValueEmailSchedule.is_active` + `next_send`

### Recommendation

Add `db_index=True` to FK fields that are frequently filtered or joined on (Django does
not index all FKs by default if `unique=False`), and add composite `indexes` in `Meta`
for the `(is_active, next_send)` pair on reminder schedule models (as `true_north`
already does for some fields).

---

## 15. Upgrade `DEFAULT_FILE_STORAGE` to New Storage Backend API

### Problem

`config/settings.py` uses:

```python
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
```

This is the Django <4.2 API.  Django 4.2+ introduced the `STORAGES` dict setting:

```python
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
```

### Recommendation

Migrate to the new `STORAGES` dict format to avoid deprecation warnings when upgrading
Django beyond 4.2.
