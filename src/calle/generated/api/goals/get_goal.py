from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.goal import Goal


def _get_kwargs(
    goal_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/goals/{goal_id}".format(
            goal_id=quote(str(goal_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | Goal | None:
    if response.status_code == 200:
        response_200 = Goal.from_dict(response.json())

        return response_200

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

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if response.status_code == 502:
        response_502 = ErrorEnvelope.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | Goal]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorEnvelope | Goal]:
    """Get Goal

     Get an owner-scoped active Goal and its currently published immutable RunSpec interface.

    Store the `goal_id` returned by Chat publish success. `title` and `description` explain the
    current published workflow. Before sending a delivery-confirmation Run, use `input_schema`
    to verify that `customer_name`, `order_reference`, and `delivery_window` match the current
    published version, and use `result_schema` to prepare downstream outcome handling.

    This endpoint does not search by title, objective, or recency, and does not expose authoring
    instructions, provider bindings, or result materialization guidance. The
    server always resolves the current published pointer for a new business key.

    Args:
        goal_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | Goal]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorEnvelope | Goal | None:
    """Get Goal

     Get an owner-scoped active Goal and its currently published immutable RunSpec interface.

    Store the `goal_id` returned by Chat publish success. `title` and `description` explain the
    current published workflow. Before sending a delivery-confirmation Run, use `input_schema`
    to verify that `customer_name`, `order_reference`, and `delivery_window` match the current
    published version, and use `result_schema` to prepare downstream outcome handling.

    This endpoint does not search by title, objective, or recency, and does not expose authoring
    instructions, provider bindings, or result materialization guidance. The
    server always resolves the current published pointer for a new business key.

    Args:
        goal_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | Goal
    """

    return sync_detailed(
        goal_id=goal_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorEnvelope | Goal]:
    """Get Goal

     Get an owner-scoped active Goal and its currently published immutable RunSpec interface.

    Store the `goal_id` returned by Chat publish success. `title` and `description` explain the
    current published workflow. Before sending a delivery-confirmation Run, use `input_schema`
    to verify that `customer_name`, `order_reference`, and `delivery_window` match the current
    published version, and use `result_schema` to prepare downstream outcome handling.

    This endpoint does not search by title, objective, or recency, and does not expose authoring
    instructions, provider bindings, or result materialization guidance. The
    server always resolves the current published pointer for a new business key.

    Args:
        goal_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | Goal]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorEnvelope | Goal | None:
    """Get Goal

     Get an owner-scoped active Goal and its currently published immutable RunSpec interface.

    Store the `goal_id` returned by Chat publish success. `title` and `description` explain the
    current published workflow. Before sending a delivery-confirmation Run, use `input_schema`
    to verify that `customer_name`, `order_reference`, and `delivery_window` match the current
    published version, and use `result_schema` to prepare downstream outcome handling.

    This endpoint does not search by title, objective, or recency, and does not expose authoring
    instructions, provider bindings, or result materialization guidance. The
    server always resolves the current published pointer for a new business key.

    Args:
        goal_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | Goal
    """

    return (
        await asyncio_detailed(
            goal_id=goal_id,
            client=client,
        )
    ).parsed
