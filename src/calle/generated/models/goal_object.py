from typing import Literal

GoalObject = Literal["goal"]

GOAL_OBJECT_VALUES: set[GoalObject] = {
    "goal",
}


def check_goal_object(value: str) -> GoalObject:
    if value in GOAL_OBJECT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_OBJECT_VALUES!r}"
    )
