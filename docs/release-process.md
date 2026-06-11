# Release Process and Rollback Guide

This document defines the UPR-004 release process for deterministic, rollback-safe production releases.

## Versioning Policy

- Semantic Versioning is required: `MAJOR.MINOR.PATCH`.
- Git tags must be prefixed with `v` (for example `v1.4.2`).
- `MAJOR` increments indicate potentially incompatible API/config changes.
- `MINOR` increments indicate backward-compatible feature releases.
- `PATCH` increments indicate backward-compatible fixes.

Current repository version source of truth:

- `VERSION` file at repository root.

## Required Release Inputs

1. Release notes file exists at `docs/releases/vX.Y.Z.md`.
2. CI required checks are green (`runtime-support-matrix`, `supply-chain-scan`, `release-gates`).
3. Release artifact rehearsal passes:
   - `kujo run tests/test_release_artifacts.kujo --interpreter`
4. Supply-chain scan gate passes with no high severity findings:
   - `kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-gates.yml --output ./results/supply-chain-scan-release-gates.json`
   - `kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-artifacts.yml --output ./results/supply-chain-scan-release-artifacts.json`
   - `kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .env.example --output ./results/supply-chain-scan-env-surface.json`
5. Release-gate override ledger is valid (if any active exceptions exist):
   - `kujo run scripts/validate_release_gate_overrides.kujo --interpreter`
   - policy: `docs/release-gate-override-policy.md`
6. Canary release replay gate passes against production-like samples:
   - `kujo run scripts/run_canary_release_replay.kujo --interpreter`
   - docs: `docs/canary-release-replay.md`
7. AI provider/model drift gate passes using pinned runtime controls and reference prompts:
   - `kujo run scripts/run_ai_provider_model_drift_check.kujo --interpreter`
   - docs: `docs/ai-provider-model-drift-controls.md`
8. Multilingual release evaluation gate passes with per-language-family quality checks:
   - `kujo run scripts/run_multilingual_release_evaluation.kujo --interpreter`
   - docs: `docs/multilingual-release-evaluation.md`
9. Chunking preset A/B evaluation gate passes on targeted mixed-format corpus:
   - `kujo run scripts/run_chunking_preset_ab_evaluation.kujo --interpreter`
   - docs: `docs/chunking-presets.md`
10. Threat-model cadence validation passes and security review checklist linkage is current:
   - `kujo run scripts/run_threat_model_review_cadence.kujo --interpreter`
   - docs: `docs/threat-modeling-review-cadence.md`
11. Penetration-test remediation gate passes so high severity findings are resolved or approved exception before production promotion:
   - `kujo run scripts/run_penetration_test_remediation_review.kujo --interpreter`
   - docs: `docs/penetration-testing-remediation-workflow.md`
12. Incident-response tabletop readiness gate passes with required scenario coverage and follow-up tracking:
   - `kujo run scripts/run_incident_response_tabletop_review.kujo --interpreter`
   - docs: `docs/incident-response-tabletop-workflow.md`
13. OpenAPI contract and generated SDK gate passes with no contract drift:
   - `kujo run scripts/run_openapi_contract_review.kujo --interpreter`
   - docs: `docs/openapi-contract-sdk.md`
14. API/config versioning policy gate passes with declared previous-minor compatibility coverage and migration-note enforcement:
   - `kujo run scripts/run_api_config_versioning_review.kujo --interpreter`
   - docs: `docs/api-config-versioning-policy.md`
15. Config schema review gate passes with full key coverage and invalid-config example validation:
   - `kujo run scripts/run_config_schema_review.kujo --interpreter`
   - docs: `docs/config-schema-reference.md`
16. Containerized/devcontainer environment gate passes with one-command onboarding path and native workflow compatibility documented:
   - `kujo run scripts/run_containerized_dev_environment_review.kujo --interpreter`
   - docs: `docs/containerized-dev-environment.md`
