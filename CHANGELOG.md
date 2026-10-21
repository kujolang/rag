# Changelog

All notable changes to Kujo RAG are documented here.

## [Unreleased]

## [1.1.0] - 2026-10-21

- Add HTTP documentation ingestion, equivalent-example retrieval preferences, and a local published-docs service workflow.
- Harden ingestion, structured document parsing, index persistence, authentication and proxy boundaries.
- Add staged Qdrant transaction recovery and rollback verification.
- Require Kujo 1.2.3 or newer and patched Node.js versions for the associated tooling.
- Preserve local/offline defaults and require target-environment evidence for hosted production promotion.

- Added launch-readiness Spec, Eval suite, Kujo/Kennel metadata, and README readiness/version wording alignment for prelaunch review gates.
- Preserve actionable `meta.load_error` diagnostics when an index exists but its
  JSON cannot be read or parsed instead of silently returning an empty index.

## [1.0.0] - 2026-08-08

- Declared the offline-first ingestion, retrieval, namespace, API, and release-evaluation surfaces stable.
- Aligned package and project metadata with the official 1.0 release.
- Retained explicit target-environment requirements for hosted deployment and live-provider claims.

## [0.1.0] - 2026-06-27

- Prepared Kujo RAG for public release with offline-first ingestion/query flows, local JSON vector storage, API contract coverage, security checks, and release-evaluation gates.
