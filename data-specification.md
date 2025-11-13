# Data specification — Demo dataset

This repository contains a small demo dataset (CSV) and a specification document describing the fields and provenance. The purpose of this demo is to illustrate how a data package for diabetes-related primary care metrics might be structured for sharing and documentation.

## Files included

- [data/sample_patients.csv](data/sample_patients.csv) — one row per patient with demographic fields.
- [data/measurements.csv](data/measurements.csv) — repeated measures per patient with clinical measurements.

Both CSV files are intentionally synthetic and contain dummy values for demonstration only.

## How the data were obtained

This is simulated data created for demonstration. No real patient data were used. Values were chosen to mimic plausible distributions and column names commonly used in primary care diabetes datasets.

## Data dictionary

- patient_id: Unique patient identifier (synthetic).
- age: Integer age in years.
- sex: 'M' or 'F'.
- ethnicity: Broad ethnicity group.
- imd_quintile: Index of Multiple Deprivation quintile (1 = most deprived, 5 = least deprived).
- date: ISO date of measurement (YYYY-MM-DD).
- hba1c_mmol_per_mol: HbA1c value in mmol/mol.
- bp_systolic: Systolic blood pressure in mmHg.
- bp_diastolic: Diastolic blood pressure in mmHg.
- weight_kg: Weight in kilograms (one decimal allowed).

## Provenance and processing notes

- Synthetic generation: values were hand-crafted to be plausible and do not correspond to any real individual.
- No identifying information is present.

## How to access the data from the published site

When this repository's data specification is published to GitHub Pages (via the manual workflow `Publish data specification`), a static site is created containing this document and the `data/` folder. Links on the published page point to the CSV files here:

- [sample_patients.csv](data/sample_patients.csv)
- [measurements.csv](data/measurements.csv)

You can click these links on the published site to download or view the raw CSV files.

## License and reuse

This demo dataset is provided for educational/demonstration purposes. You may reuse the data and documentation freely.

## Contact

Repository owner: demo maintainer (no real contact provided in this demo).


## Scripts

The `scripts/` folder contains small utility scripts used to process the demo CSVs. The primary script included in this demo is `derive_patient_status.py`, which derives patient-level blood pressure and weight categories from the example data.

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
