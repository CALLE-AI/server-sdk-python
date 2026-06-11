from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CompletionConfidence")


@_attrs_define
class CompletionConfidence:
    """
    Attributes:
        score (float): Confidence score in the 0 to 1 range for CALL-E's task completion judgment.
        label (str): Confidence label for the task completion judgment, for example `low`, `medium`, or `high`.
    """

    score: float
    label: str

    def to_dict(self) -> dict[str, Any]:
        score = self.score

        label = self.label

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "score": score,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        score = d.pop("score")

        label = d.pop("label")

        completion_confidence = cls(
            score=score,
            label=label,
        )

        return completion_confidence
