# Demo data repository

This repository is a small demo containing synthetic CSV data and a documentation page (data specification) that can be published to GitHub Pages.

What is included:

- `data/sample_patients.csv` — synthetic patient demographics
- `data/measurements.csv` — synthetic clinical measurements
- `data-specification.md` — explainer and data dictionary
- `.github/workflows/publish-pages.yml` — a manual GitHub Actions workflow that publishes the documentation and the data to the `gh-pages` branch using GitHub Pages

To publish the documentation to GitHub Pages, open the Actions tab in GitHub, locate the `Publish data specification` workflow, and trigger it manually (workflow dispatch). The workflow converts the markdown to HTML and publishes to the `gh-pages` branch.
