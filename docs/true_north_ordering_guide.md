# True North Ordering Guide (`order` / `ordering`)

This guide explains how ordering currently works in `true_north`, how users can use it, and what could be improved.

## 1) How ordering works right now in `true_north`

`true_north` has an explicit `order` field on all four hierarchy models:

```python
# true_north/models.py
class CoreValue(...):
    order = models.PositiveIntegerField(default=0)

class Goal(...):
    order = models.PositiveIntegerField(default=0)

class Milestone(...):
    order = models.PositiveIntegerField(default=0)

class ValueAction(...):
    order = models.PositiveIntegerField(default=0)
```

Each model also defines default `Meta.ordering`:

```python
# true_north/models.py
class CoreValue(...):
    class Meta:
        ordering = ["order", "name"]

class Goal(...):
    class Meta:
        ordering = ["order", "title"]

class Milestone(...):
    class Meta:
        ordering = ["order", "description"]

class ValueAction(...):
    class Meta:
        ordering = ["order", "id"]
```

The app’s forms expose `order`, so users can set it directly:

```python
# true_north/forms.py
class CoreValueForm(forms.ModelForm):
    class Meta:
        fields = ["name", "definition", "is_active", "order"]
```

List/detail/dashboard views also explicitly sort by `order` first:

```python
# true_north/views.py
CoreValue.objects.filter(user=self.request.user).order_by("order", "name")
Goal.objects.filter(user=self.request.user).order_by("order", "title")
Milestone.objects.filter(user=self.request.user).order_by("order", "description")
ValueAction.objects.filter(user=self.request.user).order_by("order", "id")
```

And tests verify this behavior:

```python
# true_north/tests/test_models.py
def test_corevalue_meta_ordering_is_order_then_name(): ...
def test_goal_meta_ordering_is_order_then_title(): ...
def test_milestone_meta_ordering_is_order_then_description(): ...
def test_task_meta_ordering_is_order_then_id(): ...  # covers ValueAction
```

## 2) How users can use `order` to arrange objects

Users can set the `order` number in Create/Edit forms (or Django admin).

- Lower numbers appear first.
- Ties are broken by the second sort key (`name`, `title`, `description`, or `id`).
- Practical pattern:
  - `10, 20, 30` for major items (room to insert later)
  - insert new items at `15`, `25`, etc. without renumbering everything

Recommended user flow:
1. Create Core Values and assign order.
2. For each Goal under a value, assign order.
3. For each Milestone under a goal, assign order.
4. For each Value Action under a milestone, assign order.
5. Revisit order during weekly review to keep priority visible.

## 3) Best-practice improvements for `true_north` (suggested)

No blockers were found, but these improvements would make ordering more robust:

1. **Auto-append order on create** when user leaves default `0` (so new items naturally go to the bottom of their scope).
2. **Add scoped uniqueness for order** (for example, `(user, order)` for CoreValue, `(user, value, order)` for Goal, etc.) if strict manual ranking is desired.
3. **Improve `OrderableMixin.reorder_all` scope**. Current implementation reorders across all rows:

   ```python
   # base/mixins.py
   @classmethod
   def reorder_all(cls):
       for index, item in enumerate(cls.objects.all().order_by("order")):
           item.order = index
           item.save()
   ```

   If used, this should usually be filtered per user/parent group.
4. **Add quick move actions in UI** (up/down buttons) to reduce manual number editing.

## 4) Review of other apps using `order` / `ordering`

Findings:
- `decide.Prompt` uses an explicit `order` field with `Meta.ordering = ["order"]`.
- Most other apps use non-manual ordering keys (for example `name`, `label`, `-created`, or relation/name pairs).
- `packing_list` orders by `["activity", "name"]` (no explicit user-controlled order field).

Suggested updates from this comparison:
1. **`decide.Prompt`**: consider deterministic tie-break ordering (`["order", "id"]`).
2. **Where manual order fields exist**: keep a documented rule for tie-breakers and scope (user/parent).
3. **Repository-wide consistency**: prefer explicit second key in `Meta.ordering` for deterministic results when values tie.
