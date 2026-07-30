from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.attempt_status import AttemptStatus
from ..models.attempt_status import check_attempt_status
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.call_transcript_turn import CallTranscriptTurn


T = TypeVar("T", bound="CallTaskAttempt")


@_attrs_define
class CallTaskAttempt:
    """
    Attributes:
        id (str): Stable outbound attempt identifier.
        phone (str): Phone number dialed by this attempt.
        status (AttemptStatus): Current lifecycle state for one outbound dial attempt.
        started_at (datetime.datetime | None): ISO 8601 timestamp when this attempt started dialing. `null` before
            dialing begins.
        completed_at (datetime.datetime | None): ISO 8601 timestamp when this attempt reached a terminal state. `null`
            while queued, dialing, or in progress.
        summary (None | str): Human-readable summary for this attempt. `null` when no attempt-level summary is
            available.
        transcript_turns (list[CallTranscriptTurn]): Structured transcript turns for this attempt. Empty when no
            transcript is available.
        provider_call_id (None | str): Provider call identifier for support correlation when available.
        failure_code (None | str): Machine-readable failure reason when this attempt failed.
        failure_message (None | str): Human-readable failure explanation when this attempt failed.
    """

    id: str
    phone: str
    status: AttemptStatus
    started_at: datetime.datetime | None
    completed_at: datetime.datetime | None
    summary: None | str
    transcript_turns: list[CallTranscriptTurn]
    provider_call_id: None | str
    failure_code: None | str
    failure_message: None | str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        phone = self.phone

        status: str = self.status

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        summary: None | str
        summary = self.summary

        transcript_turns = []
        for transcript_turns_item_data in self.transcript_turns:
            transcript_turns_item = transcript_turns_item_data.to_dict()
            transcript_turns.append(transcript_turns_item)

        provider_call_id: None | str
        provider_call_id = self.provider_call_id

        failure_code: None | str
        failure_code = self.failure_code

        failure_message: None | str
        failure_message = self.failure_message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "phone": phone,
                "status": status,
                "started_at": started_at,
                "completed_at": completed_at,
                "summary": summary,
                "transcript_turns": transcript_turns,
                "provider_call_id": provider_call_id,
                "failure_code": failure_code,
                "failure_message": failure_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_transcript_turn import CallTranscriptTurn

        d = dict(src_dict)
        id = d.pop("id")

        phone = d.pop("phone")

        status = check_attempt_status(d.pop("status"))

        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = datetime.datetime.fromisoformat(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("started_at"))

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

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        transcript_turns = []
        _transcript_turns = d.pop("transcript_turns")
        for transcript_turns_item_data in _transcript_turns:
            transcript_turns_item = CallTranscriptTurn.from_dict(
                transcript_turns_item_data
            )

            transcript_turns.append(transcript_turns_item)

        def _parse_provider_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        provider_call_id = _parse_provider_call_id(d.pop("provider_call_id"))

        def _parse_failure_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_code = _parse_failure_code(d.pop("failure_code"))

        def _parse_failure_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_message = _parse_failure_message(d.pop("failure_message"))

        call_task_attempt = cls(
            id=id,
            phone=phone,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            summary=summary,
            transcript_turns=transcript_turns,
            provider_call_id=provider_call_id,
            failure_code=failure_code,
            failure_message=failure_message,
        )

        return call_task_attempt
