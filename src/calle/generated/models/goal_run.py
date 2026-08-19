from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.goal_run_object import check_goal_run_object
from ..models.goal_run_object import GoalRunObject
from ..models.goal_run_status import check_goal_run_status
from ..models.goal_run_status import GoalRunStatus
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.goal_run_error import GoalRunError
    from ..models.goal_run_result_type_0 import GoalRunResultType0
    from ..models.goal_run_spec_snapshot import GoalRunSpecSnapshot


T = TypeVar("T", bound="GoalRun")


@_attrs_define
class GoalRun:
    """Public projection of one phone-specific execution of a published Goal. A non-null `result`
    is a successfully parsed and persisted object. A non-null `error` means the Run will not
    produce a result. When both are null, continue polling.

        Attributes:
            object_ (GoalRunObject):
            id (str): Public Goal Run identity. Persist this value and use it as `goal_run_id` when polling.
            goal_id (str): Goal identity supplied in the create path.
            run_id (str): Internal execution member exposed for correlation; do not use it in the Goal Run polling path.
            call_id (None | str): Calling call identifier selected for this Goal Run when that trusted fact is available,
                or `null` before a call identifier is persisted or when no identifier is available. This
                is different from the Goal Run `id` and nested `run_id`; it does not expose other provider
                diagnostics and must not be treated as an independent answered-call boolean.
            run_spec (GoalRunSpecSnapshot): Exact immutable RunSpec identity and version pinned by a Goal Run.
            status (GoalRunStatus): Stable telephone execution state. `queued` and `in_progress` are non-terminal;
                `completed`,
                `failed`, and `canceled` are terminal. A completed call can still have `result: null` and
                `error: null` briefly while CALL-E parses and saves the result.
            result (GoalRunResultType0 | None): Parsed result validated against the published result schema and durably
                persisted, or
                `null` while processing or when the Run has an error. Its keys vary by Goal.
            error (GoalRunError | None): Unified execution or result-processing error, or `null`. Branch on `code`; keep
                `message`
                for logs and operators. A non-null error is final and is mutually exclusive with `result`.
            created_at (datetime.datetime): UTC time at which CALL-E durably accepted this Goal Run.
            completed_at (datetime.datetime | None): UTC telephone-execution completion time, or `null` while execution is
                non-terminal.
    """

    object_: GoalRunObject
    id: str
    goal_id: str
    run_id: str
    call_id: None | str
    run_spec: GoalRunSpecSnapshot
    status: GoalRunStatus
    result: GoalRunResultType0 | None
    error: GoalRunError | None
    created_at: datetime.datetime
    completed_at: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        from ..models.goal_run_error import GoalRunError
        from ..models.goal_run_result_type_0 import GoalRunResultType0

        object_: str = self.object_

        id = self.id

        goal_id = self.goal_id

        run_id = self.run_id

        call_id: None | str
        call_id = self.call_id

        run_spec = self.run_spec.to_dict()

        status: str = self.status

        result: dict[str, Any] | None
        if isinstance(self.result, GoalRunResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        error: dict[str, Any] | None
        if isinstance(self.error, GoalRunError):
            error = self.error.to_dict()
        else:
            error = self.error

        created_at = self.created_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "object": object_,
                "id": id,
                "goal_id": goal_id,
                "run_id": run_id,
                "call_id": call_id,
                "run_spec": run_spec,
                "status": status,
                "result": result,
                "error": error,
                "created_at": created_at,
                "completed_at": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal_run_error import GoalRunError
        from ..models.goal_run_result_type_0 import GoalRunResultType0
        from ..models.goal_run_spec_snapshot import GoalRunSpecSnapshot

        d = dict(src_dict)
        object_ = check_goal_run_object(d.pop("object"))

        id = d.pop("id")

        goal_id = d.pop("goal_id")

        run_id = d.pop("run_id")

        def _parse_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_id = _parse_call_id(d.pop("call_id"))

        run_spec = GoalRunSpecSnapshot.from_dict(d.pop("run_spec"))

        status = check_goal_run_status(d.pop("status"))

        def _parse_result(data: object) -> GoalRunResultType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = GoalRunResultType0.from_dict(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GoalRunResultType0 | None, data)

        result = _parse_result(d.pop("result"))

        def _parse_error(data: object) -> GoalRunError | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = GoalRunError.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GoalRunError | None, data)

        error = _parse_error(d.pop("error"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        goal_run = cls(
            object_=object_,
            id=id,
            goal_id=goal_id,
            run_id=run_id,
            call_id=call_id,
            run_spec=run_spec,
            status=status,
            result=result,
            error=error,
            created_at=created_at,
            completed_at=completed_at,
        )

        return goal_run
