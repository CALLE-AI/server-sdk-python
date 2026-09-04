import json
from email.message import Message
from io import BytesIO
from typing import Any

import pytest

from examples import webhook_server
from examples.webhook_server import (
    WebhookHandler,
    max_request_body_bytes,
    processed_event_ids,
)


def _request(
    content_length: str | None,
    body: bytes = b"",
    event_id: str | None = None,
) -> tuple[list[tuple[int, dict[str, Any]]], WebhookHandler]:
    handler = WebhookHandler.__new__(WebhookHandler)
    handler.path = "/calle/webhook"
    handler.headers = Message()
    if content_length is not None:
        handler.headers["content-length"] = content_length
    if event_id is not None:
        handler.headers["CALL-E-Event-Id"] = event_id
    handler.rfile = BytesIO(body)
    handler.close_connection = False
    responses: list[tuple[int, dict[str, Any]]] = []
    handler._send_json = lambda status, payload: responses.append((status, payload))
    handler.do_POST()
    return responses, handler


@pytest.mark.parametrize(
    ("content_length", "expected_response"),
    [
        (None, (400, {"error": "invalid_content_length"})),
        ("invalid", (400, {"error": "invalid_content_length"})),
        ("-1", (400, {"error": "invalid_content_length"})),
        (str(max_request_body_bytes + 1), (413, {"error": "payload_too_large"})),
    ],
)
def test_webhook_rejects_unsafe_content_lengths_before_reading(
    content_length: str | None,
    expected_response: tuple[int, dict[str, str]],
) -> None:
    responses, handler = _request(content_length)

    assert responses == [expected_response]
    assert handler.rfile.tell() == 0
    assert handler.close_connection is True


def test_webhook_accepts_valid_body_within_limit() -> None:
    event_id = "evt_body_limit_control"
    body = json.dumps(
        {
            "id": event_id,
            "type": "call.completed",
            "data": {"id": "call_123"},
        }
    ).encode()
    processed_event_ids.clear()

    responses, _ = _request(str(len(body)), body, event_id)

    assert responses == [(200, {"received": True})]
    processed_event_ids.clear()


def test_webhook_bounds_local_deduplication_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(webhook_server, "max_processed_event_ids", 1)
    processed_event_ids.clear()

    for event_id in ("evt_first", "evt_second"):
        body = json.dumps(
            {"id": event_id, "type": "call.completed", "data": {"id": "call_123"}}
        ).encode()
        responses, _ = _request(str(len(body)), body, event_id)
        assert responses == [(200, {"received": True})]

    assert len(processed_event_ids) == 1
    duplicate_body = json.dumps(
        {"id": "evt_second", "type": "call.completed", "data": {"id": "call_123"}}
    ).encode()
    responses, _ = _request(str(len(duplicate_body)), duplicate_body, "evt_second")
    assert responses == [(200, {"received": True, "duplicate": True})]
    processed_event_ids.clear()
