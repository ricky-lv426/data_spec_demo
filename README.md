# Demo data repository

This repository is a small demo containing synthetic CSV data and a documentation page (data specification) that can be published to GitHub Pages.

What is included:

- `data/sample_patients.csv` — synthetic patient demographics
- `data/measurements.csv` — synthetic clinical measurements
- `data-specification.md` — explainer and data dictionary
- `scripts/` — small utility scripts to derive example outputs from the CSVs (see `scripts/README.md`)
- `tests/` — pytest unit tests for script functions
- `.github/workflows/publish-pages.yml` — manual GitHub Actions workflow that publishes the documentation and the data to the `gh-pages` branch
- `.github/workflows/python-tests.yml` — CI workflow that installs test deps and runs pytest on pushes/PRs to `main`

Quick usage

Build the site locally (the same tool used in CI):

```bash
# from repository root
pandoc data-specification.md -o site/index.html --standalone --metadata title="Data specification" --css=assets/style.css
mkdir -p site/data site/assets
cp -R data/* site/data/
cp -R assets/* site/assets/
open site/index.html
```

Platform notes

- macOS

	- Install pandoc with Homebrew: `brew install pandoc`.
	- The commands above work as-is; `open site/index.html` will open the page in the default browser.

- Linux (Debian/Ubuntu)

	- Install pandoc: `sudo apt-get update && sudo apt-get install -y pandoc`.
	- Use `xdg-open site/index.html` to open the page from a terminal.

- Windows (PowerShell)

	- Install pandoc via Chocolatey (if available): `choco install pandoc` or download the installer from https://pandoc.org/installing.html.
	- From PowerShell you can run the same pandoc command (remove the `mkdir -p` usage):

		```powershell
		pandoc data-specification.md -o site/index.html --standalone --metadata title="Data specification" --css=assets/style.css
		New-Item -ItemType Directory -Force -Path site\data,site\assets
		Copy-Item -Recurse data\* site\data\
		Copy-Item -Recurse assets\* site\assets\
		Start-Process site\index.html
		```

- Windows (cmd)

	- Use the pandoc installer from the website or Chocolatey. In cmd.exe:

		```cmd
		pandoc data-specification.md -o site/index.html --standalone --metadata title="Data specification" --css=assets/style.css
		mkdir site\data
		mkdir site\assets
		xcopy data\* site\data\ /E /I
		xcopy assets\* site\assets\ /E /I
		start site\index.html
		```

Run the demo script (derives patient-level status):

```bash
pip install -r scripts/requirements.txt
python3 scripts/derive_patient_status.py
```

Run unit tests locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
pytest -q
```

CI and workflows

- The `Publish data specification` workflow (`.github/workflows/publish-pages.yml`) is manual (workflow_dispatch) and publishes site output to the `gh-pages` branch. If the action cannot push, add a PAT as `GH_PAGES_PAT` or enable appropriate workflow permissions.
- The `Run Python tests` workflow (`.github/workflows/python-tests.yml`) runs pytest on pushes and pull requests to `main`. Tests install `scripts/requirements.txt` and `pytest` in CI.

Contributing

See `CONTRIBUTING.md` for guidance on PRs, testing, and coding conventions. In particular:

- Add unit tests for new script functions and update `scripts/requirements.txt` if you add dependencies.
- Ensure `scripts/` is importable (include `scripts/__init__.py` or ensure PYTHONPATH is set in CI) so tests can import modules under `scripts`.

If you'd like help writing tests or adjusting CI, open an issue or a draft PR and tag a maintainer.