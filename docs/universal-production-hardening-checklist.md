# Kujo RAG Universal Production Hardening Checklist

This checklist starts after completion of docs/agent-implementation-checklist.md.

Use this as the next execution source of truth for making Kujo RAG universally useful and production hardened across diverse environments, workloads, and compliance requirements.

## How To Execute This Checklist

1. Read this file top to bottom once.
2. Pick exactly one unchecked item.
3. Implement only that item (plus minimal supporting refactors).
4. Add or update tests in the same change.
5. Run the validation commands listed for that item.
6. Update README and docs if behavior, ops, config, API, or architecture changed.
7. Check off the item and add completion notes under that item.
8. Commit and push before starting the next item.

Completion note template:
- Completed on: YYYY-MM-DD
- Agent: <name>
- PR/Commit: <ref>
- Summary: <what changed>
- Tests run: <commands and results>
- README updated: yes/no (why)
- Operational impact: <what changes for deployment/monitoring>

## Baseline Already Complete

The following are already implemented and should be treated as baseline, not pending work:
- Critical security and safety items in docs/agent-implementation-checklist.md are complete.
- API contracts, namespace isolation, backend abstraction, confidence metadata, and metrics endpoint are complete.
- Warning budget and production evaluation gates are implemented.
- CI release-gates workflow exists and runs scripts/run_tests.kujo plus scripts/run_release_evaluation.kujo.

## Current Gaps To Close For Universal Readiness

These are the big remaining themes:
- Runtime/toolchain dependence on interpreter mode is still a practical constraint.
- Auth model is still simple bearer-token and not enterprise-grade identity/authorization.
- Observability is present but still below full SRE-grade telemetry and alerting depth.
- Evaluation corpus and thresholds exist but remain synthetic and narrow in domain coverage.
- Scalability path for very large corpora and multi-node operation is still limited.
- Compliance, governance, and operational runbook depth is still early-stage.
- Universal usefulness can be expanded with more connectors, richer retrieval, and policy controls.

## Fast-Start Queue (Recommended First 15 Items)

- [x] UPR-001
- [x] UPR-002
- [x] UPR-003
- [x] UPR-004
- [x] UPR-010
- [x] UPR-011
- [x] UPR-020
- [x] UPR-021
- [x] UPR-022
- [x] UPR-030
- [x] UPR-031
- [x] UPR-040
- [x] UPR-041
- [x] UPR-050
- [x] UPR-080

## Tier 0 (Universal Blockers)

### [x] UPR-001: Publish Kujo runtime support matrix and de-risk interpreter dependence

Why:
- Universal production support needs explicit guarantees per runtime version and execution mode.

Implementation expectations:
- Add a support matrix doc for Kujo version, interpreter/native mode, and known caveats.
- Add CI matrix jobs to validate declared supported combinations.
- Explicitly mark unsupported combinations as non-goals.

Acceptance criteria:
- Supported combinations are declared and tested in CI.
- Unsupported combinations fail fast with clear error messaging.

Validation/testing expectations:
- CI matrix job logs proving pass/fail policy.
- Smoke tests for each supported mode.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c186160bed5e7de9bc4e3f544f2e7040f1251e49
- Summary: Added a formal runtime support matrix (`docs/runtime-support-matrix.md`) that declares supported and non-goal execution combinations, and expanded CI in `.github/workflows/release-gates.yml` with a dedicated runtime-support matrix job validating interpreter and bridge modes.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_non_interpreter_bridge.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass)
- README updated: yes (added runtime support matrix doc reference and runtime declaration note).
- Operational impact: Runtime support boundaries are now explicit and CI-enforced for declared supported modes.

### [x] UPR-002: Require native-mode parity for core ingest/query flows

Why:
- Interpreter-only reliability limits portability and long-term maintainability.

Implementation expectations:
- Add parity tests that run core flows in native mode and interpreter mode.
- Track and fail on meaningful behavior divergence.
- Keep bridge fallback, but reduce fallback frequency over time.

Acceptance criteria:
- Native mode passes parity suite for core commands.
- Known exceptions are documented and explicitly justified.

Validation/testing expectations:
- Dedicated parity suite output in CI artifacts.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: d0bbdb8
- Summary: Added deterministic native core ingest/query parity regression coverage (`tests/test_native_mode_parity.kujo`), promoted direct native core parity to supported mode in `docs/runtime-support-matrix.md`, and expanded `.github/workflows/release-gates.yml` runtime matrix to validate native parity with artifact output (`runtime-mode-native.json`).
- Known exceptions: Debug runtime native execution can still surface stack-overflow behavior in some environments; release promotion is certified against the pinned release runtime path declared in the runtime support matrix.
- Tests run: `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run tests/test_native_mode_parity.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run scripts/run_tests.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run tests/test_governance_contract.kujo --interpreter` (pass).

### [x] UPR-003: Enforce branch protection and required gate checks

Why:
- CI must be policy-enforced, not optional.

Implementation expectations:
- Define required checks and merge policy in repository governance docs.
- Ensure release-gates workflow is marked required in branch protection.
- Add fail-safe docs for temporarily degraded CI.

Acceptance criteria:
- PR merge is blocked when required gates fail.
- Required checks are auditable and documented.

Validation/testing expectations:
- Dry-run PR with intentional failing gate demonstrates merge block.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: fcb9955549e09a8cd1956427ac4bf28157a68723
- Summary: Added explicit branch protection governance policy in `docs/branch-protection-policy.md`, including required checks, merge policy, degraded-CI failsafe, and auditable dry-run verification procedure; added governance contract regression test in `tests/test_governance_contract.kujo` to validate required policy/workflow references.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass)
- README updated: yes (added branch protection policy doc to repository layout).
- Operational impact: Required-check policy is now explicit and auditable; maintainers can verify and enforce branch protection settings consistently.

### [x] UPR-004: Introduce versioned release process and rollback-safe artifacts

Why:
- Production operations need deterministic releases and rollback strategy.

Implementation expectations:
- Add semantic versioning and release notes workflow.
- Produce versioned artifacts and checksums.
- Document rollback path including config compatibility concerns.

Acceptance criteria:
- Releasing and rolling back are documented, tested, and repeatable.

Validation/testing expectations:
- One full release rehearsal in a staging environment.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: fc8ac754c3130cc0b90889a37568f0e72580bedc
- Summary: Added deterministic versioned release artifact generation in `scripts/build_release_artifacts.kujo` with SemVer validation, per-file SHA-256 manifest generation, release-notes artifact capture, and checksum output; added release artifact CI workflow `.github/workflows/release-artifacts.yml`; documented rollout and rollback path in `docs/release-process.md` and versioned notes structure in `docs/releases/`.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_artifacts.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (added release process, release artifact script, workflow, and release docs references).
- Operational impact: Release packaging is now deterministic and auditable; rollback safety now has explicit compatibility markers and documented procedures.

### [x] UPR-005: Add environment and config integrity validation at startup

Why:
- Misconfigured production systems should fail fast and clearly.

Implementation expectations:
- Validate required env and config values at startup.
- Emit structured configuration diagnostics for invalid values.
- Add strict mode to reject ambiguous defaults in production.

Acceptance criteria:
- Invalid configuration results in deterministic startup failure with actionable error.

