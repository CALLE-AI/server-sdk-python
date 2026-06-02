from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.call_status import CallStatus, check_call_status
from ..models.webhook_call_data_object import WebhookCallDataObject, check_webhook_call_data_object
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.result_validation import ResultValidation
    from ..models.webhook_call_data_metadata import WebhookCallDataMetadata
    from ..models.webhook_call_data_structured_result_type_0 import WebhookCallDataStructuredResultType0


T = TypeVar("T", bound="WebhookCallData")


@_attrs_define
class WebhookCallData:
    """
    Attributes:
        object_ (WebhookCallDataObject):
        id (str):
        status (CallStatus):
        structured_result (None | Unset | WebhookCallDataStructuredResultType0):
        result_validation (None | ResultValidation | Unset):
        summary (None | str | Unset):
        metadata (WebhookCallDataMetadata | Unset):
        failure_code (None | str | Unset):
        failure_message (None | str | Unset):
    """

    object_: WebhookCallDataObject
    id: str
    status: CallStatus
    structured_result: None | Unset | WebhookCallDataStructuredResultType0 = UNSET
    result_validation: None | ResultValidation | Unset = UNSET
    summary: None | str | Unset = UNSET
    metadata: WebhookCallDataMetadata | Unset = UNSET
    failure_code: None | str | Unset = UNSET
    failure_message: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.result_validation import ResultValidation
        from ..models.webhook_call_data_structured_result_type_0 import WebhookCallDataStructuredResultType0

        object_: str = self.object_

        id = self.id

        status: str = self.status

        structured_result: dict[str, Any] | None | Unset
        if isinstance(self.structured_result, Unset):
            structured_result = UNSET
        elif isinstance(self.structured_result, WebhookCallDataStructuredResultType0):
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

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "object": object_,
                "id": id,
                "status": status,
            }
        )
        if structured_result is not UNSET:
            field_dict["structured_result"] = structured_result
        if result_validation is not UNSET:
            field_dict["result_validation"] = result_validation
        if summary is not UNSET:
            field_dict["summary"] = summary
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.result_validation import ResultValidation
        from ..models.webhook_call_data_metadata import WebhookCallDataMetadata
        from ..models.webhook_call_data_structured_result_type_0 import WebhookCallDataStructuredResultType0

        d = dict(src_dict)
        object_ = check_webhook_call_data_object(d.pop("object"))

        id = d.pop("id")

        status = check_call_status(d.pop("status"))

        def _parse_structured_result(data: object) -> None | Unset | WebhookCallDataStructuredResultType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_result_type_0 = WebhookCallDataStructuredResultType0.from_dict(data)

                return structured_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WebhookCallDataStructuredResultType0, data)

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

        _metadata = d.pop("metadata", UNSET)
        metadata: WebhookCallDataMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = WebhookCallDataMetadata.from_dict(_metadata)

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

        webhook_call_data = cls(
            object_=object_,
            id=id,
            status=status,
            structured_result=structured_result,
            result_validation=result_validation,
            summary=summary,
            metadata=metadata,
            failure_code=failure_code,
            failure_message=failure_message,
        )

        return webhook_call_data
