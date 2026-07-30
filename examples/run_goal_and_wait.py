import json
import math
import os
from typing import Any, NoReturn

from calle import CalleClient


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Set {name} before running this example.")
    return value


def reject_non_finite_constant(value: str) -> NoReturn:
    raise ValueError(f"{value} is not valid JSON.")


def goal_variables() -> dict[str, str | int | float | bool]:
    raw_variables = os.environ.get("CALLE_GOAL_VARIABLES", "{}")
    try:
        parsed: Any = json.loads(
            raw_variables,
            parse_constant=reject_non_finite_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("CALLE_GOAL_VARIABLES must be valid finite JSON.") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("CALLE_GOAL_VARIABLES must be a JSON object.")
    if not all(
        isinstance(key, str)
        and isinstance(value, (str, int, float, bool))
        and (not isinstance(value, float) or math.isfinite(value))
        for key, value in parsed.items()
    ):
        raise RuntimeError("CALLE_GOAL_VARIABLES values must be finite JSON scalars.")
    return parsed


def exit_on_goal_error(run: dict[str, Any]) -> None:
    if run["error"] is not None:
        raise SystemExit(1)


def main() -> None:
    goal_id = required_env("CALLE_GOAL_ID")
    with CalleClient(
        api_key=required_env("CALLE_API_KEY"),
        base_url=os.environ.get("CALLE_BASE_URL", "https://api.heycall-e.com"),
    ) as client:
        goal = client.goals.get(goal_id)
        print(json.dumps(goal, indent=2, ensure_ascii=False))

        run = client.goals.run_and_wait(
            goal_id=goal_id,
            phone=required_env("CALLE_GOAL_PHONE"),
            variables=goal_variables(),
            idempotency_key=required_env("CALLE_IDEMPOTENCY_KEY"),
            interval_seconds=float(os.environ.get("CALLE_POLL_INTERVAL_SECONDS", "2")),
            timeout_seconds=float(os.environ.get("CALLE_POLL_TIMEOUT_SECONDS", "600")),
        )

    print(json.dumps(run, indent=2, ensure_ascii=False))
    exit_on_goal_error(run)


if __name__ == "__main__":
    main()
