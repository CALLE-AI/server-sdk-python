# Release

This repository publishes the Python distribution `calle-ai`. Application code
imports it as `calle`.

## Release infrastructure

Production publishing uses PyPI Trusted Publishing. Configure the publisher
with these values:

- Owner: `CALLE-AI`
- Repository: `server-sdk-python`
- Workflow: `publish-python.yml`
- Environment: `pypi`

Configure the GitHub `pypi` environment with required reviewers, prevent
self-review, and restrict it to protected release tags. The workflow does not
use a long-lived PyPI token.

## Prepare a release

1. Set a new, previously unpublished stable version in `pyproject.toml` and
   keep the OpenAPI and generated-client version metadata aligned.
2. Move the relevant entries from `Unreleased` in [CHANGELOG.md](./CHANGELOG.md)
   into a section for that version and date.
3. Run the release gates:

   ```bash
   bash scripts/validate.sh
   ```

4. Merge the release preparation pull request into `main` after CI and review
   complete.

The validation script checks the OpenAPI contract, tests, lint, types,
examples, public-repository hygiene, distribution metadata, packaged license
files, and fresh wheel and source-distribution installs.

## Publish a stable release

1. Create a `vX.Y.Z` tag on the intended commit from `main`.
2. Publish a non-prerelease GitHub Release for that tag.
3. Approve the `pypi` environment deployment after checking the tag, version,
   commit, changelog, and build result.
4. Confirm that the publish and post-publish verification jobs complete.

The workflow rejects a tag that does not exactly match `vX.Y.Z`, differs from
the version in `pyproject.toml`, or points to a commit not contained in
`origin/main`. Before installing project dependencies, it also requires PyPI to
return an exact `404` for the candidate version; an existing version, network
failure, or any other response stops the release.

The workflow builds and validates the wheel and source distribution once and
uploads them with a SHA-256 manifest. The publish job downloads that artifact
and rechecks its exact file set, checksums, package version, MIT metadata, and
LICENSE before handing the same files to Trusted Publishing. Only the publish
job receives `id-token: write`.

Publishing and merging are separate actions: a push or merge to `main` never
publishes a package.

## Manual dry run

Running `Publish Python package` with `workflow_dispatch` only builds,
validates, and uploads the distribution artifact. A manual run never enters the
PyPI environment and never publishes.

## Post-publish verification

After upload, the workflow waits for exact-version metadata on PyPI and installs
that version into a fresh virtual environment before importing the main client
and generated Goal models.

An upload is irreversible. If registry or install smoke verification fails,
the package may already be published. Check PyPI before retrying or creating
another release; a red smoke-test job does not mean the upload was rolled back.

For a manual check from the release commit:

```bash
version="$(python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')"
curl --fail --silent --show-error "https://pypi.org/pypi/calle-ai/${version}/json" >/dev/null

tmpdir="$(mktemp -d)"
python -m venv "$tmpdir/.venv"
. "$tmpdir/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install "calle-ai==$version"
python -c 'from calle import CalleClient; c = CalleClient(api_key="smoke"); assert callable(c.goals.run_and_wait); c.close()'
```

## Version rules

- Patch releases fix SDK wrapper bugs, type issues, packaging metadata, README
  examples, or distribution issues without changing public API behavior.
- Minor releases add backward-compatible API fields, endpoints, or SDK helpers.
- Major releases make breaking public API, method signature, stable error, or
  webhook delivery contract changes.

Keep TypeScript, Python, OpenAPI, and public docs versions aligned by default. A
single-language patch is allowed only when the shared API contract and
cross-language behavior do not change.

Do not reuse a previously published version. PyPI package versions are
immutable.
