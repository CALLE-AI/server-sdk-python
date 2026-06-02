from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CallRecipient")


@_attrs_define
class CallRecipient:
    """
    Attributes:
        phone (str | Unset): E.164 phone number.
        name (str | Unset):
        locale (str | Unset):
        region (str | Unset):
    """

    phone: str | Unset = UNSET
    name: str | Unset = UNSET
    locale: str | Unset = UNSET
    region: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone = self.phone

        name = self.name

        locale = self.locale

        region = self.region

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if phone is not UNSET:
            field_dict["phone"] = phone
        if name is not UNSET:
            field_dict["name"] = name
        if locale is not UNSET:
            field_dict["locale"] = locale
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone = d.pop("phone", UNSET)

        name = d.pop("name", UNSET)

        locale = d.pop("locale", UNSET)

        region = d.pop("region", UNSET)

        call_recipient = cls(
            phone=phone,
            name=name,
            locale=locale,
            region=region,
        )

        return call_recipient
