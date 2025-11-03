# Demo data repository

This repository is a small demo containing synthetic CSV data and a documentation page (data specification) that can be published to GitHub Pages.

What is included:

- `data/sample_patients.csv` — synthetic patient demographics
- `data/measurements.csv` — synthetic clinical measurements
- `data-specification.md` — explainer and data dictionary
- `.github/workflows/publish-pages.yml` — a manual GitHub Actions workflow that publishes the documentation and the data to the `gh-pages` branch using GitHub Pages

To publish the documentation to GitHub Pages, open the Actions tab in GitHub, locate the `Publish data specification` workflow, and trigger it manually (workflow dispatch). The workflow converts the markdown to HTML and publishes to the `gh-pages` branch.

Important: if the workflow fails with a 403 permission error ("Permission to <owner>/<repo>.git denied to github-actions[bot]."), the cause is usually that the default `GITHUB_TOKEN` does not have permission to push to `gh-pages` for your repository or that branch protection / organization policies prevent the push.

Two ways to fix this:

1. (Preferred & quick) Create a Personal Access Token (PAT) with repo permissions and add it as a repository secret named `GH_PAGES_PAT`, then the workflow will use that to push. Steps:
	- In GitHub, go to Settings → Developer settings → Personal access tokens → Tokens (classic) and create a token with the `repo` scope (or a fine-grained token with appropriate repository write access).
	- In your repository, go to Settings → Secrets and variables → Actions → New repository secret. Name it `GH_PAGES_PAT` and paste the token.
	- Re-run the workflow.

2. (If you prefer to use the built-in token) In the repository Settings → Actions → General → Workflow permissions, set "Read and write permissions" for the `GITHUB_TOKEN`. Also review Branch protection rules for `gh-pages` and ensure the workflow is allowed to push (remove restrictive "Restrict who can push" rules that exclude GitHub Actions). After changing settings, re-run the workflow.

If you want, I can update the workflow further (for example add a conditional fallback) or add a validation step to fail early with a clearer message.
