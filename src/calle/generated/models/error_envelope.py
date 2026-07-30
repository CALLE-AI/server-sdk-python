from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define


if TYPE_CHECKING:
    from ..models.api_error import APIError


T = TypeVar("T", bound="ErrorEnvelope")


@_attrs_define
class ErrorEnvelope:
    """
    Attributes:
        error (APIError):
    """

    error: APIError

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error import APIError

        d = dict(src_dict)
        error = APIError.from_dict(d.pop("error"))

        error_envelope = cls(
            error=error,
        )

        return error_envelope