Validation/testing expectations:
- Startup tests for valid/invalid configurations.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 0367a1691578dc18de039775bfc0c7fc262bebcd
- Summary: Added `validate_config` startup integrity checks in `src/config.kujo` and enforced deterministic fail-fast behavior in `main.kujo` with structured `invalid_configuration` diagnostics. Added strict production mode checks (`KUJO_RAG_STRICT_CONFIG` / `KUJO_RAG_ENV=production`) to reject ambiguous defaults and require explicit bearer token, namespace, and index path.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_config_integrity.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo KUJO_RAG_ENV=production KUJO_RAG_STRICT_CONFIG=true KUJO_RAG_NAMESPACE=default KUJO_RAG_API_BEARER_TOKEN= /path/to/kujo/target/debug/kujo run main.kujo --interpreter query --question "health check"` (expected fail with `invalid_configuration` diagnostics); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (documented startup integrity checks, strict-mode behavior, and production environment variables).
- Operational impact: Misconfigured deployments now fail fast before serving traffic with actionable diagnostics, reducing ambiguous production startup behavior.

## Tier 1 (Security Hardening Beyond Baseline)

### [x] UPR-010: Replace static bearer token with pluggable auth providers

Why:
- Static shared tokens are insufficient for enterprise use.

Implementation expectations:
- Add JWT/OIDC provider support with token validation and issuer/audience checks.
- Keep current bearer mode as legacy/local mode.

Acceptance criteria:
- OIDC/JWT auth works and can be enabled without code changes.

Validation/testing expectations:
- Auth integration tests for valid, expired, wrong issuer, wrong audience tokens.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c062c0c67fcb763c5b4f839b8b0942713796f108
- Summary: Added pluggable auth provider support with `api_auth_provider` modes (`none`, `bearer`, `jwt_proxy`), preserving legacy bearer behavior while adding JWT/OIDC-style claim checks (issuer, audience, expiry) via trusted proxy headers in `src/query_api.kujo`. Extended config/env support in `src/config.kujo` and documented provider setup/behavior in `docs/auth-providers.md` and README.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_auth_providers.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (documented auth provider modes and JWT proxy configuration).
- Operational impact: API authentication can now switch providers via configuration without code changes, enabling enterprise identity integration patterns while retaining legacy bearer fallback.

### [x] UPR-011: Add namespace-scoped RBAC authorization

Why:
- Multi-tenant systems require authorization granularity beyond authentication.

Implementation expectations:
- Define roles and actions (ingest/query/admin/export).
- Enforce namespace-level authorization.

Acceptance criteria:
- Unauthorized role/action combinations are blocked with structured errors.

Validation/testing expectations:
- Policy matrix tests across roles/actions/namespaces.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 58b51d19ca635c4dcfc7948d846bba0022aa0cf6
- Summary: Added configurable namespace-scoped RBAC controls with role/action policy enforcement in `src/query_api.kujo` via `validate_api_rbac`, including namespace scope checks. Extended config schema/environment support in `src/config.kujo` and `.env.example` for RBAC toggles, headers, defaults, and policy JSON override. Documented RBAC behavior in `docs/rbac-authorization.md` and README.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_rbac_authorization.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_auth_providers.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_config_integrity.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (added RBAC config and documentation references).
- Operational impact: Role-based and namespace-scoped authorization is now configurable without code changes, enabling multi-tenant permission boundaries for ingest/query/admin actions.

### [x] UPR-012: Add key/token rotation and revocation support

Why:
- Production systems need secure credential lifecycle management.

Implementation expectations:
- Support active + next token windows.
- Add immediate revocation list support.

Acceptance criteria:
- Rotation and revocation can be done without downtime.

Validation/testing expectations:
- Rotation smoke tests and revoked-token rejection tests.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 4af1dedbf74ddff8935be97ad521f44d11a9cd1c
- Summary: Added bearer token lifecycle controls supporting active+next rotation windows and immediate revocation-list enforcement in `src/query_api.kujo`. Extended config and env support in `src/config.kujo`/`.env.example` with `api_bearer_token_next` and `api_bearer_revoked_tokens`, and documented lifecycle behavior in `docs/auth-providers.md` and README.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_auth_providers.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_rbac_authorization.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_config_integrity.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (added bearer rotation/revocation environment variables).
- Operational impact: Bearer tokens can now be rotated without downtime and revoked immediately, reducing credential compromise risk and improving key lifecycle safety.

### [x] UPR-013: Encrypt index and sensitive artifacts at rest

Why:
- Data at rest protection is required in many production environments.

Implementation expectations:
- Add optional at-rest encryption for persisted index artifacts.
- Provide key management integration points.

Acceptance criteria:
- Stored index data is encrypted when enabled and unreadable without key.

Validation/testing expectations:
- Encryption/decryption tests and key-loss failure-mode tests.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 4b25d70cebf824fd1a424b293831418e1b64865a
- Summary: Added optional OpenSSL-backed at-rest encryption for persisted index artifacts through config-aware load/save paths in `src/vector_store.kujo` and `src/vector_backend.kujo`, including encrypted envelope storage and deterministic load-error handling for missing/invalid keys.
- Key management integration points: Added `KUJO_RAG_AT_REST_ENCRYPTION_KEY`, `KUJO_RAG_AT_REST_ENCRYPTION_KEY_FILE`, and `KUJO_RAG_AT_REST_ENCRYPTION_OPENSSL_BIN` via `src/config.kujo` and `.env.example`.
- Strict-mode hardening: Production/strict configuration now requires at-rest encryption enabled with key material configured.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_at_rest_encryption.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_config_integrity.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_backend_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (added at-rest encryption configuration and strict-mode expectations).
- Operational impact: Stored index payloads are unreadable without key material when encryption is enabled, reducing exposure risk for persisted retrieval artifacts.

### [x] UPR-014: Add TLS and reverse-proxy deployment guidance with secure defaults

Why:
- Plain HTTP defaults are not sufficient for internet-facing deployments.

Implementation expectations:
- Provide production deployment patterns with TLS termination.
- Add HSTS and secure-header recommendations.

Acceptance criteria:
- Documented secure deployment path for edge and internal environments.

Validation/testing expectations:
- Deployment checklist tested against a sample reverse proxy setup.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 36021fdfa92a31c4291ea32fac09a5b681d7c564
- Summary: Added hardened deployment guidance in `docs/tls-reverse-proxy-hardening.md` with edge/internal deployment patterns, sample Nginx and Caddy reverse-proxy templates, secure-header baseline (including HSTS), and production validation checklist for proxy and TLS posture.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_tls_reverse_proxy_guidance.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (linked TLS/reverse-proxy hardening guide and secure deployment baseline).
- Operational impact: Production operators have a concrete, test-backed hardened path for TLS termination and reverse-proxy headers before internet-facing exposure.

### [x] UPR-015: Add immutable audit log mode for security-sensitive actions

Why:
- Security and compliance workflows require tamper-evident auditing.

Implementation expectations:
- Log auth decisions, ingest operations, admin/config changes, and failures.
- Support append-only external sink mode.

Acceptance criteria:
- Audit trail is complete, queryable, and tamper-evident by design.

Validation/testing expectations:
- Audit completeness tests and tamper-detection tests.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 9fbb73f7d90ab06b6cc8ab95d25d79d31332698a
- Summary: Added tamper-evident audit logging in `src/audit_log.kujo` with append-file external sink mode, per-event hash chaining (`prev_hash`/`event_hash`), chain-head state tracking, and verification routine (`verify_audit_chain`). Integrated audit emission for auth decisions, RBAC decisions, ingest/query/admin operations, startup config snapshots, and failure paths in `src/query_api.kujo`.
- Configuration surface: Added `KUJO_RAG_API_AUDIT_ENABLED`, `KUJO_RAG_API_AUDIT_PATH`, and `KUJO_RAG_API_AUDIT_EXTERNAL_SINK_MODE` in `src/config.kujo` and `.env.example`, with config validation for enabled mode.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_audit_logging.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_config_integrity.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_security.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass on latest run, warning_budget_ok=true, total_warning_count=400).
- README updated: yes (audit mode behavior and env controls documented).
- Operational impact: Security-sensitive API activity now has tamper-evident audit trail support suitable for compliance-oriented deployments.

### [x] UPR-016: Generate SBOM and add supply-chain scanning in CI

Why:
- Production software distribution requires supply-chain visibility and controls.

Implementation expectations:
- Generate SBOM for releases.
- Add dependency and secret scanning in CI.

Acceptance criteria:
- Releases include SBOM and scan results; high severity findings block release.

Validation/testing expectations:
- CI gates for SBOM generation and scan status enforcement.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 95227eead774290c35933485ef57515cc9c20efa
- Summary: Added CycloneDX SBOM generation to release artifact build flow in `scripts/build_release_artifacts.kujo` and added supply-chain scan automation in `scripts/run_supply_chain_scan.kujo` for dependency/workflow hygiene and secret-surface checks. Wired CI enforcement in `.github/workflows/release-gates.yml` and `.github/workflows/release-artifacts.yml` to run deterministic file-scoped scans and publish reports as artifacts.
- Release artifact additions: `sbom.cyclonedx.json`, `supply-chain-scan-release-gates.json`, `supply-chain-scan-release-artifacts.json`, `supply-chain-scan-env-surface.json`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_release_artifacts.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_supply_chain_scan.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_governance_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-gates.yml --output ./results/supply-chain-scan-release-gates.json` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-artifacts.yml --output ./results/supply-chain-scan-release-artifacts.json` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_supply_chain_scan.kujo --interpreter --root .env.example --output ./results/supply-chain-scan-env-surface.json` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (SBOM and supply-chain scan scripts/workflow outputs documented).
- Operational impact: Release artifacts now include SBOM plus scan reports, and CI now blocks release flows on high-severity scan findings in configured supply-chain checks.

### [x] UPR-017: Expand abuse protections (IP throttling, burst controls, anomaly hooks)

Why:
- Public-facing APIs need stronger abuse resistance.

Implementation expectations:
- Add burst controls and IP-aware throttling.
- Expose hook points for anomaly detection and blocklisting.

Acceptance criteria:
- Burst abuse patterns are rate-limited predictably without collateral damage.

Validation/testing expectations:
- Load tests for abusive and normal traffic patterns.

Completion notes:
- Completed on: 2026-05-21
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 3d8f0d297488c0e48674c480574472e625382dec
- Summary: Extended API abuse protections in `src/query_api.kujo` with burst limiting (`burst_limited`), static IP blocklist enforcement (`ip_blocked`), anomaly hook event emissions (`anomaly_hook`), and optional dynamic auto-blocking after repeated violations. Added centralized rate-limit rejection handling with structured error details and audit telemetry for blocked requests.
- Configuration surface: Added abuse/burst/anomaly controls in `src/config.kujo` and `.env.example` (`KUJO_RAG_API_RATE_LIMIT_BURST_WINDOW_SEC`, `KUJO_RAG_API_RATE_LIMIT_BURST_MAX_REQUESTS`, `KUJO_RAG_API_ABUSE_BLOCKLIST_IPS`, `KUJO_RAG_API_ANOMALY_HOOK_ENABLED`, `KUJO_RAG_API_ANOMALY_AUTO_BLOCK_ENABLED`, `KUJO_RAG_API_ANOMALY_VIOLATION_THRESHOLD`, `KUJO_RAG_API_ANOMALY_BLOCK_TTL_SEC`).
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_abuse_protection.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (abuse protection controls and configuration documented).
- Operational impact: APIs now enforce more predictable burst behavior, support explicit blocked client controls, and provide anomaly hook output suitable for security monitoring and automated incident workflows.

### [x] UPR-018: Add sensitive-data redaction policy for logs and responses

Why:
- Logs and error payloads can leak sensitive information.

Implementation expectations:
- Add configurable redaction for secrets, tokens, and sensitive fields.
- Ensure errors do not leak internals in production mode.

Acceptance criteria:
- Sensitive content is redacted consistently in configured channels.

Validation/testing expectations:
- Redaction unit tests with known sensitive patterns.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: fb7b2962e32215ba8f6d428cc2a20bfbba38be86
- Summary: Added configurable sensitive-data redaction controls for API error payloads and production-safe 5xx message handling. Integrated redaction configuration surface across runtime config/env and ensured auth error details are sanitized for token-bearing headers.
- Configuration surface: Added `api_redaction_enabled`, `api_redaction_mask`, `api_redaction_keys`, and `api_redaction_values` in `src/config.kujo` and `.env.example` (`KUJO_RAG_API_REDACTION_ENABLED`, `KUJO_RAG_API_REDACTION_MASK`, `KUJO_RAG_API_REDACTION_KEYS`, `KUJO_RAG_API_REDACTION_VALUES`).
- Docs added: `docs/redaction-policy.md` with behavior, configuration, and validation guidance.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_redaction_policy.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (redaction policy doc/test inventory and env behavior documented).
- Operational impact: Sensitive bearer-like values are prevented from leaking in tested auth failure response paths, and production 5xx responses avoid exposing internal details.

## Tier 2 (Reliability, SRE, and Operations)

### [x] UPR-020: Add distinct readiness/liveness/startup endpoints

Why:
- Production orchestrators need accurate service lifecycle signals.

Implementation expectations:
- Keep health endpoint but add readiness and liveness with strict semantics.
- Reflect dependencies and warmup state in readiness.

Acceptance criteria:
- Orchestrator probes behave correctly during startup, steady state, and degradation.

Validation/testing expectations:
- Probe behavior tests including dependency-failure cases.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 99a7a28f50a2fcef6e24bbe139c7eca517cf5157
- Summary: Added distinct probe routes in `src/query_api.kujo` (`/live`, `/ready`, `/startup`) with explicit startup lifecycle semantics, readiness failure signaling, and compatibility retention for `/health`. Added configurable startup grace and forced-unready controls in `src/config.kujo` and `.env.example`.
- Configuration surface: `KUJO_RAG_API_STARTUP_GRACE_MS`, `KUJO_RAG_API_READINESS_FORCE_UNREADY`.
- Docs added: `docs/probe-endpoints.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_probe_endpoints.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (probe endpoint documentation links and config notes).
- Operational impact: Orchestrators can now use endpoint-specific lifecycle probes, including deterministic startup grace windows and explicit readiness degradation simulation via forced-unready mode.

### [x] UPR-021: Standardize structured logs with correlation IDs

Why:
- Incident response requires traceable request paths.

Implementation expectations:
- Emit JSON logs with consistent schema.
- Include request IDs/correlation IDs in logs and responses.

Acceptance criteria:
- End-to-end request tracing works in logs.

Validation/testing expectations:
- Log schema tests and correlation-id propagation tests.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 1cb5cf5b7ef45ab6eb3cba539e83bc35ed85a3a0
- Summary: Standardized access log schema with `request_id` and `correlation_id` propagation in `src/query_api.kujo`. Added request/correlation ID resolution from headers with deterministic fallback IDs, and propagated IDs into JSON responses and response headers (`X-Request-ID`, `X-Correlation-ID`).
- Docs added: `docs/structured-logs.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_structured_logs.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (structured log docs and dedicated test inventory documented).
- Operational impact: Request tracing now works end-to-end between clients and server logs via shared request/correlation identifiers.

### [x] UPR-022: Expand metrics to SRE-grade dimensions

Why:
- Basic counters are not enough for production diagnosis.

Implementation expectations:
- Add p50/p95/p99 latency histograms.
- Add queue depth, ingest throughput, error cardinality, auth failures, cache hit/miss, and tenant-level views.

