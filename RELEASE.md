# Release

This repository publishes the Python distribution `calle-ai`. Application code imports it as `calle`.

## Current status

TestPyPI has the prerelease package:

```text
calle-ai==0.1.0b1
```

The current production PyPI release version is:

```text
calle-ai==0.2.0
```

For this release, use token-based PyPI publishing with the GitHub Actions secret `PYPI_API_TOKEN`.

## Release gates

Run these checks before publishing:

```bash
bash scripts/validate.sh
```

The validation script checks the OpenAPI contract, tests, lint, types, examples, distribution metadata, wheel install, source distribution install, and imports `CalleClient` from fresh virtual environments.

## Stable PyPI publish

1. Confirm `pyproject.toml` has a unique stable version.
2. Confirm GitHub Actions secret `PYPI_API_TOKEN` is configured.
3. Open the `Publish Python package` workflow in GitHub Actions.
4. Run the workflow from `main` with repository `pypi` and auth `token`.
5. Confirm the workflow completes the post-publish install smoke test.

Manual verification:

```bash
curl --fail --silent --show-error https://pypi.org/pypi/calle-ai/json >/dev/null

tmpdir="$(mktemp -d)"
python -m venv "$tmpdir/.venv"
. "$tmpdir/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install calle-ai==0.2.0
python -c 'from calle import CalleClient; print(CalleClient)'
```

## Version rules

- Patch releases fix SDK wrapper bugs, type issues, packaging metadata, README examples, or distribution issues without changing public API behavior.
- Minor releases add backward-compatible API fields, endpoints, or SDK helpers.
- Major releases make breaking public API, method signature, stable error, or webhook signature contract changes.

Keep TypeScript, Python, OpenAPI, and public docs versions aligned by default. A single-language patch is allowed only when the shared API contract and cross-language behavior do not change.

Do not reuse a previously published version. PyPI package versions are immutable.

## Registry identity notes

Token-based publishing requires a PyPI API token stored as the GitHub Actions secret `PYPI_API_TOKEN`.

PyPI Trusted Publishing is a future optional improvement. To switch later, configure the PyPI publisher for:

- Owner: `CALLE-AI`
- Repository: `server-sdk-python`
- Workflow filename: `publish-python.yml`
- Environment name for PyPI: `pypi`
- Project name: `calle-ai`

When using API tokens, run the workflow with auth `token`. When Trusted Publishing is configured later, run the workflow with auth `trusted-publishing`.

TestPyPI and PyPI are separate registries. TestPyPI success does not prove production PyPI availability.
