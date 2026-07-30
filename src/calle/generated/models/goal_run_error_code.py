from typing import Literal

GoalRunErrorCode = Literal[
    "call_failed",
    "canceled",
    "declined",
    "no_answer",
    "result_failed",
    "result_invalid",
    "result_unavailable",
    "timed_out",
]

GOAL_RUN_ERROR_CODE_VALUES: set[GoalRunErrorCode] = {
    "call_failed",
    "canceled",
    "declined",
    "no_answer",
    "result_failed",
    "result_invalid",
    "result_unavailable",
    "timed_out",
}


def check_goal_run_error_code(value: str) -> GoalRunErrorCode:
    if value in GOAL_RUN_ERROR_CODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_RUN_ERROR_CODE_VALUES!r}"
    )
