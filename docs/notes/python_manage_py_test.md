# `python manage.py test` Commands

* `python manage.py test` - Run all tests in the project
* `python manage.py test <app_name>` - Run all tests in the app
* `python manage.py test <app_name>.<test_name>` - Run a specific test
* `python manage.py test <app_name>.<test_name>.<test_class_name>` - Run a specific test class
* `python manage.py test <app_name>.<test_name>.<test_class_name>.<test_method_name>` - Run a specific test method

## Examples

* `python manage.py test vitals.tests.test_admin`
* `python manage.py test app_tracker.tests.test_models.ApplicationModelTest`
* `python manage.py test self_enquiry.tests.test_views.JournalConfirmDeleteViewTest.test_get_method`