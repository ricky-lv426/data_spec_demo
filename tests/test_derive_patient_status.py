import math

import pandas as pd

from scripts.derive_patient_status import (
    compute_bmi,
    weight_category,
    bp_category,
    latest_measurements,
)


def test_compute_bmi_normal():
    bmi = compute_bmi(70, 1.75)
    assert isinstance(bmi, float)
    assert math.isclose(bmi, round(70 / (1.75 ** 2), 1), rel_tol=1e-9)


def test_compute_bmi_edge_cases():
    assert compute_bmi(None, 1.75) is None
    assert compute_bmi(70, None) is None
    assert compute_bmi(70, 0) is None
    # NaN values
    assert compute_bmi(float("nan"), 1.75) is None
    assert compute_bmi(70, float("nan")) is None


def test_weight_category_boundaries():
    assert weight_category(None) is None
    assert weight_category(18.4) == "underweight"
    assert weight_category(18.5) == "normal"
    assert weight_category(24.9) == "normal"
    assert weight_category(25.0) == "overweight"
    assert weight_category(29.9) == "overweight"
    assert weight_category(30.0) == "obese"


def test_bp_category_various():
    assert bp_category(None, None) is None
    assert bp_category(150, None) == "high"
    assert bp_category(None, 95) == "high"
    assert bp_category(85, None) == "low"
    assert bp_category(None, 55) == "low"
    assert bp_category(120, 80) == "normal"
    # non-numeric input should be handled and return None
    assert bp_category("not-a-number", 80) is None


def test_latest_measurements():
    df = pd.DataFrame(
        {
            "patient_id": [1, 1, 2],
            "date": pd.to_datetime(["2020-01-01", "2021-01-01", "2020-06-01"]),
            "bp_systolic": [120, 130, 110],
        }
    )
    latest = latest_measurements(df)
    # Expect one row per patient
    assert set(latest["patient_id"]) == {1, 2}
    # For patient 1, date should be the later one
    row1 = latest[latest["patient_id"] == 1].iloc[0]
    assert row1["bp_systolic"] == 130
