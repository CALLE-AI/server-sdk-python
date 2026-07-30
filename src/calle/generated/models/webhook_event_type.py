from typing import Literal

WebhookEventType = Literal[
    "call.completed", "call.failed", "call.result_validation_failed"
]

WEBHOOK_EVENT_TYPE_VALUES: set[WebhookEventType] = {
    "call.completed",
    "call.failed",
    "call.result_validation_failed",
}


def check_webhook_event_type(value: str) -> WebhookEventType:
    if value in WEBHOOK_EVENT_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {WEBHOOK_EVENT_TYPE_VALUES!r}"
    )