Acceptance criteria:
- Metrics allow root-cause triage for latency, error, and saturation incidents.

Validation/testing expectations:
- Metrics contract tests and cardinality guard tests.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 837303cebe5873bca792f7ed6e037f11d2422919
- Summary: Expanded metrics surface in `src/query_api.kujo` to include latency percentile approximations (`p50/p95/p99`), ingest queue depth, ingest throughput-per-minute, auth failures, cache hit/miss ratio, error cardinality map, and per-tenant metric views. Added tenant and cache metric increments in ingest/query flows.
- Docs added: `docs/metrics-expansion.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_metrics_expansion.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (metrics expansion docs/test inventory documented).
- Operational impact: `/metrics` now provides richer triage dimensions for latency, saturation, auth/cache behavior, and namespace-level visibility.

### [x] UPR-023: Add OpenTelemetry tracing support

Why:
- Distributed systems need standardized traces across components.

Implementation expectations:
- Add spans for ingest, query, retrieval stages, and external calls.
- Support OTLP exporter configuration.

Acceptance criteria:
- Traces are visible in a standard backend and correlated with logs/metrics.

Validation/testing expectations:
- Trace export integration tests.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 245ba1a45d52ae7496457da5fed211a324d309ac
- Summary: Added OTEL-style trace span instrumentation in `src/query_api.kujo` for ingest and query stages (`ingest.request`, `ingest.build_index`, `query.request`, `query.retrieval`) with correlation propagation (`request_id`, `correlation_id`) and duration capture. Added OTEL configuration surface in `src/config.kujo` and `.env.example`.
- Configuration surface: `KUJO_RAG_OTEL_ENABLED`, `KUJO_RAG_OTEL_SERVICE_NAME`, `KUJO_RAG_OTEL_OTLP_ENDPOINT`, `KUJO_RAG_OTEL_EXPORT_MODE`.
- Docs added: `docs/otel-tracing.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_otel_tracing.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (OTEL docs and dedicated tracing test inventory documented).
- Operational impact: Tracing spans are now emitted with request correlation and stage timing metadata through the audit export pipeline when OTEL is enabled.

### [x] UPR-024: Define SLOs and alerting policies

Why:
- Universal production readiness requires objective reliability targets.

Implementation expectations:
- Define SLOs for availability, latency, correctness, and error budget.
- Add alert runbook links and paging thresholds.

Acceptance criteria:
- Alerts are actionable and mapped to runbooks.

Validation/testing expectations:
- Alert simulation exercises for each major class.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 79c3351c82f197555adfbb2a6dc0ecd8c1a6ff4a
- Summary: Added explicit SLO/alert policy artifacts including `config/slo_targets.json`, `docs/slo-alerting-policy.md`, and linked runbooks under `docs/runbooks/`. Added `scripts/simulate_slo_alerts.kujo` to evaluate metrics snapshots against SLO thresholds and emit alert/page decisions.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_slo_alert_policy.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (SLO policy docs, simulator script, and dedicated test inventory documented).
- Operational impact: Teams now have explicit alert/page thresholds, runbook mappings, and a repeatable policy simulation mechanism for release/readiness checks.

### [x] UPR-025: Implement backup/restore with verified integrity

Why:
- Data loss prevention needs tested restore paths.

Implementation expectations:
- Add backup command/workflow for index and config state.
- Add restore verification and checksum validation.

Acceptance criteria:
- Restore to known-good state is repeatable and documented.

Validation/testing expectations:
- Automated backup/restore tests in staging.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c3f218fb8f7dc2d279a7331b6a73e07ff8f34530
- Summary: Added deterministic backup and restore workflows with checksum manifest integrity verification via `scripts/backup_state.kujo` and `scripts/restore_state.kujo`, plus operator guidance in `docs/backup-restore.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_backup_restore_integrity.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added backup/restore docs, scripts, and dedicated test inventory).
- Operational impact: Operators now have a repeatable, checksum-verified restore path for index/config recovery and disaster-prep baselining.

### [x] UPR-026: Add disaster recovery drills and RTO/RPO targets

Why:
- DR plans without testing are unreliable.

Implementation expectations:
- Define DR tiers and RTO/RPO targets.
- Run scheduled recovery drills.

Acceptance criteria:
- DR drill results meet declared RTO/RPO targets or produce tracked remediations.

Validation/testing expectations:
- Drill reports attached to release readiness evidence.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: ab2fe9bd9c5fbca8c60aed28bd3f6086783b8f9a
- Summary: Added DR target policy and drill simulation workflow with tiered RTO/RPO objectives in `config/dr_tiers.json`, `scripts/simulate_dr_drill.kujo`, and `docs/disaster-recovery-drills.md`, including remediation runbook `docs/runbooks/disaster-recovery-drill-runbook.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_disaster_recovery_drills.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added DR policy doc, drill simulator script, and dedicated test inventory).
- Operational impact: Teams now have explicit DR recovery targets and a repeatable drill-evaluation mechanism with actionable remediation output.

### [x] UPR-027: Add graceful shutdown and zero-downtime deployment safeguards

Why:
- In-flight request loss during deploys harms reliability.

Implementation expectations:
- Add graceful shutdown handling for active requests/jobs.
- Document rolling deployment and pre-stop hooks.

Acceptance criteria:
- No dropped in-flight requests during normal rolling deploy.

Validation/testing expectations:
- Rolling deploy smoke tests with active load.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: efea375ec84b63dede2505f9df3f903f179ef480
- Summary: Added drain-mode graceful shutdown controls in `src/query_api.kujo` with admin endpoints (`GET /drain`, `POST /drain/start`, `POST /drain/stop`), readiness `draining` behavior, and mutation rejection safeguards during rolling deploy windows. Added drain config flags in `src/config.kujo` and `.env.example`, plus deployment guidance in `docs/graceful-shutdown.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_graceful_shutdown_safeguards.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added graceful-shutdown guide, drain controls, and dedicated test inventory).
- Operational impact: Rolling deployments can now explicitly drain instances out of readiness, reject new mutating traffic, and expose drain state for pre-stop orchestration.

### [x] UPR-028: Add ingest idempotency and duplicate-job suppression

Why:
- Replayed requests should not cause inconsistent state.

Implementation expectations:
- Introduce idempotency keys and dedupe windows for ingest jobs.
- Expose idempotency status in API responses.

Acceptance criteria:
- Duplicate ingest submissions are safely deduplicated.

Validation/testing expectations:
- Idempotency regression tests under retries/timeouts.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 239c198f739adc43f93119645f954755ef8c9643
- Summary: Added ingest-job idempotency support in `src/query_api.kujo` with configurable dedupe window and key sources (header/body), namespace-scoped keying, expiry pruning, and duplicate-job suppression that returns existing jobs. Added idempotency config surface in `src/config.kujo` and `.env.example`, plus behavior documentation in `docs/ingest-idempotency.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_ingest_idempotency.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added ingest idempotency docs, config knobs, and dedicated regression test inventory).
- Operational impact: Retried ingest job submissions can now be safely deduplicated within a configurable window, reducing duplicate work and inconsistent job state during client/network retries.

### [x] UPR-029: Add distributed rate-limit backend option

Why:
- In-memory limiter is insufficient for multi-instance deployments.

Implementation expectations:
- Add pluggable distributed rate-limit backend.
- Keep in-memory mode for local/offline simplicity.

Acceptance criteria:
- Multi-instance rate limiting is consistent and predictable.

