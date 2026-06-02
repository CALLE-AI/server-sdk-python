from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.webhook_event_type import WebhookEventType, check_webhook_event_type

if TYPE_CHECKING:
    from ..models.webhook_call_data import WebhookCallData


T = TypeVar("T", bound="WebhookEvent")


@_attrs_define
class WebhookEvent:
    """
    Attributes:
        id (str):
        type_ (WebhookEventType):
        created_at (datetime.datetime):
        data (WebhookCallData):
    """

    id: str
    type_: WebhookEventType
    created_at: datetime.datetime
    data: WebhookCallData

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        created_at = self.created_at.isoformat()

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "created_at": created_at,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook_call_data import WebhookCallData

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_webhook_event_type(d.pop("type"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        data = WebhookCallData.from_dict(d.pop("data"))

        webhook_event = cls(
            id=id,
            type_=type_,
            created_at=created_at,
            data=data,
        )

        return webhook_event
