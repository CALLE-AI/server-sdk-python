## Summary

Describe the SDK behavior, documentation, or release workflow change.

## Checklist

- [ ] I kept this change within the supported server SDK scope.
- [ ] I did not add browser/client-side patterns that expose CALL-E API keys.
- [ ] I updated tests, examples, or docs when behavior changed.
- [ ] I ran the relevant local checks.

## Local checks

```bash
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile examples/create_and_wait.py examples/webhook_server.py
uv build
uvx twine check dist/*
```
