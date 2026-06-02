from typing import Literal

CallPolicyOnNotReady = Literal["error"]

CALL_POLICY_ON_NOT_READY_VALUES: set[CallPolicyOnNotReady] = {
    "error",
}


def check_call_policy_on_not_ready(value: str) -> CallPolicyOnNotReady:
    if value in CALL_POLICY_ON_NOT_READY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_POLICY_ON_NOT_READY_VALUES!r}")
