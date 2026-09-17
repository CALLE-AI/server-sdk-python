import json

import httpx
import pytest
import respx

from calle import CalleClient
from calle.errors import CalleAPIError, CalleTimeoutError


COMPLETED_CALL = {
    "id": "call_123",
    "object": "call",
    "status": "completed",
    "task": "Call.",
    "phone": "+14155550100", "region": "US", "locale": "en-US", "scheduled_at": None,
    "result": {"completed_count": 1}, "error": None,
    "metadata": {"workflow_run_id": "wf_123"},
    "created_at": "2026-05-31T00:00:00Z",
    "completed_at": "2026-05-31T00:01:00Z",
}


@respx.mock
def test_create_call_uses_default_production_base_url() -> None:
    route = respx.post("https://api.heycall-e.com/v2/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test")

    client.calls.create(
        task="Call.",
        phone="+14155550100", region="US", locale="en-US", idempotency_key="wf_123",
        result_schema={"type": "object", "additionalProperties": False, "properties": {}},
    )

    assert route.called


@respx.mock
def test_create_call_sends_auth_and_idempotency_headers() -> None:
    route = respx.post("https://api.heycall-e.com/v2/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.create(
        task="Call.",
        phone="+14155550100", region="US", locale="en-US", idempotency_key="wf_123",
        result_schema={"type": "object", "additionalProperties": False, "properties": {}},
        webhook_url="https://example.com/webhook",
    )

    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer key_test"
    assert request.headers["idempotency-key"] == "wf_123"
    payload = json.loads(request.content)
    assert payload["phone"] == "+14155550100"
    assert "recipients" not in payload
    assert payload["result_schema"] == {"type": "object", "additionalProperties": False, "properties": {}}
    assert payload["webhook_url"] == "https://example.com/webhook"
    assert call["id"] == "call_123"
    assert call["result"] == {"completed_count": 1}
    assert call["error"] is None
    assert "structured_result" not in call


@respx.mock
def test_create_requires_a_stable_idempotency_key() -> None:
    with CalleClient(api_key="test") as client:
        with pytest.raises(ValueError, match="idempotency_key"):
            client.calls.create(task="Call.", phone="+14155550100", region="US", locale="en-US", idempotency_key=" ", result_schema={"type": "object", "additionalProperties": False, "properties": {}})


@respx.mock
def test_cancel_returns_the_persisted_result_error() -> None:
    canceled = {**COMPLETED_CALL, "status": "canceled", "result": None,
                "error": {"code": "canceled", "message": "Canceled.", "detail_code": None}}
    route = respx.post("https://api.heycall-e.com/v2/calls/call_123/cancel").mock(return_value=httpx.Response(200, json=canceled))
    with CalleClient(api_key="test") as client:
        assert client.calls.cancel("call_123") == canceled
    assert route.called


@respx.mock
def test_create_call_maps_api_errors() -> None:
    respx.post("https://api.heycall-e.com/v2/calls").mock(
        return_value=httpx.Response(
            409,
            json={"error": {"code": "idempotency_conflict", "message": "Conflict.", "details": {"key": "wf_123"}}},
        )
    )
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    with pytest.raises(CalleAPIError) as exc_info:
        client.calls.create(
            task="Call.",
            phone="+14155550100", region="US", locale="en-US", idempotency_key="wf_123",
            result_schema={"type": "object", "additionalProperties": False, "properties": {}},
        )

    assert exc_info.value.code == "idempotency_conflict"
    assert exc_info.value.status_code == 409
    assert exc_info.value.details == {"key": "wf_123"}


@respx.mock
def test_wait_for_result_returns_completed_call() -> None:
    queued = {**COMPLETED_CALL, "status": "queued", "result": None, "completed_at": None}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(
        side_effect=[httpx.Response(200, json=queued), httpx.Response(200, json={**COMPLETED_CALL, "result": None}), httpx.Response(200, json=COMPLETED_CALL)]
    )
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "completed"


@respx.mock
def test_wait_for_result_returns_failed_call() -> None:
    failed = {**COMPLETED_CALL, "status": "failed", "result": None, "error": {"code": "no_answer", "message": "No answer.", "detail_code": None}}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json=failed))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "failed"
    assert call["error"]["code"] == "no_answer"


@respx.mock
def test_wait_for_result_raises_timeout() -> None:
    queued = {**COMPLETED_CALL, "status": "queued", "result": None, "completed_at": None}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json=queued))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    with pytest.raises(CalleTimeoutError):
        client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.002)


def test_generated_call_round_trips_goal_compatible_result() -> None:
    from calle.generated.models.agentic_call import AgenticCall
    generated = AgenticCall.from_dict(COMPLETED_CALL)
    assert generated.result.to_dict() == {"completed_count": 1}
    assert generated.error is None
    assert generated.to_dict()["result"] == COMPLETED_CALL["result"]


@respx.mock
def test_wait_accepts_empty_result() -> None:
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json={**COMPLETED_CALL, "result": {}}))
    with CalleClient(api_key="test") as client:
        assert client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)["result"] == {}
