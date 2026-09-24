from collections.abc import Callable

import httpx
import pytest

from calle import CalleClient
from calle.errors import CalleAPIError, CalleConnectionError


Operation = Callable[[CalleClient], object]


@pytest.mark.parametrize(
    "operation",
    [
        lambda client: client.calls.get("call_123"),
        lambda client: client.goals.get("goal_123"),
    ],
)
def test_non_json_error_response_preserves_http_status(operation: Operation) -> None:
    def handle_request(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            502,
            text="<html>Bad Gateway</html>",
            headers={"content-type": "text/html"},
        )

    with httpx.Client(
        base_url="https://api.heycall-e.com",
        transport=httpx.MockTransport(handle_request),
    ) as http_client:
        client = CalleClient(api_key="key_test", http_client=http_client)
        with pytest.raises(CalleAPIError) as exc_info:
            operation(client)

    assert exc_info.value.status_code == 502
    assert exc_info.value.code == "internal_error"
    assert isinstance(exc_info.value.__cause__, ValueError)


@pytest.mark.parametrize(
    "operation",
    [
        lambda client: client.calls.get("call_123"),
        lambda client: client.goals.get("goal_123"),
    ],
)
def test_non_json_success_response_maps_to_connection_error(operation: Operation) -> None:
    def handle_request(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"not-json",
            headers={"content-type": "text/plain"},
        )

    with httpx.Client(
        base_url="https://api.heycall-e.com",
        transport=httpx.MockTransport(handle_request),
    ) as http_client:
        client = CalleClient(api_key="key_test", http_client=http_client)
        with pytest.raises(CalleConnectionError, match="invalid JSON") as exc_info:
            operation(client)

    assert isinstance(exc_info.value.__cause__, ValueError)
