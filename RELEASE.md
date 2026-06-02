# Release

This repository publishes the Python distribution `calle-ai`. Application code
imports it as `calle`.

## Current status

The package source, CI, and publish workflow are ready. The first registry
publish still requires one of these release identities:

- GitHub Actions secret `TEST_PYPI_API_TOKEN` for TestPyPI,
- GitHub Actions secret `PYPI_API_TOKEN` for PyPI, or
- PyPI/TestPyPI Trusted Publishing configured for this repository and workflow.

Until the first beta is published, use a local checkout for examples and
integration testing.

## Release gates

Run these checks before publishing:

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile examples/create_and_wait.py examples/webhook_server.py
uv build
uvx twine check dist/*
```

The CI workflow also installs the built wheel in a fresh virtual environment and
imports `CalleClient`.

## TestPyPI rehearsal

1. Confirm `pyproject.toml` has a unique beta version, for example `0.1.0b1`.
2. Confirm GitHub Actions secret `TEST_PYPI_API_TOKEN` is configured, unless the
   package has been moved to TestPyPI Trusted Publishing.
3. Open the `Publish Python package` workflow in GitHub Actions.
4. Run the workflow from `main` with repository `testpypi`.
5. Confirm the workflow completes the post-publish install smoke test.

Manual verification:

```bash
python -m venv .venv
. .venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  calle-ai==0.1.0b1
python -c 'from calle import CalleClient; print(CalleClient)'
```

## PyPI publish

Use PyPI only after the TestPyPI package has been installed and tested in at
least one backend integration.

1. Increment the version in `pyproject.toml`. PyPI package versions are
   immutable.
2. Confirm GitHub Actions secret `PYPI_API_TOKEN` is configured, unless the
   package has been moved to PyPI Trusted Publishing.
3. Run the `Publish Python package` workflow from `main` with repository `pypi`.
4. Confirm the workflow completes the post-publish install smoke test.

## Registry identity notes

PyPI Trusted Publishing is preferred once the repository is ready for public
release. Configure a pending publisher for:

- Owner: `CALLE-AI`
- Repository: `server-sdk-python`
- Workflow filename: `publish-python.yml`
- Project name: `calle-ai`
