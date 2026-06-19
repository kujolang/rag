# RAG Starter Kit

Local-first, Kujo-native retrieval-augmented generation starter kit.

This project implements an end-to-end local RAG pipeline in Kujo:

- file ingestion (recursive directory crawl)
- deterministic, de-duplicated file discovery for reproducible indexes
- markdown / text / PDF / JSON / CSV / HTML / XML / YAML / log parsing
- chunking strategies (line and fixed) with optional language/format-aware presets
- embedding provider abstraction (offline hash by default + optional AI embedding)
- persistent vector + lexical index
- hybrid retrieval (dense + lexical weighted scoring)
- source citations with file + line ranges
- query API server
- configurable API error/log redaction by sensitive key and literal value
- Kujo docs assistant demo

CLI note: `help`, `--help`, and `--version` all render the same help text in this repository; there is no separate version banner.

Agent readability note: prioritize copyable examples over tests. Examples should model the most token-efficient idioms we want agents to imitate. In CLI/demo Kujo files, prefer small local helpers such as `print_json`, `exit_json`, and read-result payload builders when the same output pattern repeats; keep tests, fixtures, and generated contracts explicit unless a behavior change requires alignment.

No Python runtime or Python package tooling is required.

## Enterprise Readiness Posture

Kujo RAG is designed as a local-first, production-oriented starter kit rather than a one-size-fits-all managed service. The repository includes strict production configuration checks, bearer/JWT-proxy auth modes, namespace isolation, RBAC, audit logging, redaction, rate limiting, retention/legal-hold controls, backup/restore workflows, OpenAPI/SDK validation, release gates, and operational runbooks.

For production deployments, enable strict mode with `KUJO_RAG_STRICT_CONFIG=true` or `KUJO_RAG_ENV=production`, set a non-default namespace and index path, configure authentication, scope ingest roots, and enable at-rest encryption. Deployment teams should still validate workload-specific latency/cost budgets, external vector backend behavior, compliance controls, and release gates before exposing the API beyond a trusted network.

## Repository Layout

