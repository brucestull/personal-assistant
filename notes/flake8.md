# Flake8 Commands

## Move `flake8` Configuration to `.flake8` File

- Before migration:
    - `config.yml`:
        ```yml
        # Step 3: run linter
        - run:
            name: Run Linter
            command: |
                pipenv run flake8 --exclude=migrations,common.py,wsgi.py,manage.py --ignore=F403,F405 --statistics
        ```

- After migration:
    - `.flake8`:
        ```yml
        [flake8]
        exclude = migrations,common.py,wsgi.py,manage.py
        extend-ignore = F403,F405
        statistics = True
        ```

    - `config.yml`:
        ```yml
        # Step 3: run linter
        - run:
            name: Run Linter
            command: |
                pipenv run flake8
        ```

## Command for This Project

* `flake8 --exclude=migrations,common.py,wsgi.py,manage.py --ignore=F403,F405 --statistics`
    * [`.circleci/config.yml`](../.circleci/config.yml)

* Codes to Ignore
    * `F403` - 'from module import *' used; unable to detect undefined names
    * `F405` - name may be undefined, or defined from star imports: module
    * `E712` - comparison to True should be 'if cond is True:' or 'if cond:'
## Examples

* `flake8 --exclude=venv*,migrations,common.py,wsgi.py,manage.py --statistics --ignore=F841`
* `flake8 --exclude=venv*,migrations,common.py,wsgi.py,manage.py --statistics --ignore=F841,E501`

* `flake8 --exclude=venv*,migrations,common.py,wsgi.py,manage.py --statistics` - Run flake8 on the entire project, excluding the virtual environment, migrations, settings.py, wsgi.py, and manage.py files, and show statistics

* `flake8` - Run flake8 on the entire project
* `flake8 <app_name>` - Run flake8 on the app
* `flake8 <app_name>/<file_name>` - Run flake8 on the file
* `flake8 <app_name>/<file_name>:<line_number>` - Run flake8 on the line number
* `flake8 <app_name>/<file_name>:<line_number>:<column_number>` - Run flake8 on the column number

* `flake8 --select <error_code>` - Run flake8 on the entire project, but only show the error code
* `flake8 --select <error_code> <app_name>` - Run flake8 on the app, but only show the error code
* `flake8 --select <error_code> <app_name>/<file_name>` - Run flake8 on the file, but only show the error code
* `flake8 --select <error_code> <app_name>/<file_name>:<line_number>` - Run flake8 on the line number, but only show the error code
* `flake8 --select <error_code> <app_name>/<file_name>:<line_number>:<column_number>` - Run flake8 on the column number, but only show the error code