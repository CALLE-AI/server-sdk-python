from typing import Literal

APIErrorCode = Literal[
    "account_concurrency_exceeded",
    "account_concurrency_unavailable",
    "call_not_ready",
    "forbidden",
    "goal_not_executable",
    "goal_not_published",
    "goal_not_ready",
    "idempotency_conflict",
    "insufficient_balance",
    "internal_error",
    "invalid_phone",
    "invalid_recipient",
    "invalid_request",
    "llm_token_budget_exceeded",
    "llm_token_budget_unavailable",
    "no_recipients",
    "not_found",
    "policy_violation",
    "provider_unavailable",
    "rate_limit_exceeded",
    "recipient_blocked",
    "recipient_result_schema_invalid",
    "result_schema_invalid",
    "schema_override_not_allowed",
    "unauthorized",
    "unsupported_language",
    "unsupported_region",
    "variables_invalid",
]

API_ERROR_CODE_VALUES: set[APIErrorCode] = {
    "account_concurrency_exceeded",
    "account_concurrency_unavailable",
    "call_not_ready",
    "forbidden",
    "goal_not_executable",
    "goal_not_published",
    "goal_not_ready",
    "idempotency_conflict",
    "insufficient_balance",
    "internal_error",
    "invalid_phone",
    "invalid_recipient",
    "invalid_request",
    "llm_token_budget_exceeded",
    "llm_token_budget_unavailable",
    "no_recipients",
    "not_found",
    "policy_violation",
    "provider_unavailable",
    "rate_limit_exceeded",
    "recipient_blocked",
    "recipient_result_schema_invalid",
    "result_schema_invalid",
    "schema_override_not_allowed",
    "unauthorized",
    "unsupported_language",
    "unsupported_region",
    "variables_invalid",
}


def check_api_error_code(value: str) -> APIErrorCode:
    if value in API_ERROR_CODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {API_ERROR_CODE_VALUES!r}"
    )
