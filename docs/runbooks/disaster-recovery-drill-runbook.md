# Disaster Recovery Drill Runbook

Use this runbook when DR drill simulations fail RTO or RPO targets.

## Trigger Conditions

- `scripts/simulate_dr_drill.kujo` returns `status: fail`.
- Recovery completion failed (`recovery_completed=false`).
- Measured RTO or RPO exceeds tier targets.

## Immediate Actions

1. Capture drill metadata (tier, restore time, data loss window, failure markers).
2. Freeze rollout of changes touching backup/restore paths.
3. Assign an incident owner and open a remediation ticket.

## Diagnostics

1. Validate latest backup manifest and checksum integrity.
2. Verify restore process used expected backup directory and target paths.
3. Inspect storage/network events during drill interval.
4. Identify dominant delay source: backup freshness, transfer latency, restore runtime, or operator workflow.

## Remediation

1. If RTO exceeded, optimize restore workflow and reduce manual steps.
2. If RPO exceeded, increase backup cadence and verify scheduler reliability.
3. If recovery failed, fix restore blockers and rerun drill before signoff.

## Exit Criteria

- Follow-up drill passes configured RTO/RPO targets for affected tier.
- Root-cause summary and remediation changes are linked in release-readiness evidence.
