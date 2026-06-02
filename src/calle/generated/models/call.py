from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.call_status import CallStatus, check_call_status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_metadata import CallMetadata
    from ..models.call_recipient import CallRecipient
    from ..models.call_structured_result_type_0 import CallStructuredResultType0
    from ..models.result_validation import ResultValidation


T = TypeVar("T", bound="Call")


@_attrs_define
class Call:
    """
    Attributes:
        id (str):
        status (CallStatus):
        task (str):
        recipient (CallRecipient):
        metadata (CallMetadata):
        created_at (datetime.datetime):
        structured_result (CallStructuredResultType0 | None | Unset):
        result_validation (None | ResultValidation | Unset):
        summary (None | str | Unset):
        transcript (None | str | Unset):
        failure_code (None | str | Unset):
        failure_message (None | str | Unset):
        completed_at (datetime.datetime | None | Unset):
    """

    id: str
    status: CallStatus
    task: str
    recipient: CallRecipient
    metadata: CallMetadata
    created_at: datetime.datetime
    structured_result: CallStructuredResultType0 | None | Unset = UNSET
    result_validation: None | ResultValidation | Unset = UNSET
    summary: None | str | Unset = UNSET
    transcript: None | str | Unset = UNSET
    failure_code: None | str | Unset = UNSET
    failure_message: None | str | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_structured_result_type_0 import CallStructuredResultType0
        from ..models.result_validation import ResultValidation

        id = self.id

        status: str = self.status

        task = self.task

        recipient = self.recipient.to_dict()

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        structured_result: dict[str, Any] | None | Unset
        if isinstance(self.structured_result, Unset):
            structured_result = UNSET
        elif isinstance(self.structured_result, CallStructuredResultType0):
            structured_result = self.structured_result.to_dict()
        else:
            structured_result = self.structured_result

        result_validation: dict[str, Any] | None | Unset
        if isinstance(self.result_validation, Unset):
            result_validation = UNSET
        elif isinstance(self.result_validation, ResultValidation):
            result_validation = self.result_validation.to_dict()
        else:
            result_validation = self.result_validation

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        transcript: None | str | Unset
        if isinstance(self.transcript, Unset):
            transcript = UNSET
        else:
            transcript = self.transcript

        failure_code: None | str | Unset
        if isinstance(self.failure_code, Unset):
            failure_code = UNSET
        else:
            failure_code = self.failure_code

        failure_message: None | str | Unset
        if isinstance(self.failure_message, Unset):
            failure_message = UNSET
        else:
            failure_message = self.failure_message

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "status": status,
                "task": task,
                "recipient": recipient,
                "metadata": metadata,
                "created_at": created_at,
            }
        )
        if structured_result is not UNSET:
            field_dict["structured_result"] = structured_result
        if result_validation is not UNSET:
            field_dict["result_validation"] = result_validation
        if summary is not UNSET:
            field_dict["summary"] = summary
        if transcript is not UNSET:
            field_dict["transcript"] = transcript
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_metadata import CallMetadata
        from ..models.call_recipient import CallRecipient
        from ..models.call_structured_result_type_0 import CallStructuredResultType0
        from ..models.result_validation import ResultValidation

        d = dict(src_dict)
        id = d.pop("id")

        status = check_call_status(d.pop("status"))

        task = d.pop("task")

        recipient = CallRecipient.from_dict(d.pop("recipient"))

        metadata = CallMetadata.from_dict(d.pop("metadata"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_structured_result(data: object) -> CallStructuredResultType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_result_type_0 = CallStructuredResultType0.from_dict(data)

                return structured_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CallStructuredResultType0 | None | Unset, data)

        structured_result = _parse_structured_result(d.pop("structured_result", UNSET))

        def _parse_result_validation(data: object) -> None | ResultValidation | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_validation_type_0 = ResultValidation.from_dict(data)

                return result_validation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResultValidation | Unset, data)

        result_validation = _parse_result_validation(d.pop("result_validation", UNSET))

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_transcript(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        transcript = _parse_transcript(d.pop("transcript", UNSET))

        def _parse_failure_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        failure_code = _parse_failure_code(d.pop("failure_code", UNSET))

        def _parse_failure_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        failure_message = _parse_failure_message(d.pop("failure_message", UNSET))

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        call = cls(
            id=id,
            status=status,
            task=task,
            recipient=recipient,
            metadata=metadata,
            created_at=created_at,
            structured_result=structured_result,
            result_validation=result_validation,
            summary=summary,
            transcript=transcript,
            failure_code=failure_code,
            failure_message=failure_message,
            completed_at=completed_at,
        )

        return call
