# Demo data repository

This repository is a small demo containing synthetic CSV data and a documentation page (data specification) that can be published to GitHub Pages.

What is included:

- `data/sample_patients.csv` — synthetic patient demographics
- `data/measurements.csv` — synthetic clinical measurements
- `data-specification.md` — explainer and data dictionary
- `.github/workflows/publish-pages.yml` — a manual GitHub Actions workflow that publishes the documentation and the data to the `gh-pages` branch using GitHub Pages

To publish the documentation to GitHub Pages, open the Actions tab in GitHub, locate the `Publish data specification` workflow, and trigger it manually (workflow dispatch). The workflow converts the markdown to HTML and publishes to the `gh-pages` branch.

Important: To get the publishing workflow to work, you need to create a Personal Access Token (PAT) with repo permissions and add it as a repository secret named `GH_PAGES_PAT`, then the workflow will use that to push. Steps to implement this are:
	- In GitHub, go to Settings → Developer settings → Personal access tokens → Tokens (classic) and create a token with the `repo` scope (or a fine-grained token with appropriate repository write access).
	- In your repository, go to Settings → Secrets and variables → Actions → New repository secret. Name it `GH_PAGES_PAT` and paste the token.
	- Run the workflow.