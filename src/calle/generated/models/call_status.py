from typing import Literal

CallStatus = Literal["canceled", "completed", "failed", "in_progress", "queued"]

CALL_STATUS_VALUES: set[CallStatus] = {
    "canceled",
    "completed",
    "failed",
    "in_progress",
    "queued",
}


def check_call_status(value: str) -> CallStatus:
    if value in CALL_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CALL_STATUS_VALUES!r}"
    )
