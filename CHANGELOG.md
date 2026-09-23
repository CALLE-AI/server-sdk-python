# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-23

### Changed

- Move `client.calls` to the single-target Calls API with required phone, result schema and idempotency key.
- Support optional region/language hints, cancellation before submission, and detailed call events.
- Expose Billing call ID, call outcome, result readiness and recorded transcript turns.
- Stop Calls and Goal Run wait helpers when result readiness is final, including unavailable results with no error.
- This is a breaking Calls migration. Retain SDK 0.7.x for historical legacy call-task IDs; see the public migration guide.
- Clarify webhook configuration, legacy batch-call requirements, and redaction of credentials and private call data.

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
