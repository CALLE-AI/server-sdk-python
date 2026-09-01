from scripts.check_public_repo_hygiene import (
    INTERNAL_LINK,
    RAW_HTTP_IP,
    UNCONFIRMED_REPO,
    scan_text,
)


def _kinds(text: str) -> set[str]:
    return {finding.kind for finding in scan_text("pull request body", text)}


def test_flags_private_context_without_echoing_source() -> None:
    internal_link = "https://" + "git" + "lab.example.invalid/team/project"
    raw_ip = "http://" + "192.0.2.10:8080/path"
    unconfirmed_repo = "CALLE" + "-AI/private-repository"
    source = f"{internal_link}\n{raw_ip}\n{unconfirmed_repo}"

    findings = scan_text("pull request body", source)

    assert {finding.kind for finding in findings} == {
        INTERNAL_LINK,
        RAW_HTTP_IP,
        UNCONFIRMED_REPO,
    }
    assert all(internal_link not in finding.describe() for finding in findings)
    assert all(raw_ip not in finding.describe() for finding in findings)
    assert all(unconfirmed_repo not in finding.describe() for finding in findings)


def test_flags_common_collaboration_links() -> None:
    collaboration_link = "https://" + "workspace." + "slack.com/archives/channel"

    assert _kinds(collaboration_link) == {INTERNAL_LINK}


def test_allows_confirmed_public_sdk_repositories() -> None:
    source = (
        "CALLE-AI/server-sdk-python.git "
        "CALLE-AI/server-sdk-typescript "
        "CALLE-AI/calle-docs"
    )

    assert scan_text("README.md", source) == []
