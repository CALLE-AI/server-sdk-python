from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.business_result_status import BusinessResultStatus
from ..models.business_result_status import check_business_result_status
from ..models.call_outcome_type_1 import CallOutcomeType1
from ..models.call_outcome_type_1 import check_call_outcome_type_1
from ..models.call_outcome_type_2_type_1 import CallOutcomeType2Type1
from ..models.call_outcome_type_2_type_1 import check_call_outcome_type_2_type_1
from ..models.call_outcome_type_3_type_1 import CallOutcomeType3Type1
from ..models.call_outcome_type_3_type_1 import check_call_outcome_type_3_type_1
from ..models.goal_run_status import check_goal_run_status
from ..models.goal_run_status import GoalRunStatus
from typing import cast
from typing import Literal
import datetime

if TYPE_CHECKING:
    from ..models.agentic_call_metadata import AgenticCallMetadata
    from ..models.agentic_call_result_type_0 import AgenticCallResultType0
    from ..models.call_transcript_turn import CallTranscriptTurn
    from ..models.goal_run_error import GoalRunError


T = TypeVar("T", bound="AgenticCall")


@_attrs_define
class AgenticCall:
    """Persisted one-shot snapshot sharing execution, call_outcome and result_status with Goal Run. Poll only while
    result_status is pending. Completed execution does not imply business success. Terminal webhooks are sent when
    result_status is no longer pending, including unavailable results.

        Attributes:
            id (str): API Call resource ID. Use this ID for API paths and event correlation, not the telephone ID in
                Billing.
            call_id (None | str): Telephone call ID shown in Billing, using the same identity as Goal Run call_id. Always
                present; null until recorded, including cancellation before dialing. Independent of business result
                availability. Does not indicate whether charges have settled. Use id, not this field, for API paths.
            object_ (Literal['call']):
            status (GoalRunStatus): Stable execution state. No-answer, busy and declined calls complete execution normally.
                Technical execution failures are failed; explicit cancellation is canceled. Completed execution
                may still have result_status=pending while its business result is being processed.
            call_outcome (CallOutcomeType1 | CallOutcomeType2Type1 | CallOutcomeType3Type1 | None): Reported telephone
                outcome, separate from business success and billing connection evidence. Null before a telephone outcome is
                known or when execution is canceled or fails technically.
            result_status (BusinessResultStatus): Pending means keep polling. Available includes an empty result object.
                Unavailable means no schema-valid business result could be produced; inspect error for technical failures. Not
                applicable is used for cancellation and technical execution failure.
            transcript (list[CallTranscriptTurn]): Recorded conversation turns in order, independent of the business result.
                Always present; empty before terminal execution or when no transcript is available. Never generated from
                result_schema.
            task (str):
            phone (str):
            region (str):
            locale (str):
            result (AgenticCallResultType0 | None): Result validated against result_schema and durably persisted. Null while
                pending, unavailable, not applicable, or on a technical error. Explicit schema-valid task fallbacks are
                preserved.
            error (GoalRunError | None): Technical execution or result-processing error, or null. No-answer, busy, declined,
                cancellation and insufficient business evidence do not populate error.
            metadata (AgenticCallMetadata):
            created_at (datetime.datetime):
            completed_at (datetime.datetime | None): UTC telephone-execution completion time, or `null` while execution is
                non-terminal.
    """

    id: str
    call_id: None | str
    object_: Literal["call"]
    status: GoalRunStatus
    call_outcome: (
        CallOutcomeType1 | CallOutcomeType2Type1 | CallOutcomeType3Type1 | None
    )
    result_status: BusinessResultStatus
    transcript: list[CallTranscriptTurn]
    task: str
    phone: str
    region: str
    locale: str
    result: AgenticCallResultType0 | None
    error: GoalRunError | None
    metadata: AgenticCallMetadata
    created_at: datetime.datetime
    completed_at: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        from ..models.agentic_call_result_type_0 import AgenticCallResultType0
        from ..models.goal_run_error import GoalRunError

        id = self.id

        call_id: None | str
        call_id = self.call_id

        object_ = self.object_

        status: str = self.status

        call_outcome: None | str
        if isinstance(self.call_outcome, str):
            call_outcome = self.call_outcome
        elif isinstance(self.call_outcome, str):
            call_outcome = self.call_outcome
        elif isinstance(self.call_outcome, str):
            call_outcome = self.call_outcome
        else:
            call_outcome = self.call_outcome

        result_status: str = self.result_status

        transcript = []
        for transcript_item_data in self.transcript:
            transcript_item = transcript_item_data.to_dict()
            transcript.append(transcript_item)

        task = self.task

        phone = self.phone

        region = self.region

        locale = self.locale

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
                "call_id": call_id,
                "object": object_,
                "status": status,
                "call_outcome": call_outcome,
                "result_status": result_status,
                "transcript": transcript,
                "task": task,
                "phone": phone,
                "region": region,
                "locale": locale,
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
        from ..models.call_transcript_turn import CallTranscriptTurn
        from ..models.goal_run_error import GoalRunError

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_id = _parse_call_id(d.pop("call_id"))

        object_ = cast(Literal["call"], d.pop("object"))
        if object_ != "call":
            raise ValueError(f"object must match const 'call', got '{object_}'")

        status = check_goal_run_status(d.pop("status"))

        def _parse_call_outcome(
            data: object,
        ) -> CallOutcomeType1 | CallOutcomeType2Type1 | CallOutcomeType3Type1 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_call_outcome_type_1 = check_call_outcome_type_1(data)

                return componentsschemas_call_outcome_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_call_outcome_type_2_type_1 = (
                    check_call_outcome_type_2_type_1(data)
                )

                return componentsschemas_call_outcome_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_call_outcome_type_3_type_1 = (
                    check_call_outcome_type_3_type_1(data)
                )

                return componentsschemas_call_outcome_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CallOutcomeType1 | CallOutcomeType2Type1 | CallOutcomeType3Type1 | None,
                data,
            )

        call_outcome = _parse_call_outcome(d.pop("call_outcome"))

        result_status = check_business_result_status(d.pop("result_status"))

        transcript = []
        _transcript = d.pop("transcript")
        for transcript_item_data in _transcript:
            transcript_item = CallTranscriptTurn.from_dict(transcript_item_data)

            transcript.append(transcript_item)

        task = d.pop("task")

        phone = d.pop("phone")

        region = d.pop("region")

        locale = d.pop("locale")

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
            call_id=call_id,
            object_=object_,
            status=status,
            call_outcome=call_outcome,
            result_status=result_status,
            transcript=transcript,
            task=task,
            phone=phone,
            region=region,
            locale=locale,
            result=result,
            error=error,
            metadata=metadata,
            created_at=created_at,
            completed_at=completed_at,
        )

        return agentic_call
