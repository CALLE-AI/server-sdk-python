from typing import Literal

GoalStatus = Literal["active"]

GOAL_STATUS_VALUES: set[GoalStatus] = {
    "active",
}


def check_goal_status(value: str) -> GoalStatus:
    if value in GOAL_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_STATUS_VALUES!r}"
    )
