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
pip install calle-ai==0.7.0
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

Run a published Goal with an explicit Goal, phone, variables, and durable
idempotency key:

```bash
export CALLE_GOAL_ID="<PUBLISHED_GOAL_ID>"
export CALLE_GOAL_PHONE="<AUTHORIZED_E164_PHONE>"
export CALLE_GOAL_VARIABLES='{"name":"Alex"}'
export CALLE_IDEMPOTENCY_KEY="<DURABLE_WORKFLOW_KEY>"
uv run python examples/run_goal_and_wait.py
```

To test against the test environment, explicitly set:

```bash
export CALLE_BASE_URL="https://test-api.heycall-e.com"
```

Run the webhook receiver example:

```bash
uv run python examples/webhook_server.py
```

The webhook receiver listens on `POST /calle/webhook` and processes terminal
event JSON. CALL-E sends terminal events only after the post-call outcome and
requested structured results are finalized.

CALL-E webhook delivery does not use a webhook secret, `CALL-E-Timestamp`, or
`CALL-E-Signature`. Use the required `CALL-E-Event-Id` header to deduplicate
at-least-once deliveries before performing side effects. The receiver example
parses JSON directly and checks that this header matches the body event id.

The `client.webhooks.verify` and `client.webhooks.unwrap` methods implement the
legacy signed-payload contract from SDK `0.2`. They remain available for source
compatibility but are deprecated and are not compatible with current unsigned
CALL-E deliveries.

## Quickstart

Run a reusable published Goal. The Goal owns its input and result schemas;
each Run supplies only a phone number, per-Run variables, and a durable
idempotency key:

```python
import os
from calle import CalleClient

client = CalleClient(api_key=os.environ["CALLE_API_KEY"])

goal = client.goals.get("goal_delivery_confirmation")
print(goal["title"], goal["published_run_spec"]["input_schema"])

run = client.goals.run_and_wait(
    goal_id=goal["id"],
    phone="+14155550100",
    variables={
        "customer_name": "Taylor",
        "order_reference": "ORD-8472",
        "delivery_window": "July 24, 2:00-4:00 PM",
    },
    idempotency_key="delivery:ORD-8472:confirm-window:v1",
)

if run["result"] is not None:
    print(run["call_id"])
    print(run["result"])
else:
    print(run["error"])
```

Persist the idempotency key before the first request and reuse it for network
retries. `wait_for_result` returns when either `result` or `error` is non-null;
an execution `status` of `completed` can still be waiting for result
materialization.

The generic one-shot call API remains available independently:

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
pip install calle-ai==0.7.0
python -c 'from calle import CalleClient; c = CalleClient(api_key="smoke"); assert callable(c.goals.run_and_wait); c.close()'
```

The current stable version is `0.7.0`. Do not reuse a previously published
PyPI version.

## Project Documents

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [SECURITY.md](./SECURITY.md)
- [RELEASE.md](./RELEASE.md)