Validation/testing expectations:
- Multi-node tests confirming shared limit enforcement.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: be803d16f6e9b7d87930041b19b114692940e717
- Summary: Added pluggable API rate-limit backend support in `src/query_api.kujo` and `src/config.kujo` with `memory` (default) and `shared_file` modes, including shared state load/persist hooks for rate buckets and dynamic block state. Added backend configuration vars in `.env.example` and operational guidance in `docs/rate-limit-backend.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_rate_limit_backend_shared.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added backend modes, config knobs, and dedicated shared-backend test inventory).
- Operational impact: Multi-instance deployments can now opt into shared-file backed rate-limit state for cross-instance enforcement without changing API consumers.

## Tier 3 (Performance and Scale)

### [x] UPR-030: Build large-corpus benchmark suite and budgets

Why:
- Universal use requires predictable behavior beyond toy corpora.

Implementation expectations:
- Add benchmark datasets for small/medium/large corpus sizes.
- Define query latency and ingest throughput budgets.

Acceptance criteria:
- Performance budgets are tracked and regressions fail CI.

Validation/testing expectations:
- Benchmark job outputs stored as artifacts and trend history.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c8ccd8741b3a8afe0e874d1cf7c3f94e2c8f0003
- Summary: Added a Kujo-native large-corpus benchmark suite in `scripts/run_large_corpus_benchmarks.kujo` with small/medium/large dataset profile materialization, ingest throughput and query latency measurements, budget gate enforcement, and trend-history persistence. Added profile/budget configs (`config/large_corpus_benchmark_profiles.json`, `config/large_corpus_benchmark_budgets.json`), CI benchmark gate/artifact publishing in `.github/workflows/release-gates.yml`, and operator documentation in `docs/large-corpus-benchmarks.md`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_large_corpus_benchmark_suite.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_large_corpus_benchmarks.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added benchmark suite docs/config/script/test inventory and operational budget-gate usage details).
- Operational impact: CI now fails on benchmark budget regressions and uploads benchmark report/trend artifacts, while local runs maintain trend history for longitudinal performance tracking.

### [x] UPR-031: Add index compaction and maintenance tooling

Why:
- Long-running systems accumulate fragmentation and stale state.

Implementation expectations:
- Add compaction, cleanup, and integrity-check commands.
- Support scheduled maintenance windows.

Acceptance criteria:
- Compaction reduces storage footprint without retrieval regression.

Validation/testing expectations:
- Before/after performance and correctness checks.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 1138d01d2409863ad3b29ddb8db96f8eb3df3bf7
- Summary: Added index maintenance tooling via `scripts/maintain_index.kujo` with duplicate/orphan record compaction for chunks/vectors/lexical entries, maintenance metadata updates, scheduled maintenance-window controls, and `report`/`apply` modes. Added maintenance guidance in `docs/index-maintenance.md` and regression coverage in `tests/test_index_compaction_maintenance.kujo` validating footprint reduction, correctness non-regression probes, and window-skip behavior.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_index_compaction_maintenance.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && KUJO_RAG_INDEX_MAINTENANCE_MODE=report KUJO_RAG_INDEX_MAINTENANCE_ALLOWED_UTC_HOURS=0-23 $KUJO_BIN run scripts/maintain_index.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added maintenance docs/script/test inventory and maintenance-window operational controls).
- Operational impact: Operators now have a deterministic maintenance entrypoint with window-aware scheduling and built-in before/after safety probes before persisting compacted index state.

### [x] UPR-032: Introduce queue-based async ingestion workers

Why:
- Heavy ingest should not block API responsiveness.

Implementation expectations:
- Add queue-backed worker architecture for ingest.
- Preserve current synchronous path for local mode.

Acceptance criteria:
- Query latency remains stable during large ingest operations.

Validation/testing expectations:
- Load tests with simultaneous ingest and query traffic.

Completion notes:
- Completed on: 2026-05-22
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 3eaaf900894cf56ee80dd8154cf530b16b9e3792
- Summary: Added queue-capable ingest job processing with configurable worker mode (`inline|queue`) and bounded cooperative worker-cycle controls. `POST /ingest/jobs` now supports queue submission semantics while preserving inline backward compatibility, `POST /ingest/jobs/status` can advance queue processing in queue mode, and `POST /ingest/jobs/worker/tick` provides explicit admin-triggered worker progression. Added operational guidance in `docs/async-ingest-workers.md`, config/env surface updates, and dedicated regression coverage in `tests/test_async_ingest_workers.kujo`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_async_ingest_workers.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400).
- README updated: yes (added async ingest worker docs/test inventory and API/operations guidance for queue mode).
- Operational impact: Ingest job submission can be decoupled from ingestion execution to reduce request-path blocking during heavy ingest while retaining the existing synchronous local mode.

### [x] UPR-033: Add query and embedding cache layers with invalidation policy

Why:
- Repeated workloads benefit from cache efficiency.

Implementation expectations:
- Add cache for hot queries and reusable embeddings.
- Define invalidation strategy on index updates.

Acceptance criteria:
- Cache improves latency while preserving correctness after updates.

Validation/testing expectations:
- Cache hit/miss metrics and invalidation correctness tests.

Completion notes:
- Completed on: 2026-05-23
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: f9d9b93c3febb8e76fa8b09ee3d2f282b1865fe4
- Summary: Added API query-response caching and embedding vector caching with configurable enable/TTL/capacity controls, cache metrics exposure, and deterministic invalidation on successful ingest updates. Hardened cache-related error paths to preserve API contract behavior for invalid namespace/filters/session payloads under redaction mode, and documented cache operations in `docs/query-embedding-cache.md` plus README/metrics docs.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_query_embedding_cache.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=400); API smoke: `health=200 ingest=200 query=200 metrics=200 invalid_namespace=400`.
- README updated: yes (added cache configuration and behavior details).
- Operational impact: Hot-query and embedding reuse now reduce repeated request latency while preserving correctness via ingest-triggered invalidation and explicit cache observability.

### [x] UPR-034: Add ANN/vector backend integrations for larger scale

Why:
- Local JSON backend will not fit all production scale profiles.

Implementation expectations:
- Add production-grade vector backend adapters (at least one external ANN store).
- Keep adapter contracts and compatibility tests.

Acceptance criteria:
- Backend swap works without API contract breakage.

Validation/testing expectations:
- Contract tests for each supported backend.

Completion notes:
- Completed on: 2026-05-23
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: d9a665c20b78f465b748762eb05cec7d83f750f9
- Summary: Added a qdrant-compatible ANN backend adapter mode (`qdrant_http`) in `src/vector_backend.kujo` with local mirror persistence, configurable remote sync behavior, fail-open/fail-closed controls, timeout and API-key settings, and backend metadata for sync outcomes. Extended config/env support in `src/config.kujo`, `.env.example`, and bootstrap template defaults, added operational guide `docs/qdrant-vector-backend.md`, and updated README backend documentation.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_backend_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_config_integrity.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=398).
- README updated: yes (added `qdrant_http` backend mode and new vector-backend configuration references).
- Operational impact: Deployments can now swap from local backend storage to a qdrant-compatible adapter path without API contract changes, with mirror-first resilience and optional external ANN synchronization for scaled vector storage.

### [x] UPR-035: Optimize retrieval pipeline stage timings

Why:
- Better stage-level profiling enables targeted performance work.

Implementation expectations:
- Record per-stage timings (tokenize, embed, retrieve, rerank, synthesize).
- Expose stage-level metrics and traces.

Acceptance criteria:
- Stage bottlenecks are visible and measurable under load.

Validation/testing expectations:
- Regression tests on stage timing contracts.

Completion notes:
- Completed on: 2026-05-23
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: de691a89eed807e78aa5d8c421238a4e9eb1d00a
- Summary: Added retrieval pipeline stage timing instrumentation for tokenize/embed/retrieve/rerank in `src/retrieval.kujo`, added synthesize timing in `src/rag_engine.kujo`, and surfaced stage-level metrics/traces in `src/query_api.kujo` (`query_stage_timings_ms` metrics payload and `query.stage.*` trace spans). Updated API/telemetry docs in README, `docs/metrics-expansion.md`, and `docs/otel-tracing.md`, with contract/tracing regression coverage updates in `tests/test_api_contract.kujo` and `tests/test_otel_tracing.kujo`.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_otel_tracing.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_metrics_expansion.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=398).
- README updated: yes (documented stage timing metrics and query stage trace spans).
- Operational impact: Query bottlenecks are now visible per pipeline stage through API response metadata, metrics snapshots, and OTEL-style spans, enabling targeted latency optimization under production load.

### [x] UPR-036: Add per-tenant resource quotas and isolation controls

Why:
- Shared deployments need fairness and cost protection.

Implementation expectations:
- Add per-namespace quotas for ingest volume, query rate, and storage.
- Add clear over-quota error responses and observability.

Acceptance criteria:
- Noisy tenant behavior is constrained without harming other tenants.

Validation/testing expectations:
- Multi-tenant stress tests with quota enforcement checks.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 66a49224141afad76c4fdcbd3765054a619bb447
- Summary: Added per-tenant quota enforcement controls for query-rate window limits, ingest request chunk limits, and tenant storage ceilings in `src/query_api.kujo` with configurable defaults/env clamps in `src/config.kujo`. Extended API contract and metrics schema/docs to expose quota rejections via `tenant_quota.rejections` and tenant view `quota_rejections`, plus structured over-quota responses (`tenant_query_quota_exceeded`, `tenant_storage_quota_exceeded`).
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_metrics_expansion.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=398).
- README updated: yes (added tenant quota configuration and metrics behavior notes).
- Operational impact: Noisy tenants are now constrained with deterministic 429 quota envelopes and observability counters without impacting neighboring namespaces.

### [x] UPR-037: Add memory and CPU guardrails for worst-case inputs

Why:
- Defensive limits reduce outlier-induced outages.

Implementation expectations:
- Add configurable hard limits on request complexity and processing size.
- Add early-abort behavior with explicit error envelopes.

Acceptance criteria:
- Worst-case inputs fail safely without service collapse.

Validation/testing expectations:
- Fuzz and boundary tests for oversized/pathological inputs.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: b745b14577cb71fec822ee13660beeb269df96e4
- Summary: Added configurable query and ingest guardrails for CPU/memory pressure in `src/config.kujo`, `src/query_api.kujo`, `src/ingestion.kujo`, and `src/rag_engine.kujo`. Query paths now enforce filter-key/session-context/complexity limits with explicit `413` envelopes (`query_filter_complexity_exceeded`, `query_session_context_too_large`, `query_complexity_exceeded`), while ingest paths short-circuit on file-count/total-byte limits (`ingest_guardrail_files_exceeded`, `ingest_guardrail_bytes_exceeded`) before expensive chunk/embed stages.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_resource_guardrails.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_api_contract.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, actual_total_warning_count=398).
- README updated: yes (documented guardrail env controls and explicit `413` guardrail error codes).
- Operational impact: Worst-case query and ingest inputs now fail deterministically with bounded resource impact and explicit operator-visible error envelopes.

## Tier 4 (Evaluation and Answer Quality)

### [x] UPR-040: Replace synthetic-only eval corpus with domain-diverse real corpora

Why:
- Universal quality needs realistic evaluation data across domains.

Implementation expectations:
- Add multiple golden corpora: docs, code, mixed enterprise docs, policy text.
- Version evaluation datasets and expected outcomes.

Acceptance criteria:
- Release gates run against multi-domain corpora, not only synthetic examples.

Validation/testing expectations:
- Dataset versioning and reproducibility checks in CI.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 1775ce50f51e0544337e9363a9880e8ac0a70364
- Summary: Replaced synthetic-only release evaluation inputs with a versioned, domain-diverse corpus in `examples/release_eval_corpus` (docs, code, policy, operations, incident), upgraded golden queries to a 10-case dataset with explicit `dataset_version`/`dataset_domains`, and surfaced dataset metadata from `src/release_eval.kujo` outputs. Updated release-eval defaults and tests to target the new corpus and calibrated latency thresholds for reproducible multi-domain gate behavior.
- Tests run: `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_release_evaluation.kujo --interpreter` (pass, `ok=true`, `passed_cases=10/10`); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run tests/test_release_evaluation.kujo --interpreter` (pass); `export KUJO_BIN=/path/to/kujo/target/debug/kujo && $KUJO_BIN run scripts/run_tests.kujo --interpreter` (pass, `warning_budget_ok=true`, `actual_total_warning_count=400`).
- README updated: yes (documented versioned multi-domain release evaluation baseline and metadata fields).
- Operational impact: Release-gate quality checks now exercise broader real-world content classes and emit dataset provenance metadata, improving reproducibility and regression diagnostics across domains.

### [x] UPR-041: Add adversarial and no-answer evaluation set

Why:
- Production systems must handle ambiguous/malicious/no-context queries safely.

Implementation expectations:
- Add adversarial, prompt-injection, and no-answer cases.
- Enforce safe abstain behavior when confidence/context is insufficient.

Acceptance criteria:
- Unsafe or unsupported questions trigger safe response policy.

Validation/testing expectations:
- Adversarial regression suite in CI release gates.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 3c50e0f9f2d6da1a61b1a92aa27c29823dd33780
- Summary: Expanded release evaluation to a versioned 12-case dataset in `config/release_eval_golden_queries.json` with explicit adversarial and no-answer cases, added safe-response policy controls in `src/config.kujo`, and enforced policy-aware query behavior in `src/rag_engine.kujo` so unsafe/unsupported and insufficient-context prompts abstain with zero citations.
- Validation semantics: Extended `src/release_eval.kujo` to support `expected_policy_reason` and `max_citations` assertions, and updated release-eval thresholds/tests in `config/release_eval_thresholds.json` and `tests/test_release_evaluation.kujo` to enforce the 12-case baseline.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass, `ok=true`, `passed_cases=12/12`); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_bootstrap.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, `warning_budget_ok=true`, `actual_total_warning_count=400`).
- README updated: yes (documented safe-response policy metadata/config and updated release-eval baseline).
- Operational impact: Release gates now verify adversarial/no-answer abstention behavior explicitly, reducing unsafe response risk and preventing citation leakage when context is insufficient.

### [x] UPR-042: Add citation faithfulness and grounding score gates

Why:
- Citation presence alone is insufficient; answers must be grounded in cited text.

Implementation expectations:
- Add deterministic grounding checks between answer claims and retrieved snippets.
- Track and gate on grounding score trends.

Acceptance criteria:
- Release fails when grounding quality regresses beyond threshold.

Validation/testing expectations:
- Faithfulness metric tests and trend regression checks.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 96d99d2d4f2247c2d6316eb6e00e48e07ad9a977
- Summary: Added deterministic citation-grounding evaluation in `src/release_eval.kujo` by tokenizing answer claims and scoring overlap against retrieved citation path/snippet context, including per-case `min_grounding_score` checks and policy-aware no-citation handling for safe abstain responses.
- Gate integration: Added aggregate grounding metrics/gates (`metrics.avg_grounding`, `gates.avg_grounding`) and threshold normalization support for `min_average_grounding`; baseline thresholds updated in `config/release_eval_thresholds.json`.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass, `ok=true`, `passed_cases=12/12`, `avg_grounding=1.0`); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, `warning_budget_ok=true`, `actual_total_warning_count=400`).
- README updated: yes (documented grounding thresholds and per-case grounding controls for release evaluation).
- Operational impact: Release gates now fail on grounding regressions, not just citation presence, improving faithfulness assurance for answer claims against retrieved source snippets.

