from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.create_agentic_call_request_metadata import (
        CreateAgenticCallRequestMetadata,
    )
    from ..models.create_agentic_call_request_result_schema import (
        CreateAgenticCallRequestResultSchema,
    )


T = TypeVar("T", bound="CreateAgenticCallRequest")


@_attrs_define
class CreateAgenticCallRequest:
    """One phone, optional region and spoken locale, and a required Goal-compatible result schema.

    Attributes:
        task (str):
        phone (str):
        result_schema (CreateAgenticCallRequestResultSchema): Required closed flat JSON Schema using the same
            calle.result.scalar-object.v1 profile as Goal. At most 32 string, boolean, integer or number properties;
            additionalProperties must be false. Nested objects, arrays, null values and schema combinators are unsupported.
        region (None | str | Unset): Optional destination region. Inferred from the phone when omitted. An explicit
            region conflicting with the phone requires corrected input.
        locale (None | str | Unset): Optional spoken BCP-47 locale. Inferred from task intent and available regional
            languages when omitted.
        metadata (CreateAgenticCallRequestMetadata | Unset):
        webhook_url (None | str | Unset):
    """

    task: str
    phone: str
    result_schema: CreateAgenticCallRequestResultSchema
    region: None | str | Unset = UNSET
    locale: None | str | Unset = UNSET
    metadata: CreateAgenticCallRequestMetadata | Unset = UNSET
    webhook_url: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        phone = self.phone

        result_schema = self.result_schema.to_dict()

        region: None | str | Unset
        if isinstance(self.region, Unset):
            region = UNSET
        else:
            region = self.region

        locale: None | str | Unset
        if isinstance(self.locale, Unset):
            locale = UNSET
        else:
            locale = self.locale

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        webhook_url: None | str | Unset
        if isinstance(self.webhook_url, Unset):
            webhook_url = UNSET
        else:
            webhook_url = self.webhook_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "task": task,
                "phone": phone,
                "result_schema": result_schema,
            }
        )
        if region is not UNSET:
            field_dict["region"] = region
        if locale is not UNSET:
            field_dict["locale"] = locale
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if webhook_url is not UNSET:
            field_dict["webhook_url"] = webhook_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_agentic_call_request_metadata import (
            CreateAgenticCallRequestMetadata,
        )
        from ..models.create_agentic_call_request_result_schema import (
            CreateAgenticCallRequestResultSchema,
        )

        d = dict(src_dict)
        task = d.pop("task")

        phone = d.pop("phone")

        result_schema = CreateAgenticCallRequestResultSchema.from_dict(
            d.pop("result_schema")
        )

        def _parse_region(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        region = _parse_region(d.pop("region", UNSET))

        def _parse_locale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        locale = _parse_locale(d.pop("locale", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateAgenticCallRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateAgenticCallRequestMetadata.from_dict(_metadata)

        def _parse_webhook_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        webhook_url = _parse_webhook_url(d.pop("webhook_url", UNSET))

        create_agentic_call_request = cls(
            task=task,
            phone=phone,
            result_schema=result_schema,
            region=region,
            locale=locale,
            metadata=metadata,
            webhook_url=webhook_url,
        )

        return create_agentic_call_request
