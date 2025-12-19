# vitals/tests/test_bp_summary.py

import pytest
from django.contrib.auth import get_user_model
from vitals.models import BloodPressure

User = get_user_model()


@pytest.mark.django_db
def test_bp_summary_roundtrip():
    u = User.objects.create_user(username="tiny", password="x")
    assert BloodPressure.objects.for_user(u).summary()["systolic_average"] is None

    BloodPressure.objects.create(user=u, systolic=120, diastolic=80, pulse=70)
    BloodPressure.objects.create(user=u, systolic=130, diastolic=85, pulse=72)
    s = BloodPressure.objects.for_user(u).summary()

    assert s["systolic_min"] == 120
    assert s["systolic_max"] == 130
    assert s["diastolic_min"] == 80
    assert s["diastolic_max"] == 85

    # statistics.median() with two values returns their average
    assert s["systolic_median"] == pytest.approx(125.0)
    assert s["diastolic_median"] == pytest.approx(82.5)

    assert isinstance(s["systolic_average"], float)
