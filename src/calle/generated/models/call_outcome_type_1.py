from typing import Literal

CallOutcomeType1 = Literal["busy", "completed", "declined", "no_answer"]

CALL_OUTCOME_TYPE_1_VALUES: set[CallOutcomeType1] = {
    "busy",
    "completed",
    "declined",
    "no_answer",
}


def check_call_outcome_type_1(value: str) -> CallOutcomeType1:
    if value in CALL_OUTCOME_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CALL_OUTCOME_TYPE_1_VALUES!r}"
    )