- `main.kujo`: CLI entrypoint (`ingest`, `query`, `serve`, `demo`)
- `VERSION`: semantic release version source of truth (`MAJOR.MINOR.PATCH`)
- `src/config.kujo`: runtime configuration loader + defaults
- `src/env_loader.kujo`: `.env` loader
- `src/ingestion.kujo`: file discovery + parser orchestration
- `src/parsers.kujo`: markdown / text / PDF parsing
- `src/chunking.kujo`: chunking strategies
- `src/embeddings.kujo`: embedding abstraction and providers
- `src/vector_store.kujo`: index model + persistence
- `src/vector_backend.kujo`: pluggable vector/lexical storage backend adapters
- `src/retrieval.kujo`: hybrid ranking + citation shaping
- `src/rag_engine.kujo`: end-to-end indexing and query orchestration
- `src/query_api.kujo`: HTTP API routes
- `src/retention_policy.kujo`: retention cutoff and legal-hold-aware purge policy logic
- `src/privacy_workflows.kujo`: namespace privacy export/delete artifact helpers
- `src/bootstrap.kujo`: adoption bootstrap template generator
- `src/release_eval.kujo`: golden-query release evaluation and threshold gating
- `src/cli_args.kujo`, `src/common.kujo`, `src/tests_helpers.kujo`: shared utility modules
- `demo/kujo_docs_assistant.kujo`: demo script
- `examples/kujo_docs/`: local docs corpus used by demo/tests
- `docs/agent-implementation-checklist.md`: prioritized execution backlog for follow-on agents
- `docs/adoption-playbook.md`: third-party adoption guide with integration recipes
- `docs/branch-protection-policy.md`: required checks and merge governance policy for protected branches
- `docs/auth-providers.md`: pluggable auth provider modes (bearer and JWT proxy)
- `docs/rbac-authorization.md`: namespace-scoped RBAC policy and action enforcement
- `docs/audit-logging.md`: immutable/tamper-evident audit mode for security-sensitive actions
- `docs/abuse-protections.md`: burst controls, IP blocklists, and anomaly hook behavior
- `docs/redaction-policy.md`: sensitive-data redaction behavior for logs and API errors
- `docs/probe-endpoints.md`: liveness/readiness/startup probe semantics and config
- `docs/structured-logs.md`: structured access log schema and correlation ID propagation rules
- `docs/metrics-expansion.md`: expanded SRE metrics dimensions and tenant views
- `docs/otel-tracing.md`: OpenTelemetry span coverage and OTLP export configuration
- `docs/slo-alerting-policy.md`: SLO targets, alert tiers, and runbook mapping
- `docs/backup-restore.md`: backup and restore workflow with checksum verification steps
- `docs/disaster-recovery-drills.md`: DR tier targets and drill evaluation workflow
- `docs/graceful-shutdown.md`: drain-mode controls and rolling deployment safeguards
- `docs/ingest-idempotency.md`: idempotency-key dedupe behavior for ingest jobs
- `docs/async-ingest-workers.md`: queue-backed ingest worker mode and operational controls
- `docs/query-embedding-cache.md`: query/embedding cache behavior and ingest-triggered invalidation policy
- `docs/data-retention-legal-hold.md`: retention windows, purge workflow, and legal-hold exemption controls
- `docs/privacy-export-delete-workflows.md`: namespace privacy export/delete controls, legal-hold interlock, and evidence artifacts
- `docs/compliance-control-mapping.md`: SOC2/ISO baseline control-to-evidence mapping with unresolved gap ownership
- `docs/compliance-evidence-review-workflow.md`: periodic compliance evidence review cadence and triage workflow
- `docs/threat-modeling-review-cadence.md`: recurring threat-model review cadence, major-change triggers, and release security checklist
- `docs/penetration-testing-remediation-workflow.md`: recurring penetration-test cadence, SLA policy, and release-blocking remediation workflow
- `docs/penetration-test-report.md`: current-cycle penetration-test report artifact
- `docs/penetration-test-remediation-evidence.md`: current-cycle remediation and approved-exception evidence ledger
- `docs/incident-response-tabletop-workflow.md`: recurring incident-response tabletop cadence, scenario coverage contract, and follow-up tracking policy
- `docs/incident-tabletop-action-report-2026-05.md`: current-cycle tabletop drill outcomes, lessons learned, and follow-up issue ledger
- `docs/openapi-contract-sdk.md`: OpenAPI contract, generated SDK, and contract-review workflow policy
- `docs/api-config-versioning-policy.md`: explicit API/config compatibility policy, deprecation windows, migration-note requirements, and previous-minor compatibility matrix contract
- `docs/config-schema-reference.md`: strict key-by-key config schema reference with type/default/deployment recommendation coverage
- `docs/containerized-dev-environment.md`: one-command containerized onboarding and VS Code devcontainer reproducibility workflow
- `docs/chaos-fault-injection-scenarios.md`: timeout/storage/dependency fault-injection scenario matrix with bounded-behavior, observability, and recovery assertions
- `docs/architecture-fitness-functions.md`: architecture guardrails for forbidden dependencies, layer boundaries, and extension-point contract enforcement
- `docs/performance-cost-budget-gates.md`: workload-class performance/resource/cost budget policy and trend-regression gate requirements
- `docs/release-readiness-scorecard.md`: weighted cross-domain release readiness criteria and go/no-go signoff workflow
- `docs/migrations/README.md`: required migration-note structure for breaking releases
- `docs/migrations/v2.0.0-template.md`: breaking-change migration-note template baseline
- `docs/qdrant-vector-backend.md`: qdrant-compatible ANN backend adapter and mirror/sync operations
- `docs/rate-limit-backend.md`: pluggable rate-limit backend modes and shared-file behavior
- `docs/large-corpus-benchmarks.md`: benchmark dataset tiers, budget gates, and trend-history workflow
- `docs/index-maintenance.md`: index compaction workflow, maintenance windows, and safety gates
- `docs/supply-chain-security.md`: SBOM generation and CI supply-chain scanning policy
- `docs/config-integrity.md`: startup config validation rules and strict-mode failure behavior
- `docs/encryption-at-rest.md`: optional OpenSSL-backed index encryption and key management guidance
- `docs/tls-reverse-proxy-hardening.md`: TLS termination and secure reverse-proxy deployment baseline
- `docs/release-process.md`: semantic versioning, release artifact, and rollback-safe release workflow
- `docs/parser-resilience.md`: parser coverage matrix, malformed-input fallback behavior, and parser sandbox controls
- `docs/chunking-presets.md`: language/format-aware chunking presets and override hierarchy
- `docs/structured-data-ingestion.md`: JSON/CSV ingest behavior and schema-aware retrieval filter contract
- `docs/releases/`: versioned release notes (`vX.Y.Z.md`)
- `docs/adr/`: architecture decision records (chunking, retrieval, offline-first)
- `docs/extension-guide.md`: parser/provider/retrieval extension workflows
- `docs/runtime-support-matrix.md`: supported Kujo runtime/version execution combinations
- `openapi/kujo-rag-openapi.json`: canonical OpenAPI contract for the current HTTP API surface
- `sdk/javascript/kujo-rag-client.generated.js`: generated JavaScript client SDK sourced from OpenAPI contract
- `config/api_config_versioning_policy.json`: machine-readable API/config versioning policy and deprecation window baseline
- `config/config_schema_reference.json`: machine-readable strict config schema baseline generated from runtime defaults
- `config/config_validation_examples.json`: invalid configuration examples with expected validation error codes
- `config/chaos_fault_injection_scenarios.json`: machine-readable chaos fault-injection scenario contract for timeout/storage/dependency reliability coverage
- `config/architecture_fitness_rules.json`: machine-readable architecture fitness rule set for forbidden dependency and extension-point checks
- `config/performance_cost_budget_policy.json`: workload-class performance/resource/cost budget policy and regression thresholds
- `compatibility/api-config/previous_minor_matrix.json`: previous-minor compatibility fixture matrix for release gating
- `Dockerfile`: container image baseline with pinned Kujo runtime build
- `docker-compose.yml`: one-command local containerized API startup path
- `.devcontainer/devcontainer.json`: VS Code devcontainer definition for reproducible contributor environments
- `tests/test_unit.kujo`: unit smoke tests
- `tests/test_integration.kujo`: end-to-end integration test
- `tests/test_release_evaluation.kujo`: release-gate regression test
- `tests/test_config_integrity.kujo`: startup config validity/strict-mode integrity checks
- `tests/test_auth_providers.kujo`: bearer and JWT proxy auth provider validation coverage
- `tests/test_rbac_authorization.kujo`: namespace-scoped RBAC role/action authorization checks
- `tests/test_abuse_protection.kujo`: burst-limit, static blocklist, and anomaly-hook abuse protection checks
- `tests/test_security.kujo`: security regressions
- `tests/test_redaction_policy.kujo`: redaction key/value masking and policy behavior checks
- `tests/test_structured_logs.kujo`: request/correlation-id propagation and structured access-log traceability
- `tests/test_metrics_expansion.kujo`: expanded metrics payload and tenant-view coverage checks
- `tests/test_otel_tracing.kujo`: tracing span emission and request-correlation propagation checks
- `tests/test_slo_alert_policy.kujo`: SLO threshold simulation and runbook linkage checks
- `tests/test_backup_restore_integrity.kujo`: backup manifest checksum and restore integrity verification checks
- `tests/test_disaster_recovery_drills.kujo`: DR drill simulation pass/fail evaluation and runbook linkage checks
- `tests/test_graceful_shutdown_safeguards.kujo`: drain-mode readiness and mutation-rejection safeguards
- `tests/test_ingest_idempotency.kujo`: duplicate ingest-job suppression and idempotency metadata checks
- `tests/test_async_ingest_workers.kujo`: queue worker progression and inline ingest-job compatibility coverage
- `tests/test_query_embedding_cache.kujo`: query cache hit/miss and ingest invalidation behavior with embedding cache metrics coverage
- `tests/test_privacy_export_delete_workflows.kujo`: end-to-end privacy export/delete flow coverage with legal-hold blocking checks
- `tests/test_rate_limit_backend_shared.kujo`: shared-backend multi-instance rate-limit consistency checks
- `tests/test_large_corpus_benchmark_suite.kujo`: budget pass/fail regression coverage for small/medium/large corpus benchmark tiers
- `tests/test_index_compaction_maintenance.kujo`: compaction footprint reduction and before/after correctness checks
- `tests/test_chunking_preset_ab_evaluation.kujo`: preset-vs-baseline chunking A/B gate pass/fail regression coverage
- `tests/test_compliance_control_mapping_baseline.kujo`: compliance control matrix baseline and periodic evidence-review workflow validation
- `tests/test_threat_model_review_cadence.kujo`: threat-model cadence gate baseline and overdue/failure-mode validation
- `tests/test_penetration_test_remediation_workflow.kujo`: penetration-test remediation gate baseline and high-severity/backlog failure-mode validation
- `tests/test_incident_response_tabletop_workflow.kujo`: incident tabletop gate baseline and required-scenario/runbook/follow-up failure-mode validation
- `tests/test_openapi_contract_sdk.kujo`: OpenAPI contract and generated SDK gate pass/fail regression coverage
- `tests/test_api_config_versioning_review.kujo`: API/config versioning policy gate pass/fail regression coverage with previous-minor compatibility checks
- `tests/test_config_schema_review.kujo`: strict config schema gate pass/fail regression coverage with invalid-example validation checks
- `tests/test_containerized_dev_environment_review.kujo`: containerized/devcontainer environment gate pass/fail regression coverage
- `tests/test_chaos_fault_injection_review.kujo`: chaos fault-injection gate pass/fail regression coverage with required fault-class assertions
- `tests/test_architecture_fitness_review.kujo`: architecture fitness gate pass/fail regression coverage for forbidden dependencies and extension-point enforcement
- `tests/test_performance_cost_budget_review.kujo`: performance/cost budget gate pass/fail regression coverage with trend-aware workload-class checks
- `tests/test_run_tests_runner_guardrails.kujo`: runtime-binary validation and env-driven subset execution guardrails for the test wrapper
- `scripts/run_release_evaluation.kujo`: standalone release-evaluation runner
- `scripts/run_chunking_preset_ab_evaluation.kujo`: chunking preset-vs-baseline A/B evaluation gate runner
- `scripts/run_compliance_control_evidence_review.kujo`: validates compliance control mappings and unresolved-gap ownership evidence
- `scripts/run_threat_model_review_cadence.kujo`: validates threat-model cadence state, milestone tracking, and release checklist linkage
- `scripts/run_penetration_test_remediation_review.kujo`: validates penetration-test scope, SLA policy, backlog linkage, and high-severity release blocking
- `scripts/run_incident_response_tabletop_review.kujo`: validates incident tabletop cadence, required scenario coverage, runbook/report presence, and follow-up issue tracking
- `scripts/run_openapi_contract_review.kujo`: validates OpenAPI contract completeness and generated SDK parity
- `scripts/run_api_config_versioning_review.kujo`: validates API/config versioning policy linkage, deprecation windows, migration docs, and previous-minor compatibility matrix
- `scripts/run_config_schema_review.kujo`: validates strict config schema coverage and invalid-config example expectations against runtime validator behavior
- `scripts/run_containerized_dev_environment_review.kujo`: validates container/devcontainer reproducibility artifacts and one-command onboarding linkage
- `scripts/run_chaos_fault_injection_review.kujo`: validates required chaos timeout/storage/dependency scenarios, bounded degradation, observability, and recovery assertions
- `scripts/run_architecture_fitness_review.kujo`: validates architecture fitness rules for forbidden dependency edges and required extension-point tokens
- `scripts/run_performance_cost_budget_review.kujo`: validates workload-class performance/resource/cost budgets against benchmark outputs with trend-regression checks
- `scripts/run_large_corpus_benchmarks.kujo`: large-corpus benchmark suite runner with throughput/latency budget gates
- `scripts/maintain_index.kujo`: index compaction and maintenance-window runner with correctness/performance safeguards
- `scripts/simulate_slo_alerts.kujo`: evaluates metrics snapshots against SLO/alert thresholds
- `scripts/backup_state.kujo`: snapshots index/config state and writes checksum manifest
- `scripts/restore_state.kujo`: verifies manifest checksums and restores known-good state
- `scripts/simulate_dr_drill.kujo`: evaluates DR drill snapshots against tiered RTO/RPO targets
- `scripts/run_tests.kujo`: Kujo-native test runner wrapper with runtime-binary validation and optional subset execution via `KUJO_RAG_TEST_FILES`
- `scripts/build_release_artifacts.kujo`: deterministic release manifest and checksum generator
- `scripts/run_supply_chain_scan.kujo`: supply-chain scan gate (secrets + dependency workflow checks)
- `.github/workflows/release-gates.yml`: CI enforcement for test, warning-budget, and release-evaluation gates
- `.github/workflows/release-artifacts.yml`: CI workflow for versioned artifact + checksum + SBOM generation and supply-chain scan enforcement on release tags
- `.github/workflows/compliance-evidence-review.yml`: scheduled/dispatch compliance control evidence review and artifact publication
- `.github/workflows/threat-model-review.yml`: scheduled/dispatch threat-model cadence validation and artifact publication
- `.github/workflows/penetration-test-remediation.yml`: scheduled/dispatch penetration-test remediation validation and artifact publication
- `.github/workflows/incident-response-tabletop-review.yml`: scheduled/dispatch incident-response tabletop validation and artifact publication
- `.github/workflows/openapi-contract-review.yml`: scheduled/dispatch OpenAPI contract and generated SDK validation and artifact publication
- `.github/workflows/api-config-versioning-review.yml`: scheduled/dispatch API/config versioning policy and previous-minor compatibility validation
- `.github/workflows/config-schema-review.yml`: scheduled/dispatch strict config schema and invalid-example validation gate
- `.github/workflows/containerized-dev-environment-review.yml`: scheduled/dispatch containerized/devcontainer reproducibility validation gate
- `.github/workflows/chaos-fault-injection-review.yml`: scheduled/dispatch chaos fault-injection scenario validation gate
- `.github/workflows/architecture-fitness-review.yml`: scheduled/dispatch architecture fitness guardrail validation gate
- `.github/workflows/performance-cost-budget-review.yml`: scheduled/dispatch workload-class performance and cost budget validation gate

