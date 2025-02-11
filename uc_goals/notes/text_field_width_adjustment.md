# `TextField` Width Adjustment with Django and Bootstrap CSS

## The Prompt

I have a Django "CreateView" which uses a "DoopDeDoo" model.

The "DoopDeDoo" model has a "snarfling"-named 'TextField'.

I am using bootstrap css with the project.

The DoopDeDoo.snarfling form field allows manual height adjustment via mouse drag but doesn't allow width adjustment.

How can I make it so the user can adjust the width of the form field 'DoopDeDoo.snarfling'?

## The Response

The issue you're encountering is due to Bootstrap's default CSS for textareas. By default, Bootstrap applies a style that only allows vertical resizing (usually via `resize: vertical;`) to textareas with the class `form-control`. To allow horizontal (or both horizontal and vertical) resizing, you need to override this CSS.

Here are two common ways to do that:

---

### 1. Override the Widget’s Inline Style in Your Django Form

If you're using a custom form (or want to modify the automatically generated one), you can override the widget for the `snarfling` field to include a style that allows both width and height adjustments. For example:

```python
from django import forms
from .models import DoopDeDoo

class DoopDeDooForm(forms.ModelForm):
    class Meta:
        model = DoopDeDoo
        fields = ['snarfling']
        widgets = {
            'snarfling': forms.Textarea(attrs={
                'style': 'resize: both;',  # Allow both horizontal and vertical resizing
                # You can also add other attributes like rows, cols, etc.
            }),
        }
```

Then, in your `CreateView`, specify this form:

```python
from django.views.generic import CreateView
from .models import DoopDeDoo
from .forms import DoopDeDooForm

class DoopDeDooCreateView(CreateView):
    model = DoopDeDoo
    form_class = DoopDeDooForm
    template_name = 'your_template.html'
    success_url = '/success/'
```

---

### 2. Override the CSS in Your Stylesheet

If you prefer not to touch the form widget attributes, you can override the Bootstrap CSS in your own stylesheet. For example, add the following CSS to your custom CSS file that’s loaded after Bootstrap:

```css
textarea.form-control {
    resize: both !important;
}
```

The `!important` ensures that your rule overrides Bootstrap's default styling.

---

### Explanation

- **Default Behavior:** Bootstrap typically sets textareas to `resize: vertical;` which only allows users to drag to adjust the height.
- **Desired Behavior:** Setting `resize: both;` allows users to adjust both the width and height of the textarea.
- **Implementation Options:** You can implement this by either modifying the widget attributes directly in your Django form or by overriding the CSS in your stylesheet.

Choose the method that best fits your project’s structure. Both approaches will allow the user to adjust the width of the `snarfling` field in your `DoopDeDoo` model.

Happy coding!
