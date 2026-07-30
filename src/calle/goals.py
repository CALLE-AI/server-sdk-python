import math
import time
from typing import Any
from urllib.parse import quote

import httpx

from calle.errors import CalleConnectionError, CalleTimeoutError, api_error_from_response


JsonObject = dict[str, Any]
GoalScalar = str | int | float | bool
GoalVariables = dict[str, GoalScalar]


class CalleGoals:
    def __init__(self, *, client: httpx.Client) -> None:
        self._client = client

    def list(self, *, limit: int = 20, after: str | None = None) -> JsonObject:
        params: dict[str, str | int] = {"limit": limit}
        if after is not None:
            params["after"] = after
        return self._request("GET", "/v1/goals", params=params)

    def get(self, goal_id: str) -> JsonObject:
        encoded_goal_id = quote(goal_id, safe="")
        return self._request("GET", f"/v1/goals/{encoded_goal_id}")

    def run(
        self,
        *,
        goal_id: str,
        phone: str,
        variables: GoalVariables | None = None,
        idempotency_key: str,
    ) -> JsonObject:
        body: JsonObject = {"phone": phone}
        if variables is not None:
            body["variables"] = variables
        encoded_goal_id = quote(goal_id, safe="")
        return self._request(
            "POST",
            f"/v1/goals/{encoded_goal_id}/runs",
            json=body,
            headers={"Idempotency-Key": idempotency_key},
        )

    def get_run(self, goal_id: str, goal_run_id: str) -> JsonObject:
        return self._get_run(goal_id, goal_run_id)

    def _get_run(
        self,
        goal_id: str,
        goal_run_id: str,
        *,
        timeout_seconds: float | None = None,
    ) -> JsonObject:
        encoded_goal_id = quote(goal_id, safe="")
        encoded_goal_run_id = quote(goal_run_id, safe="")
        request_options: dict[str, Any] = {}
        if timeout_seconds is not None:
            request_options["timeout"] = timeout_seconds
        return self._request(
            "GET",
            f"/v1/goals/{encoded_goal_id}/runs/{encoded_goal_run_id}",
            **request_options,
        )

    def wait_for_result(
        self,
        goal_id: str,
        goal_run_id: str,
        *,
        interval_seconds: float = 2.0,
        timeout_seconds: float = 600.0,
    ) -> JsonObject:
        _validate_polling_seconds(interval_seconds, "interval_seconds")
        _validate_polling_seconds(timeout_seconds, "timeout_seconds")
        deadline = time.monotonic() + timeout_seconds
        while True:
            remaining_seconds = deadline - time.monotonic()
            if remaining_seconds <= 0:
                break
            run = self._get_run(
                goal_id,
                goal_run_id,
                timeout_seconds=remaining_seconds,
            )
            if run.get("result") is not None or run.get("error") is not None:
                return run
            remaining_seconds = deadline - time.monotonic()
            if remaining_seconds <= 0:
                break
            time.sleep(min(interval_seconds, remaining_seconds))
        raise CalleTimeoutError(f"Timed out waiting for CALL-E Goal Run {goal_run_id}.")

    def run_and_wait(
        self,
        *,
        goal_id: str,
        phone: str,
        variables: GoalVariables | None = None,
        idempotency_key: str,
        interval_seconds: float = 2.0,
        timeout_seconds: float = 600.0,
    ) -> JsonObject:
        _validate_polling_seconds(interval_seconds, "interval_seconds")
        _validate_polling_seconds(timeout_seconds, "timeout_seconds")
        run = self.run(
            goal_id=goal_id,
            phone=phone,
            variables=variables,
            idempotency_key=idempotency_key,
        )
        if run.get("result") is not None or run.get("error") is not None:
            return run
        return self.wait_for_result(
            goal_id,
            str(run["id"]),
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


def _validate_polling_seconds(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number.")
