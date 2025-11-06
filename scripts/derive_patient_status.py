#!/usr/bin/env python3
"""
Derive patient-level blood-pressure and weight category using demo data (Python version)
Writes: data/derived_patient_status.csv

Usage:
    python3 scripts/derive_patient_status.py

This script mirrors the behaviour of the repository's R version but written in Python.

"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATIENTS_FILE = ROOT / "data" / "sample_patients.csv"
MEASUREMENTS_FILE = ROOT / "data" / "measurements.csv"
OUTPUT_FILE = ROOT / "data" / "derived_patient_status.csv"


def main() -> int:
    if not PATIENTS_FILE.exists():
        print(f"Missing patients file: {PATIENTS_FILE}", file=sys.stderr)
        return 2
    if not MEASUREMENTS_FILE.exists():
        print(f"Missing measurements file: {MEASUREMENTS_FILE}", file=sys.stderr)
        return 2

    patients = pd.read_csv(PATIENTS_FILE)
    measurements = pd.read_csv(MEASUREMENTS_FILE, parse_dates=["date"])

    if "date" not in measurements.columns:
        print("measurements.csv must contain a 'date' column", file=sys.stderr)
        return 2

    # Latest measurement per patient (by date)
    measurements_sorted = measurements.sort_values(["patient_id", "date"], ascending=[True, False])
    latest = measurements_sorted.drop_duplicates(subset=["patient_id"], keep="first").copy()

    df = patients.merge(
        latest[["patient_id", "date", "bp_systolic", "bp_diastolic", "weight_kg"]],
        on="patient_id",
        how="left",
    )

    # Assumed average heights (cm) by sex and ethnicity (demo-only)
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

    df = df.astype({"sex": "object", "ethnicity": "object"})
    df = df.merge(height_map, on=["sex", "ethnicity"], how="left")
    df = df.merge(sex_fallback, on="sex", how="left")
    df["height_cm"] = df["height_cm"].fillna(df["height_cm_fallback"])
    df["height_source"] = df.apply(
        lambda r: (
            "assumed_by_sex_ethnicity"
            if pd.notna(r.get("ethnicity")) and pd.notna(r.get("height_cm")) and ((r.get("sex"), r.get("ethnicity")) in set(map(tuple, height_map[["sex", "ethnicity"]].values)))
            else "assumed_by_sex"
        ),
        axis=1,
    )

    # Compute BMI
    df["height_m"] = df["height_cm"].apply(lambda x: x / 100 if pd.notna(x) else None)

    def compute_bmi(row):
        w = row.get("weight_kg")
        h = row.get("height_m")
        try:
            if pd.isna(w) or pd.isna(h) or h == 0:
                return None
            return round(float(w) / (float(h) ** 2), 1)
        except Exception:
            return None

    df["bmi"] = df.apply(compute_bmi, axis=1)

    # Weight category (BMI)
    def weight_category(bmi):
        if pd.isna(bmi):
            return None
        if bmi < 18.5:
            return "underweight"
        if bmi < 25:
            return "normal"
        if bmi < 30:
            return "overweight"
        return "obese"

    df["weight_category"] = df["bmi"].apply(weight_category)

    # Blood pressure category
    def bp_category(row):
        s = row.get("bp_systolic")
        d = row.get("bp_diastolic")
        if pd.isna(s) and pd.isna(d):
            return None
        try:
            s_val = float(s) if pd.notna(s) else None
            d_val = float(d) if pd.notna(d) else None
        except Exception:
            return None
        if (s_val is not None and s_val >= 140) or (d_val is not None and d_val >= 90):
            return "high"
        if (s_val is not None and s_val < 90) or (d_val is not None and d_val < 60):
            return "low"
        return "normal"

    df["bp_category"] = df.apply(bp_category, axis=1)

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

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote derived dataset to {OUTPUT_FILE} (rows: {len(out)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
