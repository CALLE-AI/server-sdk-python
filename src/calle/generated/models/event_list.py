from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.event_list_object import EventListObject, check_event_list_object
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.developer_event import DeveloperEvent


T = TypeVar("T", bound="EventList")


@_attrs_define
class EventList:
    """
    Attributes:
        object_ (EventListObject): Always `list` for paginated list responses.
        data (list[DeveloperEvent]): Events in this page, ordered from oldest to newest for the requested cursor window.
        next_cursor (None | str | Unset): Cursor for the next page. `null` means there are no more events.
    """

    object_: EventListObject
    data: list[DeveloperEvent]
    next_cursor: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        object_: str = self.object_

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_cursor: None | str | Unset
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "object": object_,
                "data": data,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.developer_event import DeveloperEvent

        d = dict(src_dict)
        object_ = check_event_list_object(d.pop("object"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = DeveloperEvent.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor", UNSET))

        event_list = cls(
            object_=object_,
            data=data,
            next_cursor=next_cursor,
        )

        return event_list
