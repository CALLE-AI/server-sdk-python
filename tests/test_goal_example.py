import runpy
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import pytest


example = runpy.run_path(
    str(Path(__file__).parent.parent / "examples" / "run_goal_and_wait.py")
)
goal_variables = cast(
    Callable[[], dict[str, str | int | float | bool]],
    example["goal_variables"],
)
exit_on_goal_error = cast(
    Callable[[dict[str, Any]], None],
    example["exit_on_goal_error"],
)

@pytest.mark.parametrize("variables", ['{"score":NaN}', '{"score":Infinity}', '{"score":1e999}'])
def test_goal_example_rejects_non_finite_variables(
    monkeypatch: pytest.MonkeyPatch,
    variables: str,
) -> None:
    monkeypatch.setenv("CALLE_GOAL_VARIABLES", variables)

    with pytest.raises(RuntimeError):
        goal_variables()


def test_goal_example_exits_nonzero_for_domain_error() -> None:
    with pytest.raises(SystemExit) as exc_info:
        exit_on_goal_error(
            {
                "error": {
                    "code": "no_answer",
                    "message": "No human answered.",
                    "detail_code": None,
                }
            }
        )

    assert exc_info.value.code == 1


def test_goal_example_accepts_success() -> None:
    exit_on_goal_error({"error": None})
