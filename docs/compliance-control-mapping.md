# Compliance Control Mapping Baseline

This document defines the baseline control mapping for universal production hardening loop L053 (`UPR-072`).

Canonical machine-readable source:
- `config/compliance_control_matrix.json`

Automated review output artifact:
- `results/compliance/compliance_evidence_review.json`

## Framework Scope

Baseline mappings are aligned to control families from:
- SOC 2 Trust Services Criteria (security and change/governance emphasis)
- ISO/IEC 27001 Annex A control areas

## Control Matrix

| Control ID | Framework Refs | Owner | Status | Code/Config Mappings | Process Mappings | Evidence Mappings | Gap Flag |
|---|---|---|---|---|---|---|---|
| `SOC2-CC6.1-ISO-A.5.15-authentication` | SOC2:CC6.1, ISO27001:A.5.15 | Platform Security | covered | `src/query_api.kujo`, `src/config.kujo`, `.env.example` | `docs/auth-providers.md` | `tests/test_auth_providers.kujo`, `.github/workflows/release-gates.yml` | none |
| `SOC2-CC6.6-ISO-A.8.2-authorization` | SOC2:CC6.6, ISO27001:A.8.2 | Platform Security | covered | `src/query_api.kujo`, `.env.example` | `docs/rbac-authorization.md` | `tests/test_rbac_authorization.kujo` | none |
| `SOC2-CC7.2-ISO-A.8.24-audit-trail` | SOC2:CC7.2, ISO27001:A.8.24 | Platform Reliability | covered | `src/query_api.kujo`, `.env.example` | `docs/audit-logging.md` | `tests/test_audit_logging.kujo` | none |
| `SOC2-CC6.7-ISO-A.8.24-data-lifecycle` | SOC2:CC6.7, ISO27001:A.8.24 | Data Governance | covered | `src/query_api.kujo`, `src/retention_policy.kujo`, `src/privacy_workflows.kujo`, `.env.example` | `docs/data-retention-legal-hold.md`, `docs/privacy-export-delete-workflows.md` | `tests/test_retention_legal_hold_controls.kujo`, `tests/test_privacy_export_delete_workflows.kujo` | none |
| `SOC2-CC8.1-ISO-A.8.8-vendor-risk` | SOC2:CC8.1, ISO27001:A.8.8 | Compliance Lead | partial | `scripts/run_supply_chain_scan.kujo`, `src/connectors.kujo`, `config/connectors_enterprise_stubs.json` | `docs/supply-chain-security.md`, `docs/connectors-enterprise-roadmap.md` | `tests/test_supply_chain_scan.kujo`, `.github/workflows/release-gates.yml` | yes |
| `SOC2-CC1.2-ISO-A.5.1-control-evidence-governance` | SOC2:CC1.2, ISO27001:A.5.1 | Compliance Lead | gap | `scripts/run_compliance_control_evidence_review.kujo`, `config/compliance_control_matrix.json` | `docs/compliance-control-mapping.md`, `docs/compliance-evidence-review-workflow.md` | `tests/test_compliance_control_mapping_baseline.kujo`, `.github/workflows/compliance-evidence-review.yml` | yes |

## Unresolved Gaps

Unresolved control gaps are intentionally tracked in the matrix and must include owners and target dates.

| Control ID | Gap Summary | Gap Owner | Target Date |
|---|---|---|---|
| `SOC2-CC8.1-ISO-A.8.8-vendor-risk` | Vendor assessment attestations and critical-vendor review cadence are documented only at roadmap level. | Compliance Lead | 2026-06-30 |
| `SOC2-CC1.2-ISO-A.5.1-control-evidence-governance` | Exception approvals and quarterly sign-off attestations require integration with external governance/ticketing systems. | Compliance Lead | 2026-07-31 |

## Maintenance Contract

- Any control status change must update `config/compliance_control_matrix.json`.
- Any gap marked `partial` or `gap` must include `gap_summary`, `gap_owner`, and `target_date`.
- All mapped paths in `code`, `config`, `process`, and `evidence` must resolve in-repo.
- Periodic review is enforced by `scripts/run_compliance_control_evidence_review.kujo` and `.github/workflows/compliance-evidence-review.yml`.