## Root Hygiene

- root source-of-truth files remain intentionally minimal (`main.kujo`, `VERSION`, top-level configs/docs)
- runtime outputs are isolated under ignored directories (`data/`, `results/`) and are not committed
- transient local artifacts (`*.log`, `*.tmp`, editor/cache files) are ignored by default via `.gitignore`

## Agent Search Hygiene

Canonical, copyable surfaces:

- `README.md`
- `main.kujo`
- `demo/kujo_docs_assistant.kujo`
- `docs/adoption-playbook.md`
- `docs/extension-guide.md`
- `examples/kujo_docs/`

Contract and fixture surfaces:

- `tests/`: behavior checks; read for contracts, not as style examples
- `examples/release_eval_corpus/`, `examples/multilingual_release_eval_corpus/`, `examples/parser_matrix_corpus/`, `examples/malformed_parser_corpus/`, `examples/chunking_preset_eval_corpus/`: evaluation/parser fixtures
- `config/*.json` and `compatibility/`: machine-readable gate inputs and compatibility fixtures
- `openapi/kujo-rag-openapi.json`: canonical API contract
- `sdk/javascript/kujo-rag-client.generated.js`: generated SDK; do not hand-edit
- `data/` and `results/`: ignored local runtime/generated output

Recommended search exclusions for broad cleanup sweeps:

```bash
rg "pattern" . \
	-g '!data/**' \
	-g '!results/**' \
	-g '!sdk/**' \
	-g '!openapi/**' \
	-g '!config/*.json' \
	-g '!compatibility/**'
```

Include generated or bulk paths only when the task explicitly targets contracts, fixtures, reports, or generated clients.

## Implementation Backlog

For structured, agent-executable improvement work (security, architecture, testing, and feature tiers), use:

- `docs/agent-implementation-checklist.md`
- `docs/universal-production-hardening-checklist.md`
- `docs/universal-production-loop-execution-order.md`
- `docs/universal-production-progress-log.md`
- `docs/next-session-enterprise-enhancement-checklist.md`
- `docs/next-session-enterprise-readiness-review-2026-06-19.md`

The checklist is designed so each agent can pick one item, implement it, validate it, update this README when behavior changes, and then mark the item complete.

## Release Process

For deterministic, rollback-safe releases:

1) Create release notes at `docs/releases/vX.Y.Z.md`.
2) Build artifacts + checksums:

```bash
kujo run scripts/build_release_artifacts.kujo --interpreter --version vX.Y.Z --notes ./docs/releases/vX.Y.Z.md
```

3) Confirm outputs:

- `results/releases/vX.Y.Z/release-manifest.json`
- `results/releases/vX.Y.Z/SHA256SUMS.txt`
- `results/releases/vX.Y.Z/release-notes.md`
- `results/releases/vX.Y.Z/sbom.cyclonedx.json`
- `results/releases/vX.Y.Z/supply-chain-scan-release-gates.json`
- `results/releases/vX.Y.Z/supply-chain-scan-release-artifacts.json`
- `results/releases/vX.Y.Z/supply-chain-scan-env-surface.json`

4) Trigger `.github/workflows/release-artifacts.yml` via tag push (`vX.Y.Z`) or manual dispatch.

Rollback and compatibility rules are documented in `docs/release-process.md`.

## Extension Pattern

Parser and embedding selection now use explicit registries:

- parser registry: `get_parser_registry()` in `src/parsers.kujo`
- embedding provider registry: `get_embedding_provider_registry()` in `src/embeddings.kujo`

To add a new parser/provider:

1) Add the implementation function.
2) Register it in the corresponding registry map.
3) Preserve fallback behavior (`text` parser fallback and `hash` embedding fallback).
4) Add regression tests for registry lookup and unknown-provider handling.

Implemented extension example:

- `.mdx` is now mapped to the markdown parser via registry, with unit coverage for registry + parse behavior.

For contributor-facing extension and architecture rationale docs, see:

- `docs/extension-guide.md`
- `docs/adr/README.md`

## Requirements

- Kujo language binary available (`kujo` in `PATH`, or set `KUJO_BIN`)
- For PDF extraction: `pdftotext` recommended (optional fallback is built in)

PDF extractor safety constraints:

- `KUJO_RAG_PDF_EXTRACTOR` must be a single binary/path token containing only: letters, digits, `_`, `.`, `/`, `-`
- values with shell metacharacters or command chaining (for example `;`, `&&`, `$()`) are rejected and fall back safely
- PDF file paths are shell-quoted before execution to prevent command-injection via crafted filenames
- parser timeout budget is configurable via `KUJO_RAG_PARSER_TIMEOUT_MS` (clamped to safe bounds)
- parser sandbox byte budget is configurable via `KUJO_RAG_PARSER_SANDBOX_MAX_BYTES` and triggers deterministic fallback metadata when exceeded

## Environment Setup

```bash
cp .env.example .env
```

Defaults work offline with deterministic hash embeddings.

Startup configuration integrity validation:

- startup now validates critical config fields before command execution
- invalid config exits with structured JSON diagnostics (`error: invalid_configuration`)
- strict validation mode can be enabled via `KUJO_RAG_STRICT_CONFIG=true`
- strict mode is automatically active when `KUJO_RAG_ENV=production`
- strict mode requires non-default namespace, explicit bearer token, non-default index path, and at-rest encryption with key configuration

At-rest encryption for persisted indexes:

- enable with `KUJO_RAG_AT_REST_ENCRYPTION_ENABLED=true`
- provide key material with `KUJO_RAG_AT_REST_ENCRYPTION_KEY` or `KUJO_RAG_AT_REST_ENCRYPTION_KEY_FILE`
- OpenSSL binary path can be overridden with `KUJO_RAG_AT_REST_ENCRYPTION_OPENSSL_BIN`
- encrypted index payloads are stored as envelope JSON containing ciphertext; plaintext chunks/vectors are not directly readable at rest

