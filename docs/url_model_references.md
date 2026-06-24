# URL Model and References Audit

This document tracks all Django `URL` model definitions and references across apps.

## URL model definitions

1. `base.URL` (`base/models.py`)
   - Abstract base model (`abstract = True`)
   - Cannot be instantiated directly.
2. `app_tracker.URL` (`app_tracker/models.py`)
   - Concrete model inheriting from `base.URL`
   - Can be instantiated.

## App-by-app findings

| App | URL model/reference found | Single or multiple |
| --- | --- | --- |
| `base` | Defines abstract `URL` base model; test-only subclass usage in `base/tests/test_mixins_and_models.py`. | Single model definition (abstract) |
| `app_tracker` | Defines concrete `URL` model and references it in admin, views, and URL routes. `URL.application` is a `ForeignKey` with `related_name="urls"` to `Application`. | Multiple URLs per `Application`; each `URL` has at most one `Application` |
| All other apps | No `URL` model definitions and no references to a `URL` model. | N/A |

## Key reference locations in `app_tracker`

- `app_tracker/models.py`
- `app_tracker/admin.py`
- `app_tracker/views.py`
- `app_tracker/urls.py`
