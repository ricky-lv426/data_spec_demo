# Processing workflow

This document describes how the input CSV files are transformed into the derived patient-level
summary `data/derived_patient_status.csv` in this demo repository.

## Inputs

- `data/sample_patients.csv` — one row per patient with demographics.
- `data/measurements.csv` — repeated clinical measurements per patient (contains `date`,
  `bp_systolic`, `bp_diastolic`, `weight_kg`, etc.).

## Script

The derivation is performed by the script:

- `scripts/derive_patient_status.py`
  
You can inspect or download the script and its runtime requirements here:

- [scripts/derive_patient_status.py](scripts/derive_patient_status.py)
- [scripts/requirements.txt](scripts/requirements.txt)

This script:

- Loads `data/sample_patients.csv` and `data/measurements.csv`.
- Selects each patient's latest measurement by `date`.
- Assumes an average height by `sex` and `ethnicity` (demo-only lookup).
- Computes BMI and derives `weight_category` and `bp_category`.
- Writes the one-row-per-patient output to `data/derived_patient_status.csv`.

## Running locally

Install dependencies (if not already available):

```bash
python3 -m pip install -r scripts/requirements.txt
```

Run the script:

```bash
python3 scripts/derive_patient_status.py
```

This will write `data/derived_patient_status.csv` and print the number of rows written.


## Notes

- The height assumptions and classification rules are demo-only and should not be used for
  clinical purposes.
