# Override get_queryset vs queryset

## Request

In order to get only the "Entry"s owned by 'author', should I override "get_queryset" or assign "queryset"?

```python
class EntryListView(RegistrationAcceptedMixin, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")
```

## Response

You should override `get_queryset` rather than assigning `queryset` directly. The reason is that overriding `get_queryset` allows you to dynamically filter the queryset based on the request or user, whereas assigning `queryset` in the class body applies a static filter at the time the class is defined.

### Correct approach:
```python
class EntryListView(RegistrationAcceptedMixin, ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user).order_by("-date_created")
```

### Why is `get_queryset` better?
- `get_queryset` is evaluated at request time, allowing you to reference `self.request.user` dynamically.
- Assigning `queryset` statically applies the filter at class definition time, which is not user-specific.
- Overriding `get_queryset` is the recommended Django approach for filtering querysets based on request context.

So, **use `get_queryset`** to ensure that only `Entry` instances owned by the authenticated user are retrieved.

## Request

How do I apply this logic to Django "DetailView"?

## Response

For a **Django `DetailView`**, you should override the `get_queryset` method just like in `ListView`. This ensures that only the `Entry` objects owned by the authenticated user can be accessed.

### Correct approach for `DetailView`:
```python
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Entry

class EntryDetailView(RegistrationAcceptedMixin, DetailView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)
```

### Why override `get_queryset`?
- It ensures that a user cannot access `Entry` objects belonging to other users.
- The default `get_object()` method in `DetailView` will use this filtered queryset to retrieve the object.

### Alternative: Override `get_object`
Another approach is to override `get_object` instead of `get_queryset`:

```python
class EntryDetailView(RegistrationAcceptedMixin, DetailView):
    model = Entry

    def get_object(self, queryset=None):
        return get_object_or_404(Entry, id=self.kwargs["pk"], author=self.request.user)
```

### Which method should you use?
- **`get_queryset`** is the preferred method because it ensures all queries are filtered at the database level.
- **`get_object`** is useful if you need additional custom logic (e.g., using `get_object_or_404` for cleaner error handling).

For most cases, **overriding `get_queryset` is the best approach** in `DetailView`, just like in `ListView`.
