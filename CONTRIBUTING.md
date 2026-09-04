# Contributing

This SDK is the Python server SDK for the CALL-E Developer API. It is meant for
trusted backend services, workers, and automation systems.

## Development setup

```bash
bash scripts/validate.sh
```

This command verifies the OpenAPI contract, tests, lint, types, examples,
public-repository hygiene, distribution metadata, packaged license files, and
fresh wheel and source-distribution installs.

## Local examples

```bash
export CALLE_API_KEY="calle_test_key"
export CALLE_BASE_URL="https://api.heycall-e.com"
export CALLE_EXAMPLE_PHONE="+14155550100"
uv run python examples/create_and_wait.py

export CALLE_BASE_URL="<APPROVED_TEST_API_BASE_URL>"
export CALLE_GOAL_ID="<PUBLISHED_GOAL_ID>"
export CALLE_GOAL_PHONE="<AUTHORIZED_E164_PHONE>"
export CALLE_GOAL_VARIABLES='{"name":"Alex"}'
export CALLE_IDEMPOTENCY_KEY="<DURABLE_WORKFLOW_KEY>"
uv run python examples/run_goal_and_wait.py

uv run python examples/webhook_server.py
```

The webhook example listens on `POST /calle/webhook` and processes terminal
event JSON after post-call outcome and structured-result finalization. It
deduplicates deliveries with `CALL-E-Event-Id`; CALL-E does not send timestamp
or signature headers.

## Supported scope

In scope:

- Create a call.
- Read a call.
- Poll until a terminal call result.
- List call events.
- List and read published Goals.
- Create a Goal Run with a durable idempotency key.
- Poll until a Goal Run has either a result or an error.
- Receive finalized terminal webhook events without requiring signature
  material.

Out of scope:

- Async client support.
- Batch calls.
- Cancel calls.
- Recurring or scheduled calls.
- Goal authoring and publishing.
- Project-level webhook management.
- Pydantic result schema helpers.

## API contract changes

The SDK is generated and wrapped from `openapi/calle.openapi.yaml`.

When the OpenAPI contract changes:

1. Update `openapi/calle.openapi.yaml`.
2. Regenerate generated client code:

   ```bash
   uv run openapi-python-client generate \
     --path openapi/calle.openapi.yaml \
     --config openapi-python-client.yml \
     --output-path src/calle/generated \
     --meta none \
     --overwrite
   ```

3. Update wrappers and tests for any changed behavior.
4. Run the full development check list above.

## Pull requests

Keep changes small and focused. Include tests for wrapper behavior, error
handling, webhook event handling, and any changed API contract surface.

Do not add browser examples or patterns that expose CALL-E API keys to client
code.

Update [CHANGELOG.md](./CHANGELOG.md) when a change affects package users. Pull
request titles, descriptions, tracked paths, and tracked text must not contain
private collaboration links, unencrypted IP URLs, or references to unconfirmed
public repositories in the CALL-E GitHub organization.

Run the standalone hygiene check with:

```bash
python3 scripts/check_public_repo_hygiene.py
```

The allowlist in that script contains only repositories confirmed for public
use. Add a repository only after confirming that it is public.

## License

By submitting a contribution, you agree that it may be distributed under the
[MIT License](./LICENSE).