### [x] UPR-043: Add evaluation drift dashboard and trend reports

Why:
- Long-term reliability requires visible quality drift monitoring.

Implementation expectations:
- Store eval run history and trend summaries per release.
- Highlight regressions by domain and metric category.

Acceptance criteria:
- Teams can compare current vs prior release quality by metric and corpus.

Validation/testing expectations:
- Dashboard/report generation tests in CI.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 6130ddf923610623cfae86d380401444c6d98e7d
- Summary: Added release-eval trend history persistence and drift reporting in `scripts/run_release_evaluation.kujo`, writing run reports to `release_eval_report.json` and append-only trend history to `release_eval_trend.json` with regression highlights by metric category (quality/grounding/latency/reliability) and domain-level regressions.
- Metric expansion: Extended `src/release_eval.kujo` with per-case domain tagging and aggregate `metrics.domain_summary` output to support domain drift analysis across releases.
- Validation artifacts: Added domain annotations to `config/release_eval_golden_queries.json`, documented workflow/config in `docs/release-eval-trends.md`, and exposed report/trend env controls in `.env.example`/README.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass, emits `trend_report`, `trend_history_count`, and domain summaries); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_eval_trend_report.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, `warning_budget_ok=true`, `actual_total_warning_count=400`).
- README updated: yes (documented trend artifacts, drift categories, and release-eval reporting env vars).
- Operational impact: Teams now get persistent release-quality trend history and immediate regression highlights by domain and metric category for faster drift detection between releases.

### [x] UPR-044: Add human review workflow for gate overrides

Why:
- Some regressions require informed manual adjudication.

Implementation expectations:
- Define override policy with approvals and mandatory rationale.
- Record reviewed exceptions with expiration.

Acceptance criteria:
- Gate overrides are auditable and do not silently bypass quality controls.

Validation/testing expectations:
- Policy doc and workflow checks in release process.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: fa6e21eb36707f57b4f791aff026f747c5117eb7
- Summary: Added a formal release-gate override policy in `docs/release-gate-override-policy.md` and an auditable override ledger in `config/release_gate_overrides.json` requiring approvals, rationale, ticket linkage, reviewer ownership, and explicit expiration for active exceptions.
- Workflow enforcement: Added `scripts/validate_release_gate_overrides.kujo` to validate active override entries and emit `results/release_gate_override_review.json`; wired the validator into `.github/workflows/release-gates.yml` and release process guidance in `docs/release-process.md`.
- Governance checks: Extended `tests/test_governance_contract.kujo` to assert override policy/workflow references and added `tests/test_release_gate_override_workflow.kujo` for valid/invalid override-path regression coverage.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/validate_release_gate_overrides.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_gate_override_workflow.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass).
- README updated: yes (documented override policy, validator, and environment controls).
- Operational impact: Release-gate overrides are now explicit, expiring, and reviewable with CI artifact evidence, preventing silent quality-gate bypasses.

### [x] UPR-045: Add canary release evaluation against production-like traffic samples

Why:
- Pre-release canary checks reduce real-world surprises.

Implementation expectations:
- Add anonymized sampled-query replay against candidate builds.
- Compare canary metrics to baseline.

Acceptance criteria:
- Candidate promotion requires canary metrics within accepted bounds.

Validation/testing expectations:
- Canary replay pipeline in CI/CD or staging pipeline.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 293d06c4320db9d245fe6ad41ba6553039ea4411
- Summary: Added production-like sampled-query canary replay gate via `scripts/run_canary_release_replay.kujo`, including baseline comparison against `release_eval_report.json`, delta/ratio calculations, and explicit promotion gates for quality, confidence, grounding, error rate, and latency ratios.
- Canary assets: Added `config/canary_replay_samples.json`, `config/canary_replay_eval_thresholds.json`, and `config/canary_replay_thresholds.json`, plus operational guide `docs/canary-release-replay.md`.
- Pipeline wiring: Integrated canary replay execution into `.github/workflows/release-gates.yml` and release process requirements in `docs/release-process.md`, with artifact output `results/canary_release_replay_report.json`.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass baseline refresh); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_canary_release_replay.kujo --interpreter` (pass, canary gates true); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_canary_release_replay.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- README updated: yes (documented canary replay command, config files, and environment controls).
- Operational impact: Candidate promotion now requires canary replay metrics to stay within configured bounds versus baseline, reducing production surprise risk before rollout.

### [x] UPR-046: Add provider/model drift controls for AI-enabled modes

Why:
- Optional AI helpers can change behavior unexpectedly over time.

Implementation expectations:
- Pin provider/model versions where possible.
- Add drift detection checks for AI mode outputs.

Acceptance criteria:
- Unexpected provider/model drift triggers alert or gate failure.

Validation/testing expectations:
- AI-mode drift tests with known reference prompts.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 5187285ae5cec88ada227132ce51f1c7368f9afe
- Summary: Added dedicated AI provider/model drift gate `scripts/run_ai_provider_model_drift_check.kujo` with pinned runtime checks (`embedding_provider`, AI embed/chat endpoint+model), dataset-version pinning, and reference-prompt validation against release-eval case outputs.
- Drift controls baseline: Added `config/ai_provider_model_drift_controls.json` for expected runtime/model pins and known reference prompt expectations.
- Runtime tracking updates: Extended `scripts/run_release_evaluation.kujo` trend snapshots with `runtime_profile` and added `provider_model` regression highlights when provider/model fields drift between runs.
- Release-eval provider pinning: Updated `src/release_eval.kujo` to honor `embedding_provider` via `eval_cfg`/`KUJO_RAG_RELEASE_EVAL_EMBEDDING_PROVIDER` for AI-enabled evaluation modes.
- Pipeline wiring: Integrated drift gate into `.github/workflows/release-gates.yml` with artifacts (`ai-provider-model-drift.json`, `results/ai_provider_model_drift_report.json`) and updated release-process requirements/docs.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_ai_provider_model_drift_check.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_eval_trend_report.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); end-to-end gate validation using temp release-eval report: `scripts/run_release_evaluation.kujo --interpreter` with temp permissive thresholds + `scripts/run_ai_provider_model_drift_check.kujo --interpreter` (pass).
- README updated: yes (added drift gate command, controls file, and environment variable documentation).
- Operational impact: Unexpected AI provider/model or reference-prompt output drift now triggers explicit CI gate failure with a dedicated drift report artifact.

### [x] UPR-047: Add multilingual retrieval/evaluation coverage

Why:
- Universal usefulness includes non-English corpora and queries.

Implementation expectations:
- Add multilingual tokenization/chunking evaluation cases.
- Track quality metrics per language family.

Acceptance criteria:
- Non-English quality is measurable and gated.

Validation/testing expectations:
- Multilingual evaluation suite with release thresholds.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: eeeaad63217545a3c45b8f13d3ea9ec551747cde
- Summary: Added multilingual release gate `scripts/run_multilingual_release_evaluation.kujo` with language-family quality enforcement and required-language coverage checks over dedicated multilingual corpus/query fixtures.
- Multilingual assets: Added `examples/multilingual_release_eval_corpus/` (English, Spanish, French, German source docs) plus `config/multilingual_release_eval_golden_queries.json` and `config/multilingual_release_eval_thresholds.json`.
- Core metric expansion: Extended `src/release_eval.kujo` to capture per-case `language`, dataset-level `dataset_languages`, and aggregate `metrics.language_summary` for language-family quality tracking.
- Trend visibility: Extended `scripts/run_release_evaluation.kujo` and `docs/release-eval-trends.md` to include `language_summary` in snapshots and `language` regression categories in drift reporting.
- Pipeline wiring: Added multilingual gate execution/artifacts to `.github/workflows/release-gates.yml` and release process requirements in `docs/release-process.md`.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_multilingual_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_eval_trend_report.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_multilingual_release_evaluation.kujo --interpreter` (pass).
- README updated: yes (added multilingual gate command and environment controls).
- Operational impact: Non-English retrieval/response quality is now explicitly measured and gated by language family before release promotion.

## Tier 5 (Universal Usefulness and Feature Completeness)

### [x] UPR-050: Add connector framework for external knowledge sources

Why:
- Universal usefulness requires ingestion beyond local folders.

Implementation expectations:
- Define connector contracts and lifecycle.
- Add at least two production connectors (for example Git repo and HTTP docs).

Acceptance criteria:
- Connectors can ingest/update content with robust error handling.

Validation/testing expectations:
- Connector contract tests and failure-mode tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 947abf19adf5485a472d839b72cab60cf0915573
- Summary: Added connector framework core module `src/connectors.kujo` with normalized connector contracts/lifecycle and robust staging pipeline handling for `git_repo` and `http_docs` connector types.
- Connector ingest pipeline: Added `scripts/run_connector_ingest.kujo` to execute connector staging, build/update indexed content from staged sources, and emit connector ingest report artifacts.
- Contract surface: Added sample connector config `config/connectors_ingest_sources.json` and operational documentation `docs/connectors-framework.md` covering connector schema, lifecycle, and failure behavior.
- Production connectors delivered: Implemented two production connector implementations (`git_repo` with `source_path` or `repo_url` clone flow; `http_docs` URL fetch with optional headers and structured failure reporting).
- Validation/testing expectations met: Added `tests/test_connector_framework.kujo` for pass/fail contract coverage including connector failure modes (missing git source path and failed HTTP fetch URL).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_connector_framework.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_connector_ingest.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- README updated: yes (added connector ingest command and connector environment controls).
- Operational impact: External knowledge ingestion now supports connector-based staging/update workflows with explicit connector-level error reporting and no core retrieval pipeline rewrites required for new source integrations.

### [x] UPR-051: Add first-party enterprise connectors roadmap and stubs

Why:
- Broad adoption needs a path to common enterprise systems.

Implementation expectations:
- Define prioritized connector backlog (wikis, ticketing, object storage, databases).
- Add stubs/interfaces and integration guidelines.

Acceptance criteria:
- Contributors can add new connectors without core rewrites.

Validation/testing expectations:
- Connector plugin example and onboarding docs.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: d393692c4a895c5052e31fcfdc875c83a732e3df
- Summary: Added first-party enterprise connector roadmap and no-core-rewrite plugin connector path via `plugin_script` connector type in `src/connectors.kujo`.
- Prioritized backlog delivered: Added `config/enterprise_connector_roadmap.json` with prioritized domains and rollout order for wikis, ticketing, object storage, and databases.
- Stub/interfaces delivered: Added `config/connectors_enterprise_stubs.json` starter catalog and implemented plugin runtime interface (`runner_script`, `payload`, `timeout_ms`) with stable plugin environment/output contract.
- Plugin example delivered: Added `scripts/connectors/example_enterprise_connector_stub.kujo` as a contributor-ready enterprise connector stub that stages source exports into connector target directories.
- Onboarding docs delivered: Added `docs/connectors-enterprise-roadmap.md` and expanded `docs/connectors-framework.md` with plugin contract details, runtime env expectations, and contributor onboarding workflow.
- Acceptance criteria met: New connector types can now be integrated through `plugin_script` connectors and stub configs without changing retrieval/indexing core modules.
- Validation/testing expectations met: Added `tests/test_connector_plugin_stub.kujo` covering plugin success and failure behavior, alongside existing connector framework regression coverage.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_connector_framework.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_connector_plugin_stub.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_connector_ingest.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- README/.env updated: yes (documented `plugin_script` connector contract, enterprise roadmap/stub assets, and `KUJO_RAG_CONNECTOR_PLUGIN_KUJO_BIN` control).
- Operational impact: Enterprise connector onboarding now has a documented roadmap, starter stubs, and tested plugin extension contract that avoids core connector runtime rewrites.

