from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.goal_list import GoalList
from ...types import Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
    after: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["after"] = after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/goals",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | GoalList | None:
    if response.status_code == 200:
        response_200 = GoalList.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | GoalList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    after: str | Unset = UNSET,
) -> Response[ErrorEnvelope | GoalList]:
    """List Goals

     List the authenticated owner's active, listed Goals that have a published RunSpec. For
    example, a fulfillment service can inspect the published interface for its reusable
    delivery-confirmation workflow before creating phone-specific Runs.

    Results are ordered by opaque Goal identity. Use `next_cursor` as the next request's
    `after` value; clients must not parse or construct cursor values. `title` and `description`
    help operators recognize each published workflow, but integrations should still store the
    intended `goal_id` at publish time and must not execute the first list item blindly.

    Args:
        limit (int | Unset):  Default: 20.
        after (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        after=after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    after: str | Unset = UNSET,
) -> ErrorEnvelope | GoalList | None:
    """List Goals

     List the authenticated owner's active, listed Goals that have a published RunSpec. For
    example, a fulfillment service can inspect the published interface for its reusable
    delivery-confirmation workflow before creating phone-specific Runs.

    Results are ordered by opaque Goal identity. Use `next_cursor` as the next request's
    `after` value; clients must not parse or construct cursor values. `title` and `description`
    help operators recognize each published workflow, but integrations should still store the
    intended `goal_id` at publish time and must not execute the first list item blindly.

    Args:
        limit (int | Unset):  Default: 20.
        after (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        after=after,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    after: str | Unset = UNSET,
) -> Response[ErrorEnvelope | GoalList]:
    """List Goals

     List the authenticated owner's active, listed Goals that have a published RunSpec. For
    example, a fulfillment service can inspect the published interface for its reusable
    delivery-confirmation workflow before creating phone-specific Runs.

    Results are ordered by opaque Goal identity. Use `next_cursor` as the next request's
    `after` value; clients must not parse or construct cursor values. `title` and `description`
    help operators recognize each published workflow, but integrations should still store the
    intended `goal_id` at publish time and must not execute the first list item blindly.

    Args:
        limit (int | Unset):  Default: 20.
        after (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        after=after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 20,
    after: str | Unset = UNSET,
) -> ErrorEnvelope | GoalList | None:
    """List Goals

     List the authenticated owner's active, listed Goals that have a published RunSpec. For
    example, a fulfillment service can inspect the published interface for its reusable
    delivery-confirmation workflow before creating phone-specific Runs.

    Results are ordered by opaque Goal identity. Use `next_cursor` as the next request's
    `after` value; clients must not parse or construct cursor values. `title` and `description`
    help operators recognize each published workflow, but integrations should still store the
    intended `goal_id` at publish time and must not execute the first list item blindly.

    Args:
        limit (int | Unset):  Default: 20.
        after (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            after=after,
        )
    ).parsed
