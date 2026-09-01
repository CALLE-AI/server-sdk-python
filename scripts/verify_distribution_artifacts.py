#!/usr/bin/env python3
"""Validate release artifacts and create or check their checksum manifest."""

from __future__ import annotations

import argparse
import hashlib
import re
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

MANIFEST_NAME = "SHA256SUMS"
MANIFEST_LINE_RE = re.compile(r"([0-9a-f]{64})  ([^/\s]+)")


def _project_version() -> str:
    with Path("pyproject.toml").open("rb") as stream:
        return str(tomllib.load(stream)["project"]["version"])


def _archive_files(directory: Path) -> tuple[Path, Path]:
    wheel_files = sorted(directory.glob("*.whl"))
    source_files = sorted(directory.glob("*.tar.gz"))
    if len(wheel_files) != 1 or len(source_files) != 1:
        raise ValueError("artifact directory must contain one wheel and one source archive")
    return wheel_files[0], source_files[0]


def _metadata_fields(raw_metadata: bytes) -> tuple[str | None, str | None, str | None]:
    metadata = BytesParser().parsebytes(raw_metadata)
    return metadata["Name"], metadata["Version"], metadata["License-Expression"]


def _verify_wheel(path: Path, expected_version: str, expected_license: bytes) -> None:
    with zipfile.ZipFile(path) as archive:
        metadata_names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        license_names = [
            name
            for name in archive.namelist()
            if PurePosixPath(name).name == "LICENSE" and ".dist-info/licenses/" in name
        ]
        if len(metadata_names) != 1 or len(license_names) != 1:
            raise ValueError("wheel must contain one METADATA file and one dist-info license")

        name, version, license_expression = _metadata_fields(archive.read(metadata_names[0]))
        if name != "calle-ai" or version != expected_version:
            raise ValueError("wheel name or version metadata does not match the release")
        if license_expression != "MIT":
            raise ValueError("wheel METADATA must contain License-Expression: MIT")
        if archive.read(license_names[0]) != expected_license:
            raise ValueError("wheel license differs from the repository LICENSE")


def _verify_sdist(path: Path, expected_version: str, expected_license: bytes) -> None:
    with tarfile.open(path, mode="r:gz") as archive:
        files = [member for member in archive.getmembers() if member.isfile()]
        metadata_members = [member for member in files if PurePosixPath(member.name).name == "PKG-INFO"]
        license_members = [member for member in files if PurePosixPath(member.name).name == "LICENSE"]
        if len(metadata_members) != 1 or len(license_members) != 1:
            raise ValueError("source archive must contain one PKG-INFO and one license file")

        metadata_stream = archive.extractfile(metadata_members[0])
        license_stream = archive.extractfile(license_members[0])
        if metadata_stream is None or license_stream is None:
            raise ValueError("source archive metadata or license could not be read")

        name, version, license_expression = _metadata_fields(metadata_stream.read())
        if name != "calle-ai" or version != expected_version:
            raise ValueError("source archive name or version metadata does not match the release")
        if license_expression != "MIT":
            raise ValueError("source archive PKG-INFO must contain License-Expression: MIT")
        if license_stream.read() != expected_license:
            raise ValueError("source archive license differs from the repository LICENSE")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_manifest(directory: Path, artifacts: tuple[Path, Path]) -> None:
    manifest = directory / MANIFEST_NAME
    contents = "".join(f"{_sha256(path)}  {path.name}\n" for path in artifacts)
    manifest.write_text(contents, encoding="utf-8")


def _check_manifest(directory: Path, artifacts: tuple[Path, Path]) -> None:
    manifest = directory / MANIFEST_NAME
    entries: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = MANIFEST_LINE_RE.fullmatch(line)
        if match is None or match.group(2) in entries:
            raise ValueError("checksum manifest has an invalid or duplicate entry")
        entries[match.group(2)] = match.group(1)

    expected_names = {path.name for path in artifacts}
    if set(entries) != expected_names:
        raise ValueError("checksum manifest does not match the artifact file set")
    for path in artifacts:
        if _sha256(path) != entries[path.name]:
            raise ValueError(f"checksum mismatch: {path.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected-version")
    manifest_mode = parser.add_mutually_exclusive_group(required=True)
    manifest_mode.add_argument("--write-manifest", action="store_true")
    manifest_mode.add_argument("--check-manifest", action="store_true")
    arguments = parser.parse_args()

    project_version = _project_version()
    expected_version = arguments.expected_version or project_version
    if expected_version != project_version:
        raise ValueError("expected version does not match pyproject.toml")

    expected_files = {MANIFEST_NAME} if arguments.check_manifest else set()
    artifacts = _archive_files(arguments.directory)
    expected_files.update(path.name for path in artifacts)
    if (arguments.directory / ".gitignore").is_file():
        expected_files.add(".gitignore")
    actual_files = {path.name for path in arguments.directory.iterdir() if path.is_file()}
    if actual_files != expected_files:
        raise ValueError("artifact directory contains an unexpected file set")

    expected_license = Path("LICENSE").read_bytes()
    _verify_wheel(artifacts[0], expected_version, expected_license)
    _verify_sdist(artifacts[1], expected_version, expected_license)

    if arguments.write_manifest:
        _write_manifest(arguments.directory, artifacts)
    else:
        _check_manifest(arguments.directory, artifacts)

    print("Distribution artifacts verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
