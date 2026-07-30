from typing import Literal

GoalListObject = Literal["list"]

GOAL_LIST_OBJECT_VALUES: set[GoalListObject] = {
    "list",
}


def check_goal_list_object(value: str) -> GoalListObject:
    if value in GOAL_LIST_OBJECT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOAL_LIST_OBJECT_VALUES!r}"
    )