TLS and reverse-proxy hardening:

- terminate TLS at a hardened proxy and keep Kujo RAG on loopback/private interfaces
- apply secure header baseline (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and restrictive `Content-Security-Policy`)
- use deployment checklist and sample Nginx/Caddy templates in `docs/tls-reverse-proxy-hardening.md`

Immutable audit logging mode:

- enable with `KUJO_RAG_API_AUDIT_ENABLED=true`
- configure append-only sink path with `KUJO_RAG_API_AUDIT_PATH`
- current external sink mode is `KUJO_RAG_API_AUDIT_EXTERNAL_SINK_MODE=append_file`
- audit records include hash-chain metadata (`prev_hash`, `event_hash`) for tamper-evident verification

Abuse protections and anomaly hooks:

- rate limiting includes window and burst controls (`KUJO_RAG_API_RATE_LIMIT_WINDOW_SEC`, `KUJO_RAG_API_RATE_LIMIT_MAX_REQUESTS`, `KUJO_RAG_API_RATE_LIMIT_BURST_WINDOW_SEC`, `KUJO_RAG_API_RATE_LIMIT_BURST_MAX_REQUESTS`)
- optional per-tenant quotas enforce namespace query rate, ingest volume per request, and namespace storage ceilings (`KUJO_RAG_API_TENANT_QUOTA_ENABLED`, `KUJO_RAG_API_TENANT_QUERY_RATE_WINDOW_SEC`, `KUJO_RAG_API_TENANT_QUERY_RATE_MAX_REQUESTS`, `KUJO_RAG_API_TENANT_INGEST_MAX_CHUNKS_PER_REQUEST`, `KUJO_RAG_API_TENANT_STORAGE_MAX_CHUNKS`)
- request/ingest guardrails bound worst-case CPU and memory pressure with explicit `413` envelopes (`KUJO_RAG_API_GUARDRAIL_QUERY_MAX_COMPLEXITY`, `KUJO_RAG_API_GUARDRAIL_QUERY_MAX_FILTER_KEYS`, `KUJO_RAG_API_GUARDRAIL_QUERY_MAX_SESSION_CHARS`, `KUJO_RAG_API_GUARDRAIL_INGEST_MAX_FILES`, `KUJO_RAG_API_GUARDRAIL_INGEST_MAX_TOTAL_BYTES`)
- static IP blocklist via `KUJO_RAG_API_ABUSE_BLOCKLIST_IPS`
- anomaly hook emission toggle via `KUJO_RAG_API_ANOMALY_HOOK_ENABLED`
- optional dynamic auto-block controls via `KUJO_RAG_API_ANOMALY_AUTO_BLOCK_ENABLED`, `KUJO_RAG_API_ANOMALY_VIOLATION_THRESHOLD`, and `KUJO_RAG_API_ANOMALY_BLOCK_TTL_SEC`

Sensitive-data redaction policy:

- enable/disable with `KUJO_RAG_API_REDACTION_ENABLED`
- customize mask via `KUJO_RAG_API_REDACTION_MASK`
- customize key patterns and literal value scrubbing with `KUJO_RAG_API_REDACTION_KEYS` and `KUJO_RAG_API_REDACTION_VALUES`
- in `KUJO_RAG_ENV=production`, API `5xx` errors return generic messages without details

Probe endpoints:

- `GET /live` for liveness checks
- `GET /ready` for readiness checks
- `GET /startup` for startup lifecycle checks
- configurable startup/readiness controls via `KUJO_RAG_API_STARTUP_GRACE_MS` and `KUJO_RAG_API_READINESS_FORCE_UNREADY`

Graceful drain mode for rolling deploys:

- admin controls: `GET /drain`, `POST /drain/start`, `POST /drain/stop`
- when draining, readiness returns `503` (`reason=draining`) and mutating endpoints reject with `service_draining`
- configurable controls via `KUJO_RAG_API_DRAIN_REJECT_MUTATIONS` and `KUJO_RAG_API_DRAIN_PRE_STOP_MS`

Privacy export and deletion workflows:

- admin controls: `POST /privacy/export`, `POST /privacy/delete`
- privacy deletion is blocked when namespace legal hold is active (`409 legal_hold_active`)
- each operation writes verifiable artifacts under `./results/privacy/`
- operator guidance and request/response contracts are documented in `docs/privacy-export-delete-workflows.md`

Compliance control mapping baseline:

- canonical control mapping source: `config/compliance_control_matrix.json`
- periodic review runner: `kujo run scripts/run_compliance_control_evidence_review.kujo --interpreter`
- review workflow and triage policy: `docs/compliance-evidence-review-workflow.md`

Threat modeling and security review cadence:

- machine-readable cadence state: `config/threat_model_review_plan.json`
- periodic cadence runner: `kujo run scripts/run_threat_model_review_cadence.kujo --interpreter`
- review template and release checklist policy: `docs/threat-modeling-review-cadence.md`

Penetration testing and remediation workflow:

- machine-readable cadence and finding state: `config/penetration_test_review_plan.json`
- remediation backlog mapping: `config/penetration_test_remediation_backlog.json`
- periodic remediation gate runner: `kujo run scripts/run_penetration_test_remediation_review.kujo --interpreter`
- workflow and release-blocking policy: `docs/penetration-testing-remediation-workflow.md`

Incident response tabletop workflow:

- machine-readable tabletop cadence and scenario state: `config/incident_response_tabletop_plan.json`
- periodic tabletop gate runner: `kujo run scripts/run_incident_response_tabletop_review.kujo --interpreter`
- workflow contract and release linkage policy: `docs/incident-response-tabletop-workflow.md`

Ingest idempotency and duplicate suppression:

- `POST /ingest/jobs` accepts idempotency keys from header/body and deduplicates retries inside the configured window
- response payload includes idempotency metadata (`enabled`, `key`, `deduplicated`, `window_sec`, `expires_at`)
- configurable controls via `KUJO_RAG_API_INGEST_IDEMPOTENCY_ENABLED`, `KUJO_RAG_API_INGEST_IDEMPOTENCY_WINDOW_SEC`, and `KUJO_RAG_API_INGEST_IDEMPOTENCY_HEADER`

Queue-backed async ingest workers:

- set `KUJO_RAG_API_INGEST_JOBS_MODE=queue` to decouple `POST /ingest/jobs` submission from ingest execution
- tune worker progression with `KUJO_RAG_API_INGEST_WORKER_BATCH_SIZE` and `KUJO_RAG_API_INGEST_WORKER_MAX_RUNNING`
- `POST /ingest/jobs/status` advances one worker cycle in queue mode and returns worker metadata (`mode`, `processed_jobs`)
- `POST /ingest/jobs/worker/tick` allows explicit admin-triggered worker cycles

Query and embedding cache layers:

- query-response cache controls are configurable via `KUJO_RAG_API_QUERY_CACHE_ENABLED`, `KUJO_RAG_API_QUERY_CACHE_TTL_SEC`, and `KUJO_RAG_API_QUERY_CACHE_MAX_ENTRIES`
- embedding cache controls are configurable via `KUJO_RAG_EMBEDDING_CACHE_ENABLED` and `KUJO_RAG_EMBEDDING_CACHE_MAX_ENTRIES`
- successful ingest updates invalidate namespace query-cache entries and clear embedding cache state
- query responses include `data.cache.hit` to indicate cache-hit vs cache-miss execution

Language/format-aware chunking presets:

- enable preset routing with `KUJO_RAG_CHUNK_PRESETS_ENABLED=true`
- optionally override preset definitions with `KUJO_RAG_CHUNK_PRESETS_JSON`
- resolved profile metadata is emitted on chunks as `chunk.meta.chunk_profile_*`
- run preset-vs-baseline gate: `kujo run scripts/run_chunking_preset_ab_evaluation.kujo --interpreter`

