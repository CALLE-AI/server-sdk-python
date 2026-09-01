#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
uv sync --all-groups
uv run python scripts/verify_openapi_contract.py
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile \
  examples/create_and_wait.py \
  examples/run_goal_and_wait.py \
  examples/webhook_server.py
python3 scripts/check_public_repo_hygiene.py
uv build
uvx twine check dist/*
uv run python scripts/verify_distribution_artifacts.py dist --write-manifest
bash scripts/smoke_install_dist.sh dist/*.whl
bash scripts/smoke_install_dist.sh dist/*.tar.gz
