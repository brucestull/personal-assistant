

```bash
[01/Jun/2025 10:45:59] "GET /care-craft/notes/ HTTP/1.1" 500 87088
Internal Server Error: /care-craft/notes/
Traceback (most recent call last):
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/handlers/exception.py", line 56, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/views/generic/base.py", line 103, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/views/generic/base.py", line 142, in dispatch
    return handler(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/views/generic/list.py", line 154, in get
    self.object_list = self.get_queryset()
                       ^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/views/generic/list.py", line 34, in get_queryset
    queryset = self.model._default_manager.all()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'all'
```

## Resolution

- Had `Note` model insead of `CareCraftNote` model