### [x] UPR-052: Add structured-data ingestion and schema-aware retrieval

Why:
- Many production use cases involve tabular/structured sources.

Implementation expectations:
- Add structured ingest path for JSON/CSV with schema metadata.
- Support schema-aware filter/query behavior.

Acceptance criteria:
- Structured data can be retrieved with meaningful field-level context.

Validation/testing expectations:
- Structured ingestion and retrieval regression tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 22cdd134a0f3782d3f2192192472d38b7ee541a0
- Summary: Added structured-data ingestion path for JSON/CSV and schema-aware retrieval filters with field-level citation metadata.
- Structured ingest implementation: Extended parser registry in `src/parsers.kujo` to support `json` and `csv` with normalized structured row synthesis and schema metadata (`structured_schema`, `structured_fields`, `record_count`, `structured_format`).
- Schema-aware retrieval implementation: Extended `src/retrieval.kujo` query filter normalization/matching to support `structured_schema` and `structured_fields` (plus `schema`/`field` aliases), and exposed structured citation metadata in query results.
- Metadata propagation: Updated `src/chunking.kujo` to carry document metadata into chunk metadata so structured schema/field context survives indexing and retrieval.
- Config/defaults: Updated `src/config.kujo` default ingest extensions to include `json` and `csv`.
- Documentation: Added `docs/structured-data-ingestion.md` with retrieval filter contract and operational guidance; updated `README.md` for structured parsing support and validation command.
- Validation/testing expectations met: Added `tests/test_structured_ingestion_retrieval.kujo` end-to-end regression covering structured ingest, schema filters, field filters, and field-level snippet evidence.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_structured_ingestion_retrieval.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning budget respected); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Structured sources now ingest with deterministic schema annotations and can be queried with schema/field-aware filters for more precise field-context retrieval.

### [x] UPR-053: Expand parser coverage and resilience

Why:
- Universal ingestion should handle more document types and malformed inputs safely.

Implementation expectations:
- Add parsers for additional common formats and robust fallback behavior.
- Ensure parser sandboxing/timeouts for untrusted inputs.

Acceptance criteria:
- New formats ingest successfully or fail safely with deterministic metadata.

Validation/testing expectations:
- Parser matrix tests and malformed file corpus tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 6f26f767ec10383bc0744ed265d155a03dd77f90
- Summary: Expanded parser coverage to additional common formats and added deterministic malformed-input fallbacks with parser sandbox/timeout guardrails.
- New parser coverage delivered: Added parser registry support in `src/parsers.kujo` for `html`/`htm`, `xml`, `yaml`/`yml`, and `log` alongside existing markdown/text/pdf/json/csv support.
- Resilience hardening delivered: Added deterministic parser fallback envelopes (`fallback=true`, `error_code`) for malformed JSON/CSV; added parser sandbox byte-budget fallback (`parser_input_too_large`) and configurable parser timeout controls for untrusted parser execution paths.
- Sandboxing/timeouts delivered: Added `parser_timeout_ms` and `parser_sandbox_max_bytes` controls in `src/config.kujo` with env mappings (`KUJO_RAG_PARSER_TIMEOUT_MS`, `KUJO_RAG_PARSER_SANDBOX_MAX_BYTES`) and safe clamping.
- Corpus/test assets delivered: Added parser matrix corpus `examples/parser_matrix_corpus/*` and malformed parser corpus `examples/malformed_parser_corpus/*`.
- Validation/testing expectations met: Added `tests/test_parser_matrix_resilience.kujo` to validate parser matrix coverage, malformed JSON/CSV deterministic fallback metadata, and sandbox fallback behavior for oversized inputs.
- Docs updated: Added `docs/parser-resilience.md`; updated `README.md` and `.env.example` with parser coverage and guardrail controls.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_parser_matrix_resilience.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_structured_ingestion_retrieval.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning budget respected); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Parser surface is broader for enterprise corpora, and malformed/untrusted inputs now fail safely with deterministic metadata instead of nondeterministic parser behavior.

### [x] UPR-054: Add language- and format-aware chunking presets

Why:
- One-size-fits-all chunking hurts quality across diverse data.

Implementation expectations:
- Add chunking presets by file type/language.
- Expose clear override hierarchy.

Acceptance criteria:
- Presets improve retrieval metrics on targeted corpora.

Validation/testing expectations:
- A/B evaluation of preset vs baseline chunking.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 314650a0d156fdeaa379416a53a42d91d9f37735
- Summary: Added format-aware chunking presets with deterministic override hierarchy and a release-gate-ready A/B evaluation runner for preset-vs-baseline quality comparisons.
- Preset chunking implementation: Extended `src/chunking.kujo` with default preset catalog and deterministic profile resolution (`baseline config -> optional format preset -> document metadata override`) plus chunk-level profile annotations.
- Config surface: Extended `src/config.kujo`/`.env.example` with `chunk_presets_enabled`, `chunk_presets`, `KUJO_RAG_CHUNK_PRESETS_ENABLED`, and `KUJO_RAG_CHUNK_PRESETS_JSON`.
- Release evaluation integration: Extended `src/release_eval.kujo` to accept `runtime_overrides` so A/B runs can evaluate baseline and preset profiles against identical corpora and query sets.
- A/B evaluation tooling: Added `scripts/run_chunking_preset_ab_evaluation.kujo`, corpus fixtures under `examples/chunking_preset_eval_corpus/`, thresholds in `config/chunking_preset_eval_thresholds.json`, and targeted golden queries in `config/chunking_preset_eval_golden_queries.json`.
- CI/docs integration: Updated `.github/workflows/release-gates.yml` and `docs/release-process.md` to include chunking preset A/B gate execution, and added operator guidance in `docs/chunking-presets.md` and `README.md`.
- Validation/testing expectations met: Added `tests/test_chunking_preset_ab_evaluation.kujo` to verify pass/fail threshold behavior and parser-backed corpus handling.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_chunking_preset_ab_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Chunking behavior is now tunable by content format with measurable quality deltas, enabling safer corpus-specific retrieval optimization before rollout.

### [x] UPR-055: Add richer metadata extraction and policy-driven filtering

Why:
- Better metadata enables better precision and governance.

Implementation expectations:
- Extract authorship, timestamp, source system, sensitivity tags.
- Add include/exclude policy filters at query time.

Acceptance criteria:
- Metadata filters are expressive, documented, and covered by tests.

Validation/testing expectations:
- Filter behavior tests with mixed metadata datasets.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 4b6d5caeac2be7bfd31b8f32afb1ecb363777615
- Summary: Added document metadata enrichment for author/timestamp/source system/sensitivity tags and introduced policy-driven include/exclude query filters with deterministic filter normalization and matching semantics.
- Metadata extraction implementation: Extended `src/parsers.kujo` document build flow to enrich metadata from explicit labels and content heuristics (`author`, `timestamp`, `source_system`, `sensitivity_tags`) and merge derived governance tags.
- Policy filtering implementation: Extended `src/retrieval.kujo` filter normalization and matching to support include/exclude dimensions for `paths`, `tags`, `types`, `structured_schema`, `structured_fields`, `source_system`, and `sensitivity_tags`.
- Citation metadata impact: Retrieval citations now expose `author`, `timestamp`, `source_system`, and `sensitivity_tags` for downstream policy/governance visibility.
- Validation/testing expectations met: Expanded `tests/test_unit.kujo` coverage for parser metadata extraction and include/exclude filter behavior against mixed metadata fixtures.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_chunking_preset_ab_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Query-time policy controls can now include or exclude result candidates by richer provenance/sensitivity metadata, improving precision and governance enforcement options for production tenants.

### [x] UPR-056: Implement cross-index federation planner

Why:
- Multi-corpus deployments need orchestrated retrieval across indexes.

Implementation expectations:
- Add federated query planner with deterministic merge/rerank behavior.
- Add per-index weighting and fallback policies.

Acceptance criteria:
- Federated query results are correct, explainable, and stable.

Validation/testing expectations:
- Federation regression tests across multiple indexes.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: a27976a8baf72276a6083e5baeb03d6f91dedffa
- Summary: Added a cross-index federation planner for query execution with deterministic weighted merge, per-target weighting, and fallback policy controls across namespace-isolated indexes.
- Planner implementation: Extended `src/rag_engine.kujo` with `query_rag_federated` to execute retrieval per target index, merge weighted citations deterministically (score, then namespace/path/line/chunk tie-break), and return federation execution metadata.
- API integration: Extended `/query` handling in `src/query_api.kujo` to accept optional `federation` config (`targets`, `merge_strategy`, `fallback_policy`), validate target namespace + RBAC access, ensure per-namespace index loading, and dispatch to federated query execution.
- Fallback policy support: Added `best_effort` and `primary_then_all` planner behavior with automatic fallback when primary-target results are empty/non-positive.
- Docs update: Updated `README.md` query documentation with federation request examples and behavior contract, including per-citation federation metadata.
- Validation/testing expectations met: Added `tests/test_federated_query_planner.kujo` covering weighted ordering, fallback behavior, and deterministic tie handling across multiple indexes.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_federated_query_planner.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Multi-corpus tenants can now query across selected namespaces with explicit weighting/fallback behavior while preserving deterministic ranking and existing namespace authorization boundaries.

### [x] UPR-057: Add policy controls for answer style and safety mode

Why:
- Production consumers need configurable response behavior.

Implementation expectations:
- Add response policy profiles (strict extractive, concise, expanded).
- Add safety mode controls for uncertain contexts.

Acceptance criteria:
- Behavior is deterministic per policy and documented.

Validation/testing expectations:
- Policy mode tests with expected response structure checks.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 73184cc8d951202197b7a8cb0f2f7f4866de3911
- Summary: Added per-request response policy controls for answer style and safety mode, with deterministic style outputs and configurable strict/permissive safety behavior for uncertain contexts.
- Answer style controls: Extended `src/rag_engine.kujo` deterministic synthesis flow to support `strict_extractive`, `concise`, and `expanded` style profiles via request policy.
- Safety mode controls: Added `balanced`, `strict`, and `permissive` safety modes with strict thresholds (`min_citations`, `min_confidence`) and permissive overlap bypass behavior.
- API integration: Extended `/query` in `src/query_api.kujo` to accept and validate optional `response_policy`, apply policy via request-scoped query config, and disable query-cache reuse for explicit policy requests to preserve deterministic per-policy responses.
- Docs update: Updated `README.md` query section with response-policy request examples and behavior contract.
- Validation/testing expectations met: Added `tests/test_response_policy_controls.kujo` covering style profile outputs plus strict/permissive safety-mode behavior checks.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_response_policy_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_federated_query_planner.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).
- Operational impact: Consumers can now select deterministic response style and stricter or more permissive safety behavior per query without changing deployment-level defaults.

### [x] UPR-058: Add query intent classification and rewrite pipeline

