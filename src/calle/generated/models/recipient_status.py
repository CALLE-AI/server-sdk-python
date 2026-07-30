from typing import Literal

RecipientStatus = Literal["completed", "failed", "in_progress", "pending", "skipped"]

RECIPIENT_STATUS_VALUES: set[RecipientStatus] = {
    "completed",
    "failed",
    "in_progress",
    "pending",
    "skipped",
}


def check_recipient_status(value: str) -> RecipientStatus:
    if value in RECIPIENT_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {RECIPIENT_STATUS_VALUES!r}"
    )
