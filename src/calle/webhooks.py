import hashlib
import hmac
import json
from typing import Any, Mapping

from calle.errors import CalleWebhookSignatureError


class CalleWebhooks:
    def verify(self, *, raw_body: bytes | str, timestamp: str, signature: str, secret: str) -> bool:
        """Verify a legacy HMAC signature.

        Deprecated: CALL-E no longer sends timestamp or signature headers. This
        method remains available for integrations that use their own compatible
        signing layer.
        """
        expected = _signature(raw_body=raw_body, timestamp=timestamp, secret=secret)
        return hmac.compare_digest(signature, expected)

    def unwrap(self, *, raw_body: bytes | str, headers: Mapping[str, str], secret: str) -> dict[str, Any]:
        """Verify and parse a legacy signed webhook payload.

        Deprecated: current CALL-E webhooks are unsigned. This method retains the
        SDK 0.2 trust boundary and must not be used to parse current deliveries.
        """
        timestamp = _header(headers, "CALL-E-Timestamp")
        signature = _header(headers, "CALL-E-Signature")
        if timestamp is None or signature is None:
            raise CalleWebhookSignatureError("Missing CALL-E webhook signature headers.")
        if not self.verify(raw_body=raw_body, timestamp=timestamp, signature=signature, secret=secret):
            raise CalleWebhookSignatureError("Invalid CALL-E webhook signature.")
        body = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body
        parsed = json.loads(body.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise CalleWebhookSignatureError("CALL-E webhook payload must be a JSON object.")
        return parsed


def _header(headers: Mapping[str, str], name: str) -> str | None:
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return None


def _signature(*, raw_body: bytes | str, timestamp: str, secret: str) -> str:
    body = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body
    digest = hmac.new(secret.encode("utf-8"), timestamp.encode("utf-8") + b"." + body, hashlib.sha256).hexdigest()
    return f"v1={digest}"
