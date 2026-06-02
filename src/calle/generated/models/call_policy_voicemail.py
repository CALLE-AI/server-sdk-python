from typing import Literal

CallPolicyVoicemail = Literal["do_not_leave"]

CALL_POLICY_VOICEMAIL_VALUES: set[CallPolicyVoicemail] = {
    "do_not_leave",
}


def check_call_policy_voicemail(value: str) -> CallPolicyVoicemail:
    if value in CALL_POLICY_VOICEMAIL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_POLICY_VOICEMAIL_VALUES!r}")
