# Flake8 Commands

* `flake8 --exclude=venv*,migrations,settings.py,wsgi.py,manage.py --statistics --ignore=F841`
* `flake8 --exclude=venv*,migrations,settings.py,wsgi.py,manage.py --statistics --ignore=F841,E501`

* `flake8 --exclude=venv*,migrations,settings.py,wsgi.py,manage.py --statistics` - Run flake8 on the entire project, excluding the virtual environment, migrations, settings.py, wsgi.py, and manage.py files, and show statistics

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