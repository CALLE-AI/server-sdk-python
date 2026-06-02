from typing import Literal

APIErrorCode = Literal[
    "call_not_ready",
    "forbidden",
    "idempotency_conflict",
    "insufficient_balance",
    "internal_error",
    "invalid_request",
    "not_found",
    "policy_violation",
    "provider_unavailable",
    "rate_limit_exceeded",
    "recipient_blocked",
    "unauthorized",
    "unsupported_language",
    "unsupported_region",
]

API_ERROR_CODE_VALUES: set[APIErrorCode] = {
    "call_not_ready",
    "forbidden",
    "idempotency_conflict",
    "insufficient_balance",
    "internal_error",
    "invalid_request",
    "not_found",
    "policy_violation",
    "provider_unavailable",
    "rate_limit_exceeded",
    "recipient_blocked",
    "unauthorized",
    "unsupported_language",
    "unsupported_region",
}


def check_api_error_code(value: str) -> APIErrorCode:
    if value in API_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {API_ERROR_CODE_VALUES!r}")
