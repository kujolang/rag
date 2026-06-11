# Large-Corpus Benchmarks and Budgets

UPR-030 adds a deterministic benchmark suite that scales the baseline corpus into small/medium/large dataset tiers, measures ingest throughput and query latency, and enforces budget gates.

## What The Suite Measures

For each profile tier in `config/large_corpus_benchmark_profiles.json`:

- materialized dataset document count (`copies_per_source * source_file_count`)
- ingest elapsed time (`build_rag_index`) and ingest throughput (`docs/sec`)
- query latency for configured benchmark prompts over configured iterations
- average and p95 query latency
- query execution error count

Budget gates are loaded from `config/large_corpus_benchmark_budgets.json`:

- `min_ingest_docs_per_sec`
- `max_avg_query_latency_ms`
- `max_p95_query_latency_ms`

The benchmark exits non-zero when any profile misses budget gates, so CI fails on performance regressions.

## Run Locally

```bash
kujo run scripts/run_large_corpus_benchmarks.kujo --interpreter
```

Default outputs:

- report: `results/large_corpus_benchmark_report.json`
- trend history: `results/large_corpus_benchmark_trend.json`
- generated datasets: `results/benchmark_datasets/*`
- benchmark indexes: `results/benchmark_indexes/*`

## CI Integration

The release gate workflow runs the benchmark suite and uploads outputs as artifacts:

- `large-corpus-benchmarks.json` (step stdout capture)
- `results/large_corpus_benchmark_report.json`
- `results/large_corpus_benchmark_trend.json`

This provides artifact-backed benchmark evidence for each CI run and a persisted local trend history file for regression tracking over time.
