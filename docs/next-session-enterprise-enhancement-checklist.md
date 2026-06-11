# Next Session Enterprise Enhancement Checklist

Scope: follow-on hardening and enterprise-readiness work after L053/UPR-072 closure.

## Execution Rules

- [ ] Run baseline gates before any edits: `tests/test_api_contract.kujo`, `tests/test_security.kujo`, `tests/test_retention_legal_hold_controls.kujo`, `tests/test_privacy_export_delete_workflows.kujo`, and `scripts/run_tests.kujo` with explicit `KUJO_BIN`
- [ ] Keep loop-boundary discipline: implement, validate, update docs/checklists, then commit
- [ ] For each item, attach evidence artifact paths under `results/` and reference them in docs

## Security

- [ ] Add API payload size abuse regression coverage for large nested JSON objects and malformed UTF-8 edge cases
- [ ] Expand legal-hold audit coverage: assert start/stop operations always emit immutable audit entries
- [ ] Add reverse-proxy hardening validation script for required headers and forwarded-IP trust-chain assumptions
- [ ] Add periodic config-drift check for critical production settings (`KUJO_RAG_STRICT_CONFIG`, encryption-at-rest, auth mode)

## Performance

- [ ] Add benchmark trend gate for query P95/P99 regressions across small/medium/large corpus tiers
- [ ] Add cache-efficiency regression tests for namespace-heavy workloads (query + embedding cache hit-rate floors)
- [ ] Add index-maintenance smoke benchmark in CI to detect compaction regressions early
- [ ] Add lightweight startup-time budget gate for `serve` mode in production-like configuration

## Functionality

- [ ] Add deterministic export package manifest for privacy exports (artifact checksums + schema version)
- [ ] Add connector ingest idempotency verification for repeated external sync runs
- [ ] Add structured partial-failure response contract tests for multi-step workflows (export/delete/restore)
- [ ] Add operator-facing "enterprise quickstart" flow doc linking auth, audit, retention, backup/restore, and release gates

## Release/Governance

- [ ] Create release-readiness scorecard draft with weighted pass/fail criteria and explicit blocker classes
- [ ] Add CI job that validates docs/code reference integrity for checklist-linked artifacts
- [ ] Add compliance matrix freshness alert when `last_reviewed_at_unix_ms` exceeds cadence window
- [ ] Define ownership rotation for unresolved compliance/security gaps with escalation SLA

## Root/Layout Hygiene

- [ ] Keep runtime-generated evidence in `results/` only; ensure no root-level transient files are tracked
- [ ] Validate `.gitignore` coverage for local tooling artifacts introduced during new loops
- [ ] Reconfirm top-level layout remains entrypoint/docs/config focused (no feature logic outside `src/` and `scripts/`)
