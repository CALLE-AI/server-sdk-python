from typing import Literal

BusinessResultStatus = Literal["available", "not_applicable", "pending", "unavailable"]

BUSINESS_RESULT_STATUS_VALUES: set[BusinessResultStatus] = {
    "available",
    "not_applicable",
    "pending",
    "unavailable",
}


def check_business_result_status(value: str) -> BusinessResultStatus:
    if value in BUSINESS_RESULT_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BUSINESS_RESULT_STATUS_VALUES!r}"
    )
