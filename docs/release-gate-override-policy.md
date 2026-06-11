# Release Gate Override Policy

This policy defines the human review workflow for temporary release-gate overrides.

## Principles

- Overrides are exceptional and time-bounded.
- Overrides must not silently bypass release quality controls.
- Every override must be auditable, attributable, and linked to a tracked remediation ticket.

## Required fields for active overrides

Active entries in `config/release_gate_overrides.json` must include:

- `id`: unique override identifier
- `active`: must be `true` for an active exception
- `gates`: one or more target gate keys (for example `quality_pass_rate`, `avg_grounding`)
- `rationale`: non-empty explanation of why temporary override is needed
- `ticket`: incident/remediation ticket reference
- `approvers`: at least two explicit approvers
- `reviewed_by`: release owner accountable for the decision
- `expires_at_unix_ms`: hard expiration timestamp in unix milliseconds

## Review workflow

1. Release owner confirms failing gate evidence in `release_eval_report.json`.
2. Two approvers review risk and remediation plan.
3. Active override entry is recorded in `config/release_gate_overrides.json`.
4. Validator is executed:
   - `kujo run scripts/validate_release_gate_overrides.kujo --interpreter`
5. Validator artifact is archived:
   - `results/release_gate_override_review.json`
6. Override is removed after remediation and before expiration.

## Expiration and cleanup

- Expired overrides are invalid and fail validation.
- Active overrides without expiration are invalid.
- Overrides must be removed once remediation lands.

## CI governance checks

`release-gates` workflow runs `scripts/validate_release_gate_overrides.kujo` and uploads `release-gate-overrides.json` plus `results/release_gate_override_review.json` as artifacts for auditability.
