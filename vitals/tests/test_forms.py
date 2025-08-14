# vitals/tests/test_forms.py
from django.test import TestCase

from vitals.forms import BodyWeightForm


class BodyWeightFormTests(TestCase):
    def test_measurement_must_be_positive(self):
        f = BodyWeightForm(data={"subject": 1, "measurement": 0})
        self.assertFalse(f.is_valid())
        self.assertIn("measurement", f.errors)
