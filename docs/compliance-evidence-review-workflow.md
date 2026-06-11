# Compliance Evidence Review Workflow

This workflow defines periodic review for the L053 compliance control mapping baseline (`UPR-072`).

## Review Cadence

- Standard cadence: every 30 days.
- Source of truth: `config/compliance_control_matrix.json` (`review_cadence_days`, `last_reviewed_at_unix_ms`).
- Scheduled automation: `.github/workflows/compliance-evidence-review.yml`.

## Automated Review Command

```bash
kujo run scripts/run_compliance_control_evidence_review.kujo --interpreter
```

Default outputs:
- `results/compliance/compliance_evidence_review.json`

## What The Review Validates

- Matrix exists and declares a version.
- At least one control is mapped.
- Every control has an owner.
- Every mapped path in `code`, `config`, `process`, and `evidence` resolves.
- Any `partial` or `gap` control includes `gap_summary`, `gap_owner`, and `target_date`.
- Periodic review workflow assets are present.

## Triage Procedure

1. Run the review command locally when CI fails or before monthly compliance check-in.
2. Inspect `gates` and `control_checks` in `results/compliance/compliance_evidence_review.json`.
3. For unresolved gaps:
- Confirm owner and target date remain valid.
- Open or update tracking issue in governance tooling.
4. Update `last_reviewed_at_unix_ms` in `config/compliance_control_matrix.json` after each completed review.
5. Commit updates with evidence and include summary in release/governance notes.

## Escalation and Ownership

- Primary owner: Compliance Lead.
- Secondary owners: Platform Security, Platform Reliability, Data Governance (by control ownership in the matrix).
- If a gap target date is missed, escalate in the next hardening loop and track remediation in progress log follow-ups.
