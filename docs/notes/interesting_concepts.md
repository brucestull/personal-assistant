# Interesting Concepts

## `self.assertEqual` vs `self.assertTrue` vs `self.assertFalse`

`app_tracker/tests/test_models.py`:
```python
class ApplicationModelTest(TestCase):
    # ...
    def test_has_email_sending_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_email_sending").default
        # Either of these will work:
        self.assertEqual(default, False)
        self.assertFalse(default)
    # ...
```

