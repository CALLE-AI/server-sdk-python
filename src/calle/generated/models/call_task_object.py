from typing import Literal

CallTaskObject = Literal["call_task"]

CALL_TASK_OBJECT_VALUES: set[CallTaskObject] = {
    "call_task",
}


def check_call_task_object(value: str) -> CallTaskObject:
    if value in CALL_TASK_OBJECT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CALL_TASK_OBJECT_VALUES!r}"
    )
