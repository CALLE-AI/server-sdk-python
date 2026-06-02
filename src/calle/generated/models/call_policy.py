from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.call_policy_on_not_ready import CallPolicyOnNotReady, check_call_policy_on_not_ready
from ..models.call_policy_voicemail import CallPolicyVoicemail, check_call_policy_voicemail
from ..types import UNSET, Unset

T = TypeVar("T", bound="CallPolicy")


@_attrs_define
class CallPolicy:
    """
    Attributes:
        max_attempts (int | Unset):  Default: 1.
        voicemail (CallPolicyVoicemail | Unset):  Default: 'do_not_leave'.
        on_not_ready (CallPolicyOnNotReady | Unset):  Default: 'error'.
    """

    max_attempts: int | Unset = 1
    voicemail: CallPolicyVoicemail | Unset = "do_not_leave"
    on_not_ready: CallPolicyOnNotReady | Unset = "error"

    def to_dict(self) -> dict[str, Any]:
        max_attempts = self.max_attempts

        voicemail: str | Unset = UNSET
        if not isinstance(self.voicemail, Unset):
            voicemail = self.voicemail

        on_not_ready: str | Unset = UNSET
        if not isinstance(self.on_not_ready, Unset):
            on_not_ready = self.on_not_ready

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if max_attempts is not UNSET:
            field_dict["max_attempts"] = max_attempts
        if voicemail is not UNSET:
            field_dict["voicemail"] = voicemail
        if on_not_ready is not UNSET:
            field_dict["on_not_ready"] = on_not_ready

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_attempts = d.pop("max_attempts", UNSET)

        _voicemail = d.pop("voicemail", UNSET)
        voicemail: CallPolicyVoicemail | Unset
        if isinstance(_voicemail, Unset):
            voicemail = UNSET
        else:
            voicemail = check_call_policy_voicemail(_voicemail)

        _on_not_ready = d.pop("on_not_ready", UNSET)
        on_not_ready: CallPolicyOnNotReady | Unset
        if isinstance(_on_not_ready, Unset):
            on_not_ready = UNSET
        else:
            on_not_ready = check_call_policy_on_not_ready(_on_not_ready)

        call_policy = cls(
            max_attempts=max_attempts,
            voicemail=voicemail,
            on_not_ready=on_not_ready,
        )

        return call_policy
