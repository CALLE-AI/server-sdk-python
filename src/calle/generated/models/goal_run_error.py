from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define


from ..models.goal_run_error_code import check_goal_run_error_code
from ..models.goal_run_error_code import GoalRunErrorCode
from typing import cast


T = TypeVar("T", bound="GoalRunError")


@_attrs_define
class GoalRunError:
    """Unified safe error returned when a Goal Run cannot produce a usable result.

    Attributes:
        code (GoalRunErrorCode):
        message (str): Human-readable safe explanation. Do not parse this field for application logic.
        detail_code (None | str): Optional low-cardinality diagnostic detail safe for logs or narrow application
            branching.
    """

    code: GoalRunErrorCode
    message: str
    detail_code: None | str

    def to_dict(self) -> dict[str, Any]:
        code: str = self.code

        message = self.message

        detail_code: None | str
        detail_code = self.detail_code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
                "detail_code": detail_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = check_goal_run_error_code(d.pop("code"))

        message = d.pop("message")

        def _parse_detail_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        detail_code = _parse_detail_code(d.pop("detail_code"))

        goal_run_error = cls(
            code=code,
            message=message,
            detail_code=detail_code,
        )

        return goal_run_error
