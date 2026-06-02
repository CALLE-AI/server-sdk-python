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
