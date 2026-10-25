import json
import runpy
from collections.abc import Callable
from pathlib import Path
from typing import cast

import httpx
import pytest
import respx

from calle import CalleConnectionError


example = runpy.run_path(str(Path(__file__).parent.parent / "examples" / "create_and_wait.py"))
main = cast(Callable[[], None], example["main"])


@respx.mock
def test_call_example_resumes_without_creating_another_call(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CALLE_BASE_URL", "https://api.heycall-e.com")
    monkeypatch.setattr("sys.argv", ["create_and_wait.py"])
    created = {"id": "call_example", "call_id": "billing_example", "result_status": "pending"}
    completed = {**created, "result_status": "available", "result": {"can_attend": "yes"}}
    create = respx.post("https://api.heycall-e.com/v2/calls").respond(202, json=created)
    read = respx.get("https://api.heycall-e.com/v2/calls/call_example").mock(
        side_effect=[httpx.ConnectError("Offline polling failure."), httpx.Response(200, json=completed)]
    )

    with pytest.raises(CalleConnectionError) as exc_info:
        main()

    assert exc_info.value.call_id == "call_example"
    output = capsys.readouterr()
    assert "--call-id call_example" in output.err
    assert output.out == ""
    monkeypatch.setattr("sys.argv", ["create_and_wait.py", "--call-id", exc_info.value.call_id])
    main()

    assert json.loads(capsys.readouterr().out) == completed
    assert create.call_count == 1
    assert read.call_count == 2
    assert [request.method for request, _ in respx.calls] == ["POST", "GET", "GET"]


@respx.mock
def test_call_example_does_not_invent_an_id_after_create_failure(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CALLE_BASE_URL", "https://api.heycall-e.com")
    monkeypatch.setattr("sys.argv", ["create_and_wait.py"])
    create = respx.post("https://api.heycall-e.com/v2/calls").mock(
        side_effect=httpx.ConnectError("Offline creation failure.")
    )

    with pytest.raises(CalleConnectionError) as exc_info:
        main()

    assert exc_info.value.call_id is None
    output = capsys.readouterr()
    assert "same request and idempotency key" in output.err
    assert "--call-id" not in output.err
    assert output.out == ""
    assert create.call_count == 1
    assert len(respx.calls) == 1


@pytest.mark.parametrize("call_id", ["", " "])
@respx.mock
def test_call_example_rejects_empty_resume_id(monkeypatch, call_id) -> None:
    monkeypatch.setattr("sys.argv", ["create_and_wait.py", "--call-id", call_id])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert len(respx.calls) == 0
