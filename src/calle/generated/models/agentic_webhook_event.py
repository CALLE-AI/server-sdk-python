from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.agentic_webhook_event_type import AgenticWebhookEventType
from ..models.agentic_webhook_event_type import check_agentic_webhook_event_type
import datetime

if TYPE_CHECKING:
    from ..models.agentic_call import AgenticCall


T = TypeVar("T", bound="AgenticWebhookEvent")


@_attrs_define
class AgenticWebhookEvent:
    """v2 terminal webhook. data is identical to the terminal GET response. A valid call completion can carry a failed
    custom result. Retries reuse the same event id.

        Attributes:
            id (str):
            type_ (AgenticWebhookEventType):
            created_at (datetime.datetime):
            data (AgenticCall): Persisted one-shot snapshot with the same result/error contract as Goal Run. Continue
                polling while both are null, even when status is completed. An empty result object is ready. Execution
                completion does not imply business success. Terminal webhooks are sent after result or error is ready.
    """

    id: str
    type_: AgenticWebhookEventType
    created_at: datetime.datetime
    data: AgenticCall

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
        from ..models.agentic_call import AgenticCall

        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_agentic_webhook_event_type(d.pop("type"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        data = AgenticCall.from_dict(d.pop("data"))

        agentic_webhook_event = cls(
            id=id,
            type_=type_,
            created_at=created_at,
            data=data,
        )

        return agentic_webhook_event
