#!/usr/bin/env bash
set -euo pipefail

artifact="${1:?usage: bash scripts/smoke_install_dist.sh dist/<artifact>}"
smoke_dir="$(mktemp -d)"
trap 'rm -rf "$smoke_dir"' EXIT

if command -v python3 >/dev/null 2>&1; then
  python_cmd="python3"
elif command -v python >/dev/null 2>&1; then
  python_cmd="python"
else
  echo "Missing python3 or python on PATH." >&2
  exit 1
fi

"$python_cmd" -m venv "$smoke_dir/.venv"
. "$smoke_dir/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install "$artifact"
python -c 'from calle import CalleClient; print(CalleClient)'
