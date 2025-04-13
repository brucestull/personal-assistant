# Send Email Tests

## Test 1

`python manage.py shell`

```python
import os
from django.core.mail import send_mail

send_mail(
    'Subject here: From Django Shell',
    # `message`
    'Here is the message: From Django Shell',
    # `from_email`
    'admin@fakeemail.app',
    # `recipient_list`
    [os.getenv('MY_VALIDATED_EMAIL')],
)
```

## Test 2

`python manage.py shell`

```python
from boosts.models import Inspirational
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

inspirational = get_object_or_404(Inspirational, pk=1)
send_mail(
    inspirational.author,
    inspirational.body,
    'admin@email.app',
    ['FlynntKnapp@email.app'],
)


## Test 3

`python manage.py shell`

```python
from boosts.models import Inspirational
from accounts.models import CustomUser as User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

sender = User.objects.get(pk=2)

inspirational = get_object_or_404(Inspirational, pk=1)
send_mail(
    f"Your Inspirational for the Day from: {inspirational.author}",
    inspirational.body,
    sender.email,
    ['FlynntKnapp@email.app'],
)

```

