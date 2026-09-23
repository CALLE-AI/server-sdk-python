import httpx
from attrs import define

from calle.generated import AuthenticatedClient, Client
from calle.generated.api.legacy_calls.get_call import _get_kwargs as get_call_kwargs
from calle.generated.api.legacy_calls.list_call_events import (
    _get_kwargs as list_call_events_kwargs,
)


@define
class DerivedClient(Client):
    pass


@define
class DerivedAuthenticatedClient(AuthenticatedClient):
    pass


def test_generated_client_repr_does_not_expose_credentials() -> None:
    secret = "repr_sentinel_secret"
    client = Client(
        base_url="https://api.heycall-e.com",
        cookies={"session": secret},
        headers={"X-Secret": secret},
    )
    authenticated_client = AuthenticatedClient(
        base_url="https://api.heycall-e.com",
        token=secret,
    )
    derived_client = DerivedClient(
        base_url=f"https://{secret}@api.heycall-e.com",
        headers={"X-Secret": secret},
    )
    derived_authenticated_client = DerivedAuthenticatedClient(
        base_url="https://api.heycall-e.com",
        token=secret,
    )

    for value in (
        client,
        authenticated_client,
        derived_client,
        derived_authenticated_client,
    ):
        assert secret not in repr(value)

    client.get_httpx_client()
    authenticated_client.get_httpx_client()
    try:
        assert secret not in repr(client)
        assert secret not in repr(authenticated_client)
    finally:
        client.get_httpx_client().close()
        authenticated_client.get_httpx_client().close()


def test_generated_call_id_stays_in_one_url_path_segment() -> None:
    client = httpx.Client(base_url="https://api.heycall-e.com")
    try:
        get_path = get_call_kwargs("..")["url"]
        events_path = list_call_events_kwargs("..")["url"]

        assert client.build_request("GET", get_path).url.raw_path == b"/v1/calls/%2E%2E"
        assert (
            client.build_request("GET", events_path).url.raw_path
            == b"/v1/calls/%2E%2E/events"
        )
    finally:
        client.close()


def test_generated_single_target_call_paths_encode_opaque_ids() -> None:
    from calle.generated.api.calls.cancel_agentic_call import _get_kwargs as cancel_kwargs
    from calle.generated.api.calls.get_agentic_call import _get_kwargs as get_kwargs
    from calle.generated.api.calls.list_agentic_call_events import _get_kwargs as events_kwargs

    with httpx.Client(base_url="https://api.heycall-e.com") as client:
        for method, kwargs, suffix in [
            ("GET", get_kwargs(".."), ""),
            ("GET", events_kwargs(".."), "/events"),
            ("POST", cancel_kwargs(".."), "/cancel"),
        ]:
            assert client.build_request(method, kwargs["url"]).url.raw_path == (
                f"/v2/calls/%2E%2E{suffix}".encode()
            )
