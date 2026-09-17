from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.agentic_webhook_event import AgenticWebhookEvent
from ...models.webhook_acknowledgement import WebhookAcknowledgement
from ...models.webhook_event import WebhookEvent


def _get_kwargs(
    *,
    body: AgenticWebhookEvent | WebhookEvent,
    call_e_event_id: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["CALL-E-Event-Id"] = call_e_event_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/calle/webhook",
    }

    if isinstance(body, WebhookEvent):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | WebhookAcknowledgement | None:
    if response.status_code == 200:
        response_200 = WebhookAcknowledgement.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | WebhookAcknowledgement]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AgenticWebhookEvent | WebhookEvent,
    call_e_event_id: str,
) -> Response[Any | WebhookAcknowledgement]:
    """Server Message

     CALL-E sends this request after a call reaches a terminal state and its post-call outcome and
    requested structured results are finalized. Configure this URL with `webhook_url` on create call or
    through project-level webhook settings.

    Args:
        call_e_event_id (str):
        body (AgenticWebhookEvent | WebhookEvent): Terminal event for either a legacy v1 call task
            or an Agentic v2 call. Inspect data.object to distinguish the payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | WebhookAcknowledgement]
    """

    kwargs = _get_kwargs(
        body=body,
        call_e_event_id=call_e_event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AgenticWebhookEvent | WebhookEvent,
    call_e_event_id: str,
) -> Any | WebhookAcknowledgement | None:
    """Server Message

     CALL-E sends this request after a call reaches a terminal state and its post-call outcome and
    requested structured results are finalized. Configure this URL with `webhook_url` on create call or
    through project-level webhook settings.

    Args:
        call_e_event_id (str):
        body (AgenticWebhookEvent | WebhookEvent): Terminal event for either a legacy v1 call task
            or an Agentic v2 call. Inspect data.object to distinguish the payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | WebhookAcknowledgement
    """

    return sync_detailed(
        client=client,
        body=body,
        call_e_event_id=call_e_event_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AgenticWebhookEvent | WebhookEvent,
    call_e_event_id: str,
) -> Response[Any | WebhookAcknowledgement]:
    """Server Message

     CALL-E sends this request after a call reaches a terminal state and its post-call outcome and
    requested structured results are finalized. Configure this URL with `webhook_url` on create call or
    through project-level webhook settings.

    Args:
        call_e_event_id (str):
        body (AgenticWebhookEvent | WebhookEvent): Terminal event for either a legacy v1 call task
            or an Agentic v2 call. Inspect data.object to distinguish the payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | WebhookAcknowledgement]
    """

    kwargs = _get_kwargs(
        body=body,
        call_e_event_id=call_e_event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AgenticWebhookEvent | WebhookEvent,
    call_e_event_id: str,
) -> Any | WebhookAcknowledgement | None:
    """Server Message

     CALL-E sends this request after a call reaches a terminal state and its post-call outcome and
    requested structured results are finalized. Configure this URL with `webhook_url` on create call or
    through project-level webhook settings.

    Args:
        call_e_event_id (str):
        body (AgenticWebhookEvent | WebhookEvent): Terminal event for either a legacy v1 call task
            or an Agentic v2 call. Inspect data.object to distinguish the payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | WebhookAcknowledgement
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            call_e_event_id=call_e_event_id,
        )
    ).parsed
