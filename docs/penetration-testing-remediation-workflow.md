# Penetration Testing and Remediation Workflow

This workflow defines recurring penetration testing cadence, severity-based remediation SLAs, and release-blocking policy for unresolved critical/high findings.

## Cadence and Scope

- Standard cadence: every 30 days and before production promotion milestones.
- Source of truth: `config/penetration_test_review_plan.json`.
- Scheduled automation: `.github/workflows/penetration-test-remediation.yml`.

Minimum test scope each cycle:

- authentication, RBAC, and namespace-isolation abuse paths
- privacy export/delete and legal-hold interlock behavior
- release/control-plane admin endpoints and policy bypass attempts

## Severity-Based Remediation SLAs

SLA defaults are enforced from `severity_sla_days` in `config/penetration_test_review_plan.json`:

- `critical`: 2 days
- `high`: 7 days
- `medium`: 30 days
- `low`: 90 days

## Release Blocking Policy

High severity findings block production promotion until resolved or approved exception.

Approved exceptions must include:

- exception identifier
- approver
- expiration timestamp
- linked remediation backlog ticket

## Backlog Tracking Integration

- Findings are tracked in `config/penetration_test_remediation_backlog.json`.
- Every finding in the plan must map to a backlog ticket.
- Backlog ticket entries must reference the originating finding and remediation evidence.

## Pen Test Report and Remediation Evidence

Each cycle must include both:

- pen test report artifact (`docs/penetration-test-report.md`)
- remediation evidence artifact (`docs/penetration-test-remediation-evidence.md`)

## Automated Validation Command

```bash
kujo run scripts/run_penetration_test_remediation_review.kujo --interpreter
```

Primary artifact output:

- `results/security/penetration_test_remediation_status.json`

## Triage Procedure

1. Run the review command locally when CI fails or before release sign-off.
2. Inspect `gates`, `unresolved_high_findings`, and `overdue_findings` in `results/security/penetration_test_remediation_status.json`.
3. For each failing finding:
   - update or create backlog remediation ticket,
   - attach updated remediation evidence,
   - resolve finding or file a time-bounded approved exception.
