from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast
import datetime

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
    """One phone, explicit dialing locale and a required Goal-compatible result schema.

    Attributes:
        task (str):
        phone (str):
        region (str):
        locale (str):
        result_schema (CreateAgenticCallRequestResultSchema): Required closed flat JSON Schema using the same
            calle.result.scalar-object.v1 profile as Goal. At most 32 string, boolean, integer or number properties;
            additionalProperties must be false. Nested objects, arrays, null values and schema combinators are unsupported.
        scheduled_at (datetime.datetime | None | Unset): Reserved draft field. Non-null values currently return
            scheduling_unavailable; do not use until scheduled authorization is enabled.
        metadata (CreateAgenticCallRequestMetadata | Unset):
        webhook_url (None | str | Unset):
    """

    task: str
    phone: str
    region: str
    locale: str
    result_schema: CreateAgenticCallRequestResultSchema
    scheduled_at: datetime.datetime | None | Unset = UNSET
    metadata: CreateAgenticCallRequestMetadata | Unset = UNSET
    webhook_url: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        task = self.task

        phone = self.phone

        region = self.region

        locale = self.locale

        result_schema = self.result_schema.to_dict()

        scheduled_at: None | str | Unset
        if isinstance(self.scheduled_at, Unset):
            scheduled_at = UNSET
        elif isinstance(self.scheduled_at, datetime.datetime):
            scheduled_at = self.scheduled_at.isoformat()
        else:
            scheduled_at = self.scheduled_at

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
                "region": region,
                "locale": locale,
                "result_schema": result_schema,
            }
        )
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at
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

        region = d.pop("region")

        locale = d.pop("locale")

        result_schema = CreateAgenticCallRequestResultSchema.from_dict(
            d.pop("result_schema")
        )

        def _parse_scheduled_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_at_type_0 = datetime.datetime.fromisoformat(data)

                return scheduled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        scheduled_at = _parse_scheduled_at(d.pop("scheduled_at", UNSET))

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
            region=region,
            locale=locale,
            result_schema=result_schema,
            scheduled_at=scheduled_at,
            metadata=metadata,
            webhook_url=webhook_url,
        )

        return create_agentic_call_request
