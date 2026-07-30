from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.goal_list_object import check_goal_list_object
from ..models.goal_list_object import GoalListObject
from typing import cast

if TYPE_CHECKING:
    from ..models.goal import Goal


T = TypeVar("T", bound="GoalList")


@_attrs_define
class GoalList:
    """Cursor-paginated collection of the authenticated owner's listed, active, published Goal
    interfaces. Use this for discovery or recovery of a known Goal id, not as title search.

        Attributes:
            object_ (GoalListObject): Always `list` for paginated list responses.
            data (list[Goal]): Goal interfaces in stable opaque-id order. Do not assume the first item is the Goal your
                workflow should execute; store the intended `goal_id` when it is published.
            next_cursor (None | str): Opaque cursor for the next page. `null` means there are no more Goals.
    """

    object_: GoalListObject
    data: list[Goal]
    next_cursor: None | str

    def to_dict(self) -> dict[str, Any]:
        object_: str = self.object_

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "object": object_,
                "data": data,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal import Goal

        d = dict(src_dict)
        object_ = check_goal_list_object(d.pop("object"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Goal.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        goal_list = cls(
            object_=object_,
            data=data,
            next_cursor=next_cursor,
        )

        return goal_list
