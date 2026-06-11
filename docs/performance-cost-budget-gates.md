# Performance and Cost Budget Gates

This document defines UPR-086 workload-class budget gates for performance, resource usage, and estimated runtime cost.

## Purpose

- Enforce latency/throughput and resource budgets by workload class.
- Detect regressions with trend comparison against prior benchmark runs.
- Block release promotion when budget regression thresholds are exceeded.

## Inputs and Policy

- Benchmark report source: `results/large_corpus_benchmark_report.json`
- Policy baseline: `config/performance_cost_budget_policy.json`
- Trend history: `results/performance/performance_cost_budget_trend.json`

The policy defines:

1. `workload_classes` budgets (`small`, `medium`, `large`)
2. `cost_model` coefficients used for estimated per-query and per-1k-query cost
3. `regression_thresholds` for latency, throughput retention, and estimated cost drift

## Gate Runner

Run budget evaluation:

```bash
kujo run scripts/run_performance_cost_budget_review.kujo --interpreter
```

Run pass/fail regression test:

```bash
kujo run tests/test_performance_cost_budget_review.kujo --interpreter
```

Output artifact:

- `results/performance/performance_cost_budget_status.json`

## CI and Release Integration

- Dedicated workflow: `.github/workflows/performance-cost-budget-review.yml`
- Required release-gate linkage: `.github/workflows/release-gates.yml`
- Required release input linkage: `docs/release-process.md`