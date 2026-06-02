from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.call_policy import CallPolicy
    from ..models.call_recipient import CallRecipient
    from ..models.create_call_request_context import CreateCallRequestContext
    from ..models.create_call_request_metadata import CreateCallRequestMetadata
    from ..models.create_call_request_result_schema import CreateCallRequestResultSchema


T = TypeVar("T", bound="CreateCallRequest")


@_attrs_define
class CreateCallRequest:
    """
    Attributes:
        task (str):
        recipient (CallRecipient):
        result_schema (CreateCallRequestResultSchema):
        context (CreateCallRequestContext | Unset):
        policy (CallPolicy | Unset):
        metadata (CreateCallRequestMetadata | Unset):
        webhook_url (str | Unset):
    """

    task: str
    recipient: CallRecipient
    result_schema: CreateCallRequestResultSchema
    context: CreateCallRequestContext | Unset = UNSET
    policy: CallPolicy | Unset = UNSET
    metadata: CreateCallRequestMetadata | Unset = UNSET
    webhook_url: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        recipient = self.recipient.to_dict()

        result_schema = self.result_schema.to_dict()

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        webhook_url = self.webhook_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "task": task,
                "recipient": recipient,
                "result_schema": result_schema,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context
        if policy is not UNSET:
            field_dict["policy"] = policy
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if webhook_url is not UNSET:
            field_dict["webhook_url"] = webhook_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_policy import CallPolicy
        from ..models.call_recipient import CallRecipient
        from ..models.create_call_request_context import CreateCallRequestContext
        from ..models.create_call_request_metadata import CreateCallRequestMetadata
        from ..models.create_call_request_result_schema import CreateCallRequestResultSchema

        d = dict(src_dict)
        task = d.pop("task")

        recipient = CallRecipient.from_dict(d.pop("recipient"))

        result_schema = CreateCallRequestResultSchema.from_dict(d.pop("result_schema"))

        _context = d.pop("context", UNSET)
        context: CreateCallRequestContext | Unset
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = CreateCallRequestContext.from_dict(_context)

        _policy = d.pop("policy", UNSET)
        policy: CallPolicy | Unset
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = CallPolicy.from_dict(_policy)

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateCallRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateCallRequestMetadata.from_dict(_metadata)

        webhook_url = d.pop("webhook_url", UNSET)

        create_call_request = cls(
            task=task,
            recipient=recipient,
            result_schema=result_schema,
            context=context,
            policy=policy,
            metadata=metadata,
            webhook_url=webhook_url,
        )

        return create_call_request
