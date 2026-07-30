from typing import Literal

GoalRunStatus = Literal["canceled", "completed", "failed", "in_progress", "queued"]

GOAL_RUN_STATUS_VALUES: set[GoalRunStatus] = {
    "canceled",
    "completed",
    "failed",
    "in_progress",
    "queued",
}


def check_goal_run_status(value: str) -> GoalRunStatus:
    if value in GOAL_RUN_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_RUN_STATUS_VALUES!r}"
    )
