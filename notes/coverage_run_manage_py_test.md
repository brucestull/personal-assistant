# `coverage run manage.py test` Commands

* `coverage run manage.py test` - Run all tests in the project
* `coverage run manage.py test <app_name>` - Run all tests in the app
* `coverage run manage.py test <app_name>.<test_name>` - Run a specific test module
* `coverage run manage.py test <app_name>.<test_name>.<test_class_name>` - Run a specific test class
* `coverage run manage.py test <app_name>.<test_name>.<test_class_name>.<test_method_name>` - Run a specific test method

## Examples

* `coverage run manage.py test vitals.tests.test_admin`