Distributed rate-limit backend options:

- `KUJO_RAG_API_RATE_LIMIT_BACKEND=memory|shared_file`
- `KUJO_RAG_API_RATE_LIMIT_BACKEND_FILE` configures shared state path for `shared_file` mode
- shared backend enables cross-instance limit enforcement when instances share filesystem state

Large-corpus benchmark suite and budgets:

- run `kujo run scripts/run_large_corpus_benchmarks.kujo --interpreter` to execute small/medium/large corpus tier benchmarks
- dataset profile definitions live in `config/large_corpus_benchmark_profiles.json`
- throughput/latency budgets live in `config/large_corpus_benchmark_budgets.json`
- outputs are written to `results/large_corpus_benchmark_report.json` and `results/large_corpus_benchmark_trend.json`
- benchmark budgets are CI-enforced in `.github/workflows/release-gates.yml`

Index compaction and maintenance windows:

- run `kujo run scripts/maintain_index.kujo --interpreter` for report mode or set `KUJO_RAG_INDEX_MAINTENANCE_MODE=apply` to persist compaction output
- compaction removes duplicate/orphan index records and updates maintenance metadata counters
- maintenance windows are controlled by `KUJO_RAG_INDEX_MAINTENANCE_ALLOWED_UTC_HOURS` and can be bypassed manually with `KUJO_RAG_INDEX_MAINTENANCE_IGNORE_WINDOW=true`
- apply mode enforces before/after probe correctness and latency-regression safety checks before writing changes

Vector backend adapter modes:

- `local_json` (default): persisted JSON index at `KUJO_RAG_INDEX_PATH`
- `memory` (reference scaffold): key-scoped adapter state selected by `KUJO_RAG_VECTOR_BACKEND_MEMORY_KEY`
- `qdrant_http`: qdrant-compatible ANN adapter with local mirror persistence and optional remote sync (`KUJO_RAG_VECTOR_BACKEND_QDRANT_*`)

For third-party adoption patterns (minimum setup, docs/code/mixed recipes, deployment options, and troubleshooting), see:

- `docs/adoption-playbook.md`

## Quick Start

1) Build index from local docs:

```bash
kujo run main.kujo --interpreter ingest --path ./examples/kujo_docs --recursive true
```

Expected output shape:

```json
{"ok":true,"command":"ingest","namespace":"default","index_path":"./data/rag_index.json","path":"./examples/kujo_docs","recursive":true,"summary":{"documents":4,"chunks":4},"stats":{"files_seen":4},"errors":[]}
```

2) Query the index:

```bash
kujo run main.kujo --interpreter query --question "How does Kujo handle module imports?"
```

Expected output shape:

```json
{"answer":"...","citations":[{"path":"./examples/kujo_docs/LANGUAGE_SPEC.md","line_start":1,"line_end":6}],"count":4}
```

Optional namespace override for tenant/project isolation:

```bash
kujo run main.kujo --interpreter ingest --path ./examples/kujo_docs --recursive true --namespace team_a
kujo run main.kujo --interpreter query --question "How does Kujo handle module imports?" --namespace team_a
```

3) Run API server:

```bash
kujo run main.kujo --interpreter serve --host 127.0.0.1 --port 8787
```

4) Run demo assistant:

```bash
kujo run main.kujo --interpreter demo
```

5) Generate a bootstrap template for external repository adoption:

```bash
kujo run main.kujo --interpreter bootstrap --target ./results/bootstrap_repo
```

6) Use execution bridge to prefer non-interpreter mode with automatic fallback:

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_main_auto.kujo --interpreter query --question "What is Kujo optimized for?"
```

## Third-Party Adoption Quick Recipes

These recipes are expanded in `docs/adoption-playbook.md` and are intended to minimize setup effort in external projects.

Documentation corpus:

```bash
export KUJO_RAG_INGEST_EXTENSIONS=md,markdown,txt
export KUJO_RAG_CHUNK_STRATEGY=line
kujo run main.kujo --interpreter ingest --path ./docs --recursive true
```

Code repository:

```bash
export KUJO_RAG_INGEST_EXTENSIONS=kujo,md,txt
export KUJO_RAG_CHUNK_STRATEGY=fixed
export KUJO_RAG_CHUNK_SIZE=1100
export KUJO_RAG_CHUNK_OVERLAP=180
kujo run main.kujo --interpreter ingest --path ./src --recursive true
```

Mixed content workspace:

```bash
export KUJO_RAG_INGEST_EXTENSIONS=md,markdown,txt,kujo,pdf
export KUJO_RAG_CHUNK_STRATEGY=line
export KUJO_RAG_TOP_K=8
kujo run main.kujo --interpreter ingest --path ./knowledge --recursive true
```

## API

OpenAPI contract and generated JavaScript SDK:

- OpenAPI: `openapi/kujo-rag-openapi.json`
- JS SDK: `sdk/javascript/kujo-rag-client.generated.js`
- regenerate + validate SDK parity: `KUJO_RAG_OPENAPI_REGENERATE=true kujo run scripts/run_openapi_contract_review.kujo --interpreter`

### Health

```bash
curl -s http://127.0.0.1:8787/health
```

### Ingest

```bash
curl -s -X POST http://127.0.0.1:8787/ingest \
	-H "Content-Type: application/json" \
	-d '{"path":"./examples/kujo_docs","recursive":true,"namespace":"default"}'
```

`/ingest` path scope is restricted to configured roots. By default this repo is configured for `./examples` in `.env.example`.
Requests outside configured roots return `403` with `ingest_path_forbidden`.

### Ingest Jobs

Create an ingest job with lifecycle tracking (`submitted` -> `running` -> `succeeded|failed`):

```bash
curl -s -X POST http://127.0.0.1:8787/ingest/jobs \
	-H "Content-Type: application/json" \
	-d '{"path":"./examples/kujo_docs","recursive":true,"namespace":"default"}'
```

Mode behavior:

- `KUJO_RAG_API_INGEST_JOBS_MODE=inline` (default): runs job work in the request and typically returns terminal status.
- `KUJO_RAG_API_INGEST_JOBS_MODE=queue`: returns quickly with `job.status=submitted`; worker cycles process queued jobs.

Poll job status:

```bash
curl -s -X POST http://127.0.0.1:8787/ingest/jobs/status \
	-H "Content-Type: application/json" \
	-d '{"job_id":"<job-id>"}'
```

Manually trigger one worker cycle (admin):

```bash
curl -s -X POST http://127.0.0.1:8787/ingest/jobs/worker/tick
```

`/ingest` remains available as the synchronous ingest endpoint for existing clients.

### Query

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"What is Kujo optimized for?","namespace":"default"}'
```

Namespace behavior:

- `namespace` is optional on `/ingest`, `/ingest/jobs`, and `/query`
- when omitted, the API uses `KUJO_RAG_NAMESPACE` (default `default`)
- when `KUJO_RAG_NAMESPACE_INDEX_ISOLATION=true` (default), each namespace writes to an isolated index path derived from `KUJO_RAG_INDEX_PATH` (for example `rag_index__team_a.json`)
- namespaces must be 1-64 characters and match `[a-z0-9_-]`

Optional metadata filters can scope retrieval by file path, extension, and tags:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"How does retrieval work?","filters":{"path":"examples/kujo_docs","extension":"md","tags":["markdown"]}}'
```

Filter behavior:

- `path`: string or array of strings; chunk path must contain at least one value
- `extension`: string or array (with or without leading `.`); file extension must match at least one value
- `tags`: string or array of strings; chunk tags match explicit metadata tags plus inferred kind/extension tags
- additional metadata filter keys: `structured_schema`, `structured_fields`, `author`, `timestamp`, `source_system`, `sensitivity_tags`
- filters support include/exclude blocks: `{"filters":{"include":{...},"exclude":{...}}}`
- filters are optional; omitted filters preserve existing unfiltered behavior

Optional cross-index federation can query multiple namespaces with deterministic weighted merge:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"critical outage","namespace":"team_a","federation":{"merge_strategy":"weighted_score","fallback_policy":"primary_then_all","targets":[{"namespace":"team_a","weight":1.0},{"namespace":"team_b","weight":0.7}]}}'
```

