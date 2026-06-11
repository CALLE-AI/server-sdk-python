# calle-ai

Python server SDK for the CALL-E Developer API.

Use this SDK from backend services, workers, and other trusted server
environments. Do not expose CALL-E API keys in browser code.

## Documentation

- Developer docs: <https://docs.heycall-e.com/>
- SDK guide: <https://docs.heycall-e.com/#/sdks>
- API Reference: <https://docs.heycall-e.com/#/api-reference>
- Webhooks: <https://docs.heycall-e.com/#/webhooks>
- Changelog: <https://docs.heycall-e.com/#/changelog>

## Install

Install the stable package from PyPI:

```bash
pip install calle-ai
```

Pin the current stable release when your deployment process requires exact package reproducibility:

```bash
pip install calle-ai==0.2.0
```

Use a local checkout for development and package smoke tests:

```bash
bash scripts/validate.sh
```

## Examples

Set the API key before running call examples:

```bash
export CALLE_API_KEY="calle_test_key"
export CALLE_BASE_URL="https://api.heycall-e.com"
export CALLE_EXAMPLE_PHONE="+14155550100"
```

Run the create-and-wait example from a local checkout:

```bash
uv run python examples/create_and_wait.py
```

Run the webhook receiver example:

```bash
export CALLE_WEBHOOK_SECRET="whsec_test_key"
uv run python examples/webhook_server.py
```

The webhook receiver listens on `POST /calle/webhook` and verifies
`CALL-E-Timestamp` and `CALL-E-Signature` against the raw request body.

## Quickstart

```python
import os
from calle import CalleClient

client = CalleClient(
    api_key=os.environ["CALLE_API_KEY"],
    base_url="https://api.heycall-e.com",
)

call = client.calls.create_and_wait(
    task="Call each recipient and ask whether they can attend Friday lunch in San Francisco.",
    recipients=[{"phones": ["+14155550100"], "region": "US", "locale": "en-US"}],
    result_schema={
        "type": "object",
        "required": ["completed_count"],
        "properties": {
            "completed_count": {"type": "integer"},
        },
    },
    recipient_result_schema={
        "type": "object",
        "required": ["can_attend"],
        "properties": {
            "can_attend": {"type": "string", "enum": ["yes", "no", "unknown"]},
        },
    },
    metadata={"workflow_run_id": "wf_123"},
    idempotency_key="wf_123_friday_lunch",
)

print(call["status"], call["structured_result"])
print(call["task_completed"], call["completion_confidence"], call["evidence"])
print(call["recipients"][0]["structured_result"])
```

## Webhook Verification

```python
event = client.webhooks.unwrap(
    raw_body=raw_body,
    headers=headers,
    secret=os.environ["CALLE_WEBHOOK_SECRET"],
)
```

## Release

This repository publishes the Python distribution `calle-ai`. Application code
imports it as `calle`.

See [RELEASE.md](./RELEASE.md) for the release checklist, GitHub Actions
workflow, and post-publish install smoke test.

Prerequisites:

- Create a PyPI API token and add it to this repository as the GitHub Actions secret `PYPI_API_TOKEN`.
- Keep the package version in `pyproject.toml` unique before each publish.

Manual stable PyPI publish:

1. Open the `Publish Python package` GitHub Actions workflow.
2. Run it from `main` with repository `pypi` and auth `token`.
3. Verify install in a temporary environment:

```bash
python -m venv .venv
. .venv/bin/activate
pip install calle-ai==0.2.0
python -c 'from calle import CalleClient; print(CalleClient)'
```

The current stable version is `0.2.0`. Do not reuse a previously published PyPI version.

## Project Documents

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [SECURITY.md](./SECURITY.md)
- [RELEASE.md](./RELEASE.md)
