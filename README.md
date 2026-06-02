# calle-ai

Python server SDK for the CALL-E Developer API.

Use this SDK from backend services, workers, and other trusted server
environments. Do not expose CALL-E API keys in browser code.

## Install

```bash
pip install calle-ai
```

For the first TestPyPI rehearsal:

```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  calle-ai==0.1.0b1
```

## Examples

Set the API key before running call examples:

```bash
export CALLE_API_KEY="calle_test_key"
export CALLE_BASE_URL="https://api.example.com"
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
    base_url="https://api.example.com",
)

call = client.calls.create_and_wait(
    task="Call the recipient and ask whether they can attend Friday lunch in San Francisco.",
    recipient={"phone": "+14155550100", "region": "US", "locale": "en-US"},
    result_schema={
        "type": "object",
        "required": ["can_attend"],
        "properties": {
            "can_attend": {"type": "string", "enum": ["yes", "no", "unknown"]},
        },
        "additionalProperties": False,
    },
    metadata={"workflow_run_id": "wf_123"},
    idempotency_key="wf_123_friday_lunch",
)

print(call["status"], call["structured_result"])
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

Prerequisites:

- Create a TestPyPI API token and add it as the GitHub Actions secret
  `TEST_PYPI_API_TOKEN`.
- Create a PyPI API token and add it as the GitHub Actions secret
  `PYPI_API_TOKEN`.
- Keep the package version in `pyproject.toml` unique before each publish.

Manual TestPyPI rehearsal:

1. Open the `Publish Python package` GitHub Actions workflow.
2. Run it from `main` with repository `testpypi`.
3. Verify install in a temporary environment:

```bash
python -m venv .venv
. .venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  calle-ai==0.1.0b1
python -c 'from calle import CalleClient; print(CalleClient)'
```

Use repository `pypi` only after the TestPyPI package has been installed and
tested.
