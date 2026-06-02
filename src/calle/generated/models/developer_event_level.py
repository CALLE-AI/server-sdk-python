from typing import Literal

DeveloperEventLevel = Literal["debug", "error", "info", "warning"]

DEVELOPER_EVENT_LEVEL_VALUES: set[DeveloperEventLevel] = {
    "debug",
    "error",
    "info",
    "warning",
}


def check_developer_event_level(value: str) -> DeveloperEventLevel:
    if value in DEVELOPER_EVENT_LEVEL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEVELOPER_EVENT_LEVEL_VALUES!r}")
