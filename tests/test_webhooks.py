import hmac
import hashlib

import pytest

from calle import CalleClient
from calle.errors import CalleWebhookSignatureError


def _sign(*, raw_body: bytes, timestamp: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), timestamp.encode("utf-8") + b"." + raw_body, hashlib.sha256).hexdigest()
    return f"v1={digest}"


def test_verify_accepts_valid_signature() -> None:
    client = CalleClient(api_key="key_test")
    raw_body = b'{"id":"evt_123","type":"call.completed","created_at":"2026-05-31T00:00:00Z","data":{"object":"call","id":"call_123","status":"completed"}}'
    timestamp = "1780035123"
    signature = _sign(raw_body=raw_body, timestamp=timestamp, secret="whsec_dev")

    assert client.webhooks.verify(raw_body=raw_body, timestamp=timestamp, signature=signature, secret="whsec_dev")


def test_unwrap_returns_event() -> None:
    client = CalleClient(api_key="key_test")
    raw_body = b'{"id":"evt_123","type":"call.completed","created_at":"2026-05-31T00:00:00Z","data":{"object":"call","id":"call_123","status":"completed"}}'
    timestamp = "1780035123"
    signature = _sign(raw_body=raw_body, timestamp=timestamp, secret="whsec_dev")

    event = client.webhooks.unwrap(
        raw_body=raw_body,
        headers={"CALL-E-Timestamp": timestamp, "CALL-E-Signature": signature},
        secret="whsec_dev",
    )

    assert event["id"] == "evt_123"
    assert event["type"] == "call.completed"


def test_unwrap_rejects_invalid_signature() -> None:
    client = CalleClient(api_key="key_test")

    with pytest.raises(CalleWebhookSignatureError):
        client.webhooks.unwrap(
            raw_body=b'{"id":"evt_123"}',
            headers={"CALL-E-Timestamp": "1780035123", "CALL-E-Signature": "v1=bad"},
            secret="whsec_dev",
        )
