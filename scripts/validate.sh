#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
uv sync --all-groups
uv run python scripts/verify_openapi_contract.py
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile examples/create_and_wait.py examples/webhook_server.py
uv build
uvx twine check dist/*
bash scripts/smoke_install_dist.sh dist/*.whl
bash scripts/smoke_install_dist.sh dist/*.tar.gz
