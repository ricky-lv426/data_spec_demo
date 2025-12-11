#!/usr/bin/env python3
"""
Derive patient-level blood-pressure and weight category using demo data (Python version)
Writes: data/derived_patient_status.csv

Usage:
    python3 scripts/derive_patient_status.py
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    import pandas as pd
except ImportError:  # pragma: no cover - helpful runtime message if dependencies missing
    print("Missing dependency 'pandas'. Install with: pip install -r scripts/requirements.txt", file=sys.stderr)
    raise SystemExit(3)

ROOT = Path(__file__).resolve().parents[1]
PATIENTS_FILE = ROOT / "data" / "sample_patients.csv"
MEASUREMENTS_FILE = ROOT / "data" / "measurements.csv"
OUTPUT_FILE = ROOT / "data" / "derived_patient_status.csv"


def load_patients(path: Path) -> pd.DataFrame:
    """Load patients CSV.

    Parameters
    ----------
    path : pathlib.Path
        Path to the patients CSV file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing patient records as read from ``path``.
    """
    return pd.read_csv(path)


def load_measurements(path: Path) -> pd.DataFrame:
    """Load measurements CSV and parse the date column.

    Parameters
    ----------
    path : pathlib.Path
        Path to the measurements CSV file.

    Returns
    -------
    pandas.DataFrame
        Measurements with the ``date`` column parsed as datetimes.
    """
    return pd.read_csv(path, parse_dates=["date"])


def latest_measurements(measurements: pd.DataFrame) -> pd.DataFrame:
    """Return the most recent measurement per patient.

    Parameters
    ----------
    measurements : pandas.DataFrame
        Measurements table containing at least ``patient_id`` and ``date`` columns.

    Returns
    -------
    pandas.DataFrame
        One-row-per-patient DataFrame containing the latest measurement (largest ``date``)
        for each ``patient_id``.
    """
    sorted_df = measurements.sort_values(["patient_id", "date"], ascending=[True, False])
    return sorted_df.drop_duplicates(subset=["patient_id"], keep="first").copy()


def _build_height_maps() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Build demo height lookup tables.

    Returns
    -------
    tuple
        A tuple containing two DataFrames: (height_map, sex_fallback).

        - ``height_map`` has columns (sex, ethnicity, height_cm) and provides assumed
          average heights by sex and ethnicity (demo-only).
        - ``sex_fallback`` has columns (sex, height_cm_fallback) with sex-level defaults.
    """
    height_map = pd.DataFrame(
        [
            ("M", "White", 175),
            ("F", "White", 162),
            ("M", "Black", 174),
            ("F", "Black", 161),
            ("M", "Asian", 169),
            ("F", "Asian", 157),
            ("M", "Mixed", 173),
            ("F", "Mixed", 161),
            ("M", "Other", 172),
            ("F", "Other", 160),
        ],
        columns=["sex", "ethnicity", "height_cm"],
    )

    sex_fallback = pd.DataFrame([("M", 174), ("F", 161)], columns=["sex", "height_cm_fallback"])
    return height_map, sex_fallback


def assume_heights(df: pd.DataFrame) -> pd.DataFrame:
    """Populate assumed heights for patients using sex and ethnicity.

    The function merges demo height tables into ``df`` and sets the following columns:

    - ``height_cm``: assumed height in centimetres
    - ``height_source``: string indicating whether the assumption used sex+ethnicity or sex-only
    - ``height_m``: height in metres (float) or None

    Parameters
    ----------
    df : pandas.DataFrame
        Patient-level DataFrame containing at least ``sex`` and ``ethnicity`` columns.

    Returns
    -------
    pandas.DataFrame
        The input dataframe augmented with ``height_cm``, ``height_source`` and ``height_m``.
    """
    height_map, sex_fallback = _build_height_maps()
    df = df.astype({"sex": "object", "ethnicity": "object"})
    df = df.merge(height_map, on=["sex", "ethnicity"], how="left")
    df = df.merge(sex_fallback, on="sex", how="left")
    df["height_cm"] = df["height_cm"].fillna(df["height_cm_fallback"])

    # Which mapping produced the height?
    known_pairs = set(map(tuple, height_map[["sex", "ethnicity"]].values))

    def _height_source(row):
        if pd.notna(row.get("ethnicity")) and ((row.get("sex"), row.get("ethnicity")) in known_pairs):
            return "assumed_by_sex_ethnicity"
        return "assumed_by_sex"

    df["height_source"] = df.apply(_height_source, axis=1)
    df["height_m"] = df["height_cm"].apply(lambda x: x / 100 if pd.notna(x) else None)
    return df


