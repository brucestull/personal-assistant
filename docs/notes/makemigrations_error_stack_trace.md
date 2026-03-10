# `python manage.py makemigrations` Error Stack Trace

## GitHub Copilot Chat 'Stack Trace' Explanation

```text
A stack trace is a report of the active stack frames at a certain point in time during the execution of a program. In Python, a stack trace is generated when an error occurs during the execution of a program.

The stack trace provides a detailed report of the error, including the type of error, the line number where the error occurred, and the sequence of function calls that led up to the error. Each function call is represented by a stack frame, which contains information about the function, its arguments, and its local variables.

The stack trace is a valuable tool for debugging Python programs, as it provides a detailed view of the program's execution at the time of the error. By examining the stack trace, you can often identify the source of the error and take steps to correct it.

In the excerpt you provided, the stack trace is reporting an OperationalError caused by a missing table in the database. The error occurred on line 240, which is where the execute method is called on the cursor object.
```

## `python manage.py makemigrations` Error Stack Trace

```powershell
(personal-assistant) PS C:\Users\Bruce\Programming\personal-assistant> python manage.py makemigrations
Traceback (most recent call last):
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\sqlite3\base.py", line 357, in execute
    return Database.Cursor.execute(self, query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: vitals_bloodpressure

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\Bruce\Programming\personal-assistant\manage.py", line 22, in <module>
    main()
  File "C:\Users\Bruce\Programming\personal-assistant\manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\__init__.py", line 446, in execute_from_command_line
    utility.execute()
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\__init__.py", line 440, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 402, in run_from_argv
    self.execute(*args, **cmd_options)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 443, in execute
    self.check()
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 475, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\registry.py", line 88, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\urls.py", line 42, in check_url_namespaces_unique
    all_namespaces = _load_all_namespaces(resolver)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\urls.py", line 61, in _load_all_namespaces    
    url_patterns = getattr(resolver, "url_patterns", [])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\utils\functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\resolvers.py", line 715, in url_patterns
    patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
                       ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\utils\functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\resolvers.py", line 708, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "C:\Users\Bruce\Programming\personal-assistant\config\urls.py", line 37, in <module>
    path("vitals/", include("vitals.urls")),
                    ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\conf.py", line 38, in include
    urlconf_module = import_module(urlconf_module)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\urls.py", line 3, in <module>
    from vitals.views import (
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\views.py", line 23, in <module>
    class BloodPressureListView(LoginRequiredMixin, ListView):
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\views.py", line 49, in BloodPressureListView
    average_and_median_all = BloodPressure.get_average_and_median()
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\models.py", line 58, in get_average_and_median
    if len(systolic_values) == 0:
       ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 376, in __len__
    self._fetch_all()
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 1867, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 281, in __iter__
    for row in compiler.results_iter(
               ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\sql\compiler.py", line 1349, in results_iter    
    results = self.execute_sql(
              ^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\sql\compiler.py", line 1398, in execute_sql     
    cursor.execute(sql, params)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 102, in execute
    return super().execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 80, in _execute_with_wrappers 
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\sqlite3\base.py", line 357, in execute        
    return Database.Cursor.execute(self, query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.OperationalError: no such table: vitals_bloodpressure
(personal-assistant) PS C:\Users\Bruce\Programming\personal-assistant> python manage.py migrate       
Traceback (most recent call last):
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\sqlite3\base.py", line 357, in execute        
    return Database.Cursor.execute(self, query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: vitals_bloodpressure

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\Bruce\Programming\personal-assistant\manage.py", line 22, in <module>
    main()
  File "C:\Users\Bruce\Programming\personal-assistant\manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\__init__.py", line 446, in execute_from_command_line
    utility.execute()
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\__init__.py", line 440, in execute        
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 402, in run_from_argv      
    self.execute(*args, **cmd_options)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 448, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 96, in wrapped
    res = handle_func(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\commands\migrate.py", line 97, in handle  
    self.check(databases=[database])
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\management\base.py", line 475, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\registry.py", line 88, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\urls.py", line 42, in check_url_namespaces_unique
    all_namespaces = _load_all_namespaces(resolver)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\core\checks\urls.py", line 61, in _load_all_namespaces    
    url_patterns = getattr(resolver, "url_patterns", [])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\utils\functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\resolvers.py", line 715, in url_patterns
    patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
                       ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\utils\functional.py", line 57, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\resolvers.py", line 708, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "C:\Users\Bruce\Programming\personal-assistant\config\urls.py", line 37, in <module>
    path("vitals/", include("vitals.urls")),
                    ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\urls\conf.py", line 38, in include
    urlconf_module = import_module(urlconf_module)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\urls.py", line 3, in <module>
    from vitals.views import (
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\views.py", line 23, in <module>
    class BloodPressureListView(LoginRequiredMixin, ListView):
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\views.py", line 49, in BloodPressureListView
    average_and_median_all = BloodPressure.get_average_and_median()
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\Programming\personal-assistant\vitals\models.py", line 58, in get_average_and_median
    if len(systolic_values) == 0:
       ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 376, in __len__
    self._fetch_all()
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 1867, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\query.py", line 281, in __iter__
    for row in compiler.results_iter(
               ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\sql\compiler.py", line 1349, in results_iter    
    results = self.execute_sql(
              ^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\models\sql\compiler.py", line 1398, in execute_sql     
    cursor.execute(sql, params)
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 102, in execute
    return super().execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 80, in _execute_with_wrappers 
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bruce\.virtualenvs\personal-assistant-lW_q8YHG\Lib\site-packages\django\db\backends\sqlite3\base.py", line 357, in execute        
    return Database.Cursor.execute(self, query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.OperationalError: no such table: vitals_bloodpressure
(personal-assistant) PS C:\Users\Bruce\Programming\personal-assistant> 
```
