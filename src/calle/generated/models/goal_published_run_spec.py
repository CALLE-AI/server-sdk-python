from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


if TYPE_CHECKING:
    from ..models.goal_published_run_spec_input_schema import (
        GoalPublishedRunSpecInputSchema,
    )
    from ..models.goal_published_run_spec_result_schema import (
        GoalPublishedRunSpecResultSchema,
    )


T = TypeVar("T", bound="GoalPublishedRunSpec")


@_attrs_define
class GoalPublishedRunSpec:
    """Read-only published RunSpec interface for a Goal. Applications should inspect the schemas
    before constructing variables and should record the version used by deployments.

        Attributes:
            id (str): Opaque immutable RunSpec identity.
            version (int): Monotonic published version within this Goal. A later publish affects only new Runs.
            input_schema (GoalPublishedRunSpecInputSchema): Normalized JSON Schema for per-Run `variables`. Respect
                `required`, property types, enum
                values, defaults, and `additionalProperties`; invalid input is rejected before execution.
            result_schema (GoalPublishedRunSpecResultSchema): Normalized JSON Schema for `result`. CALL-E exposes a result
                only after it is
                validated against this exact pinned schema and durably persisted.
    """

    id: str
    version: int
    input_schema: GoalPublishedRunSpecInputSchema
    result_schema: GoalPublishedRunSpecResultSchema

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        version = self.version

        input_schema = self.input_schema.to_dict()

        result_schema = self.result_schema.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "version": version,
                "input_schema": input_schema,
                "result_schema": result_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal_published_run_spec_input_schema import (
            GoalPublishedRunSpecInputSchema,
        )
        from ..models.goal_published_run_spec_result_schema import (
            GoalPublishedRunSpecResultSchema,
        )

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        input_schema = GoalPublishedRunSpecInputSchema.from_dict(d.pop("input_schema"))

        result_schema = GoalPublishedRunSpecResultSchema.from_dict(
            d.pop("result_schema")
        )

        goal_published_run_spec = cls(
            id=id,
            version=version,
            input_schema=input_schema,
            result_schema=result_schema,
        )

        return goal_published_run_spec
