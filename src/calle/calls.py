import time
from typing import Any

import httpx

from calle.errors import CalleConnectionError, CalleTimeoutError, api_error_from_response


JsonObject = dict[str, Any]


class CalleCalls:
    def __init__(self, *, client: httpx.Client) -> None:
        self._client = client

    def create(
        self,
        *,
        task: str,
        recipient: JsonObject,
        result_schema: JsonObject,
        context: JsonObject | None = None,
        policy: JsonObject | None = None,
        metadata: JsonObject | None = None,
        webhook_url: str | None = None,
        idempotency_key: str | None = None,
    ) -> JsonObject:
        body = {
            "task": task,
            "recipient": recipient,
            "context": context,
            "result_schema": result_schema,
            "policy": policy,
            "metadata": metadata,
            "webhook_url": webhook_url,
        }
        payload = {key: value for key, value in body.items() if value is not None}
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._request("POST", "/v1/calls", json=payload, headers=headers)

    def get(self, call_id: str) -> JsonObject:
        return self._request("GET", f"/v1/calls/{call_id}")

    def list_events(self, call_id: str, *, cursor: str | None = None, limit: int | None = None) -> JsonObject:
        params = {key: value for key, value in {"cursor": cursor, "limit": limit}.items() if value is not None}
        return self._request("GET", f"/v1/calls/{call_id}/events", params=params)

    def wait_for_result(
        self,
        call_id: str,
        *,
        interval_seconds: float = 2.0,
        timeout_seconds: float = 600.0,
    ) -> JsonObject:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() <= deadline:
            call = self.get(call_id)
            if call.get("status") in {"completed", "failed", "canceled"}:
                return call
            time.sleep(interval_seconds)
        raise CalleTimeoutError(f"Timed out waiting for CALL-E call {call_id}.")

    def create_and_wait(self, **kwargs: Any) -> JsonObject:
        interval_seconds = float(kwargs.pop("interval_seconds", 2.0))
        timeout_seconds = float(kwargs.pop("timeout_seconds", 600.0))
        call = self.create(**kwargs)
        return self.wait_for_result(
            str(call["id"]),
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> JsonObject:
        try:
            response = self._client.request(method, path, **kwargs)
        except httpx.TimeoutException as exc:
            raise CalleTimeoutError("CALL-E API request timed out.") from exc
        except httpx.HTTPError as exc:
            raise CalleConnectionError("CALL-E API request failed before receiving a response.") from exc

        if response.status_code >= 400:
            raise api_error_from_response(response.status_code, response.json())
        payload = response.json()
        if not isinstance(payload, dict):
            raise CalleConnectionError("CALL-E API returned a non-object JSON response.")
        return payload
