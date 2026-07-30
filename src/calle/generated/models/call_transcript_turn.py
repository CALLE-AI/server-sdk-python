from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define


from ..models.transcript_speaker import check_transcript_speaker
from ..models.transcript_speaker import TranscriptSpeaker
from typing import cast


T = TypeVar("T", bound="CallTranscriptTurn")


@_attrs_define
class CallTranscriptTurn:
    """
    Attributes:
        offset_seconds (int | None): Seconds from the start of the attempt. `null` when the source line did not include
            a parseable timestamp.
        speaker (TranscriptSpeaker): Speaker label for one transcript turn.
        text (str): Spoken text for this transcript turn.
    """

    offset_seconds: int | None
    speaker: TranscriptSpeaker
    text: str

    def to_dict(self) -> dict[str, Any]:
        offset_seconds: int | None
        offset_seconds = self.offset_seconds

        speaker: str = self.speaker

        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "offset_seconds": offset_seconds,
                "speaker": speaker,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_offset_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        offset_seconds = _parse_offset_seconds(d.pop("offset_seconds"))

        speaker = check_transcript_speaker(d.pop("speaker"))

        text = d.pop("text")

        call_transcript_turn = cls(
            offset_seconds=offset_seconds,
            speaker=speaker,
            text=text,
        )

        return call_transcript_turn
