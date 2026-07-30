from typing import Literal

GoalRunObject = Literal["goal_run"]

GOAL_RUN_OBJECT_VALUES: set[GoalRunObject] = {
    "goal_run",
}


def check_goal_run_object(value: str) -> GoalRunObject:
    if value in GOAL_RUN_OBJECT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_RUN_OBJECT_VALUES!r}"
    )
