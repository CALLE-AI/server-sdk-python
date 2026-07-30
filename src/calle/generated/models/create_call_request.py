from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.call_task_recipient_request import CallTaskRecipientRequest
    from ..models.create_call_request_metadata import CreateCallRequestMetadata
    from ..models.create_call_request_recipient_result_schema_type_0 import (
        CreateCallRequestRecipientResultSchemaType0,
    )
    from ..models.create_call_request_result_schema_type_0 import (
        CreateCallRequestResultSchemaType0,
    )


T = TypeVar("T", bound="CreateCallRequest")


@_attrs_define
class CreateCallRequest:
    """
    Attributes:
        task (str): Natural-language instruction for the call task. Include the goal, relevant details the voice agent
            should know, and the exact information you want collected.
        recipients (list[CallTaskRecipientRequest] | None | Unset): Optional explicit recipients for this call task.
            Omit it when the task text already contains the phone targets CALL-E should use.
        result_schema (CreateCallRequestResultSchemaType0 | None | Unset): Optional JSON Schema object that defines the
            structured result CALL-E should extract for the whole call task.

            CALL-E passes the schema, including field `description` values, to the extraction model after the call reaches a
            terminal state. Use descriptions to explain field meaning and enum selection logic, for example: "Use strong
            when the prospect asks about pricing, demos, or next steps."

            Descriptions guide extraction but are not hard validation rules. Hard validation comes from `type`, `required`,
            `enum`, and `additionalProperties`.

            Supported schema features are `type`, `properties`, `required`, `enum`, nested `object` fields, simple
            `array.items`, `description`, and `additionalProperties: false`. Unsupported features include `$ref`, `oneOf`,
            `anyOf`, `allOf`, recursive schemas, complex format validation, and `additionalProperties: true`.

            Prefer string enums over booleans for business decisions that may be unclear, and include an `unknown` enum
            value when the call may not provide enough evidence.
        recipient_result_schema (CreateCallRequestRecipientResultSchemaType0 | None | Unset): Optional JSON Schema
            object that defines the structured result CALL-E should extract independently for each recipient.

            This is useful for batch calls where each recipient needs their own outcome, such as `can_attend`, `confirmed`,
            `requested_callback`, or `interest_level`.

            Do not use reserved recipient response field names such as `summary`, `status`, `transcript`, `call_id`, or
            timing fields as custom result fields. Use names such as `customer_summary`, `notes`, or `reason` instead.

            Field `description` values are passed to the extraction model and should explain how enum values should be
            selected. Descriptions guide extraction but are not hard validation rules. Hard validation comes from `type`,
            `required`, `enum`, and `additionalProperties`.

            Object schemas are strict by default. Fields not declared in `properties` are rejected, and unsupported or
            invalid recipient results are returned as `null`.
        metadata (CreateCallRequestMetadata | Unset): Optional caller-owned metadata echoed on the call and webhook
            payloads. Use this for workflow ids, tenant ids, or internal correlation keys.
        webhook_url (str | Unset): Optional per-request HTTPS webhook URL. When provided, CALL-E sends terminal call
            events to this URL in addition to project-level webhook delivery.
    """

    task: str
    recipients: list[CallTaskRecipientRequest] | None | Unset = UNSET
    result_schema: CreateCallRequestResultSchemaType0 | None | Unset = UNSET
    recipient_result_schema: (
        CreateCallRequestRecipientResultSchemaType0 | None | Unset
    ) = UNSET
    metadata: CreateCallRequestMetadata | Unset = UNSET
    webhook_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_call_request_recipient_result_schema_type_0 import (
            CreateCallRequestRecipientResultSchemaType0,
        )
        from ..models.create_call_request_result_schema_type_0 import (
            CreateCallRequestResultSchemaType0,
        )

        task = self.task

        recipients: list[dict[str, Any]] | None | Unset
        if isinstance(self.recipients, Unset):
            recipients = UNSET
        elif isinstance(self.recipients, list):
            recipients = []
            for recipients_type_0_item_data in self.recipients:
                recipients_type_0_item = recipients_type_0_item_data.to_dict()
                recipients.append(recipients_type_0_item)

        else:
            recipients = self.recipients

        result_schema: dict[str, Any] | None | Unset
        if isinstance(self.result_schema, Unset):
            result_schema = UNSET
        elif isinstance(self.result_schema, CreateCallRequestResultSchemaType0):
            result_schema = self.result_schema.to_dict()
        else:
            result_schema = self.result_schema

        recipient_result_schema: dict[str, Any] | None | Unset
        if isinstance(self.recipient_result_schema, Unset):
            recipient_result_schema = UNSET
        elif isinstance(
            self.recipient_result_schema, CreateCallRequestRecipientResultSchemaType0
        ):
            recipient_result_schema = self.recipient_result_schema.to_dict()
        else:
            recipient_result_schema = self.recipient_result_schema

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        webhook_url = self.webhook_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "task": task,
            }
        )
        if recipients is not UNSET:
            field_dict["recipients"] = recipients
        if result_schema is not UNSET:
            field_dict["result_schema"] = result_schema
        if recipient_result_schema is not UNSET:
            field_dict["recipient_result_schema"] = recipient_result_schema
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if webhook_url is not UNSET:
            field_dict["webhook_url"] = webhook_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_task_recipient_request import CallTaskRecipientRequest
        from ..models.create_call_request_metadata import CreateCallRequestMetadata
        from ..models.create_call_request_recipient_result_schema_type_0 import (
            CreateCallRequestRecipientResultSchemaType0,
        )
        from ..models.create_call_request_result_schema_type_0 import (
            CreateCallRequestResultSchemaType0,
        )

        d = dict(src_dict)
        task = d.pop("task")

        def _parse_recipients(
            data: object,
        ) -> list[CallTaskRecipientRequest] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                recipients_type_0 = []
                _recipients_type_0 = data
                for recipients_type_0_item_data in _recipients_type_0:
                    recipients_type_0_item = CallTaskRecipientRequest.from_dict(
                        recipients_type_0_item_data
                    )

                    recipients_type_0.append(recipients_type_0_item)

                return recipients_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CallTaskRecipientRequest] | None | Unset, data)

        recipients = _parse_recipients(d.pop("recipients", UNSET))

        def _parse_result_schema(
            data: object,
        ) -> CreateCallRequestResultSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_schema_type_0 = CreateCallRequestResultSchemaType0.from_dict(
                    data
                )

                return result_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateCallRequestResultSchemaType0 | None | Unset, data)

        result_schema = _parse_result_schema(d.pop("result_schema", UNSET))

        def _parse_recipient_result_schema(
            data: object,
        ) -> CreateCallRequestRecipientResultSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recipient_result_schema_type_0 = (
                    CreateCallRequestRecipientResultSchemaType0.from_dict(data)
                )

                return recipient_result_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CreateCallRequestRecipientResultSchemaType0 | None | Unset, data
            )

        recipient_result_schema = _parse_recipient_result_schema(
            d.pop("recipient_result_schema", UNSET)
        )

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateCallRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateCallRequestMetadata.from_dict(_metadata)

        webhook_url = d.pop("webhook_url", UNSET)

        create_call_request = cls(
            task=task,
            recipients=recipients,
            result_schema=result_schema,
            recipient_result_schema=recipient_result_schema,
            metadata=metadata,
            webhook_url=webhook_url,
        )

        return create_call_request
