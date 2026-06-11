# API and Config Versioning Policy

This document defines the explicit API and configuration versioning contract for Kujo RAG production upgrades.

## Scope

The policy applies to:

- HTTP API contract versioning (`openapi/kujo-rag-openapi.json`)
- release manifest compatibility markers (`config_schema_version`, `api_contract_version`)
- migration notes that accompany any breaking API/config change
- previous minor compatibility validation before promotion

## Backward Compatibility Rules

1. Release tags use Semantic Versioning (`MAJOR.MINOR.PATCH`).
2. `PATCH` releases must preserve API and config behavior.
3. `MINOR` releases must remain backward-compatible for existing clients/configs in the same major line.
4. Breaking API/config changes require a `MAJOR` release and migration documentation.
5. OpenAPI metadata must remain aligned:
   - `info.version` tracks release SemVer.
   - `info.x-kujo-rag-api-version` tracks API contract version (for example `v1`).

## Deprecation Windows

The minimum deprecation windows before removal are:

- API contract behavior: 180 days
- config key/schema behavior: 180 days

Deprecations must be documented in release notes and include replacement guidance.

## Migration Notes for Breaking Changes

Every release with breaking API/config changes must include migration notes under `docs/migrations/`.

Required migration note path:

- `docs/migrations/vX.Y.Z.md`

Required migration note sections:

- Summary of breaking changes
- Compatibility impact
- Upgrade steps
- Rollback constraints
- Validation checklist

Use `docs/migrations/v2.0.0-template.md` as the template baseline.

## Previous Minor Compatibility Matrix

Compatibility baselines are declared in:

- `config/api_config_versioning_policy.json`
- `compatibility/api-config/previous_minor_matrix.json`

Each entry in the previous-minor matrix must define:

- prior release version (`release`)
- expected API contract version (`api_contract_version`)
- expected config schema version (`config_schema_version`)
- compatibility expectation (`expected_compatible`)

A release is promotion-eligible only when all declared previous minor compatibility entries validate as compatible.

## Validation and Release Gates

Run the deterministic policy gate:

- `kujo run scripts/run_api_config_versioning_review.kujo --interpreter`

CI workflow:

- `.github/workflows/api-config-versioning-review.yml`

Release-process linkage:

- `docs/release-process.md` requires the gate and this policy before promotion.
