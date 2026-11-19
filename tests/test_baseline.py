import pytest

from marathon_predictor.baseline import riegel_predict


def test_target_km_equals_distance_km():
    assert riegel_predict(1800, 42.195) == 1800


def test_known_riegel_prediction():
    predicted_time = riegel_predict(6300, 21.0975)  # 21.0975 km = half marathon
    assert predicted_time == pytest.approx(13135, abs=0.1)


def test_exponent_equals_one():
    # If exponent = 1, predicted time should be proportional to distance
    predicted_time = riegel_predict(3600, 10, target_km=42.195, exponent=1)
    expected_time = 3600 * (42.195 / 10)
    assert predicted_time == pytest.approx(expected_time, abs=0.1)
