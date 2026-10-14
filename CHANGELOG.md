# Changelog

All notable changes to Kujo RAG are documented here.

## [1.1.0] - 2026-10-14

- Add negotiated HTTP document ingestion, equivalent example selection, retrieval measurements, and local published documentation snapshots/service.
- Harden atomic index persistence, parsing, quotas, privacy, descriptor-relative ingestion, staged Qdrant transactions, and Cloudflare proxy identity/RBAC.
- Pass artifact-builder options after the runtime argument separator; make the canary negative control independent of machine speed.
- Keep hosted production certification deployment-specific; see [release notes](docs/releases/v1.1.0.md).

- Added launch-readiness Spec, Eval suite, Kujo/Kennel metadata, and README readiness/version wording alignment for prelaunch review gates.
- Preserve actionable `meta.load_error` diagnostics when an index exists but its
  JSON cannot be read or parsed instead of silently returning an empty index.

## [1.0.0] - 2026-08-08

- Declared the offline-first ingestion, retrieval, namespace, API, and release-evaluation surfaces stable.
- Aligned package and project metadata with the official 1.0 release.
- Retained explicit target-environment requirements for hosted deployment and live-provider claims.

## [0.1.0] - 2026-06-27

- Prepared Kujo RAG for public release with offline-first ingestion/query flows, local JSON vector storage, API contract coverage, security checks, and release-evaluation gates.