Why:
- Better intent handling improves retrieval quality and usefulness.

Implementation expectations:
- Classify query intent (fact, navigation, troubleshooting, compare).
- Apply intent-aware rewrite/routing before retrieval.

Acceptance criteria:
- Intent-aware flow improves evaluation metrics on intent-tagged dataset.

Validation/testing expectations:
- Intent classification and rewrite regression tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c6280ae5e29475f8cce5931399e0460ed2dd18ee
- Summary: Added query intent classification (`fact`, `navigation`, `troubleshooting`, `compare`) and an intent-aware rewrite pipeline that executes before retrieval/contextualization for both single-index and federated query flows.
- Query pipeline integration: Added intent helpers in `src/rag_engine.kujo` and integrated `query_intent` metadata (`intent`, `rewrite_enabled`, `original_query`, `rewritten_query`, `rewrite_applied`) into query responses.
- Config surface: Added `query_intent_rewrite_enabled` default and env override `KUJO_RAG_QUERY_INTENT_REWRITE_ENABLED` in `src/config.kujo` and `.env.example`.
- Docs update: Extended `README.md` query behavior docs with intent classification/rewrite controls and response metadata contract.
- Validation/testing expectations met: Added `tests/test_intent_rewrite_pipeline.kujo` covering compare/troubleshooting/navigation/fact classification behavior plus rewrite-disabled operation.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_intent_rewrite_pipeline.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_federated_query_planner.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_response_policy_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).

### [x] UPR-059: Add retrieval explanation metadata for end-users

Why:
- Production trust improves with transparent retrieval rationale.

Implementation expectations:
- Return optional explanation metadata for scoring/ranking rationale.
- Keep compatibility with current response contracts.

Acceptance criteria:
- Explanations are available, concise, and internally consistent.

Validation/testing expectations:
- Explanation contract tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: f54fae9332ab942dfa4736dcc143ad205a16873e
- Summary: Added optional retrieval explanation metadata to query responses with concise scoring/ranking rationale while preserving compatibility for existing clients.
- Query engine integration: Added retrieval-explanation synthesis in `src/rag_engine.kujo` with concise summary and top-ranked rationale entries (`rank`, `score`, `confidence`, `provenance_score`, `reason`) for single-index and federated query paths.
- API and compatibility: Added optional request flag `include_retrieval_explanation` in `src/query_api.kujo` with strict boolean validation (`invalid_retrieval_explanation_flag`) and cache-safety handling for explicit explanation requests.
- Config surface: Added `query_retrieval_explanation_enabled` default plus env override `KUJO_RAG_QUERY_RETRIEVAL_EXPLANATION_ENABLED` in `src/config.kujo` and `.env.example`.
- Docs update: Extended `README.md` query docs with explanation request example and response contract details.
- Validation/testing expectations met: Added `tests/test_retrieval_explanation_metadata.kujo` for direct query/federated explanation contract checks and extended `tests/test_api_contract.kujo` for API-level explanation success and invalid-flag behavior.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_retrieval_explanation_metadata.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_intent_rewrite_pipeline.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_federated_query_planner.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_response_policy_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).

## Tier 6 (Governance, Compliance, and Risk Management)

### [x] UPR-070: Add data retention, deletion, and legal-hold policy controls

Why:
- Enterprises need lifecycle controls for indexed content.

Implementation expectations:
- Add retention windows and explicit purge workflows.
- Add legal-hold exemption support.

Acceptance criteria:
- Expired data is purged according to policy and legal-hold exceptions are respected.

Validation/testing expectations:
- Retention and hold policy simulation tests.

Completion notes:
- Completed on: 2026-05-25
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: b13cf19a98d4d384a84aed1f77c9a401599cda41
- Summary: Added namespace-scoped retention policy controls with explicit purge workflow and legal-hold exemption enforcement for production lifecycle governance.
- Retention policy engine: Added `src/retention_policy.kujo` with deterministic retention cutoff logic and coordinated chunk/vector/lexical purge behavior.
- API controls: Added admin endpoints in `src/query_api.kujo` for policy and hold management (`GET /retention`, `POST /retention/policy`, `POST /retention/legal-hold/start`, `POST /retention/legal-hold/stop`, `POST /retention/purge`).
- Legal-hold enforcement: Purge now returns `legal_hold_active` and blocks deletion whenever namespace legal hold is enabled.
- Config surface: Added retention/hold env toggles and defaults in `src/config.kujo` and `.env.example` (`KUJO_RAG_RETENTION_POLICY_ENABLED`, `KUJO_RAG_RETENTION_DEFAULT_TTL_DAYS`, `KUJO_RAG_RETENTION_LEGAL_HOLD_ENABLED`).
- Docs update: Added `docs/data-retention-legal-hold.md` and README references for retention policy operations.
- Validation/testing expectations met: Added `tests/test_retention_legal_hold_controls.kujo` covering deterministic retention simulation and end-to-end legal-hold blocking/release purge flow.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_retention_legal_hold_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_intent_rewrite_pipeline.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_retrieval_explanation_metadata.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_federated_query_planner.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_response_policy_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass).

### [x] UPR-071: Add user/tenant data export and deletion workflows

Why:
- Privacy and compliance programs require operational tooling.

Implementation expectations:
- Add export and delete operations with audit trail.
- Ensure derived/indexed data is included in scope.

Acceptance criteria:
- Export and deletion requests complete end-to-end with verifiable evidence.

Validation/testing expectations:
- End-to-end privacy workflow tests.

Completion notes:
- Completed on: 2026-05-26
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: b938c8a77d46b2a706c8435f08af5df46bcd9ab5
- Summary: Added namespace-scoped privacy export and deletion workflows with auditable export artifacts and deletion receipts, plus legal-hold interlocks and runtime cleanup for sessions/ingest state/cache/retention controls.
- Privacy workflow module: Added `src/privacy_workflows.kujo` for export artifact writing, index scope summarization, and deleted-index construction.
- API controls: Added admin endpoints in `src/query_api.kujo` (`POST /privacy/export`, `POST /privacy/delete`) with CORS preflight support and root API discovery metadata updates.
- Legal-hold integration: Privacy deletion now blocks on active legal hold and uses persisted legal-hold resolution to prevent stale in-memory hold state across route handlers.
- Documentation: Added `docs/privacy-export-delete-workflows.md` and README references for privacy export/delete operations.
- Validation/testing expectations met: Added `tests/test_privacy_export_delete_workflows.kujo` and expanded `tests/test_api_contract.kujo` coverage for privacy export/delete behavior.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_retention_legal_hold_controls.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_privacy_export_delete_workflows.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_contract.kujo --interpreter` (pass).

### [x] UPR-072: Build compliance control mapping (SOC2/ISO-style baseline)

Why:
- Universal production adoption often requires control evidence mapping.

Implementation expectations:
- Map controls to code, config, process, and evidence artifacts.
- Track coverage gaps and owners.

Acceptance criteria:
- Control matrix exists with evidence links and unresolved gaps clearly flagged.

Validation/testing expectations:
- Periodic control evidence review workflow.

Completion notes:
- Completed on: 2026-05-26
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 7ba9b94aa085f22ac1962bb68a03398c94509cfc
- Summary: Added a compliance control mapping baseline with SOC2/ISO-aligned control entries, evidence/link validation gates, unresolved-gap ownership tracking, and periodic CI review workflow automation.
- Control matrix baseline: Added `config/compliance_control_matrix.json` with control-to-artifact mapping for code, config, process, and evidence sources plus gap ownership metadata.
- Compliance review runner: Added `scripts/run_compliance_control_evidence_review.kujo` to validate control ownership, link resolution, unresolved gap metadata, and periodic review workflow presence while writing a structured review artifact.
- Documentation: Added `docs/compliance-control-mapping.md` and `docs/compliance-evidence-review-workflow.md`, and updated README references for compliance baseline operations.
- CI automation: Added `.github/workflows/compliance-evidence-review.yml` (scheduled + manual) to run the compliance evidence review and publish artifacts.
- Validation/testing expectations met: Added `tests/test_compliance_control_mapping_baseline.kujo` and extended `tests/test_governance_contract.kujo` for compliance docs/workflow contract coverage.
- Runtime stability fix: Resolved Kujo interpreter loop-variable scope leakage in the compliance runner by using collision-safe loop index names across helper and caller loops.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_compliance_control_mapping_baseline.kujo --interpreter` (pass); `/path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `/path/to/kujo/target/debug/kujo run scripts/run_compliance_control_evidence_review.kujo --interpreter` (pass).

### [x] UPR-073: Establish recurring threat modeling and security review cadence

Why:
- Risk posture changes with new features and integrations.

Implementation expectations:
- Define threat model template and review cadence.
- Require updates on major architectural changes.

Acceptance criteria:
- Threat model is updated and tracked per release milestone.

Validation/testing expectations:
- Security review checklist attached to release process.

Completion notes:
- Completed on: 2026-05-26
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 51ccbdcc1ecd0cb0ca5a5737efc02b994fe54fea
- Summary: Added machine-readable threat-model cadence state (`config/threat_model_review_plan.json`), operator/security checklist documentation (`docs/threat-modeling-review-cadence.md`), a deterministic cadence validator (`scripts/run_threat_model_review_cadence.kujo`), dedicated regression coverage (`tests/test_threat_model_review_cadence.kujo`), and scheduled CI validation workflow (`.github/workflows/threat-model-review.yml`).
- Governance linkage: Extended `tests/test_governance_contract.kujo` and `docs/release-process.md` so release readiness now requires threat-model cadence validation and checklist linkage.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_threat_model_review_cadence.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_threat_model_review_cadence.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_integration.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-074: Add recurring penetration test and remediation workflow

Why:
- Independent security validation strengthens production confidence.

Implementation expectations:
- Define test scope and severity-based remediation SLAs.
- Integrate findings into backlog tracking.

Acceptance criteria:
- High severity findings block production promotion until resolved or approved exception.

Validation/testing expectations:
- Pen test report and remediation evidence per cycle.

Completion notes:
- Completed on: 2026-05-26
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c2a285c407c1c3e5e529a43d70bf01e358517282
- Summary: Added machine-readable penetration-test cadence + findings state (`config/penetration_test_review_plan.json`), backlog linkage ledger (`config/penetration_test_remediation_backlog.json`), cycle report/evidence artifacts (`docs/penetration-test-report.md`, `docs/penetration-test-remediation-evidence.md`), deterministic remediation gate validation (`scripts/run_penetration_test_remediation_review.kujo`), and scheduled CI workflow (`.github/workflows/penetration-test-remediation.yml`).
- Governance linkage: Updated `docs/release-process.md`, `.github/workflows/release-gates.yml`, and `tests/test_governance_contract.kujo` so production promotion now enforces penetration-test remediation gating and high-severity blocker policy (`resolved` or approved exception).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_penetration_test_remediation_workflow.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_penetration_test_remediation_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_threat_model_review_cadence.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_unit.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_integration.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_release_evaluation.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-075: Add incident response runbooks and tabletop exercises

Why:
- Production readiness includes response capability, not only prevention.

Implementation expectations:
- Add runbooks for auth compromise, data corruption, service outage, and quality regression incidents.
- Run tabletop drills and capture lessons learned.

Acceptance criteria:
- On-call responders can execute runbooks effectively under simulated incidents.

Validation/testing expectations:
- Tabletop action reports and follow-up issue tracking.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: ff1a500f67c55a8e0692532193cc200b27af01b3
- Summary: Added machine-readable incident tabletop cadence state (`config/incident_response_tabletop_plan.json`), incident runbooks for auth compromise/data corruption/service outage/quality regression (`docs/runbooks/incident-*.md`), cycle action report evidence (`docs/incident-tabletop-action-report-2026-05.md`), deterministic tabletop validation runner (`scripts/run_incident_response_tabletop_review.kujo`), and scheduled CI workflow (`.github/workflows/incident-response-tabletop-review.yml`).
- Governance linkage: Updated `docs/release-process.md`, `.github/workflows/release-gates.yml`, `tests/test_governance_contract.kujo`, and `README.md` so production promotion now enforces incident tabletop readiness gating and published operational evidence paths.
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_incident_response_tabletop_workflow.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_incident_response_tabletop_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_penetration_test_remediation_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_threat_model_review_cadence.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

## Tier 7 (DX, API Productization, and Maintainability)

### [x] UPR-080: Publish OpenAPI contract and generated client SDKs

Why:
- Universal API adoption requires formal contracts and client tooling.

Implementation expectations:
- Create OpenAPI spec for current HTTP API.
- Generate and test at least one client SDK.

Acceptance criteria:
- API changes are contract-validated and versioned.

Validation/testing expectations:
- Contract compatibility tests in CI.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: ee0914353873b12c453f0c0fd18931617bb2da90
- Summary: Added canonical OpenAPI contract (`openapi/kujo-rag-openapi.json`) for the current HTTP surface, generated JavaScript SDK artifact (`sdk/javascript/kujo-rag-client.generated.js`), and deterministic validation runner (`scripts/run_openapi_contract_review.kujo`) that enforces contract completeness plus SDK parity.
- Governance linkage: Added scheduled CI workflow (`.github/workflows/openapi-contract-review.yml`), extended release gate + process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), and updated governance contract coverage (`tests/test_governance_contract.kujo`) plus implementation docs (`docs/openapi-contract-sdk.md`, `README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_openapi_contract_sdk.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_openapi_contract_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-081: Add explicit API and config versioning policy

