from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="CreateCallRequestResultSchemaType0")


@_attrs_define
class CreateCallRequestResultSchemaType0:
    """Optional JSON Schema object that defines the structured result CALL-E should extract for the whole call task.

    CALL-E passes the schema, including field `description` values, to the extraction model after the call reaches a
    terminal state. Use descriptions to explain field meaning and enum selection logic, for example: "Use strong when
    the prospect asks about pricing, demos, or next steps."

    Descriptions guide extraction but are not hard validation rules. Hard validation comes from `type`, `required`,
    `enum`, and `additionalProperties`.

    Supported schema features are `type`, `properties`, `required`, `enum`, nested `object` fields, simple
    `array.items`, `description`, and `additionalProperties: false`. Unsupported features include `$ref`, `oneOf`,
    `anyOf`, `allOf`, recursive schemas, complex format validation, and `additionalProperties: true`.

    Prefer string enums over booleans for business decisions that may be unclear, and include an `unknown` enum value
    when the call may not provide enough evidence.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        create_call_request_result_schema_type_0 = cls()

        create_call_request_result_schema_type_0.additional_properties = d
        return create_call_request_result_schema_type_0

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
