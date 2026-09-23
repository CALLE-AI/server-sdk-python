# calle-ai

> This branch prepares **SDK 1.0.0 (unreleased)** for the Agentic `/v2/calls` API.
> The published 0.7.0 SDK still uses `/v1/calls`. Use the local build for the
> examples below; backend rollout and scheduled authorization are not complete.

Python server SDK for the CALL-E Developer API.

Use this SDK from backend services, workers, and other trusted server
environments. Do not expose CALL-E API keys in browser code.

One-shot v2 uses the same `result` / `error` contract as Goal Runs. A required
closed scalar-object result schema defines the business fields. SDK wait helpers
continue while `result_status` is `pending`, even after execution reaches `completed`.
Empty `{}` is a ready result. Webhook data matches the persisted GET snapshot.

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
retries. `wait_for_result` returns when `result_status` is no longer `pending`;
an execution `status` of `completed` can still be waiting for result
materialization.

## One-shot migration in 1.0 (unreleased)

The `calls` wrapper now submits one explicit phone to `/v2/calls` and requires
an idempotency key. Keep the key for retries. The backend continues serving
existing v1 integrations; use SDK 0.7.x for historical v1 call ids.

```python
call = client.calls.create_and_wait(
    task="Ask whether Friday lunch is confirmed.",
    phone="<AUTHORIZED_E164_PHONE>", region="US", locale="en-US",
    result_schema={
        "type": "object", "additionalProperties": False, "required": ["answer"],
        "properties": {"answer": {"type": "string", "enum": ["yes", "no", "unknown"]}},
    },
    idempotency_key="lunch:friday:confirmation:v1",
)
if call["error"] is None:
    print(call["result"])
else:
    print(call["error"])
# Cancel a queued call before provider submission:
# client.calls.cancel(call_id)
```

Replace `recipient` / `recipients` with `phone`, `region`, and `locale`.
Define the required `result_schema` (`resultSchema` in TypeScript) using Goal's
`calle.result.scalar-object.v1` profile: at most 32 scalar properties and
`additionalProperties: false`. Flatten old nested fields; arrays and null values
are unsupported. Old `structured_result`, `result_error`, summary,
confidence and provider attempt fields are removed. Request business summaries or
completion flags explicitly as scalar fields in the schema when needed.
Batch and recurring workflows belong to reusable Goals.

Calls and Goal Runs always expose `transcript`, an array of recorded turns with
`speaker` (`bot`, `user`, `unknown`), nullable `offset_seconds`, and `text`.
Before execution ends or without available transcript, the array is empty.
A pending, unavailable or failed business result does not remove an available
terminal transcript. Webhook data uses the same shape.

The returned object is `call`. Consume `result` and `error` exactly as for Goal Runs.
Poll while result_status is pending (resultStatus in TypeScript). No-answer, busy
and declined are ordinary call_outcome values (callOutcome in TypeScript).
Unavailable business evidence uses result_status=unavailable and error=null.
Explicit schema-valid task fallbacks remain results. Technical failures use error.
Cancellation uses result_status=not_applicable and no error. GET reads committed state and
terminal webhooks contain the same ready snapshot. Deduplicate by event id.

Cancellation returns `409 call_cannot_cancel` after provider submission begins.
Calls accept immediate execution only. If authorization expires after submission,
`error.detail_code=authorization_expired` means the provider may still complete the call; do not
create an automatic replacement call.

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
