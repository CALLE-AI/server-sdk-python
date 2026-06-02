from typing import Literal

WebhookCallDataObject = Literal["call"]

WEBHOOK_CALL_DATA_OBJECT_VALUES: set[WebhookCallDataObject] = {
    "call",
}


def check_webhook_call_data_object(value: str) -> WebhookCallDataObject:
    if value in WEBHOOK_CALL_DATA_OBJECT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WEBHOOK_CALL_DATA_OBJECT_VALUES!r}")
