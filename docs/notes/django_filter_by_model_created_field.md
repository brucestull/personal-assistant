# Django Filter by Model Created Field

[Django Filtrado Modelo Creado - ChatGPT](https://chat.openai.com/share/bef66c40-3759-4388-b814-71fbd18efd3c)

I'm using Django with bootstrap.

Help me modify my `UnimportantNote` model, create a view, create a template, to have a filter by the inherited `created` field?

```python

class CreatedUpdatedBase(models.Model):
    """
    An abstract base class model that provides self-updating `created` and
    `updated` fields.
    """

    created = models.DateTimeField(
        "Created",
        auto_now_add=True,
        help_text="The date and time this object was created.",
    )
    updated = models.DateTimeField(
        "Updated",
        auto_now=True,
        help_text="The date and time this object was last updated.",
    )

    class Meta:
        abstract = True


class Note(CreatedUpdatedBase):
    """
    A note.
    """

    title = models.CharField(
        "Title",
        max_length=255,
        help_text="The title of this note.",
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    content = models.TextField(
        "Content",
        help_text="The content of this note.",
        blank=True,
    )
    url = models.URLField(
        "URL",
        help_text="A reference URL for this note.",
        blank=True,
    )
    main_image = models.ImageField(
        verbose_name="Main Image",
        help_text="Add an image for the note.",
        # `upload_to` is a required argument for `ImageField`.
        # It specifies the path to which the uploaded file will be saved.
        upload_to="test_uploads/",
        blank=True,
        null=True,
    )

    def display_content(self):
        """
        This function returns a truncated version of the note's content.
        This can be used in the admin panel and other places where the full
        content is not needed.
        """
        return self.content[:30] + ("..." if len(self.content) > 30 else "")

    def __str__(self):
        return (
            f"{self.title} - {self.content[:50]}"
            f"{'...' if len(self.content) > 50 else ''}"
        )

    class Meta:
        # Use `abstract = True` to make this model an abstract base class which doesn't
        # have a model table created in the database.
        abstract = True
        # `verbose_name` and `verbose_name_plural` and `ordering` are declared in the
        # child class.


class UnimportantNote(Note):
    """
    Model for `UnimportantNote`.
    """

    main_image = models.ImageField(
        verbose_name="Main Image",
        help_text="Add an image for the note.",
        # `upload_to` is a required argument for `ImageField`.
        # It specifies the path to which the uploaded file will be saved.
        upload_to="unimportant_notes/",
        blank=True,
        null=True,
    )
    tag = models.ManyToManyField(
        NoteTag,
        verbose_name="Tags",
        help_text="Tags for this note.",
        blank=True,
        related_name="unimportant_notes",
    )

    def display_tags(self):
        """
        Display the tags for this note.
        """
        return ", ".join([tag.name for tag in self.tag.all()])

    def __str__(self):
        return self.title

    class Meta:
        # These `Meta` options are used to configure the behavior of this child model.
        verbose_name = "Unimportant Note"
        verbose_name_plural = "Unimportant Notes"
        ordering = ("-created",)
```

To facilitate filtering by the `created` field in your `UnimportantNote` model, we'll walk through modifying the model (if needed), creating a view that handles filtering, and creating a template that allows users to specify their filter criteria. Since your model already inherits the `created` field from `CreatedUpdatedBase`, no modifications are necessary to the model itself. The focus will be on implementing the view and template.

### 1. View

We will create a view that fetches all `UnimportantNote` instances and allows filtering by the `created` field. This can be achieved using Django's `Q` objects for complex queries (if needed) and by fetching filter parameters from the request's query parameters.

Here's an example of how you might implement such a view:

```python
from django.shortcuts import render
from django.db.models import Q
from .models import UnimportantNote
from django.utils.dateparse import parse_date

def unimportant_notes_list(request):
    notes = UnimportantNote.objects.all()

    # Filtering by 'created' field if the 'start_date' and/or 'end_date' are provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
        notes = notes.filter(created__date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        notes = notes.filter(created__date__lte=end_date)

    context = {
        'notes': notes,
    }
    return render(request, 'unimportant_notes/list.html', context)
```

Ensure you have `from django.utils.dateparse import parse_date` to handle date parsing from query parameters.

### 2. Template

Next, you'll need a template where users can input their filtering criteria (e.g., a start and end date) and where the filtered list of `UnimportantNote` instances will be displayed. This template could be named `unimportant_notes/list.html` as referenced in the view above.

```html
{% extends "base.html" %}

{% block content %}
<h2>Unimportant Notes</h2>

<!-- Filter Form -->
<form method="get">
    <label for="start_date">Start Date:</label>
    <input type="date" id="start_date" name="start_date" value="{{ request.GET.start_date }}">

    <label for="end_date">End Date:</label>
    <input type="date" id="end_date" name="end_date" value="{{ request.GET.end_date }}">

    <button type="submit">Filter</button>
</form>

<!-- Notes List -->
<ul>
    {% for note in notes %}
    <li>
        <strong>{{ note.title }}</strong> (Created: {{ note.created }})
        <p>{{ note.display_content }}</p>
    </li>
    {% empty %}
    <li>No notes found.</li>
    {% endfor %}
</ul>
{% endblock %}
```

This template includes a simple form for filtering by start and end dates and lists the notes that match the criteria. It uses the `{{ request.GET.start_date }}` and `{{ request.GET.end_date }}` to repopulate the form fields with the user's input, making the filtering experience smoother.

### Final Steps

- Ensure that the view is registered in your application's URLconf.
- Adjust the template to fit within your project's structure and styling conventions, particularly how it extends from your base template.
- Test the filtering functionality to make sure it works as expected with various date ranges.

This approach offers a basic, functional way to filter `UnimportantNote` instances by their creation date within a Django application using Bootstrap for styling.
