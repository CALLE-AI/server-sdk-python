from typing import Literal

AgenticWebhookEventType = Literal["call.canceled", "call.completed", "call.failed"]

AGENTIC_WEBHOOK_EVENT_TYPE_VALUES: set[AgenticWebhookEventType] = {
    "call.canceled",
    "call.completed",
    "call.failed",
}


def check_agentic_webhook_event_type(value: str) -> AgenticWebhookEventType:
    if value in AGENTIC_WEBHOOK_EVENT_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENTIC_WEBHOOK_EVENT_TYPE_VALUES!r}"
    )
