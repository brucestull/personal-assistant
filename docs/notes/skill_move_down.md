# `skill_move_down` Django View



## Request

Here is my `skill_move_up` Django function view:

```python
def skill_move_up(request, skill_id):
    """
    View function to move a `Skill` object up in the list.
    """
    with transaction.atomic():
        skill = get_object_or_404(Skill, id=skill_id)
        previous_skill = (
            Skill.objects.filter(order__lt=skill.order).order_by("-order").first()
        )

        if previous_skill:
            skill.order, previous_skill.order = previous_skill.order, skill.order
            skill.save()
            previous_skill.save()

    return redirect("career_organizerator:skill-list")
```

Help me write a `skill_move_down` method?

## Response

Certainly! To create a `skill_move_down` function, we'll follow a similar logic to the `skill_move_up` function, but instead, we'll find the next `Skill` object in the list (i.e., the one with the next higher `order`) and swap their `order` values. This effectively moves the selected skill down in the list.

Here's how the `skill_move_down` function could look:

```python
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from .models import Skill  # Adjust the import path according to your project structure

def skill_move_down(request, skill_id):
    """
    View function to move a `Skill` object down in the list.
    """
    with transaction.atomic():
        skill = get_object_or_404(Skill, id=skill_id)
        # Find the next skill in the list (i.e., the one with a greater `order` value)
        next_skill = (
            Skill.objects.filter(order__gt=skill.order).order_by("order").first()
        )

        if next_skill:
            # Swap the `order` values of the skills to move the selected skill down
            skill.order, next_skill.order = next_skill.order, skill.order
            skill.save()
            next_skill.save()

    return redirect("career_organizerator:skill-list")
```

This function works similarly to the `skill_move_up` function but in the opposite direction. It identifies the next `Skill` object (i.e., the one immediately below the current skill in the order) and swaps their `order` values, effectively moving the selected skill down the list.

Make sure to replace `"career_organizerator:skill-list"` with the correct name for your list view's URL name, if it's different. Also, ensure that your `Skill` model has an `order` field that determines the position of each skill in the list.
