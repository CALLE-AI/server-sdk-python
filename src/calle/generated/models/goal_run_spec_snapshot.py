from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define


T = TypeVar("T", bound="GoalRunSpecSnapshot")


@_attrs_define
class GoalRunSpecSnapshot:
    """Exact immutable RunSpec identity and version pinned by a Goal Run.

    Attributes:
        id (str): Exact immutable RunSpec id pinned when the Goal Run was accepted.
        version (int): Published RunSpec version pinned for this Goal Run.
    """

    id: str
    version: int

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        goal_run_spec_snapshot = cls(
            id=id,
            version=version,
        )

        return goal_run_spec_snapshot
