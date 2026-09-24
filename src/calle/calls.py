import time
from typing import Any
from urllib.parse import quote

import httpx

from calle.errors import CalleAPIError, CalleConnectionError, CalleTimeoutError, api_error_from_response


JsonObject = dict[str, Any]


class CalleCalls:
    def __init__(self, *, client: httpx.Client) -> None:
        self._client = client

    def create(
        self,
        *,
        task: str,
        phone: str,
        region: str | None = None,
        locale: str | None = None,
        idempotency_key: str,
        result_schema: JsonObject,
        metadata: JsonObject | None = None,
        webhook_url: str | None = None,
    ) -> JsonObject:
        if not idempotency_key.strip():
            raise ValueError("A stable idempotency_key is required.")
        body = {
            "task": task, "phone": phone, "region": region, "locale": locale,
            "result_schema": result_schema,
            "metadata": metadata, "webhook_url": webhook_url,
        }
        payload = {key: value for key, value in body.items() if value is not None}
        headers = {"Idempotency-Key": idempotency_key}
        return self._request("POST", "/v2/calls", json=payload, headers=headers)

    def get(self, call_id: str) -> JsonObject:
        return self._request("GET", _call_path(call_id))

    def cancel(self, call_id: str) -> JsonObject:
        return self._request("POST", f"{_call_path(call_id)}/cancel")

    def list_events(self, call_id: str, *, cursor: str | None = None, limit: int | None = None) -> JsonObject:
        params = {key: value for key, value in {"cursor": cursor, "limit": limit}.items() if value is not None}
        return self._request("GET", f"{_call_path(call_id)}/events", params=params)

    def wait_for_result(
        self,
        call_id: str,
        *,
        interval_seconds: float = 2.0,
        timeout_seconds: float = 600.0,
    ) -> JsonObject:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() <= deadline:
            try:
                call = self.get(call_id)
            except CalleAPIError as exc:
                if exc.code != "call_not_ready":
                    raise
            else:
                if call["result_status"] != "pending":
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


def _call_path(call_id: str) -> str:
    encoded_call_id = quote(call_id, safe="").replace(".", "%2E")
    return f"/v2/calls/{encoded_call_id}"
