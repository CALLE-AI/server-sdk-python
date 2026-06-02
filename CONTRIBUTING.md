# Contributing

This SDK is the Python server SDK for the CALL-E Developer API. It is meant for
trusted backend services, workers, and automation systems.

## Development setup

```bash
uv sync --all-groups
uv run pytest -q
uv run ruff check .
uv run mypy src/calle
uv run python -m py_compile examples/create_and_wait.py examples/webhook_server.py
uv build
uvx twine check dist/*
```

## Local examples

```bash
export CALLE_API_KEY="calle_test_key"
export CALLE_BASE_URL="https://api.example.com"
export CALLE_EXAMPLE_PHONE="+14155550100"
uv run python examples/create_and_wait.py

export CALLE_WEBHOOK_SECRET="whsec_test_key"
uv run python examples/webhook_server.py
```

The webhook example listens on `POST /calle/webhook` and verifies
`CALL-E-Timestamp` plus `CALL-E-Signature` against the raw request body.

## Phase 1 scope

In scope:

- Create a call.
- Read a call.
- Poll until a terminal call result.
- List call events.
- Verify and unwrap signed webhook events.

Out of scope for Phase 1:

- Async client support.
- Batch calls.
- Cancel calls.
- Recurring or scheduled calls.
- Project-level webhook management.
- Pydantic result schema helpers.

## API contract changes

The SDK is generated and wrapped from `openapi/calle.openapi.yaml`.

When the OpenAPI contract changes:

1. Update `openapi/calle.openapi.yaml`.
2. Regenerate generated client code if the generated package is in use.
3. Update wrappers and tests for any changed behavior.
4. Run the full development check list above.

## Pull requests

Keep changes small and focused. Include tests for wrapper behavior, error
handling, webhook signature verification, and any changed API contract surface.

Do not add browser examples or patterns that expose CALL-E API keys to client
code.
