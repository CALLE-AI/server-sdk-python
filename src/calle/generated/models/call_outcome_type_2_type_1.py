from typing import Literal

CallOutcomeType2Type1 = Literal["busy", "completed", "declined", "no_answer"]

CALL_OUTCOME_TYPE_2_TYPE_1_VALUES: set[CallOutcomeType2Type1] = {
    "busy",
    "completed",
    "declined",
    "no_answer",
}


def check_call_outcome_type_2_type_1(value: str) -> CallOutcomeType2Type1:
    if value in CALL_OUTCOME_TYPE_2_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CALL_OUTCOME_TYPE_2_TYPE_1_VALUES!r}"
    )
