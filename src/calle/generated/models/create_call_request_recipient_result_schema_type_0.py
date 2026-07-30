from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="CreateCallRequestRecipientResultSchemaType0")


@_attrs_define
class CreateCallRequestRecipientResultSchemaType0:
    """Optional JSON Schema object that defines the structured result CALL-E should extract independently for each
    recipient.

    This is useful for batch calls where each recipient needs their own outcome, such as `can_attend`, `confirmed`,
    `requested_callback`, or `interest_level`.

    Do not use reserved recipient response field names such as `summary`, `status`, `transcript`, `call_id`, or timing
    fields as custom result fields. Use names such as `customer_summary`, `notes`, or `reason` instead.

    Field `description` values are passed to the extraction model and should explain how enum values should be selected.
    Descriptions guide extraction but are not hard validation rules. Hard validation comes from `type`, `required`,
    `enum`, and `additionalProperties`.

    Object schemas are strict by default. Fields not declared in `properties` are rejected, and unsupported or invalid
    recipient results are returned as `null`.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create_call_request_recipient_result_schema_type_0 = cls()

        create_call_request_recipient_result_schema_type_0.additional_properties = d
        return create_call_request_recipient_result_schema_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
