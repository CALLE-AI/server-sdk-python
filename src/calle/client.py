import httpx

from calle.calls import CalleCalls
from calle.webhooks import CalleWebhooks


class CalleClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.heycall-e.com",
        timeout: float = 30.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._owned_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )
        self.calls = CalleCalls(client=self._client)
        self.webhooks = CalleWebhooks()

    def close(self) -> None:
        if self._owned_client:
            self._client.close()

    def __enter__(self) -> "CalleClient":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()
