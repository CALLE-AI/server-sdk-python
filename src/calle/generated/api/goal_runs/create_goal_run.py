from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.create_goal_run_request import CreateGoalRunRequest
from ...models.error_envelope import ErrorEnvelope
from ...models.goal_run import GoalRun


def _get_kwargs(
    goal_id: str,
    *,
    body: CreateGoalRunRequest,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/goals/{goal_id}/runs".format(
            goal_id=quote(str(goal_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | GoalRun | None:
    if response.status_code == 201:
        response_201 = GoalRun.from_dict(response.json())

        return response_201

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

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

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
    *,
    client: AuthenticatedClient | Client,
    body: CreateGoalRunRequest,
    idempotency_key: str,
) -> Response[ErrorEnvelope | GoalRun]:
    """Create Goal Run

     Create one singleton Goal Run for a published Goal.

    In a delivery-confirmation integration, `phone` identifies one customer and `variables`
    provide that order's reference and proposed window. CALL-E atomically resolves and pins the
    published RunSpec, validates the variables, and durably accepts execution.

    The request cannot select, replace, or relax schemas or the materialization contract. The
    first accepted request and an exact idempotent replay both return `201` with the same Goal
    Run identity. A `201` response means durable acceptance, not that the recipient answered or
    that `result` is ready.

    Args:
        goal_id (str):
        idempotency_key (str):
        body (CreateGoalRunRequest): One phone-specific submission against the Goal's currently
            published RunSpec. The object is
            closed: target wrappers, per-Run region/locale/display-name hints, task text, schemas,
            RunSpec
            selectors, provider settings, and unknown fields are not accepted. Region, callee locale,
            and
            runtime profile come from the published Goal. Use the required `Idempotency-Key` header
            for
            retry safety.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalRun]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateGoalRunRequest,
    idempotency_key: str,
) -> ErrorEnvelope | GoalRun | None:
    """Create Goal Run

     Create one singleton Goal Run for a published Goal.

    In a delivery-confirmation integration, `phone` identifies one customer and `variables`
    provide that order's reference and proposed window. CALL-E atomically resolves and pins the
    published RunSpec, validates the variables, and durably accepts execution.

    The request cannot select, replace, or relax schemas or the materialization contract. The
    first accepted request and an exact idempotent replay both return `201` with the same Goal
    Run identity. A `201` response means durable acceptance, not that the recipient answered or
    that `result` is ready.

    Args:
        goal_id (str):
        idempotency_key (str):
        body (CreateGoalRunRequest): One phone-specific submission against the Goal's currently
            published RunSpec. The object is
            closed: target wrappers, per-Run region/locale/display-name hints, task text, schemas,
            RunSpec
            selectors, provider settings, and unknown fields are not accepted. Region, callee locale,
            and
            runtime profile come from the published Goal. Use the required `Idempotency-Key` header
            for
            retry safety.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalRun
    """

    return sync_detailed(
        goal_id=goal_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateGoalRunRequest,
    idempotency_key: str,
) -> Response[ErrorEnvelope | GoalRun]:
    """Create Goal Run

     Create one singleton Goal Run for a published Goal.

    In a delivery-confirmation integration, `phone` identifies one customer and `variables`
    provide that order's reference and proposed window. CALL-E atomically resolves and pins the
    published RunSpec, validates the variables, and durably accepts execution.

    The request cannot select, replace, or relax schemas or the materialization contract. The
    first accepted request and an exact idempotent replay both return `201` with the same Goal
    Run identity. A `201` response means durable acceptance, not that the recipient answered or
    that `result` is ready.

    Args:
        goal_id (str):
        idempotency_key (str):
        body (CreateGoalRunRequest): One phone-specific submission against the Goal's currently
            published RunSpec. The object is
            closed: target wrappers, per-Run region/locale/display-name hints, task text, schemas,
            RunSpec
            selectors, provider settings, and unknown fields are not accepted. Region, callee locale,
            and
            runtime profile come from the published Goal. Use the required `Idempotency-Key` header
            for
            retry safety.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GoalRun]
    """

    kwargs = _get_kwargs(
        goal_id=goal_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    goal_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateGoalRunRequest,
    idempotency_key: str,
) -> ErrorEnvelope | GoalRun | None:
    """Create Goal Run

     Create one singleton Goal Run for a published Goal.

    In a delivery-confirmation integration, `phone` identifies one customer and `variables`
    provide that order's reference and proposed window. CALL-E atomically resolves and pins the
    published RunSpec, validates the variables, and durably accepts execution.

    The request cannot select, replace, or relax schemas or the materialization contract. The
    first accepted request and an exact idempotent replay both return `201` with the same Goal
    Run identity. A `201` response means durable acceptance, not that the recipient answered or
    that `result` is ready.

    Args:
        goal_id (str):
        idempotency_key (str):
        body (CreateGoalRunRequest): One phone-specific submission against the Goal's currently
            published RunSpec. The object is
            closed: target wrappers, per-Run region/locale/display-name hints, task text, schemas,
            RunSpec
            selectors, provider settings, and unknown fields are not accepted. Region, callee locale,
            and
            runtime profile come from the published Goal. Use the required `Idempotency-Key` header
            for
            retry safety.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GoalRun
    """

    return (
        await asyncio_detailed(
            goal_id=goal_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
