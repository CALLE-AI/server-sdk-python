from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.goal_run_status import check_goal_run_status
from ..models.goal_run_status import GoalRunStatus
from typing import cast
from typing import Literal
import datetime

if TYPE_CHECKING:
    from ..models.agentic_call_metadata import AgenticCallMetadata
    from ..models.agentic_call_result_type_0 import AgenticCallResultType0
    from ..models.goal_run_error import GoalRunError


T = TypeVar("T", bound="AgenticCall")


@_attrs_define
class AgenticCall:
    """Persisted one-shot snapshot with the same result/error contract as Goal Run. Continue polling while both are null,
    even when status is completed. An empty result object is ready. Execution completion does not imply business
    success. Terminal webhooks are sent after result or error is ready.

        Attributes:
            id (str):
            object_ (Literal['call']):
            status (GoalRunStatus): Stable telephone execution state. `queued` and `in_progress` are non-terminal;
                `completed`,
                `failed`, and `canceled` are terminal. A completed call can still have `result: null` and
                `error: null` briefly while CALL-E parses and saves the result.
            task (str):
            phone (str):
            region (str):
            locale (str):
            scheduled_at (datetime.datetime | None):
            result (AgenticCallResultType0 | None): Result validated against the submitted result_schema and durably
                persisted, or null while processing or on error.
            error (GoalRunError | None): Unified execution or result-processing error, or `null`. Branch on `code`; keep
                `message`
                for logs and operators. A non-null error is final and is mutually exclusive with `result`.
            metadata (AgenticCallMetadata):
            created_at (datetime.datetime):
            completed_at (datetime.datetime | None): UTC telephone-execution completion time, or `null` while execution is
                non-terminal.
    """

    id: str
    object_: Literal["call"]
    status: GoalRunStatus
    task: str
    phone: str
    region: str
    locale: str
    scheduled_at: datetime.datetime | None
    result: AgenticCallResultType0 | None
    error: GoalRunError | None
    metadata: AgenticCallMetadata
    created_at: datetime.datetime
    completed_at: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        from ..models.agentic_call_result_type_0 import AgenticCallResultType0
        from ..models.goal_run_error import GoalRunError

        id = self.id

        object_ = self.object_

        status: str = self.status

        task = self.task

        phone = self.phone

        region = self.region

        locale = self.locale

        scheduled_at: None | str
        if isinstance(self.scheduled_at, datetime.datetime):
            scheduled_at = self.scheduled_at.isoformat()
        else:
            scheduled_at = self.scheduled_at

        result: dict[str, Any] | None
        if isinstance(self.result, AgenticCallResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        error: dict[str, Any] | None
        if isinstance(self.error, GoalRunError):
            error = self.error.to_dict()
        else:
            error = self.error

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "object": object_,
                "status": status,
                "task": task,
                "phone": phone,
                "region": region,
                "locale": locale,
                "scheduled_at": scheduled_at,
                "result": result,
                "error": error,
                "metadata": metadata,
                "created_at": created_at,
                "completed_at": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agentic_call_metadata import AgenticCallMetadata
        from ..models.agentic_call_result_type_0 import AgenticCallResultType0
        from ..models.goal_run_error import GoalRunError

        d = dict(src_dict)
        id = d.pop("id")

        object_ = cast(Literal["call"], d.pop("object"))
        if object_ != "call":
            raise ValueError(f"object must match const 'call', got '{object_}'")

        status = check_goal_run_status(d.pop("status"))

        task = d.pop("task")

        phone = d.pop("phone")

        region = d.pop("region")

        locale = d.pop("locale")

        def _parse_scheduled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_at_type_0 = datetime.datetime.fromisoformat(data)

                return scheduled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        scheduled_at = _parse_scheduled_at(d.pop("scheduled_at"))

        def _parse_result(data: object) -> AgenticCallResultType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = AgenticCallResultType0.from_dict(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgenticCallResultType0 | None, data)

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

        metadata = AgenticCallMetadata.from_dict(d.pop("metadata"))

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

        agentic_call = cls(
            id=id,
            object_=object_,
            status=status,
            task=task,
            phone=phone,
            region=region,
            locale=locale,
            scheduled_at=scheduled_at,
            result=result,
            error=error,
            metadata=metadata,
            created_at=created_at,
            completed_at=completed_at,
        )

        return agentic_call
