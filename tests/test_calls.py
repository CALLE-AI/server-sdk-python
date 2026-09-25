import json

import httpx
import pytest
import respx

from calle import CalleClient
from calle.errors import CalleAPIError, CalleTimeoutError


COMPLETED_CALL = {
    "id": "call_123",
    "call_id": "billing-call-123",
    "object": "call",
    "status": "completed",
    "call_outcome": "completed", "result_status": "available",
    "transcript": [],
    "task": "Call.",
    "phone": "+14155550100", "region": "US", "locale": "en-US",
    "result": {"completed_count": 1}, "error": None,
    "metadata": {"workflow_run_id": "wf_123"},
    "created_at": "2026-05-31T00:00:00Z",
    "completed_at": "2026-05-31T00:01:00Z",
}

RESULT_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {}}


@respx.mock
@pytest.mark.parametrize("call_id", [None, "billing-call-123"])
def test_billing_call_id_is_separate_from_api_id(call_id: str | None) -> None:
    from calle.generated.models import AgenticCall

    body = {**COMPLETED_CALL, "call_id": call_id}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json=body))
    with CalleClient(api_key="test") as client:
        call = client.calls.get("call_123")
    assert call["id"] == "call_123"
    assert call["call_id"] == call_id
    generated = AgenticCall.from_dict(call)
    assert generated.call_id == call_id
    assert generated.to_dict()["call_id"] == call_id


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
def test_create_omits_target_hints_and_returns_resolved_values() -> None:
    route = respx.post("https://api.heycall-e.com/v2/calls").mock(return_value=httpx.Response(202, json=COMPLETED_CALL))
    with CalleClient(api_key="test") as client:
        call = client.calls.create(task="Ask in English.", phone="+14155550100", idempotency_key="infer-target",
                                  result_schema={"type": "object", "properties": {}, "additionalProperties": False})
    body = json.loads(route.calls.last.request.content)
    assert "region" not in body and "locale" not in body
    assert (call["region"], call["locale"]) == ("US", "en-US")


@respx.mock
def test_transcript_survives_unavailable_business_result() -> None:
    from calle.generated.models import AgenticCall

    turns = [{"speaker": "bot", "offset_seconds": 0, "text": "Hello."},
             {"speaker": "unknown", "offset_seconds": None, "text": "Unattributed words."}]
    body = {**COMPLETED_CALL, "result_status": "unavailable", "result": None, "transcript": turns}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json=body))
    with CalleClient(api_key="test") as client:
        result = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.1)
    assert result["transcript"] == turns
    assert AgenticCall.from_dict(result).to_dict()["transcript"] == turns


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
def test_create_call_aliases_phone_on_recipients_list() -> None:
    route = respx.post("https://api.heycall-e.com/v2/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    client.calls.create(
        task="Call.",
        recipients=[{"phone": "+14155550100", "region": "US", "locale": "en-US"}],
        idempotency_key="wf_123",
        result_schema=RESULT_SCHEMA,
    )

    payload = json.loads(route.calls.last.request.content)
    assert payload["phone"] == "+14155550100"
    assert payload["region"] == "US"
    assert payload["locale"] == "en-US"
    assert "recipients" not in payload


@respx.mock
def test_create_call_aliases_phone_on_singular_recipient() -> None:
    route = respx.post("https://api.heycall-e.com/v2/calls").mock(return_value=httpx.Response(200, json=COMPLETED_CALL))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    client.calls.create(
        task="Call.",
        recipient={"phone": "+14155550100", "region": "US", "locale": "en-US"},
        idempotency_key="wf_123",
        result_schema=RESULT_SCHEMA,
    )

    payload = json.loads(route.calls.last.request.content)
    assert payload["phone"] == "+14155550100"
    assert payload["region"] == "US"
    assert payload["locale"] == "en-US"
    assert "recipients" not in payload


def test_normalize_recipient_aliases_phone_to_phones() -> None:
    from calle.calls import _normalize_recipient

    assert _normalize_recipient({"phone": "+14155550100", "region": "US", "locale": "en-US"}) == {
        "phones": ["+14155550100"],
        "region": "US",
        "locale": "en-US",
    }


@respx.mock
def test_create_requires_a_stable_idempotency_key() -> None:
    with CalleClient(api_key="test") as client:
        with pytest.raises(ValueError, match="idempotency_key"):
            client.calls.create(task="Call.", phone="+14155550100", region="US", locale="en-US", idempotency_key=" ", result_schema={"type": "object", "additionalProperties": False, "properties": {}})


@respx.mock
def test_cancel_returns_the_persisted_result_error() -> None:
    canceled = {**COMPLETED_CALL, "status": "canceled", "call_outcome": None,
                "result_status": "not_applicable", "result": None, "error": None}
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
    queued = {**COMPLETED_CALL, "status": "queued", "call_outcome": None, "result_status": "pending", "result": None, "completed_at": None}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(
        side_effect=[httpx.Response(200, json=queued), httpx.Response(200, json={**COMPLETED_CALL, "result_status": "pending", "result": None}), httpx.Response(200, json=COMPLETED_CALL)]
    )
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "completed"


@pytest.mark.parametrize("outcome", ["no_answer", "busy", "declined"])
@respx.mock
def test_wait_for_result_returns_ordinary_outcome_without_result_or_error(outcome) -> None:
    failed = {**COMPLETED_CALL, "call_outcome": outcome, "result_status": "unavailable", "result": None, "error": None}
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json=failed))
    client = CalleClient(api_key="key_test", base_url="https://api.heycall-e.com")

    call = client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)

    assert call["status"] == "completed"
    assert call["call_outcome"] == outcome
    assert call["error"] is None


@respx.mock
def test_wait_for_result_raises_timeout() -> None:
    queued = {**COMPLETED_CALL, "status": "queued", "call_outcome": None, "result_status": "pending", "result": None, "completed_at": None}
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
    respx.get("https://api.heycall-e.com/v2/calls/call_123").mock(return_value=httpx.Response(200, json={**COMPLETED_CALL, "result_status": "available", "result": {}}))
    with CalleClient(api_key="test") as client:
        assert client.calls.wait_for_result("call_123", interval_seconds=0.001, timeout_seconds=0.5)["result"] == {}


def test_call_id_stays_in_one_url_path_segment() -> None:
    requests: list[httpx.Request] = []

    def handle_request(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    call_id = "../goals?admin=1#fragment%2F"
    with httpx.Client(
        base_url="https://api.heycall-e.com",
        transport=httpx.MockTransport(handle_request),
    ) as http_client:
        client = CalleClient(api_key="key_test", http_client=http_client)
        client.calls.get(call_id)
        client.calls.list_events(call_id)

    encoded_id = "%2E%2E%2Fgoals%3Fadmin%3D1%23fragment%252F"
    assert requests[0].url.raw_path == f"/v2/calls/{encoded_id}".encode()
    assert requests[1].url.raw_path == f"/v2/calls/{encoded_id}/events".encode()
