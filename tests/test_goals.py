import json

import httpx
import pytest
import respx

import calle.goals as goals_module
from calle import CalleClient
from calle.errors import CalleAPIError, CalleTimeoutError
from calle.generated.models import Goal, GoalRun


PUBLISHED_GOAL = {
    "object": "goal",
    "id": "goal_delivery",
    "title": "Delivery window confirmation",
    "description": "Confirm a delivery window or collect a preferred alternative.",
    "status": "active",
    "published_run_spec": {
        "id": "rspec_delivery_v4",
        "version": 4,
        "input_schema": {
            "type": "object",
            "required": ["order_reference"],
            "properties": {"order_reference": {"type": "string"}},
        },
        "result_schema": {
            "type": "object",
            "required": ["delivery_outcome"],
            "properties": {"delivery_outcome": {"type": "string"}},
        },
    },
}

QUEUED_RUN = {
    "object": "goal_run",
    "id": "rgrp_delivery_8472",
    "goal_id": "goal_delivery",
    "run_id": "run_delivery_8472",
    "call_id": None,
    "run_spec": {"id": "rspec_delivery_v4", "version": 4},
    "status": "queued",
    "result": None,
    "error": None,
    "created_at": "2026-07-22T10:00:00Z",
    "completed_at": None,
}


def test_generated_goal_models_parse_public_api_examples() -> None:
    goal = Goal.from_dict(PUBLISHED_GOAL)
    run = GoalRun.from_dict(QUEUED_RUN)

    assert goal.id == "goal_delivery"
    assert goal.published_run_spec.version == 4
    assert run.id == "rgrp_delivery_8472"
    assert run.call_id is None
    assert run.run_spec.id == "rspec_delivery_v4"


@respx.mock
def test_list_goals_uses_default_production_url_and_pagination() -> None:
    route = respx.get("https://api.heycall-e.com/v1/goals").mock(
        return_value=httpx.Response(
            200,
            json={"object": "list", "data": [PUBLISHED_GOAL], "next_cursor": "goalcur_later"},
        )
    )
    client = CalleClient(api_key="key_test")

    goals = client.goals.list(limit=10, after="goalcur_next")

    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer key_test"
    assert dict(request.url.params) == {"limit": "10", "after": "goalcur_next"}
    assert goals["next_cursor"] == "goalcur_later"
    assert goals["data"][0]["title"] == "Delivery window confirmation"
    assert goals["data"][0]["published_run_spec"]["input_schema"] == PUBLISHED_GOAL["published_run_spec"][
        "input_schema"
    ]


@respx.mock
def test_get_goal_returns_published_interface() -> None:
    route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery").mock(
        return_value=httpx.Response(200, json=PUBLISHED_GOAL)
    )
    client = CalleClient(api_key="key_test")

    goal = client.goals.get("goal_delivery")

    assert route.called
    assert goal["published_run_spec"]["result_schema"] == PUBLISHED_GOAL["published_run_spec"]["result_schema"]


@respx.mock
def test_goal_paths_percent_encode_opaque_ids() -> None:
    get_goal_route = respx.get("https://api.heycall-e.com/v1/goals/goal%2Fdelivery").mock(
        return_value=httpx.Response(200, json=PUBLISHED_GOAL)
    )
    create_run_route = respx.post("https://api.heycall-e.com/v1/goals/goal%2Fdelivery/runs").mock(
        return_value=httpx.Response(201, json=QUEUED_RUN)
    )
    get_run_route = respx.get(
        "https://api.heycall-e.com/v1/goals/goal%2Fdelivery/runs/rgrp%2F8472%3Fview%3D1"
    ).mock(return_value=httpx.Response(200, json=QUEUED_RUN))
    client = CalleClient(api_key="key_test")

    client.goals.get("goal/delivery")
    client.goals.run(
        goal_id="goal/delivery",
        phone="+14155550100",
        idempotency_key="delivery:ORD-8472:v1",
    )
    client.goals.get_run("goal/delivery", "rgrp/8472?view=1")

    assert get_goal_route.called
    assert create_run_route.called
    assert get_run_route.called


