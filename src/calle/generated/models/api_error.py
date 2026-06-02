from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.api_error_code import APIErrorCode, check_api_error_code

if TYPE_CHECKING:
    from ..models.api_error_details import APIErrorDetails


T = TypeVar("T", bound="APIError")


@_attrs_define
class APIError:
    """
    Attributes:
        code (APIErrorCode):
        message (str):
        details (APIErrorDetails):
    """

    code: APIErrorCode
    message: str
    details: APIErrorDetails

    def to_dict(self) -> dict[str, Any]:
        code: str = self.code

        message = self.message

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_details import APIErrorDetails

        d = dict(src_dict)
        code = check_api_error_code(d.pop("code"))

        message = d.pop("message")

        details = APIErrorDetails.from_dict(d.pop("details"))

        api_error = cls(
            code=code,
            message=message,
            details=details,
        )

        return api_error
