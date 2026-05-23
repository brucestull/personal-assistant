# Registration Accepted Status Report (2026-05-23)

## Scope

Scanned all application `views.py` (vanilla Django views) and `api_views.py` (REST views) for registration-accepted enforcement.

Enforcement mechanisms checked:

- `base.mixins.RegistrationAcceptedMixin`
- `base.decorators.registration_accepted_required`
- REST-specific equivalent used by API viewsets: `base.permissions.RegistrationAcceptedPermission`

## Findings

### Vanilla Django views

Authenticated view access is enforced with either:

- `RegistrationAcceptedMixin` on class-based views, or
- `@registration_accepted_required` on function-based views.

### REST views

The following REST viewsets now enforce registration-accepted status in addition to authentication:

- `bus_drive/api_views.py::ThoughtViewSet`
- `item_location/api_views.py::StorageLocationViewSet`
- `item_location/api_views.py::ItemViewSet`

## Gaps found and corrected

The scan identified authenticated endpoints that previously did not enforce `registration_accepted=True`:

- `boosts/views.py::send_random_inspirational_to_self` (used `@login_required`)
- `kanban_cabinet/views.py` authenticated CBVs using `LoginRequiredMixin` only
- `warcrafting/views.py` authenticated CBVs using `LoginRequiredMixin` only
- REST API viewsets in `bus_drive/api_views.py` and `item_location/api_views.py` using `IsAuthenticated` only

These gaps were updated so authenticated access now consistently requires `registration_accepted=True`.

## Validation coverage added

Focused tests were added/updated to verify denied access (`403`) for authenticated users with `registration_accepted=False`:

- `boosts/tests/test_views.py`
- `kanban_cabinet/tests/test_views.py`
- `warcrafting/tests/test_views.py`
- `bus_drive/tests/test_api.py`
- `item_location/tests/test_api.py`
