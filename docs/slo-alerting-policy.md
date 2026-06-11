# SLO and Alerting Policy

This document defines reliability objectives and actionable alerting policy.

## SLO Targets

Canonical targets are in `config/slo_targets.json` for:

- availability
- query latency p95
- answer correctness
- error-budget burn

## Alerting Tiers

- Alert threshold
: Signals elevated risk and requires investigation during active working hours.

- Page threshold
: Signals severe customer impact and requires immediate on-call response.

## Runbook Mapping

Each SLO entry includes a runbook path under `docs/runbooks/`.

## Simulation and Validation

- Use `scripts/simulate_slo_alerts.kujo` to evaluate synthetic or captured metrics snapshots.
- Treat simulation output as release-readiness evidence for alert policy operability.
