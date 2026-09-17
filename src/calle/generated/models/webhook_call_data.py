from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.call_status import CallStatus
from ..models.call_status import check_call_status
from ..models.webhook_call_data_object import check_webhook_call_data_object
from ..models.webhook_call_data_object import WebhookCallDataObject
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.call_task_recipient import CallTaskRecipient
    from ..models.completion_confidence import CompletionConfidence
    from ..models.webhook_call_data_metadata import WebhookCallDataMetadata
    from ..models.webhook_call_data_structured_result_type_0 import (
        WebhookCallDataStructuredResultType0,
    )


T = TypeVar("T", bound="WebhookCallData")


@_attrs_define
class WebhookCallData:
    """
    Attributes:
        id (str): Public CALL-E call task identifier. Store this id to fetch state, list events, and correlate webhooks.
        object_ (WebhookCallDataObject): Always `call_task` for call task responses.
        status (CallStatus): Current lifecycle state of a CALL-E call. `in_progress` includes post-call result
            finalization; terminal states are published only after the post-call outcome is available.
        task (str): Original task instruction submitted when the call task was created.
        recipients (list[CallTaskRecipient]): Recipient states for this call task.
        structured_result (None | WebhookCallDataStructuredResultType0): Schema-valid structured result object extracted
            for the whole call task using `result_schema`.

            `null` means CALL-E could not produce a schema-valid task-level result from the terminal call evidence, or no
            `result_schema` was provided. Check recipient-level `structured_result` when you use `recipient_result_schema`
            for batch calls.
        summary (None | str): Short human-readable summary of the call task outcome. `null` while the call task is still
            running or when no useful summary is available.
        task_completed (bool | None): Post-summary judgment for whether the task reached a clear end state for the user.
            `null` until CALL-E has a terminal post-summary outcome.
        completion_confidence (CompletionConfidence | None): Confidence for `task_completed`. `null` until CALL-E has a
            terminal post-summary outcome.
        evidence (list[str]): Short evidence items supporting the post-summary task outcome. Empty until CALL-E has
            terminal evidence.
        metadata (WebhookCallDataMetadata): Caller-owned metadata submitted on the create call request.
        failure_code (None | str): Machine-readable failure reason when `status` is `failed`; otherwise `null`.
        failure_message (None | str): Human-readable failure explanation when `status` is `failed`; otherwise `null`.
        created_at (datetime.datetime): ISO 8601 timestamp when CALL-E accepted the call request.
        completed_at (datetime.datetime | None): ISO 8601 timestamp when the complete terminal call result was
            published. `null` while queued or in progress.
    """

    id: str
    object_: WebhookCallDataObject
    status: CallStatus
    task: str
    recipients: list[CallTaskRecipient]
    structured_result: None | WebhookCallDataStructuredResultType0
    summary: None | str
    task_completed: bool | None
    completion_confidence: CompletionConfidence | None
    evidence: list[str]
    metadata: WebhookCallDataMetadata
    failure_code: None | str
    failure_message: None | str
    created_at: datetime.datetime
    completed_at: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        from ..models.completion_confidence import CompletionConfidence
        from ..models.webhook_call_data_structured_result_type_0 import (
            WebhookCallDataStructuredResultType0,
        )

        id = self.id

        object_: str = self.object_

        status: str = self.status

        task = self.task

        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item = recipients_item_data.to_dict()
            recipients.append(recipients_item)

        structured_result: dict[str, Any] | None
        if isinstance(self.structured_result, WebhookCallDataStructuredResultType0):
            structured_result = self.structured_result.to_dict()
        else:
            structured_result = self.structured_result

        summary: None | str
        summary = self.summary

        task_completed: bool | None
        task_completed = self.task_completed

        completion_confidence: dict[str, Any] | None
        if isinstance(self.completion_confidence, CompletionConfidence):
            completion_confidence = self.completion_confidence.to_dict()
        else:
            completion_confidence = self.completion_confidence

        evidence = self.evidence

        metadata = self.metadata.to_dict()

        failure_code: None | str
        failure_code = self.failure_code

        failure_message: None | str
        failure_message = self.failure_message

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
                "recipients": recipients,
                "structured_result": structured_result,
                "summary": summary,
                "task_completed": task_completed,
                "completion_confidence": completion_confidence,
                "evidence": evidence,
                "metadata": metadata,
                "failure_code": failure_code,
                "failure_message": failure_message,
                "created_at": created_at,
                "completed_at": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_task_recipient import CallTaskRecipient
        from ..models.completion_confidence import CompletionConfidence
        from ..models.webhook_call_data_metadata import WebhookCallDataMetadata
        from ..models.webhook_call_data_structured_result_type_0 import (
            WebhookCallDataStructuredResultType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        object_ = check_webhook_call_data_object(d.pop("object"))

        status = check_call_status(d.pop("status"))

        task = d.pop("task")

        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in _recipients:
            recipients_item = CallTaskRecipient.from_dict(recipients_item_data)

            recipients.append(recipients_item)

        def _parse_structured_result(
            data: object,
        ) -> None | WebhookCallDataStructuredResultType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_result_type_0 = (
                    WebhookCallDataStructuredResultType0.from_dict(data)
                )

                return structured_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WebhookCallDataStructuredResultType0, data)

        structured_result = _parse_structured_result(d.pop("structured_result"))

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        def _parse_task_completed(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        task_completed = _parse_task_completed(d.pop("task_completed"))

        def _parse_completion_confidence(data: object) -> CompletionConfidence | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                completion_confidence_type_0 = CompletionConfidence.from_dict(data)

                return completion_confidence_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CompletionConfidence | None, data)

        completion_confidence = _parse_completion_confidence(
            d.pop("completion_confidence")
        )

        evidence = cast(list[str], d.pop("evidence"))

        metadata = WebhookCallDataMetadata.from_dict(d.pop("metadata"))

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

        webhook_call_data = cls(
            id=id,
            object_=object_,
            status=status,
            task=task,
            recipients=recipients,
            structured_result=structured_result,
            summary=summary,
            task_completed=task_completed,
            completion_confidence=completion_confidence,
            evidence=evidence,
            metadata=metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            created_at=created_at,
            completed_at=completed_at,
        )

        return webhook_call_data
