from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.recipient_status import check_recipient_status
from ..models.recipient_status import RecipientStatus
from typing import cast

if TYPE_CHECKING:
    from ..models.call_task_attempt import CallTaskAttempt
    from ..models.call_task_recipient_structured_result_type_0 import (
        CallTaskRecipientStructuredResultType0,
    )


T = TypeVar("T", bound="CallTaskRecipient")


@_attrs_define
class CallTaskRecipient:
    """
    Attributes:
        id (str): Stable recipient identifier within the call task.
        phones (list[str]): Phone numbers associated with this recipient.
        locale (None | str): BCP 47 locale hint used for this recipient when available.
        region (None | str): Country or region code used for routing and compliance checks when available.
        status (RecipientStatus): Current lifecycle state for one recipient in a call task.
        structured_result (CallTaskRecipientStructuredResultType0 | None): Schema-valid structured result object
            extracted for this recipient using `recipient_result_schema`.

            `null` means CALL-E could not produce a schema-valid result for this recipient from the terminal call evidence,
            or no `recipient_result_schema` was provided.
        summary (None | str): Short human-readable summary for this recipient. `null` while the recipient is still
            running or when no useful summary is available.
        attempts (list[CallTaskAttempt]): Outbound dial attempts made for this recipient.
    """

    id: str
    phones: list[str]
    locale: None | str
    region: None | str
    status: RecipientStatus
    structured_result: CallTaskRecipientStructuredResultType0 | None
    summary: None | str
    attempts: list[CallTaskAttempt]

    def to_dict(self) -> dict[str, Any]:
        from ..models.call_task_recipient_structured_result_type_0 import (
            CallTaskRecipientStructuredResultType0,
        )

        id = self.id

        phones = self.phones

        locale: None | str
        locale = self.locale

        region: None | str
        region = self.region

        status: str = self.status

        structured_result: dict[str, Any] | None
        if isinstance(self.structured_result, CallTaskRecipientStructuredResultType0):
            structured_result = self.structured_result.to_dict()
        else:
            structured_result = self.structured_result

        summary: None | str
        summary = self.summary

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "phones": phones,
                "locale": locale,
                "region": region,
                "status": status,
                "structured_result": structured_result,
                "summary": summary,
                "attempts": attempts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_task_attempt import CallTaskAttempt
        from ..models.call_task_recipient_structured_result_type_0 import (
            CallTaskRecipientStructuredResultType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        phones = cast(list[str], d.pop("phones"))

        def _parse_locale(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        locale = _parse_locale(d.pop("locale"))

        def _parse_region(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        region = _parse_region(d.pop("region"))

        status = check_recipient_status(d.pop("status"))

        def _parse_structured_result(
            data: object,
        ) -> CallTaskRecipientStructuredResultType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_result_type_0 = (
                    CallTaskRecipientStructuredResultType0.from_dict(data)
                )

                return structured_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CallTaskRecipientStructuredResultType0 | None, data)

        structured_result = _parse_structured_result(d.pop("structured_result"))

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = CallTaskAttempt.from_dict(attempts_item_data)

            attempts.append(attempts_item)

        call_task_recipient = cls(
            id=id,
            phones=phones,
            locale=locale,
            region=region,
            status=status,
            structured_result=structured_result,
            summary=summary,
            attempts=attempts,
        )

        return call_task_recipient
