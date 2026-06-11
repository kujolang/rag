# Chaos and Fault-Injection Scenarios

This document defines the UPR-084 reliability review baseline for controlled failure testing in Kujo RAG.

## Goals

- Validate bounded behavior under injected faults.
- Prove graceful degradation instead of uncontrolled crashes.
- Require observability signals for every fault class.
- Require recovery verification after fault removal.

## Canonical Scenario Matrix

Source of truth: `config/chaos_fault_injection_scenarios.json`

Required scenario classes:

1. timeout
2. storage failure
3. dependency failure

Each scenario must define:

- `fault_type`
- `enabled`
- `expected.bounded_behavior`
- `expected.observability_signal`
- `expected.recovery_check`
- `assertions` including `bounded_behavior`, `observability_signal`, and `recovery_check`

## Execution Contract

Run deterministic validation:

```bash
kujo run scripts/run_chaos_fault_injection_review.kujo --interpreter
```

Run pass/fail regression suite:

```bash
kujo run tests/test_chaos_fault_injection_review.kujo --interpreter
```

Gate output artifact:

- `results/reliability/chaos_fault_injection_status.json`

## Operational Notes

- This baseline focuses on repeatable policy-level chaos coverage, not ad hoc one-off experiments.
- Scenario changes must update both the JSON matrix and this document in the same change.
- Release promotion requires this gate to pass via `release-gates` CI.