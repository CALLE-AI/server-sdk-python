from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.agentic_call import AgenticCall
from ...models.error_envelope import ErrorEnvelope


def _get_kwargs(
    call_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/calls/{call_id}/cancel".format(
            call_id=quote(str(call_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgenticCall | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = AgenticCall.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgenticCall | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    call_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgenticCall | ErrorEnvelope]:
    """Cancel before provider submission

     Cancellation is idempotent for terminal calls. Once provider submission starts, returns 409
    call_cannot_cancel; it does not hang up an active call.

    Args:
        call_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgenticCall | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    call_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AgenticCall | ErrorEnvelope | None:
    """Cancel before provider submission

     Cancellation is idempotent for terminal calls. Once provider submission starts, returns 409
    call_cannot_cancel; it does not hang up an active call.

    Args:
        call_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgenticCall | ErrorEnvelope
    """

    return sync_detailed(
        call_id=call_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    call_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AgenticCall | ErrorEnvelope]:
    """Cancel before provider submission

     Cancellation is idempotent for terminal calls. Once provider submission starts, returns 409
    call_cannot_cancel; it does not hang up an active call.

    Args:
        call_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgenticCall | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    call_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AgenticCall | ErrorEnvelope | None:
    """Cancel before provider submission

     Cancellation is idempotent for terminal calls. Once provider submission starts, returns 409
    call_cannot_cancel; it does not hang up an active call.

    Args:
        call_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgenticCall | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            call_id=call_id,
            client=client,
        )
    ).parsed