Federation behavior:

- `federation.targets` is required when federation is provided; each target supports `namespace` and optional `weight` (default `1.0`)
- `merge_strategy` currently supports `weighted_score` with deterministic tie-breaking (namespace/path/line/chunk id)
- `fallback_policy` supports `best_effort` and `primary_then_all`
- query response includes a `federation` summary block and per-citation federation metadata (`federation_namespace`, `federation_weight`, `federation_index_path`)

Optional response policy controls can tune answer style and safety behavior per request:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"critical outage","response_policy":{"style":"concise","safety_mode":"strict","min_citations":2,"min_confidence":0.45}}'
```

Response policy behavior:

- `style`: `strict_extractive`, `concise`, or `expanded`
- `safety_mode`: `balanced` (default), `strict`, or `permissive`
- strict safety supports optional thresholds: `min_citations`, `min_confidence`
- query response includes normalized `response_policy` and `safe_response_policy` metadata

Optional retrieval explanation metadata can be requested per query:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"critical outage","include_retrieval_explanation":true}'
```

Retrieval explanation behavior:

- `include_retrieval_explanation` is optional and must be a boolean when provided
- query response includes `retrieval_explanation` when enabled, with concise ranking rationale (`summary`, `intent`, `rewrite_applied`, `search_query`, `ranking`)
- global default can be set with `KUJO_RAG_QUERY_RETRIEVAL_EXPLANATION_ENABLED`

Intent classification and rewrite behavior:

- query execution classifies intent into `fact`, `navigation`, `troubleshooting`, or `compare`
- when `KUJO_RAG_QUERY_INTENT_REWRITE_ENABLED=true` (default), retrieval runs against a rewritten query variant tuned for that intent class
- query response includes `query_intent` metadata: `intent`, `rewrite_enabled`, `original_query`, `rewritten_query`, and `rewrite_applied`

Optional conversational mode can be enabled per request by sending `session_id`:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-d '{"query":"What about performance tradeoffs?","session_id":"my-session-1"}'
```

Session behavior:

- stateless mode remains default when `session_id` is omitted
- per-session history is isolated by `namespace + session_id`
- history is bounded by `KUJO_RAG_SESSION_HISTORY_MAX_TURNS` (default `4`)

Retention and legal-hold controls:

- `GET /retention` returns configured defaults and namespace overrides for retention and legal-hold state
- `POST /retention/policy` sets namespace retention policy (`enabled`, `ttl_days`)
- `POST /retention/legal-hold/start` and `POST /retention/legal-hold/stop` manage namespace legal-hold state
- `POST /retention/purge` applies retention purge for a namespace and returns purge summary counts
- when legal hold is active, purge is blocked with `legal_hold_active`

### Optional API Auth Providers

Configure `KUJO_RAG_API_AUTH_PROVIDER`:

- `none` (default local mode): auth disabled
- `bearer`: legacy static bearer token
- `jwt_proxy`: issuer/audience/expiry checks using trusted proxy claim headers

Bearer mode configuration:

- `KUJO_RAG_API_AUTH_PROVIDER=bearer`
- `KUJO_RAG_API_BEARER_TOKEN=<token>`
- `KUJO_RAG_API_BEARER_TOKEN_NEXT=<next_token>` (optional rotation window)
- `KUJO_RAG_API_BEARER_REVOKED_TOKENS=<csv_tokens>` (optional immediate revocation)

JWT proxy mode configuration:

- `KUJO_RAG_API_AUTH_PROVIDER=jwt_proxy`
- `KUJO_RAG_API_JWT_ISSUER=<issuer>`
- `KUJO_RAG_API_JWT_AUDIENCE=<audience>`
- `KUJO_RAG_API_JWT_CLOCK_SKEW_SEC=60` (optional)

JWT proxy mode expects these headers on authenticated requests:

- `Authorization: Bearer <token>`
- `x-kujo-claim-iss`
- `x-kujo-claim-aud`
- `x-kujo-claim-exp`

Optional namespace RBAC controls:

- `KUJO_RAG_API_RBAC_ENABLED=true`
- `KUJO_RAG_API_RBAC_DEFAULT_ROLE=admin`
- `KUJO_RAG_API_RBAC_ROLE_HEADER=x-kujo-role`
- `KUJO_RAG_API_RBAC_NAMESPACE_HEADER=x-kujo-namespace`
- `KUJO_RAG_API_RBAC_POLICY_JSON={"admin":["ingest","query","admin"],"writer":["ingest","query"],"reader":["query"]}`

RBAC enforces action permissions (`ingest`, `query`, `admin`) and optional namespace scope restrictions per request.

Example bearer-mode authenticated query:

```bash
curl -s -X POST http://127.0.0.1:8787/query \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer your-token" \
	-d '{"query":"What is Kujo optimized for?"}'
