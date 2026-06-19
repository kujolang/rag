# Next Session Enterprise Readiness Review - 2026-06-19

Scope: follow-on work after the June 19 hardening pass. The project is a strong production-oriented starter kit, but "universally useful" enterprise readiness still depends on validating deployment-specific workloads, integrations, and governance controls.

## This Session Closed

- [x] Confirmed tracked root layout remains intentionally minimal: `main.kujo`, docs, config, container files, and release metadata only.
- [x] Added deterministic, de-duplicated ingestion file discovery so index builds are more reproducible across filesystems.
- [x] Strengthened API redaction so `KUJO_RAG_API_REDACTION_VALUES` scrubs sensitive literals inside larger string fields.
- [x] Updated README positioning to describe production posture honestly and call out strict-mode deployment requirements.
- [x] Added focused regression coverage in `tests/test_unit.kujo` and `tests/test_redaction_policy.kujo`.

## Next Security Enhancements

- [ ] Add API JSON payload abuse guardrails for maximum nesting depth, array/object node count, and malformed UTF-8 or non-object payload edge cases.
- [ ] Add a config-drift gate that fails production-like runs when auth, encryption, strict mode, or ingest root scope drift from approved baselines.
- [ ] Add reverse-proxy header trust validation for forwarded IP, TLS termination assumptions, and required security headers.
- [ ] Expand audit coverage assertions for legal-hold start/stop, privacy delete/export, retention purge, and queue worker failures.

## Next Performance Enhancements

- [ ] Add query P95/P99 trend gates across small, medium, and large corpus profiles using the existing benchmark policy files.
- [ ] Add namespace-heavy cache-efficiency tests for query cache and embedding cache hit-rate floors.
- [ ] Add a startup-time budget gate for `serve` with production-like strict configuration.
- [ ] Profile large recursive ingest with deterministic discovery enabled and document any meaningful overhead or mitigation.

## Next Functionality Enhancements

- [ ] Add deterministic privacy export package manifests with checksums, schema version, namespace, generated-at timestamp, and legal-hold state.
- [ ] Add connector ingest idempotency verification for repeated external sync runs.
- [ ] Add partial-failure response contracts for export, delete, restore, connector ingest, and queued ingest workflows.
- [ ] Add an operator-facing enterprise quickstart that links auth, RBAC, audit, retention/legal hold, backup/restore, release gates, and rollback.

## Next Presentation Enhancements

- [ ] Add a short architecture diagram to README or `docs/adoption-playbook.md` showing ingest, parse, chunk, embed, store, retrieve, API, and ops gates.
- [ ] Add a "choose your deployment path" table for CLI-only, local API, team API, and regulated enterprise deployment.
- [ ] Add a crisp demo script that showcases Kujo language strengths: local-first setup, typed JSON outputs, strict config failures, and deterministic release gates.
- [ ] Add README badges or a compact release-gate status table once CI evidence is current.

## Suggested First Loop Next Session

Start with API JSON payload abuse guardrails because it improves security and robustness without requiring external services. Validate with `tests/test_security.kujo`, `tests/test_api_contract.kujo`, and `scripts/run_tests.kujo` using an explicit `KUJO_BIN`.
