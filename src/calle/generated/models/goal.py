from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


from ..models.goal_object import check_goal_object
from ..models.goal_object import GoalObject
from ..models.goal_status import check_goal_status
from ..models.goal_status import GoalStatus
from typing import cast

if TYPE_CHECKING:
    from ..models.goal_published_run_spec import GoalPublishedRunSpec


T = TypeVar("T", bound="Goal")


@_attrs_define
class Goal:
    """Owner-scoped active Goal and its currently published immutable RunSpec interface. This is an
    execution contract, not an authoring record: it includes a developer-facing title and
    description but omits prompts, provider settings, and history.

        Attributes:
            object_ (GoalObject): Always `goal` for Goal responses.
            id (str): Opaque Goal identity. This is distinct from the nested RunSpec identity.
            title (None | str): Short developer-facing title from the current published RunSpec. It may be null for an
                untitled Goal.
            description (str): Developer-facing summary of what the current published Goal does. This is not the execution
                prompt.
            status (GoalStatus): Always `active`; non-executable Goals are not returned by this surface.
            published_run_spec (GoalPublishedRunSpec): Read-only published RunSpec interface for a Goal. Applications should
                inspect the schemas
                before constructing variables and should record the version used by deployments.
    """

    object_: GoalObject
    id: str
    title: None | str
    description: str
    status: GoalStatus
    published_run_spec: GoalPublishedRunSpec

    def to_dict(self) -> dict[str, Any]:
        object_: str = self.object_

        id = self.id

        title: None | str
        title = self.title

        description = self.description

        status: str = self.status

        published_run_spec = self.published_run_spec.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "object": object_,
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "published_run_spec": published_run_spec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal_published_run_spec import GoalPublishedRunSpec

        d = dict(src_dict)
        object_ = check_goal_object(d.pop("object"))

        id = d.pop("id")

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        description = d.pop("description")

        status = check_goal_status(d.pop("status"))

        published_run_spec = GoalPublishedRunSpec.from_dict(d.pop("published_run_spec"))

        goal = cls(
            object_=object_,
            id=id,
            title=title,
            description=description,
            status=status,
            published_run_spec=published_run_spec,
        )

        return goal