```

For full provider behavior and security notes, see `docs/auth-providers.md`.
For namespace role/permission enforcement details, see `docs/rbac-authorization.md`.

### Optional CORS Allow-List

CORS is disabled by default for secure minimal behavior.

- enable with `KUJO_RAG_API_CORS_ENABLED=true`
- configure allow-list with `KUJO_RAG_API_CORS_ALLOWED_ORIGINS` (comma-separated origins)
- disallowed origins do not receive `Access-Control-Allow-Origin`

Example:

```bash
export KUJO_RAG_API_CORS_ENABLED=true
export KUJO_RAG_API_CORS_ALLOWED_ORIGINS=https://app.example,https://localhost:3000
```

Strict-mode example:

```bash
export KUJO_RAG_ENV=production
export KUJO_RAG_STRICT_CONFIG=true
export KUJO_RAG_NAMESPACE=team_prod
export KUJO_RAG_INDEX_PATH=./data/team_prod_index.json
export KUJO_RAG_API_BEARER_TOKEN=replace-with-secure-token
```

When enabled, API routes include CORS headers for allowed origins and handle preflight `OPTIONS` requests on `/`, `/health`, `/ingest`, `/ingest/jobs`, `/ingest/jobs/status`, `/ingest/jobs/worker/tick`, and `/query`.

Query responses are grounded drafts built from retrieved sources. They include:

- synthesized answer text
- aggregate confidence (`confidence`, `confidence_band`, `confidence_summary`)
- scored citations with source file path and line ranges
- calibrated citation confidence (`provenance_score`, `confidence_band`, `confidence_components`)
- response context (`namespace`, `query`, `query_intent`, `search_query`)
- stage timings (`stage_timings_ms`)

### Metrics

```bash
curl -s http://127.0.0.1:8787/metrics
```

Metrics export includes:

- ingest counters: `ingest_requests`, `ingest_errors`
- query counters: `query_requests`, `query_errors`
- latency buckets for ingest/query: `lt_100ms`, `lt_500ms`, `lt_1000ms`, `gte_1000ms`
- cache counters and state: `cache_hits`, `cache_misses`, `cache_hit_ratio`, `query_cache_entries`, `embedding_cache_hits`, `embedding_cache_misses`, `embedding_cache_entries`

### Response Contract

API responses are envelope-based:

- success: `{ "ok": true, "data": ... }`
- error: `{ "ok": false, "error": { "code": "...", "message": "...", "details": {...} } }`

Common error codes:

- `invalid_json`
- `invalid_body`
- `invalid_body_type`
- `missing_query`
- `query_too_large`
- `body_too_large`
- `rate_limited`
- `invalid_filters`
- `invalid_session_id`
- `invalid_namespace`
- `missing_job_id`
- `ingest_job_not_found`

## Tests

Test harness notes:

- shared assertions live in `tests_helpers.kujo` and are used by both unit and integration suites
- API contract coverage lives in `tests/test_api_contract.kujo` (health, ingest, query/filter contracts, malformed payloads, size limits, rate limiting)
- security regression coverage lives in `tests/test_security.kujo` (path restrictions, auth, body-type safety, PDF extractor hardening)
- backend adapter contract coverage lives in `tests/test_backend_contract.kujo` (local JSON + memory adapter load/save contract)
- bootstrap adoption smoke coverage lives in `tests/test_bootstrap.kujo` (template generation + ingest/query e2e)
- non-interpreter bridge coverage lives in `tests/test_non_interpreter_bridge.kujo` (native-first command path with interpreter fallback)
- release-gate coverage lives in `tests/test_release_evaluation.kujo` (golden-query quality/latency/error thresholds)
- `scripts/run_tests.kujo` reports per-suite warning counts to make runtime/type-checking noise easier to track over time
- `scripts/run_tests.kujo` enforces warning-budget baselines from `config/test_warning_budget.json`
- `scripts/run_tests.kujo` includes a CI-ready release gate stage via `tests/test_release_evaluation.kujo`
- `scripts/run_tests.kujo` preflight-validates `KUJO_BIN` and fails fast with structured `fatal_error` output when the binary does not support `run`
- `scripts/run_tests.kujo` supports targeted subsets with `KUJO_RAG_TEST_FILES=<comma-separated-test-paths>` for faster local loops

Run directly:

```bash
kujo run tests/test_unit.kujo --interpreter
kujo run tests/test_integration.kujo --interpreter
kujo run tests/test_release_evaluation.kujo --interpreter
kujo run tests/test_backend_contract.kujo --interpreter
kujo run tests/test_bootstrap.kujo --interpreter
kujo run tests/test_non_interpreter_bridge.kujo --interpreter
kujo run tests/test_api_contract.kujo --interpreter
kujo run tests/test_security.kujo --interpreter
kujo run tests/test_connector_framework.kujo --interpreter
kujo run tests/test_connector_plugin_stub.kujo --interpreter
kujo run tests/test_structured_ingestion_retrieval.kujo --interpreter
kujo run tests/test_parser_matrix_resilience.kujo --interpreter
```

Or via wrapper (set `KUJO_BIN` if needed):

```bash
KUJO_BIN=/absolute/path/to/kujo /absolute/path/to/kujo run scripts/run_tests.kujo --interpreter
```

Focused subset wrapper run:

```bash
KUJO_BIN=/absolute/path/to/kujo KUJO_RAG_TEST_FILES=tests/test_api_contract.kujo,tests/test_security.kujo /absolute/path/to/kujo run scripts/run_tests.kujo --interpreter
```

Warning budget baseline:

- `config/test_warning_budget.json` defines max allowed totals for `total_warning_count` and `total_undefined_function_warning_count`
- wrapper runs fail when warning totals exceed budget, preventing warning-noise regressions across releases

Release evaluation and thresholds:

- `config/release_eval_golden_queries.json` defines versioned golden release queries (`dataset_version`) and domain coverage metadata (`dataset_domains`) alongside expected citation/answer characteristics, including optional per-case `min_grounding_score`
- `config/release_eval_thresholds.json` defines gate thresholds for quality pass rate, latency, error rate, confidence, and citation grounding (`min_average_grounding`)
- current hardened baseline uses 12 versioned golden queries across docs, code, policy, operations, incident, adversarial, and no-answer domains with stricter quality/confidence/grounding thresholds (`min_quality_pass_rate=0.875`, `min_average_confidence=0.35`, `min_average_grounding=0.5`)
- standalone evaluation command:

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_release_evaluation.kujo --interpreter
```

AI provider/model drift gate command:

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_ai_provider_model_drift_check.kujo --interpreter
```

Multilingual release evaluation gate command:

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_multilingual_release_evaluation.kujo --interpreter
```

