from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_envelope import ErrorEnvelope
from ...models.goal_run import GoalRun


def _get_kwargs(
    goal_id: str,
    goal_run_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/goals/{goal_id}/runs/{goal_run_id}".format(
            goal_id=quote(str(goal_id), safe=""),
            goal_run_id=quote(str(goal_run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | GoalRun | None:
    if response.status_code == 200:
        response_200 = GoalRun.from_dict(response.json())

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
) -> Response[ErrorEnvelope | GoalRun]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    goal_id: str,
    goal_run_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorEnvelope | GoalRun]:
    """Get Goal Run

     Get an owner- and Goal-scoped Run and its structured result facts.

    This is a pure read of the immutable execution snapshot. It does not resolve the current
    Goal pointer, dispatch work, or start result materialization. Use the `GoalRun.id` returned
    by create as `goal_run_id`; the nested telephone `run_id` is not valid in this path.

    Poll until either `result` or `error` is non-null. A non-null `result` is the parsed object
    validated against the published result schema. A non-null `error` means this Run will not
    produce a result. `status: completed` with both fields null means result processing is still
    in progress.

    Args:
        goal_id (str):
        goal_run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalRun]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
        goal_run_id=goal_run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    goal_id: str,
    goal_run_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorEnvelope | GoalRun | None:
    """Get Goal Run

     Get an owner- and Goal-scoped Run and its structured result facts.

    This is a pure read of the immutable execution snapshot. It does not resolve the current
    Goal pointer, dispatch work, or start result materialization. Use the `GoalRun.id` returned
    by create as `goal_run_id`; the nested telephone `run_id` is not valid in this path.

    Poll until either `result` or `error` is non-null. A non-null `result` is the parsed object
    validated against the published result schema. A non-null `error` means this Run will not
    produce a result. `status: completed` with both fields null means result processing is still
    in progress.

    Args:
        goal_id (str):
        goal_run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalRun
    """

    return sync_detailed(
        goal_id=goal_id,
        goal_run_id=goal_run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    goal_id: str,
    goal_run_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorEnvelope | GoalRun]:
    """Get Goal Run

     Get an owner- and Goal-scoped Run and its structured result facts.

    This is a pure read of the immutable execution snapshot. It does not resolve the current
    Goal pointer, dispatch work, or start result materialization. Use the `GoalRun.id` returned
    by create as `goal_run_id`; the nested telephone `run_id` is not valid in this path.

    Poll until either `result` or `error` is non-null. A non-null `result` is the parsed object
    validated against the published result schema. A non-null `error` means this Run will not
    produce a result. `status: completed` with both fields null means result processing is still
    in progress.

    Args:
        goal_id (str):
        goal_run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalRun]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
        goal_run_id=goal_run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    goal_id: str,
    goal_run_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorEnvelope | GoalRun | None:
    """Get Goal Run

     Get an owner- and Goal-scoped Run and its structured result facts.

    This is a pure read of the immutable execution snapshot. It does not resolve the current
    Goal pointer, dispatch work, or start result materialization. Use the `GoalRun.id` returned
    by create as `goal_run_id`; the nested telephone `run_id` is not valid in this path.

    Poll until either `result` or `error` is non-null. A non-null `result` is the parsed object
    validated against the published result schema. A non-null `error` means this Run will not
    produce a result. `status: completed` with both fields null means result processing is still
    in progress.

    Args:
        goal_id (str):
        goal_run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalRun
    """

    return (
        await asyncio_detailed(
            goal_id=goal_id,
            goal_run_id=goal_run_id,
            client=client,
        )
    ).parsed
