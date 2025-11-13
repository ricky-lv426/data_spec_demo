# scripts

This folder contains a small script to derive patient-level blood pressure and weight categories from the demo CSVs in `data/`.

Files
- `derive_patient_status.py` — reads `data/sample_patients.csv` and `data/measurements.csv`, selects the latest measurement per patient, computes BMI using assumed average heights (by sex and ethnicity), assigns weight categories (underweight / normal / overweight / obese) and blood-pressure categories (low / normal / high), then writes `data/derived_patient_status.csv`.

Assumptions and thresholds
- Average heights (cm) are assumed per sex & ethnicity for this demo. These are approximate and only for illustrative purposes.
- BMI categories use standard cutoffs:
  - underweight: BMI < 18.5
  - normal: 18.5 ≤ BMI < 25
  - overweight: 25 ≤ BMI < 30
  - obese: BMI ≥ 30
- Blood pressure is classified as:
  - high: systolic >= 140 or diastolic >= 90
  - low: systolic < 90 or diastolic < 60
  - normal: otherwise

Usage

Python version

Install dependencies (from the repository root):

```bash
pip install -r scripts/requirements.txt
```

Then run the script from the repository root:

```bash
python3 scripts/derive_patient_status.py
```

Output

- `data/derived_patient_status.csv` — contains `patient_id`, `bp_category`, `weight_category`, BMI and supporting columns.

Notes

- This is a small demo script with reasonable defaults. If you want different average heights, alternative BP thresholds, or another rule for selecting weight/BP (e.g. mean instead of latest), edit `scripts/derive_patient_status.py` accordingly.
