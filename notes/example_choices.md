# Code Example for Django `choices` Field

```python
from django.db import models

class Pain(models.Model):
    """
    Model for user's pain level. This is a subjective value.

    Attributes:
        value (int): The user's pain level.
    """
    # ...
    PAIN_CHOICES = (
        (0, 'No pain'),
        (1, 'Mild pain'),
        (2, 'Moderate pain'),
        (3, 'Severe pain'),
        (4, 'Very severe pain'),
        (5, 'Intense pain'),
        (6, 'Incapacitating pain'),
        (7, 'Unbearable pain'),
    )

    value = models.IntegerField(choices=PAIN_CHOICES)

    # ...
```