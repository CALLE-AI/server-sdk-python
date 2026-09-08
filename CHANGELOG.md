# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.1] - 2026-09-04

### Added

- MIT license, including explicit coverage for the published `calle-ai`
  versions `0.6.0` and `0.7.0`, plus public contribution, security, and
  ownership information.
- A public-repository hygiene check for tracked paths, tracked text, and pull
  request metadata.

### Changed

- Prevented generated client representations from exposing credentials and
  kept call identifiers inside their intended URL path segment.
- Bounded webhook example request bodies and documented its production limits.
- Locked the release build and package-validation toolchain.
- Stable publishing is initiated by a versioned GitHub Release and uses PyPI
  Trusted Publishing.