@respx.mock
def test_run_goal_sends_only_phone_variables_and_idempotency_identity() -> None:
    route = respx.post("https://api.heycall-e.com/v1/goals/goal_delivery/runs").mock(
        return_value=httpx.Response(201, json=QUEUED_RUN)
    )
    client = CalleClient(api_key="key_test")

    run = client.goals.run(
        goal_id="goal_delivery",
        phone="+14155550100",
        variables={"order_reference": "ORD-8472"},
        idempotency_key="delivery:ORD-8472:v1",
    )

    request = route.calls.last.request
    assert request.headers["idempotency-key"] == "delivery:ORD-8472:v1"
    assert json.loads(request.content) == {
        "phone": "+14155550100",
        "variables": {"order_reference": "ORD-8472"},
    }
    assert run["id"] == "rgrp_delivery_8472"
    assert run["run_spec"] == {"id": "rspec_delivery_v4", "version": 4}


@respx.mock
def test_wait_for_result_ignores_completed_status_until_result_exists() -> None:
    materializing = {
        **QUEUED_RUN,
        "status": "completed",
        "completed_at": "2026-07-22T10:01:00Z",
    }
    succeeded = {
        **materializing,
        "call_id": "calling_call_delivery_8472",
        "result": {"delivery_outcome": "confirmed"},
    }
    route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        side_effect=[
            httpx.Response(200, json=materializing),
            httpx.Response(200, json=succeeded),
        ]
    )
    client = CalleClient(api_key="key_test")

    run = client.goals.wait_for_result(
        "goal_delivery",
        "rgrp_delivery_8472",
        interval_seconds=0.001,
        timeout_seconds=0.5,
    )

    assert run["result"] == {"delivery_outcome": "confirmed"}
    assert run["call_id"] == "calling_call_delivery_8472"
    assert route.call_count == 2


@respx.mock
def test_wait_for_result_returns_domain_error_as_data() -> None:
    failed = {
        **QUEUED_RUN,
        "status": "failed",
        "error": {
            "code": "no_answer",
            "message": "No human answered the call.",
            "detail_code": "provider_no_answer",
        },
        "completed_at": "2026-07-22T10:01:00Z",
    }
    respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        return_value=httpx.Response(200, json=failed)
    )
    client = CalleClient(api_key="key_test")

    run = client.goals.wait_for_result(
        "goal_delivery",
        "rgrp_delivery_8472",
        interval_seconds=0.001,
        timeout_seconds=0.5,
    )

    assert run["error"] == {
        "code": "no_answer",
        "message": "No human answered the call.",
        "detail_code": "provider_no_answer",
    }


@respx.mock
def test_run_and_wait_polls_returned_goal_run_identity() -> None:
    create_route = respx.post("https://api.heycall-e.com/v1/goals/goal_delivery/runs").mock(
        return_value=httpx.Response(201, json=QUEUED_RUN)
    )
    poll_route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        return_value=httpx.Response(
            200,
            json={
                **QUEUED_RUN,
                "status": "completed",
                "result": {"delivery_outcome": "confirmed"},
                "completed_at": "2026-07-22T10:01:00Z",
            },
        )
    )
    client = CalleClient(api_key="key_test")

    run = client.goals.run_and_wait(
        goal_id="goal_delivery",
        phone="+14155550100",
        idempotency_key="delivery:ORD-8472:v1",
        interval_seconds=0.001,
        timeout_seconds=0.5,
    )

    assert create_route.called
    assert poll_route.called
    assert run["result"] == {"delivery_outcome": "confirmed"}


@respx.mock
def test_run_and_wait_returns_terminal_idempotent_replay_without_polling() -> None:
    succeeded = {
        **QUEUED_RUN,
        "status": "completed",
        "result": {"delivery_outcome": "confirmed"},
        "completed_at": "2026-07-22T10:01:00Z",
    }
    create_route = respx.post("https://api.heycall-e.com/v1/goals/goal_delivery/runs").mock(
        return_value=httpx.Response(201, json=succeeded)
    )
    client = CalleClient(api_key="key_test")

    run = client.goals.run_and_wait(
        goal_id="goal_delivery",
        phone="+14155550100",
        idempotency_key="delivery:ORD-8472:v1",
    )

    assert create_route.call_count == 1
    assert run["result"] == {"delivery_outcome": "confirmed"}


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("interval_seconds", float("nan")),
        ("timeout_seconds", 0.0),
    ],
)
@respx.mock
def test_run_and_wait_rejects_invalid_polling_seconds_before_create(
    parameter: str,
    value: float,
) -> None:
    route = respx.post("https://api.heycall-e.com/v1/goals/goal_delivery/runs").mock(
        return_value=httpx.Response(201, json=QUEUED_RUN)
    )
    client = CalleClient(api_key="key_test")
    options = {"interval_seconds": 1.0, "timeout_seconds": 1.0}
    options[parameter] = value

    with pytest.raises(ValueError, match=f"{parameter} must be a finite positive number"):
        client.goals.run_and_wait(
            goal_id="goal_delivery",
            phone="+14155550100",
            idempotency_key="delivery:ORD-8472:v1",
            **options,
        )

    assert route.call_count == 0