17. Chaos and fault-injection gate passes with required timeout/storage/dependency scenario coverage and recovery assertions:
   - `kujo run scripts/run_chaos_fault_injection_review.kujo --interpreter`
   - docs: `docs/chaos-fault-injection-scenarios.md`
18. Architecture fitness gate passes with forbidden dependency checks and extension-point contract enforcement:
   - `kujo run scripts/run_architecture_fitness_review.kujo --interpreter`
   - docs: `docs/architecture-fitness-functions.md`
19. Performance and cost budget gate passes with workload-class latency/throughput/resource/cost budgets and trend-regression checks:
   - `kujo run scripts/run_performance_cost_budget_review.kujo --interpreter`
   - docs: `docs/performance-cost-budget-gates.md`
20. Release readiness scorecard gate passes with weighted cross-domain criteria and explicit signoff:
   - `kujo run scripts/run_release_readiness_scorecard_review.kujo --interpreter`
   - docs: `docs/release-readiness-scorecard.md`

## Build Versioned Artifacts

Generate deterministic release artifacts with checksums:

```bash
kujo run scripts/build_release_artifacts.kujo --interpreter --version vX.Y.Z --notes ./docs/releases/vX.Y.Z.md
```

This produces:

- `results/releases/vX.Y.Z/release-manifest.json`
- `results/releases/vX.Y.Z/SHA256SUMS.txt`
- `results/releases/vX.Y.Z/release-notes.md`
- `results/releases/vX.Y.Z/sbom.cyclonedx.json`

`release-manifest.json` includes:

- normalized release version and tag
- build timestamp
- compatibility markers (`config_schema_version`, `api_contract_version`)
- per-file SHA-256 checksums

## GitHub Release Workflow

Use `.github/workflows/release-artifacts.yml`.

Triggers:

- push tag `v*.*.*`
- manual `workflow_dispatch` with explicit version

Workflow behavior:

1. Builds Kujo runtime.
2. Runs `scripts/build_release_artifacts.kujo` with release version and notes path.
3. Verifies SBOM output exists for the release tag.
4. Runs `scripts/run_supply_chain_scan.kujo` and writes `supply-chain-scan.json` into the release artifact directory.
5. Blocks on high severity findings.
6. Runs canary replay gate and emits `results/canary_release_replay_report.json`.
7. Runs AI provider/model drift gate and emits `results/ai_provider_model_drift_report.json`.
8. Runs multilingual release evaluation gate and emits `results/multilingual_release_eval_report.json`.
9. Runs chunking preset A/B evaluation gate and emits `results/chunking_preset_ab_report.json`.
10. Validates release-gate override ledger and emits audit artifact `results/release_gate_override_review.json`.
11. Runs penetration-test remediation gate and emits `results/security/penetration_test_remediation_status.json`.
12. Runs release readiness scorecard gate and emits `results/release/release_readiness_scorecard_status.json`.
13. Uploads generated release directory as a CI artifact.

## Rollback Procedure

Use rollback only when current release is unstable or violates release gates.

1. Identify target rollback tag `vA.B.C`.
2. Verify target artifact checksums in `results/releases/vA.B.C/SHA256SUMS.txt`.
3. Restore target runtime/config bundle.
4. Re-run gate verification on rollback target:
   - `kujo run scripts/run_release_evaluation.kujo --interpreter`
   - `kujo run scripts/run_tests.kujo --interpreter`
5. Record incident and rollback rationale in the next release notes file.

## Config Compatibility Rules

Rollback is considered safe only when both values match between source and target release manifests:

- `compatibility.config_schema_version`
- `compatibility.api_contract_version`

If either marker differs:

- treat rollback as migration-required
- run an explicit staging rehearsal before production rollback
- document required config/data transforms in release notes

## Staging Rehearsal Requirement

At least one full release rehearsal must be completed in staging before production promotion:

1. Create release notes for candidate version.
2. Generate release artifacts.
3. Deploy candidate in staging.
4. Execute smoke ingest/query and release gate scripts.
5. Perform rollback to prior tag and re-verify gates.
6. Store evidence (command outputs + manifest/checksum paths) with the release ticket.