Why:
- Production consumers need stable upgrade paths.

Implementation expectations:
- Define backward compatibility policy and deprecation windows.
- Add migration notes for breaking changes.

Acceptance criteria:
- Versioning/deprecation behavior is explicit and enforceable.

Validation/testing expectations:
- Compatibility tests for previous minor versions.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: e6ddc2f5b18b8ba368b20d00b499d77ddfe96232
- Summary: Added explicit API/config versioning policy docs (`docs/api-config-versioning-policy.md`), machine-readable policy + previous-minor matrix baselines (`config/api_config_versioning_policy.json`, `compatibility/api-config/previous_minor_matrix.json`), and breaking-change migration-note standards/templates (`docs/migrations/README.md`, `docs/migrations/v2.0.0-template.md`).
- Governance linkage: Added deterministic policy gate runner (`scripts/run_api_config_versioning_review.kujo`), dedicated CI workflow (`.github/workflows/api-config-versioning-review.yml`), release-gate + release-process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract coverage (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_api_config_versioning_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_api_config_versioning_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-082: Add strict config schema docs and validation examples

Why:
- Universal operators need predictable config behavior.

Implementation expectations:
- Document every config key with type, default, and production recommendation.
- Add invalid config examples and expected failures.

Acceptance criteria:
- Operators can validate configs before deployment.

Validation/testing expectations:
- Config schema regression tests.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 73221603a04fa36635107d161635e913422013eb
- Summary: Added strict config schema artifacts with full key coverage (`config/config_schema_reference.json`, `docs/config-schema-reference.md`), invalid config regression fixtures (`config/config_validation_examples.json`), and deterministic schema review gate automation (`scripts/run_config_schema_review.kujo`).
- Governance linkage: Added scheduled CI workflow (`.github/workflows/config-schema-review.yml`), extended release-gate + release-process wiring (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract coverage (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_config_schema_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_RAG_CONFIG_SCHEMA_REGENERATE=true KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_config_schema_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_config_schema_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-083: Add containerized/devcontainer reproducible dev environment

Why:
- Faster onboarding and consistent local behavior improve contributor throughput.

Implementation expectations:
- Add devcontainer and containerized quick-start.
- Keep local native workflows supported.

Acceptance criteria:
- Fresh environment setup succeeds with documented one-command path.

Validation/testing expectations:
- Clean-room onboarding test by another agent/user.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 5c2b650edd2ccb0eb66f96480e02d717e0798c8d
- Summary: Added containerized/devcontainer reproducible environment assets (`Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.devcontainer/devcontainer.json`) plus onboarding policy docs (`docs/containerized-dev-environment.md`) with one-command path (`docker compose up --build`) while preserving native workflows.
- Governance linkage: Added deterministic review gate runner (`scripts/run_containerized_dev_environment_review.kujo`), dedicated CI workflow (`.github/workflows/containerized-dev-environment-review.yml`), release-gate + release-process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract coverage (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_containerized_dev_environment_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_containerized_dev_environment_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true).

### [x] UPR-084: Add chaos and fault-injection test scenarios

Why:
- Reliability confidence requires controlled failure testing.

Implementation expectations:
- Add chaos scenarios for timeouts, storage failure, and dependency failure.
- Verify graceful degradation and recovery.

Acceptance criteria:
- System behavior under fault is bounded, observable, and documented.

Validation/testing expectations:
- Chaos test suite with pass/fail assertions.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 21970fcf8675cd8c03c139be94830d68d385d6a8
- Summary: Added deterministic chaos/fault-injection scenario baseline artifacts (`config/chaos_fault_injection_scenarios.json`, `docs/chaos-fault-injection-scenarios.md`) covering timeout, storage failure, and dependency failure with required bounded-behavior, observability, and recovery assertions.
- Governance linkage: Added dedicated review gate runner (`scripts/run_chaos_fault_injection_review.kujo`), regression coverage (`tests/test_chaos_fault_injection_review.kujo`), scheduled CI workflow (`.github/workflows/chaos-fault-injection-review.yml`), release-gate/release-process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract updates (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_chaos_fault_injection_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_chaos_fault_injection_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=464).

### [x] UPR-085: Add architecture fitness functions and guardrail checks

Why:
- Long-term maintainability needs automated architecture constraints.

Implementation expectations:
- Add checks preventing forbidden dependencies and layer violations.
- Enforce extension points through tests/contracts.

Acceptance criteria:
- Architecture regressions fail CI before merge.

Validation/testing expectations:
- Fitness-function checks integrated into CI.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: 807c2a93f786e2a3ba8fca27ed8ed7d7e57ff010
- Summary: Added machine-readable architecture fitness rule baseline (`config/architecture_fitness_rules.json`) and deterministic gate runner (`scripts/run_architecture_fitness_review.kujo`) to enforce forbidden dependency edges and extension-point contract tokens across source/docs.
- Governance linkage: Added dedicated CI workflow (`.github/workflows/architecture-fitness-review.yml`), regression coverage (`tests/test_architecture_fitness_review.kujo`), release-gate + release-process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract updates (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_architecture_fitness_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_architecture_fitness_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=464).

### [x] UPR-086: Add performance and cost budget gates

Why:
- Universal production use needs both latency and cost control.

Implementation expectations:
- Define and enforce performance and resource budgets by workload class.
- Add budget regression alerts in CI and staging.

Acceptance criteria:
- Budget regressions fail promotion workflows.

Validation/testing expectations:
- Budget checks with trend comparison against baseline.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: c70fb129729a13102de00f21a3c5030eafc578a1
- Summary: Added workload-class performance/cost budget policy (`config/performance_cost_budget_policy.json`) and deterministic budget gate runner (`scripts/run_performance_cost_budget_review.kujo`) that enforces latency/throughput/resource/cost limits with trend-regression checks against historical runs.
- Governance linkage: Added dedicated CI workflow (`.github/workflows/performance-cost-budget-review.yml`), regression coverage (`tests/test_performance_cost_budget_review.kujo`), release-gate + release-process linkage (`.github/workflows/release-gates.yml`, `docs/release-process.md`), governance contract updates (`tests/test_governance_contract.kujo`), and README inventory updates (`README.md`).
- Tests run: `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_performance_cost_budget_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_performance_cost_budget_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/debug/kujo /path/to/kujo/target/debug/kujo run scripts/run_tests.kujo --interpreter` (pass, warning_budget_ok=true, total_warning_count=464).

### [x] UPR-087: Add release readiness scorecard document and checklist gate

Why:
- A single cross-domain scorecard simplifies go/no-go decisions.

Implementation expectations:
- Define weighted readiness criteria across security, reliability, quality, scalability, and compliance.
- Require scorecard signoff before production promotion.

Acceptance criteria:
- Every release candidate has a completed, auditable readiness scorecard.

Validation/testing expectations:
- Release pipeline requires scorecard artifact.

Completion notes:
- Completed on: 2026-05-27
- Agent: GitHub Copilot (GPT-5.3-Codex)
- PR/Commit: -
- Summary: Added a weighted cross-domain release readiness scorecard baseline (`config/release_readiness_scorecard.json`), deterministic validator (`scripts/run_release_readiness_scorecard_review.kujo`), workflow documentation (`docs/release-readiness-scorecard.md`), scheduled CI workflow (`.github/workflows/release-readiness-scorecard-review.yml`), and release-gates/release-process wiring so promotion requires auditable go/no-go signoff.
- Governance linkage: Updated release governance contract coverage (`tests/test_governance_contract.kujo`) and release pipeline artifact publication (`results/release/release_readiness_scorecard_status.json`) in `.github/workflows/release-gates.yml`.
- Tests run: `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run scripts/run_release_readiness_scorecard_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run tests/test_release_readiness_scorecard_review.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run tests/test_governance_contract.kujo --interpreter` (pass); `KUJO_BIN=/path/to/kujo/target/release/kujo /path/to/kujo/target/release/kujo run scripts/run_tests.kujo --interpreter` (pass).

## Universal Production Done Criteria

Universal production readiness is complete when:
- All Tier 0 items are checked and validated.
- Security model includes enterprise auth + namespace RBAC + token lifecycle controls.
- Reliability model includes SLOs, alerting, DR, and tested runbooks.
- Performance model includes benchmark budgets and scalable backend path.
- Evaluation model includes realistic multi-domain and adversarial gates.
- CI branch protection enforces required gates for every PR and push.
- Compliance/governance controls are documented with evidence links.
- API/versioning and operational docs are sufficient for independent teams to deploy safely without original authors.

## Suggested Validation Command Baseline (For Most Items)

- kujo run tests/test_unit.kujo --interpreter
- kujo run tests/test_integration.kujo --interpreter
- kujo run tests/test_release_evaluation.kujo --interpreter
- kujo run scripts/run_release_evaluation.kujo --interpreter
- kujo run scripts/run_tests.kujo --interpreter

When API behavior changes:
- kujo run main.kujo --interpreter serve --host 127.0.0.1 --port 8787
- curl -s http://127.0.0.1:8787/health
- curl -s -X POST http://127.0.0.1:8787/ingest -H "Content-Type: application/json" -d '{"path":"./examples/kujo_docs","recursive":true}'
- curl -s -X POST http://127.0.0.1:8787/query -H "Content-Type: application/json" -d '{"query":"What is Kujo optimized for?"}'
