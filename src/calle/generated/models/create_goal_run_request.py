from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset


if TYPE_CHECKING:
    from ..models.goal_variables import GoalVariables


T = TypeVar("T", bound="CreateGoalRunRequest")


@_attrs_define
class CreateGoalRunRequest:
    """One phone-specific submission against the Goal's currently published RunSpec. The object is
    closed: target wrappers, per-Run region/locale/display-name hints, task text, schemas, RunSpec
    selectors, provider settings, and unknown fields are not accepted. Region, callee locale, and
    runtime profile come from the published Goal. Use the required `Idempotency-Key` header for
    retry safety.

        Attributes:
            phone (str): Recipient phone in canonical E.164 form: `+`, country code, and subscriber number with
                no spaces, punctuation, or extension. The caller must be authorized to contact it.
                CALL-E validates it against the published Goal's fixed Voice Target policy.
            variables (GoalVariables | Unset): Dynamic variable map validated by the exact published input schema pinned
                during acceptance.
                Read the Goal interface rather than hard-coding undocumented keys.
    """

    phone: str
    variables: GoalVariables | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone = self.phone

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "phone": phone,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal_variables import GoalVariables

        d = dict(src_dict)
        phone = d.pop("phone")

        _variables = d.pop("variables", UNSET)
        variables: GoalVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = GoalVariables.from_dict(_variables)

        create_goal_run_request = cls(
            phone=phone,
            variables=variables,
        )

        return create_goal_run_request