def compute_bmi(weight_kg: Optional[float], height_m: Optional[float]) -> Optional[float]:
    """Compute Body Mass Index (BMI).

    Parameters
    ----------
    weight_kg : float or None
        Weight in kilograms.
    height_m : float or None
        Height in metres.

    Returns
    -------
    float or None
        BMI rounded to 1 decimal place, or ``None`` if inputs are missing or invalid.
    """
    try:
        if pd.isna(weight_kg) or pd.isna(height_m) or height_m == 0:
            return None
        return round(float(weight_kg) / (float(height_m) ** 2), 1)
    except Exception:
        return None


def weight_category(bmi: Optional[float]) -> Optional[str]:
    """Classify weight category from BMI.

    Parameters
    ----------
    bmi : float or None
        Body Mass Index.

    Returns
    -------
    str or None
        One of ``'underweight'``, ``'normal'``, ``'overweight'``, ``'obese'`` or ``None`` if BMI
        is missing.
    """
    if pd.isna(bmi):
        return None
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    return "obese"


def bp_category(bp_systolic: Optional[float], bp_diastolic: Optional[float]) -> Optional[str]:
    """Categorise blood pressure using systolic and diastolic values.

    Parameters
    ----------
    bp_systolic : float or None
        Systolic blood pressure (mmHg).
    bp_diastolic : float or None
        Diastolic blood pressure (mmHg).

    Returns
    -------
    str or None
        ``'high'`` if systolic >= 140 or diastolic >= 90,
        ``'low'`` if systolic < 90 or diastolic < 60,
        ``'normal'`` otherwise, or ``None`` when both inputs are missing.
    """
    if pd.isna(bp_systolic) and pd.isna(bp_diastolic):
        return None
    try:
        s_val = float(bp_systolic) if pd.notna(bp_systolic) else None
        d_val = float(bp_diastolic) if pd.notna(bp_diastolic) else None
    except Exception:
        return None
    if (s_val is not None and s_val >= 140) or (d_val is not None and d_val >= 90):
        return "high"
    if (s_val is not None and s_val < 90) or (d_val is not None and d_val < 60):
        return "low"
    return "normal"


def derive_patient_status(patients: pd.DataFrame, measurements: pd.DataFrame) -> pd.DataFrame:
    """Derive patient-level status from patients and measurements.

    Parameters
    ----------
    patients : pandas.DataFrame
        Patient-level DataFrame containing at least a ``patient_id`` column and
        demographic columns used for height assumption (``sex``, ``ethnicity``).
    measurements : pandas.DataFrame
        Measurement records containing at least ``patient_id``, ``date``, ``bp_systolic``,
        ``bp_diastolic`` and ``weight_kg``.

    Returns
    -------
    pandas.DataFrame
        One-row-per-patient DataFrame with derived columns including ``bmi``,
        ``weight_category``, ``bp_category``, and assumed height fields.
    """
    latest = latest_measurements(measurements)
    df = patients.merge(
        latest[["patient_id", "date", "bp_systolic", "bp_diastolic", "weight_kg"]],
        on="patient_id",
        how="left",
    )

    df = assume_heights(df)

    # BMI
    df["bmi"] = df.apply(lambda r: compute_bmi(r.get("weight_kg"), r.get("height_m")), axis=1)
    df["weight_category"] = df["bmi"].apply(weight_category)

    # BP category
    df["bp_category"] = df.apply(lambda r: bp_category(r.get("bp_systolic"), r.get("bp_diastolic")), axis=1)

    out = df[
        [
            "patient_id",
            "sex",
            "ethnicity",
            "date",
            "bp_systolic",
            "bp_diastolic",
            "bp_category",
            "weight_kg",
            "height_cm",
            "height_source",
            "bmi",
            "weight_category",
        ]
    ].rename(columns={"date": "measurement_date"})

    return out


def save_output(df: pd.DataFrame, path: Path) -> None:
    """Save derived DataFrame to CSV.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be written to disk.
    path : pathlib.Path
        Destination file path for the CSV to create. Parent directories will be
        created if they do not exist.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> int:
    """Command-line entry point.

    Returns
    -------
    int
        Exit code: 0 for success, 2 for missing input files or malformed data,
        3 for missing dependencies.
    """
    if not PATIENTS_FILE.exists():
        print(f"Missing patients file: {PATIENTS_FILE}", file=sys.stderr)
        return 2
    if not MEASUREMENTS_FILE.exists():
        print(f"Missing measurements file: {MEASUREMENTS_FILE}", file=sys.stderr)
        return 2

    patients = load_patients(PATIENTS_FILE)
    measurements = load_measurements(MEASUREMENTS_FILE)

    if "date" not in measurements.columns:
        print("measurements.csv must contain a 'date' column", file=sys.stderr)
        return 2

    out = derive_patient_status(patients, measurements)
    save_output(out, OUTPUT_FILE)
    print(f"Wrote derived dataset to {OUTPUT_FILE} (rows: {len(out)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
