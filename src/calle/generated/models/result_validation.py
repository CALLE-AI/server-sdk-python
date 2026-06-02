from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResultValidation")


@_attrs_define
class ResultValidation:
    """
    Attributes:
        valid (bool):
        error_code (str | Unset):
        message (str | Unset):
    """

    valid: bool
    error_code: str | Unset = UNSET
    message: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        valid = self.valid

        error_code = self.error_code

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "valid": valid,
            }
        )
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        valid = d.pop("valid")

        error_code = d.pop("error_code", UNSET)

        message = d.pop("message", UNSET)

        result_validation = cls(
            valid=valid,
            error_code=error_code,
            message=message,
        )

        return result_validation
