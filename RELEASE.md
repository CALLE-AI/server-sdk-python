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
uv run python scripts/verify_openapi_contract.py
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile examples/create_and_wait.py examples/webhook_server.py
uv build
uvx twine check dist/*
python -m venv /tmp/calle-python-sdk-smoke
. /tmp/calle-python-sdk-smoke/bin/activate
python -m pip install dist/*.whl
python -c 'from calle import CalleClient; print(CalleClient)'
deactivate
python -m venv /tmp/calle-python-sdk-sdist-smoke
. /tmp/calle-python-sdk-sdist-smoke/bin/activate
python -m pip install dist/*.tar.gz
python -c 'from calle import CalleClient; print(CalleClient)'
```

The CI workflow also installs the built wheel in a fresh virtual environment and
imports `CalleClient`.

## TestPyPI rehearsal

1. Confirm `pyproject.toml` has a unique beta version, for example `0.1.0b1`.
2. Confirm GitHub Actions secret `TEST_PYPI_API_TOKEN` is configured, unless the
   package has been moved to TestPyPI Trusted Publishing.
3. Open the `Publish Python package` workflow in GitHub Actions.
4. Run the workflow from `main` with repository `testpypi` and the selected
   release identity.
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
3. Run the `Publish Python package` workflow from `main` with repository `pypi`
   and the selected release identity.
4. Confirm the workflow completes the post-publish install smoke test.

## Registry identity notes

PyPI Trusted Publishing is preferred once the repository is ready for public
release. Because `calle-ai` has not been published yet, configure a pending
publisher first. TestPyPI and PyPI are separate registries, so configure the
publisher separately in each registry you plan to use.

Configure the pending publisher for:

- Owner: `CALLE-AI`
- Repository: `server-sdk-python`
- Workflow filename: `publish-python.yml`
- Environment name for TestPyPI: `testpypi`
- Environment name for PyPI: `pypi`
- Project name: `calle-ai`

When using Trusted Publishing, run the workflow with auth
`trusted-publishing`. When using API tokens, run it with auth `token` and
configure `TEST_PYPI_API_TOKEN` or `PYPI_API_TOKEN`.

If the package already exists on PyPI later, use the project's Publishing page
to add or update the trusted publisher with the same owner, repository, workflow
filename, and environment.
