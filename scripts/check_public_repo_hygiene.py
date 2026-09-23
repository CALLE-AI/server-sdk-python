#!/usr/bin/env python3
"""Reject private-context references before they enter the public repository."""

from __future__ import annotations

import ipaddress
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC_CALLE_REPOS = frozenset(
    {
        "awesome-phone-call-agents",
        "call-e-integrations",
        "calle-docs",
        "n8n-nodes-calle",
        "server-sdk-python",
        "server-sdk-typescript",
    }
)

COLLABORATION_HOSTS = (
    "atlassian.net",
    "docs.google.com",
    "drive.google.com",
    "feishu.cn",
    "larksuite.com",
    "linear.app",
    "notion.site",
    "notion.so",
    "slack.com",
)

URL_RE = re.compile(r"https?://[^\s<>{}\"']+", re.IGNORECASE)
CALLE_REPO_RE = re.compile(
    r"(?<![@A-Za-z0-9_.-])CALLE-AI/([A-Za-z0-9_.-]+)", re.IGNORECASE
)

INTERNAL_LINK = "internal collaboration link"
RAW_HTTP_IP = "unencrypted IP URL"
UNCONFIRMED_REPO = "unconfirmed CALLE-AI repository reference"


@dataclass(frozen=True)
class Finding:
    location: str
    kind: str

    def describe(self) -> str:
        return f"{self.location}: {self.kind}"


def _is_collaboration_host(hostname: str) -> bool:
    hostname = hostname.lower().rstrip(".")
    if any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in COLLABORATION_HOSTS
    ):
        return True

    return any(label.startswith("gitlab") for label in hostname.split("."))


def _is_ip_address(hostname: str) -> bool:
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return True


def scan_text(label: str, text: str) -> list[Finding]:
    findings: list[Finding] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in URL_RE.finditer(line):
            parsed = urlsplit(match.group(0))
            hostname = parsed.hostname
            if hostname is None:
                continue

            location = f"{label}:{line_number}:{match.start() + 1}"
            if _is_collaboration_host(hostname):
                findings.append(Finding(location, INTERNAL_LINK))
            if parsed.scheme.lower() == "http" and _is_ip_address(hostname):
                findings.append(Finding(location, RAW_HTTP_IP))

        for match in CALLE_REPO_RE.finditer(line):
            repository = match.group(1).lower().removesuffix(".git")
            if repository not in PUBLIC_CALLE_REPOS:
                location = f"{label}:{line_number}:{match.start() + 1}"
                findings.append(Finding(location, UNCONFIRMED_REPO))

    return findings


def _tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(os.fsdecode(raw_path)) for raw_path in result.stdout.split(b"\0") if raw_path]


def _read_tracked_text(path: Path) -> str | None:
    try:
        if path.is_symlink():
            raw = os.fsencode(os.readlink(path))
        else:
            raw = path.read_bytes()
    except FileNotFoundError:
        return None

    if b"\0" in raw:
        return None
    return raw.decode("utf-8", errors="replace")


def main() -> int:
    findings: list[Finding] = []

    for path in _tracked_paths():
        relative_path = path.as_posix()
        findings.extend(scan_text(f"path {relative_path}", relative_path))

        text = _read_tracked_text(path)
        if text is not None:
            findings.extend(scan_text(relative_path, text))

    findings.extend(scan_text("pull request title", os.environ.get("PR_TITLE", "")))
    findings.extend(scan_text("pull request body", os.environ.get("PR_BODY", "")))

    if not findings:
        print("Public repository hygiene check passed.")
        return 0

    print("Public repository hygiene check failed:", file=sys.stderr)
    for finding in findings:
        print(f"- {finding.describe()}", file=sys.stderr)
    print(
        "Remove the reference, or confirm a public repository and update the explicit allowlist.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
