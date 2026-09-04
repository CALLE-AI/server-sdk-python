# calle-ai

[![PyPI version](https://img.shields.io/pypi/v/calle-ai)](https://pypi.org/project/calle-ai/)
[![Python versions](https://img.shields.io/pypi/pyversions/calle-ai)](https://pypi.org/project/calle-ai/)
[![CI](https://github.com/CALLE-AI/server-sdk-python/actions/workflows/ci.yml/badge.svg)](https://github.com/CALLE-AI/server-sdk-python/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Python server SDK for the CALL-E Developer API.

Use this SDK from backend services, workers, and other trusted server
environments. Do not expose CALL-E API keys in browser code.

## Documentation

- Developer docs: <https://docs.heycall-e.com/>
- SDK guide: <https://docs.heycall-e.com/#/sdks>
- API Reference: <https://docs.heycall-e.com/#/api-reference>
- Webhooks: <https://docs.heycall-e.com/#/webhooks>
- Product changelog: <https://docs.heycall-e.com/#/changelog>
- TypeScript SDK: <https://github.com/CALLE-AI/server-sdk-typescript>

## SDK surface

- `client.calls` creates, reads, and polls call tasks and lists call events.
- `client.goals` lists and reads published Goals and runs them with structured
  results.
- `examples/webhook_server.py` shows how to receive current terminal webhook
  events.

## Install

Install the stable package from PyPI:

```bash
pip install calle-ai
```

For reproducible deployments, pin the package version selected by your
dependency-management workflow.

Use a local checkout for development and package smoke tests:

```bash
bash scripts/validate.sh
```

Python 3.11 or newer is required.

## Configuration

Create one `CalleClient` and close it when your process no longer needs it:

| Option | Required | Description |
| --- | --- | --- |
| `api_key` | Yes | CALL-E API key. Load it from a server-side secret store or environment variable. |
| `base_url` | No | API base URL. Defaults to `https://api.heycall-e.com`. |
| `timeout` | No | HTTP request timeout in seconds. Defaults to `30.0`. |
| `http_client` | No | Configured `httpx.Client` used as-is. It must define the required base URL, authentication, transport, and timeout. |

With the default HTTP client, use `CalleClient` as a context manager so the SDK
closes its connection pool:

```python
import os
from calle import CalleClient

with CalleClient(api_key=os.environ["CALLE_API_KEY"]) as client:
    call = client.calls.get("call_123")
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

To use an approved non-production environment, explicitly set:

```bash
export CALLE_BASE_URL="<APPROVED_TEST_API_BASE_URL>"
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
It defaults to a 10 MiB request-body limit and returns `413` for larger
payloads. Set `CALLE_WEBHOOK_MAX_BODY_BYTES` to match your ingress limits.

The bounded in-memory deduplication cache is only for local example use and
retains the latest 10,000 event ids. Production deployments must use a
production server or ingress with read deadlines and durable deduplication
storage with an explicit retention policy.

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

## Error handling

The SDK exports errors for API responses, authentication, rate limits,
timeouts, and connection failures:

```python
import os
from calle import CalleAPIError, CalleClient

with CalleClient(api_key=os.environ["CALLE_API_KEY"]) as client:
    try:
        client.calls.get("call_123")
    except CalleAPIError as error:
        print(error.status_code, error.code, error.details)
        raise
```

## Release

This repository publishes the Python distribution `calle-ai`. Application code
imports it as `calle`.

Merging to `main` runs CI and does not publish the package. A stable publish is
triggered only by publishing a GitHub Release with a matching `vX.Y.Z` tag;
manually running the workflow performs a dry run. See [RELEASE.md](./RELEASE.md)
for release gates and registry checks.

## Support and security

Use [GitHub Issues](https://github.com/CALLE-AI/server-sdk-python/issues) for
reproducible SDK bugs and feature requests. Do not report vulnerabilities in a
public issue. Follow [SECURITY.md](./SECURITY.md) for private reporting.

## License

This project is licensed under the [MIT License](./LICENSE). The same license
applies to the published PyPI distributions `calle-ai==0.6.0` and
`calle-ai==0.7.0`.

## Project Documents

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [SECURITY.md](./SECURITY.md)
- [RELEASE.md](./RELEASE.md)
