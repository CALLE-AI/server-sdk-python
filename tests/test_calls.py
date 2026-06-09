import json

import httpx
import pytest
import respx

from calle import CalleClient
from calle.errors import CalleAPIError, CalleTimeoutError


COMPLETED_CALL = {
    "id": "call_123",
    "status": "completed",
    "task": "Call.",
    "recipient": {"phone": "+14155550100", "region": "US", "locale": "en-US"},
    "structured_result": {"can_attend": "yes"},
    "result_validation": {"valid": True},
    "summary": "Done.",
    "transcript": None,
    "metadata": {"workflow_run_id": "wf_123"},
    "failure_code": None,
    "failure_message": None,
    "created_at": "2026-05-31T00:00:00Z",
    "completed_at": "2026-05-31T00:01:00Z",
}


@respx.mock
def test_create_call_uses_default_production_base_url() -> None:
    route = respx.post("https://api.heycall-e.com/v1/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test")

    client.calls.create(
        task="Call.",
        recipient={"phone": "+14155550100", "region": "US", "locale": "en-US"},
        result_schema={"type": "object", "properties": {}},
    )

    assert route.called


@respx.mock
def test_create_call_sends_auth_and_idempotency_headers() -> None:
    route = respx.post("https://api.heycall-e.com/v1/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.create(
        task="Call.",
        recipient={"phone": "+14155550100", "region": "US", "locale": "en-US"},
        result_schema={"type": "object", "properties": {}},
        webhook_url="https://example.com/webhook",
        idempotency_key="wf_123",
    )

    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer key_test"
    assert request.headers["idempotency-key"] == "wf_123"
    payload = json.loads(request.content)
    assert payload["result_schema"] == {"type": "object", "properties": {}}
    assert payload["webhook_url"] == "https://example.com/webhook"
    assert call["id"] == "call_123"
    assert call["structured_result"] == {"can_attend": "yes"}


@respx.mock
def test_create_call_maps_api_errors() -> None:
    respx.post("https://api.heycall-e.com/v1/calls").mock(
        return_value=httpx.Response(
            409,
            json={"error": {"code": "idempotency_conflict", "message": "Conflict.", "details": {"key": "wf_123"}}},
        )
    )
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    with pytest.raises(CalleAPIError) as exc_info:
        client.calls.create(
            task="Call.",
            recipient={"phone": "+14155550100", "region": "US", "locale": "en-US"},
            result_schema={"type": "object", "properties": {}},
        )

    assert exc_info.value.code == "idempotency_conflict"
    assert exc_info.value.status_code == 409
    assert exc_info.value.details == {"key": "wf_123"}


@respx.mock
def test_wait_for_result_returns_completed_call() -> None:
    queued = {**COMPLETED_CALL, "status": "queued", "structured_result": None, "completed_at": None}
    respx.get("https://api.heycall-e.com/v1/calls/call_123").mock(
        side_effect=[httpx.Response(200, json=queued), httpx.Response(200, json=COMPLETED_CALL)]
    )
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "completed"


@respx.mock
def test_wait_for_result_returns_failed_call() -> None:
    failed = {**COMPLETED_CALL, "status": "failed", "failure_code": "no_answer"}
    respx.get("https://api.heycall-e.com/v1/calls/call_123").mock(return_value=httpx.Response(200, json=failed))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "failed"
    assert call["failure_code"] == "no_answer"


@respx.mock
def test_wait_for_result_raises_timeout() -> None:
    queued = {**COMPLETED_CALL, "status": "queued", "structured_result": None, "completed_at": None}
    respx.get("https://api.heycall-e.com/v1/calls/call_123").mock(return_value=httpx.Response(200, json=queued))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    with pytest.raises(CalleTimeoutError):
        client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.002)
