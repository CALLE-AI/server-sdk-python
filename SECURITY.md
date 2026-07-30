# Security

## Supported versions

The SDK is in Phase 1 beta preparation. Security fixes are applied to the
current beta line.

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities. Use GitHub private
vulnerability reporting if it is enabled for this repository; otherwise contact
the CALL-E maintainers directly.

Send a private report to the CALL-E maintainers with:

- Affected package and version.
- Reproduction steps or proof of concept.
- Expected impact.
- Any relevant logs with secrets removed.

## Secret handling

This SDK is for trusted server environments only. Do not expose CALL-E API keys
in browser code, mobile apps, public logs, or client-side bundles.

## Webhook receivers

CALL-E terminal webhooks do not include a webhook secret,
`CALL-E-Timestamp`, or `CALL-E-Signature`. Do not treat the event id or payload
as cryptographic proof of origin.

Treat the receiver as a public, untrusted-input boundary: accept only the
intended route, validate the JSON event shape, compare `CALL-E-Event-Id` with
the body event id, and persist that id before side effects so retries are
idempotent. If an integration requires origin assurance before a sensitive
action, fetch the referenced call through the authenticated Calls API and
compare its terminal snapshot.
