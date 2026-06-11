from typing import Literal

AttemptStatus = Literal["canceled", "completed", "dialing", "failed", "in_progress", "queued"]

ATTEMPT_STATUS_VALUES: set[AttemptStatus] = {
    "canceled",
    "completed",
    "dialing",
    "failed",
    "in_progress",
    "queued",
}


def check_attempt_status(value: str) -> AttemptStatus:
    if value in ATTEMPT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ATTEMPT_STATUS_VALUES!r}")
