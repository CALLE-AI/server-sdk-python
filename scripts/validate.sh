#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
uv sync --all-groups --locked
uv run --locked python scripts/verify_openapi_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked mypy src/calle
uv run --locked python -m py_compile \
  examples/create_and_wait.py \
  examples/run_goal_and_wait.py \
  examples/webhook_server.py
uv run --locked python scripts/check_public_repo_hygiene.py
uv build --no-build-isolation
uv run --locked twine check dist/*
uv run --locked python scripts/verify_distribution_artifacts.py dist --write-manifest
bash scripts/smoke_install_dist.sh dist/*.whl
bash scripts/smoke_install_dist.sh dist/*.tar.gz
