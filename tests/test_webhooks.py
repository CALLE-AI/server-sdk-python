import hashlib
import hmac
import json

import pytest

from calle import CalleClient, CalleWebhookSignatureError


def _sign(*, raw_body: bytes, timestamp: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), timestamp.encode("utf-8") + b"." + raw_body, hashlib.sha256).hexdigest()
    return f"v1={digest}"


def _terminal_event() -> dict[str, object]:
    return {
        "id": "evt_123",
        "type": "call.completed",
        "created_at": "2026-07-29T10:00:00Z",
        "data": {
            "id": "call_123",
            "object": "call_task",
            "status": "completed",
            "structured_result": {"completed_count": 1},
            "summary": "The recipient confirmed attendance.",
            "task_completed": True,
            "completion_confidence": {"score": 0.92, "label": "high"},
            "evidence": ["The recipient said yes."],
            "completed_at": "2026-07-29T10:00:00Z",
        },
    }


def test_legacy_verify_accepts_valid_signature() -> None:
    client = CalleClient(api_key="key_test")
    raw_body = b'{"id":"evt_123","type":"call.completed","created_at":"2026-05-31T00:00:00Z","data":{"object":"call","id":"call_123","status":"completed"}}'
    timestamp = "1780035123"
    signature = _sign(raw_body=raw_body, timestamp=timestamp, secret="whsec_dev")

    assert client.webhooks.verify(raw_body=raw_body, timestamp=timestamp, signature=signature, secret="whsec_dev")


def test_legacy_unwrap_returns_finalized_event_after_signature_verification() -> None:
    client = CalleClient(api_key="key_test")
    raw_body = json.dumps(_terminal_event()).encode()
    timestamp = "1780035123"
    signature = _sign(raw_body=raw_body, timestamp=timestamp, secret="whsec_dev")

    event = client.webhooks.unwrap(
        raw_body=raw_body,
        headers={"CALL-E-Timestamp": timestamp, "CALL-E-Signature": signature},
        secret="whsec_dev",
    )

    assert event["id"] == "evt_123"
    assert event["type"] == "call.completed"
    assert event["data"]["structured_result"] == {"completed_count": 1}
    assert event["data"]["task_completed"] is True
    assert event["data"]["completion_confidence"] == {"score": 0.92, "label": "high"}
    assert event["data"]["evidence"] == ["The recipient said yes."]


def test_legacy_unwrap_rejects_missing_signature_headers() -> None:
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleWebhookSignatureError, match="Missing"):
        client.webhooks.unwrap(
            raw_body=json.dumps(_terminal_event()),
            headers={},
            secret="whsec_dev",
        )


def test_legacy_unwrap_rejects_tampered_body() -> None:
    client = CalleClient(api_key="key_test")
    timestamp = "1780035123"
    original_body = json.dumps(_terminal_event())
    signature = _sign(
        raw_body=original_body.encode(),
        timestamp=timestamp,
        secret="whsec_dev",
    )

    with pytest.raises(CalleWebhookSignatureError, match="Invalid"):
        client.webhooks.unwrap(
            raw_body=original_body.replace("call.completed", "call.failed"),
            headers={"CALL-E-Timestamp": timestamp, "CALL-E-Signature": signature},
            secret="whsec_dev",
        )
