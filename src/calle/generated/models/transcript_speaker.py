from typing import Literal

TranscriptSpeaker = Literal["bot", "unknown", "user"]

TRANSCRIPT_SPEAKER_VALUES: set[TranscriptSpeaker] = {
    "bot",
    "unknown",
    "user",
}


def check_transcript_speaker(value: str) -> TranscriptSpeaker:
    if value in TRANSCRIPT_SPEAKER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TRANSCRIPT_SPEAKER_VALUES!r}")
