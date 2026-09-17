from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.agentic_call import AgenticCall
from ...models.create_agentic_call_request import CreateAgenticCallRequest
from ...models.error_envelope import ErrorEnvelope


def _get_kwargs(
    *,
    body: CreateAgenticCallRequest,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/calls",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgenticCall | ErrorEnvelope | None:
    if response.status_code == 202:
        response_202 = AgenticCall.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = ErrorEnvelope.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

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
    *,
    client: AuthenticatedClient | Client,
    body: CreateAgenticCallRequest,
    idempotency_key: str,
) -> Response[AgenticCall | ErrorEnvelope]:
    """Create a single Agentic call

     Accept one phone for durable Agentic execution. Batch recipients, recurrence and
    recipient_result_schema are not accepted. The accepted request and result_schema are immutable. In
    this draft scheduled_at is reserved and non-null values return 422 scheduling_unavailable until
    renewable execution authorization is configured.

    Args:
        idempotency_key (str):
        body (CreateAgenticCallRequest): One phone, explicit dialing locale and a required Goal-
            compatible result schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgenticCall | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateAgenticCallRequest,
    idempotency_key: str,
) -> AgenticCall | ErrorEnvelope | None:
    """Create a single Agentic call

     Accept one phone for durable Agentic execution. Batch recipients, recurrence and
    recipient_result_schema are not accepted. The accepted request and result_schema are immutable. In
    this draft scheduled_at is reserved and non-null values return 422 scheduling_unavailable until
    renewable execution authorization is configured.

    Args:
        idempotency_key (str):
        body (CreateAgenticCallRequest): One phone, explicit dialing locale and a required Goal-
            compatible result schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgenticCall | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateAgenticCallRequest,
    idempotency_key: str,
) -> Response[AgenticCall | ErrorEnvelope]:
    """Create a single Agentic call

     Accept one phone for durable Agentic execution. Batch recipients, recurrence and
    recipient_result_schema are not accepted. The accepted request and result_schema are immutable. In
    this draft scheduled_at is reserved and non-null values return 422 scheduling_unavailable until
    renewable execution authorization is configured.

    Args:
        idempotency_key (str):
        body (CreateAgenticCallRequest): One phone, explicit dialing locale and a required Goal-
            compatible result schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgenticCall | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateAgenticCallRequest,
    idempotency_key: str,
) -> AgenticCall | ErrorEnvelope | None:
    """Create a single Agentic call

     Accept one phone for durable Agentic execution. Batch recipients, recurrence and
    recipient_result_schema are not accepted. The accepted request and result_schema are immutable. In
    this draft scheduled_at is reserved and non-null values return 422 scheduling_unavailable until
    renewable execution authorization is configured.

    Args:
        idempotency_key (str):
        body (CreateAgenticCallRequest): One phone, explicit dialing locale and a required Goal-
            compatible result schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgenticCall | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
