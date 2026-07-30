from typing import Any


class CalleAPIError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class CalleAuthenticationError(CalleAPIError):
    pass


class CalleRateLimitError(CalleAPIError):
    pass


class CalleTimeoutError(Exception):
    pass


class CalleConnectionError(Exception):
    pass


class CalleWebhookSignatureError(Exception):
    """Legacy signed-webhook validation error retained for SDK 0.2 compatibility."""

    pass


def api_error_from_response(status_code: int, payload: object) -> CalleAPIError:
    envelope = payload if isinstance(payload, dict) else {}
    raw_error = envelope.get("error")
    error: dict[str, Any] = raw_error if isinstance(raw_error, dict) else {}
    raw_code = error.get("code")
    raw_message = error.get("message")
    raw_details = error.get("details")
    code = raw_code if isinstance(raw_code, str) else "internal_error"
    message = raw_message if isinstance(raw_message, str) else "CALL-E API request failed."
    details = raw_details if isinstance(raw_details, dict) else {}
    if status_code in {401, 403}:
        return CalleAuthenticationError(code=code, message=message, status_code=status_code, details=details)
    if status_code == 429:
        return CalleRateLimitError(code=code, message=message, status_code=status_code, details=details)
    return CalleAPIError(code=code, message=message, status_code=status_code, details=details)