Connector framework ingest command:

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_connector_ingest.kujo --interpreter
```

- release evaluation now writes a report artifact (`./results/release_eval_report.json` by default) and appends trend history (`./results/release_eval_trend.json`) with drift highlights against the prior run
- trend report includes metric-category regressions (quality, grounding, latency, reliability) plus domain-level regressions when domain pass rates or grounding scores drop versus the previous snapshot
- release evaluation trend workflow details are documented in `docs/release-eval-trends.md`
- human-reviewed gate overrides are managed through `config/release_gate_overrides.json` and validated by `scripts/validate_release_gate_overrides.kujo` (policy: `docs/release-gate-override-policy.md`)
- canary promotion checks replay production-like sampled queries via `scripts/run_canary_release_replay.kujo` using `config/canary_replay_samples.json` and acceptance bounds from `config/canary_replay_thresholds.json` (docs: `docs/canary-release-replay.md`)
- AI provider/model drift checks are enforced by `scripts/run_ai_provider_model_drift_check.kujo` using pinned runtime controls in `config/ai_provider_model_drift_controls.json` and known reference prompts from release-eval outputs (docs: `docs/ai-provider-model-drift-controls.md`)
- multilingual release evaluation checks are enforced by `scripts/run_multilingual_release_evaluation.kujo` using multilingual corpus/query fixtures and per-language-family thresholds (docs: `docs/multilingual-release-evaluation.md`)
- connector staging and ingest are handled by `scripts/run_connector_ingest.kujo` through connector contracts (`git_repo`, `http_docs`, `plugin_script`) defined in `config/connectors_ingest_sources.json` (docs: `docs/connectors-framework.md`)
- enterprise connector roadmap and starter stub catalog are tracked in `config/enterprise_connector_roadmap.json` and `config/connectors_enterprise_stubs.json` (onboarding: `docs/connectors-enterprise-roadmap.md`)

- release candidates fail when the golden evaluation thresholds regress
- GitHub Actions enforces these gates automatically on push/pull_request via `.github/workflows/release-gates.yml`

## Operational Notes

- Index path is configurable (`KUJO_RAG_INDEX_PATH`)
- Namespace default and index isolation are configurable (`KUJO_RAG_NAMESPACE`, `KUJO_RAG_NAMESPACE_INDEX_ISOLATION`)
- Vector backend adapter selection is configurable (`KUJO_RAG_VECTOR_BACKEND`, `KUJO_RAG_VECTOR_BACKEND_MEMORY_KEY`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_URL`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_COLLECTION`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_SYNC_ENABLED`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_TIMEOUT_MS`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_FAIL_OPEN`, `KUJO_RAG_VECTOR_BACKEND_QDRANT_MIRROR_PATH`)
- Query output now includes deterministic provenance/confidence calibration for both citation-level and response-level trust metadata
- Index persistence uses schema versioning (latest schema: `2.0`) with automatic migration from legacy `1.0` indexes
- Unsupported index schema versions load safely with actionable error metadata under index `meta.load_error`
- Citation line ranges are strategy-aware: fixed chunks use character-to-line mapping and line-overlap chunks keep non-inverted line boundaries
- Citation ranges are approximate at chunk boundaries (especially around newline boundary overlaps), but guaranteed non-negative and non-inverted
- CLI integer flags (for example `--port`) are validated strictly and return structured errors for invalid values
- Retrieval ranking now uses deterministic top-k selection (`O(n * k)`) instead of global full-list selection sort (`O(n^2)`)
- Ingest uses incremental indexing by document content hash: unchanged docs reuse stored chunks/vectors, changed docs are re-embedded, and deleted docs are pruned on next ingest
- Incremental ingest stats are returned in summary under `incremental` (`reindexed_docs`, `unchanged_docs`, `deleted_docs`)
- Hybrid weights are configurable (`KUJO_RAG_HYBRID_ALPHA`, `KUJO_RAG_HYBRID_BETA`)
- Reranking is configurable with deterministic modes: `none` (default) or `mmr` (`KUJO_RAG_RERANK_STRATEGY`, `KUJO_RAG_RERANK_MMR_LAMBDA`)
- Chunking behavior is configurable (`KUJO_RAG_CHUNK_STRATEGY`, `KUJO_RAG_CHUNK_SIZE`, `KUJO_RAG_CHUNK_OVERLAP`)
- Max ingest file size is configurable (`KUJO_RAG_MAX_FILE_BYTES`)
- Optional AI embeddings and answer generation are available via endpoint/model env vars
- API body size is configurable (`KUJO_RAG_API_MAX_BODY_BYTES`)
- API query size is configurable (`KUJO_RAG_API_MAX_QUERY_CHARS`)
- Query/ingest guardrails are configurable (`KUJO_RAG_API_GUARDRAIL_QUERY_MAX_COMPLEXITY`, `KUJO_RAG_API_GUARDRAIL_QUERY_MAX_FILTER_KEYS`, `KUJO_RAG_API_GUARDRAIL_QUERY_MAX_SESSION_CHARS`, `KUJO_RAG_API_GUARDRAIL_INGEST_MAX_FILES`, `KUJO_RAG_API_GUARDRAIL_INGEST_MAX_TOTAL_BYTES`)
- API query-response cache is configurable (`KUJO_RAG_API_QUERY_CACHE_ENABLED`, `KUJO_RAG_API_QUERY_CACHE_TTL_SEC`, `KUJO_RAG_API_QUERY_CACHE_MAX_ENTRIES`)
- Safe query response policy is configurable (`KUJO_RAG_QUERY_SAFE_RESPONSE_ENABLED`, `KUJO_RAG_QUERY_SAFE_RESPONSE_MIN_OVERLAP_RATIO`, `KUJO_RAG_QUERY_SAFE_RESPONSE_MESSAGE`) and emits `safe_response_policy` metadata (`triggered`, `reason`, `overlap_ratio`) in query responses
- Embedding cache is configurable (`KUJO_RAG_EMBEDDING_CACHE_ENABLED`, `KUJO_RAG_EMBEDDING_CACHE_MAX_ENTRIES`)
- CORS behavior is configurable (`KUJO_RAG_API_CORS_ENABLED`, `KUJO_RAG_API_CORS_ALLOWED_ORIGINS`)
- Session history bound is configurable (`KUJO_RAG_SESSION_HISTORY_MAX_TURNS`)
- Optional API bearer auth is configurable (`KUJO_RAG_API_BEARER_TOKEN`)
- API rate limiting is configurable (`KUJO_RAG_API_RATE_LIMIT_WINDOW_SEC`, `KUJO_RAG_API_RATE_LIMIT_MAX_REQUESTS`)
- API rate state eviction/capping is configurable (`KUJO_RAG_API_RATE_LIMIT_BUCKET_TTL_SEC`, `KUJO_RAG_API_RATE_LIMIT_MAX_KEYS`)
- Per-tenant quota controls are configurable (`KUJO_RAG_API_TENANT_QUOTA_ENABLED`, `KUJO_RAG_API_TENANT_QUERY_RATE_WINDOW_SEC`, `KUJO_RAG_API_TENANT_QUERY_RATE_MAX_REQUESTS`, `KUJO_RAG_API_TENANT_INGEST_MAX_CHUNKS_PER_REQUEST`, `KUJO_RAG_API_TENANT_STORAGE_MAX_CHUNKS`)
- API ingest path scope is configurable (`KUJO_RAG_API_INGEST_ALLOWED_ROOTS`, comma-separated roots)
- Deterministic JSON access logs can be toggled (`KUJO_RAG_API_ACCESS_LOG`)
- API metrics are exported via `GET /metrics` for ingest/query counters and latency buckets
- Query stage timings are exported via `query_stage_timings_ms` in `GET /metrics` (`tokenize`, `embed`, `retrieve`, `rerank`, `synthesize`)
- Tenant quota policy and rejection counters are exported via `tenant_quota` in `GET /metrics`, with per-namespace rejection detail in `tenant_views.*.quota_rejections`
- Guardrail rejections return explicit `413` error codes (`query_filter_complexity_exceeded`, `query_session_context_too_large`, `query_complexity_exceeded`, `ingest_guardrail_files_exceeded`, `ingest_guardrail_bytes_exceeded`) to fail worst-case inputs safely before expensive processing
- Query pipeline traces include per-stage spans (`query.stage.*`) when OTEL tracing is enabled
- release evaluation inputs are configurable (`KUJO_RAG_RELEASE_EVAL_GOLDEN_PATH`, `KUJO_RAG_RELEASE_EVAL_THRESHOLDS_PATH`, `KUJO_RAG_RELEASE_EVAL_CORPUS_PATH`, `KUJO_RAG_RELEASE_EVAL_INDEX_PATH`)
- release evaluation provider/runtime selection is configurable (`KUJO_RAG_RELEASE_EVAL_EMBEDDING_PROVIDER`)
- release evaluation reporting outputs are configurable (`KUJO_RAG_RELEASE_EVAL_OUTPUT_PATH`, `KUJO_RAG_RELEASE_EVAL_TREND_PATH`, `KUJO_RAG_RELEASE_EVAL_TREND_HISTORY_LIMIT`)
- AI provider/model drift gate controls are configurable (`KUJO_RAG_AI_DRIFT_CONTROLS_PATH`, `KUJO_RAG_AI_DRIFT_RELEASE_REPORT_PATH`, `KUJO_RAG_AI_DRIFT_REPORT_PATH`)
- release gate override workflow is configurable (`KUJO_RAG_RELEASE_GATE_OVERRIDES_PATH`, `KUJO_RAG_RELEASE_GATE_OVERRIDE_REPORT_PATH`)
- canary replay inputs/outputs are configurable (`KUJO_RAG_CANARY_GOLDEN_PATH`, `KUJO_RAG_CANARY_EVAL_THRESHOLDS_PATH`, `KUJO_RAG_CANARY_CORPUS_PATH`, `KUJO_RAG_CANARY_INDEX_PATH`, `KUJO_RAG_CANARY_BASELINE_REPORT_PATH`, `KUJO_RAG_CANARY_ACCEPTANCE_PATH`, `KUJO_RAG_CANARY_OUTPUT_PATH`)
- multilingual release-eval inputs/outputs are configurable (`KUJO_RAG_MULTILINGUAL_EVAL_GOLDEN_PATH`, `KUJO_RAG_MULTILINGUAL_EVAL_THRESHOLDS_PATH`, `KUJO_RAG_MULTILINGUAL_EVAL_CORPUS_PATH`, `KUJO_RAG_MULTILINGUAL_EVAL_INDEX_PATH`, `KUJO_RAG_MULTILINGUAL_EVAL_OUTPUT_PATH`, `KUJO_RAG_MULTILINGUAL_EVAL_EMBEDDING_PROVIDER`)
- connector framework paths are configurable (`KUJO_RAG_CONNECTOR_CONFIG_PATH`, `KUJO_RAG_CONNECTOR_STAGING_ROOT`, `KUJO_RAG_CONNECTOR_INDEX_PATH`, `KUJO_RAG_CONNECTOR_REPORT_PATH`, `KUJO_RAG_CONNECTOR_EMBEDDING_PROVIDER`, `KUJO_RAG_CONNECTOR_PLUGIN_KUJO_BIN`)

## Readiness Status

Current status: verified locally with enforced release gates and offline fallback behavior.

Runtime support declarations are tracked in `docs/runtime-support-matrix.md`, including supported and unsupported execution combinations and CI validation expectations.

Validated:

- unit and integration test scripts execute successfully
- release evaluation gate executes successfully against golden queries and thresholds
- CI workflow enforces warning-budget and release-evaluation gates on push/pull_request
- end-to-end demo flow executes successfully
- HTTP API smoke flow (`/health`, `/ingest`, `/query`) works with local docs
- offline deterministic retrieval works without external AI services

Known constraints (Kujo runtime/toolchain related):

- commands are documented with `--interpreter` because this is currently the most reliable mode for multi-module import workflows
- `scripts/run_main_auto.kujo` provides a native-first execution bridge that falls back to interpreter mode for key command paths
- interpreter runs can emit undefined-function warnings from type-checking paths even when runtime execution succeeds
- AI helpers (`ai_embedding`, `ai_chat`) are treated as optional: if unavailable or failing, this starter kit gracefully falls back to offline behavior

## Why `--interpreter` in examples?

This starter kit uses Kujo module imports heavily. In the current Kujo toolchain state, interpreter mode is the most reliable execution path for multi-module import/call flows, so commands are documented with `--interpreter` for deterministic behavior.

## License

MIT