@respx.mock
def test_run_goal_maps_api_error() -> None:
    respx.post("https://api.heycall-e.com/v1/goals/goal_delivery/runs").mock(
        return_value=httpx.Response(
            409,
            json={
                "error": {
                    "code": "idempotency_conflict",
                    "message": "The key was already used with different input.",
                    "details": {"key": "delivery:ORD-8472:v1"},
                }
            },
        )
    )
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleAPIError) as exc_info:
        client.goals.run(
            goal_id="goal_delivery",
            phone="+14155550100",
            idempotency_key="delivery:ORD-8472:v1",
        )

    assert exc_info.value.code == "idempotency_conflict"
    assert exc_info.value.status_code == 409


@respx.mock
def test_wait_for_result_raises_timeout_while_result_and_error_are_null() -> None:
    respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        return_value=httpx.Response(200, json=QUEUED_RUN)
    )
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleTimeoutError):
        client.goals.wait_for_result(
            "goal_delivery",
            "rgrp_delivery_8472",
            interval_seconds=0.001,
            timeout_seconds=0.002,
        )


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("interval_seconds", 0.0),
        ("interval_seconds", -1.0),
        ("interval_seconds", float("nan")),
        ("interval_seconds", float("inf")),
        ("timeout_seconds", 0.0),
        ("timeout_seconds", -1.0),
        ("timeout_seconds", float("nan")),
        ("timeout_seconds", float("inf")),
    ],
)
@respx.mock
def test_wait_for_result_rejects_invalid_polling_seconds_without_request(
    parameter: str,
    value: float,
) -> None:
    route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        return_value=httpx.Response(200, json=QUEUED_RUN)
    )
    client = CalleClient(api_key="key_test")
    options = {"interval_seconds": 1.0, "timeout_seconds": 1.0}
    options[parameter] = value

    with pytest.raises(ValueError, match=f"{parameter} must be a finite positive number"):
        client.goals.wait_for_result(
            "goal_delivery",
            "rgrp_delivery_8472",
            **options,
        )

    assert route.call_count == 0


@respx.mock
def test_wait_for_result_limits_poll_request_to_remaining_timeout() -> None:
    route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        side_effect=httpx.ReadTimeout("poll request timed out")
    )
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleTimeoutError) as exc_info:
        client.goals.wait_for_result(
            "goal_delivery",
            "rgrp_delivery_8472",
            interval_seconds=1.0,
            timeout_seconds=0.25,
        )

    request_timeout = route.calls.last.request.extensions["timeout"]
    assert all(0 < value <= 0.25 for value in request_timeout.values())
    assert isinstance(exc_info.value.__cause__, httpx.ReadTimeout)


@respx.mock
def test_wait_for_result_does_not_sleep_past_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    route = respx.get("https://api.heycall-e.com/v1/goals/goal_delivery/runs/rgrp_delivery_8472").mock(
        return_value=httpx.Response(200, json=QUEUED_RUN)
    )
    clock = [100.0]
    sleeps: list[float] = []

    monkeypatch.setattr(goals_module.time, "monotonic", lambda: clock[0])

    def advance_clock(seconds: float) -> None:
        sleeps.append(seconds)
        clock[0] += seconds

    monkeypatch.setattr(goals_module.time, "sleep", advance_clock)
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleTimeoutError):
        client.goals.wait_for_result(
            "goal_delivery",
            "rgrp_delivery_8472",
            interval_seconds=10.0,
            timeout_seconds=1.0,
        )

    assert sleeps == [1.0]
    assert route.call_count == 1
