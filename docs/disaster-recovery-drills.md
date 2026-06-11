# Disaster Recovery Drills and RTO/RPO Targets

This policy defines DR recovery tiers, target objectives, and a repeatable drill evaluation workflow.

## Recovery Targets

Targets are stored in `config/dr_tiers.json`:

- `standard`: `RTO <= 60 minutes`, `RPO <= 15 minutes`
- `critical`: `RTO <= 30 minutes`, `RPO <= 5 minutes`

Each tier maps to `docs/runbooks/disaster-recovery-drill-runbook.md` for remediation when drills fail.

## Drill Evaluation Workflow

1. Capture a drill snapshot JSON with fields:
   - `tier`
   - `actual_restore_minutes`
   - `actual_data_loss_minutes`
   - `recovery_completed`
2. Run:

```bash
DR_TARGETS_PATH=config/dr_tiers.json \
DR_DRILL_PATH=results/dr_drill_snapshot.json \
kujo run scripts/simulate_dr_drill.kujo --interpreter
```

3. Review output:
   - `status: pass` means targets met.
   - `status: fail` includes issue list and runbook path.

## Cadence and Evidence

- Run DR drill simulation for each release candidate.
- Run a full restore rehearsal at least monthly.
- Store drill snapshots and simulator output under `results/` as release-readiness evidence.
