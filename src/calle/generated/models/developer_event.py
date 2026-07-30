from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.call_status import CallStatus
from ..models.call_status import check_call_status
from ..models.developer_event_level import check_developer_event_level
from ..models.developer_event_level import DeveloperEventLevel
import datetime

if TYPE_CHECKING:
    from ..models.developer_event_details import DeveloperEventDetails


T = TypeVar("T", bound="DeveloperEvent")


@_attrs_define
class DeveloperEvent:
    """
    Attributes:
        id (str): Public event identifier.
        type_ (str): Developer-facing event type, for example `call.completed`.
        call_id (str): Public CALL-E call identifier associated with this event.
        created_at (datetime.datetime): ISO 8601 timestamp when the event was emitted.
        level (DeveloperEventLevel): Event severity for log routing and alerting.
        status (CallStatus): Current lifecycle state of a CALL-E call. `in_progress` includes post-call result
            finalization; terminal states are published only after the post-call outcome is available.
        message (str): Short human-readable event message.
        details (DeveloperEventDetails): Event-specific structured details. Shape depends on the event type.
    """

    id: str
    type_: str
    call_id: str
    created_at: datetime.datetime
    level: DeveloperEventLevel
    status: CallStatus
    message: str
    details: DeveloperEventDetails

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        call_id = self.call_id

        created_at = self.created_at.isoformat()

        level: str = self.level

        status: str = self.status

        message = self.message

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
                "call_id": call_id,
                "created_at": created_at,
                "level": level,
                "status": status,
                "message": message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.developer_event_details import DeveloperEventDetails

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        call_id = d.pop("call_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        level = check_developer_event_level(d.pop("level"))

        status = check_call_status(d.pop("status"))

        message = d.pop("message")

        details = DeveloperEventDetails.from_dict(d.pop("details"))

        developer_event = cls(
            id=id,
            type_=type_,
            call_id=call_id,
            created_at=created_at,
            level=level,
            status=status,
            message=message,
            details=details,
        )

        return developer_event
