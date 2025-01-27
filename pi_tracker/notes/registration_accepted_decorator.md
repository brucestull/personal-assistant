# Registration Accepted Decorator

[Django decorator for registration](https://chatgpt.com/share/67970c1c-86cc-8002-9bad-ba695ed907f5)

You can create a custom decorator for the same rules (`user.is_authenticated` and `user.registration_accepted`) for a function-based view in Django. Here's how you can implement it:

```python
from django.http import HttpResponseForbidden
from functools import wraps

def registration_accepted_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this page.")
        
        # Check if the user's registration is accepted
        if not getattr(request.user, "registration_accepted", False):
            return HttpResponseForbidden("Your registration has not been accepted.")
        
        # Call the original view function if checks pass
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
```

### How to use the decorator:

You can apply the `@registration_accepted_required` decorator to your function-based view like this:

```python
from django.shortcuts import render

@registration_accepted_required
def my_view(request):
    # Your view logic here
    return render(request, "my_template.html")
```

### Explanation:

1. **`@wraps`**:
   - Preserves the original view's metadata (like its name and docstring).
   
2. **`request.user.is_authenticated`**:
   - Ensures the user is logged in. If not, a `403 Forbidden` response is returned.

3. **`getattr(request.user, "registration_accepted", False)`**:
   - Checks if the `registration_accepted` attribute exists on the `User` object and if it's `True`.

4. **`HttpResponseForbidden`**:
   - Returns a 403 Forbidden response if any of the checks fail.

This decorator can now be used with any function-based view to enforce the same rules as your `RegistrationAcceptedMixin`.
