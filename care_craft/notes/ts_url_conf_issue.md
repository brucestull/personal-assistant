#

```bash
(personal-assistant) flynntknapp@DELL-DESK:~/Programming/personal-assistant$  cd /home/flynntknapp/Programming/personal-assistant ; /usr/bin/env /home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/bin/python /home/flynntknapp/.vscode-server/extensions/ms-python.debugpy-2025.8.0-linux-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher 59927 -- /home/flynntknapp/Programming/personal-assistant/manage.py runserver 
Watching for file changes with StatReloader
Performing system checks...

Exception in thread django-main-thread:
Traceback (most recent call last):
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 717, in url_patterns
    iter(patterns)
TypeError: 'module' object is not iterable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/threading.py", line 1045, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.11/threading.py", line 982, in run
    self._target(*self._args, **self._kwargs)
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/utils/autoreload.py", line 64, in wrapper
    fn(*args, **kwargs)
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/management/commands/runserver.py", line 134, in inner_run
    self.check(display_num_errors=True)
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/management/base.py", line 475, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/checks/registry.py", line 88, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/checks/urls.py", line 14, in check_url_config
    return check_resolver(resolver)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/core/checks/urls.py", line 24, in check_resolver
    return check_method()
           ^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 494, in check
    for pattern in self.url_patterns:
                   ^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/utils/functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 715, in url_patterns
    patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
                       ^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/utils/functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 708, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/flynntknapp/Programming/personal-assistant/config/urls.py", line 54, in <module>
    path("care-craft/", include("care_craft.urls")),
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/conf.py", line 38, in include
    urlconf_module = import_module(urlconf_module)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/flynntknapp/Programming/personal-assistant/care_craft/urls.py", line 3, in <module>
    from . import views
  File "/home/flynntknapp/Programming/personal-assistant/care_craft/views.py", line 34, in <module>
    class CareCraftNoteDeleteView(DeleteView):
  File "/home/flynntknapp/Programming/personal-assistant/care_craft/views.py", line 36, in CareCraftNoteDeleteView
    success_url = reverse("care_craft:note_list")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/base.py", line 54, in reverse
    app_list = resolver.app_dict[ns]
               ^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 633, in app_dict
    self._populate()
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 543, in _populate
    for url_pattern in reversed(self.url_patterns):
                                ^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/utils/functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/flynntknapp/.local/share/virtualenvs/personal-assistant-Y8r_Smg_/lib/python3.11/site-packages/django/urls/resolvers.py", line 725, in url_patterns
    raise ImproperlyConfigured(msg.format(name=self.urlconf_name)) from e
django.core.exceptions.ImproperlyConfigured: The included URLconf 'config.urls' does not appear to have any patterns in it. If you see the 'urlpatterns' variable with valid patterns in the file then the issue is probably caused by a circular import.
(personal-assistant) flynntknapp@DELL-DESK:~/Programming/personal-assistant$
```
