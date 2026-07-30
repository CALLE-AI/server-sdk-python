from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="CallTaskRecipientRequest")


@_attrs_define
class CallTaskRecipientRequest:
    """
    Attributes:
        phones (list[str]): Phone numbers in E.164 format for this recipient. Replace placeholders such as
            `<RECIPIENT_1_E164_PHONE>` with phone numbers you own or are authorized to call.
        locale (None | str | Unset): BCP 47 locale hint for the conversation, for example `en-US`.
        region (None | str | Unset): Recipient country or region code used for routing and compliance checks, for
            example `US`.
    """

    phones: list[str]
    locale: None | str | Unset = UNSET
    region: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phones = self.phones

        locale: None | str | Unset
        if isinstance(self.locale, Unset):
            locale = UNSET
        else:
            locale = self.locale

        region: None | str | Unset
        if isinstance(self.region, Unset):
            region = UNSET
        else:
            region = self.region

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phones": phones,
            }
        )
        if locale is not UNSET:
            field_dict["locale"] = locale
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phones = cast(list[str], d.pop("phones"))

        def _parse_locale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        locale = _parse_locale(d.pop("locale", UNSET))

        def _parse_region(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        region = _parse_region(d.pop("region", UNSET))

        call_task_recipient_request = cls(
            phones=phones,
            locale=locale,
            region=region,
        )

        return call_task_recipient_request
