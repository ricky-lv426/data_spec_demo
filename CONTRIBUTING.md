# Contributing / Working practices

Thanks for contributing to this demo data specification repository. This document describes the working practices for raising issues, creating pull requests (PRs), and publishing the documentation. Follow these steps to help keep contributions clear, reviewable and safe.

## Quick checklist for contributors

- Fork the repository and create a feature branch for your change.
- Open an issue first if your change is non-trivial (data changes, schema changes, or workflow changes).
- Create a PR that targets `main` from a feature branch with a clear title and description.
- Link the PR to the issue (if any), include a short summary and a checklist of what changed.
- If you change CSV formats or columns, document the change in `data-specification.md` and explain the rationale.

## Branching and branch names

- Use descriptive branch names. Examples:
  - `fix/typo-data-spec`
  - `feat/add-example-measurement`
  - `chore/update-workflow`

## Issues

- Use issues to propose new features, report problems, or request changes to the data spec.
- When opening an issue include:
  - A short title summarising the request.
  - Reproducible steps or a small example (when relevant).
  - The proposed change or expected behaviour.
  - Any security or privacy concerns.

## Pull requests (PRs)

What to include in the PR description:

- A short summary of what the PR does.
- The motivation for the change and links to any related issue(s).
- A checklist of what reviewers should verify (see PR checklist below).

PR checklist (suggested)

- [ ] The PR has a clear title and description.
- [ ] There is a linked issue if the change is non-trivial.
- [ ] `data-specification.md` has been updated for any schema/field changes.
- [ ] CSV changes are synthetic (this repo contains only synthetic/demo data) and include a note explaining why values changed.
- [ ] Workflow changes documented and tested (e.g., local test or documented steps to run on Actions).

## Review process

- At least one reviewer should approve changes before merging.
- For changes that affect published outputs (site, CSVs, layout), reviewers should:
  - Build the site locally (instructions below) and confirm the `index.html` and links look correct.
  - Inspect CSVs for expected headers and sample values.

## How to build and preview locally

You can generate the site locally with `pandoc` (the same tool used in CI/workflow):

1. Install pandoc (macOS: `brew install pandoc`).
2. From the repository root run:

```bash
cd data_spec_demo
pandoc data-specification.md -o site/index.html --standalone --metadata title="Data specification" --css=assets/style.css
mkdir -p site/data site/assets
cp -R data/* site/data/
cp -R assets/* site/assets/
open site/index.html
```

This opens a local preview of the generated site; check the CSV links under `data/` and the styling.

## Publishing and workflows

- This repository uses a manual GitHub Actions workflow (`.github/workflows/publish-pages.yml`) to build the site and publish to the `gh-pages` branch.
- The workflow is intentionally `workflow_dispatch` (manual) only. To run the workflow:
  - Go to the repository on GitHub → Actions → "Publish data specification" → Run workflow.

Permissions notes

- If the workflow fails with a 403 ("Permission to ... denied to github-actions[bot]"), follow the README guidance to add a Personal Access Token (PAT) as a repository secret named `GH_PAGES_PAT`, or enable "Read and write" workflow permissions in the repository settings. Document any organizational constraints in the issue or PR so reviewers can check them.

## CSV and data change rules

- This repo contains synthetic demo data only. Never add real patient or identifiable data.
- When changing column names/types in CSVs:
  - Update `data-specification.md` to document the change and reasoning.
  - Add a short note in the PR description describing how downstream consumers should adapt.

## Commit messages

- Keep commit messages concise and meaningful. Use prefixes like `fix:`, `feat:`, `docs:`, `chore:` where helpful.

## Security and privacy

- This repository uses only synthetic data. Do not add secrets, tokens, or private data in commits. Use GitHub Secrets for tokens needed by workflows.

## Maintainers and escalation

- If you're unsure how to proceed, open an issue and tag a maintainer or team. If a PR requires special permissions (for example changes to the Pages settings), note that in the PR so maintainers can take action.

Thank you for contributing — clear issues and small, focused PRs make reviews fast and reliable.
