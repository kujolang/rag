# Index Compaction and Maintenance

UPR-031 adds an index maintenance utility for long-running deployments.

## Script

- `scripts/maintain_index.kujo`

Modes:

- `report` (default): analyze and simulate compaction without writing index changes
- `apply`: run maintenance checks and persist compacted index only when gates pass

## What Compaction Does

- removes duplicate chunks by `chunk_id`
- removes duplicate vectors and lexical entries by `chunk_id`
- removes orphan vectors/lexical entries with no matching chunk
- refreshes maintenance metadata and summary counters in index `meta`

## Correctness and Performance Safety Gates

Before writing compacted output in `apply` mode, the script runs probe queries before and after compaction and enforces:

- correctness gate: no probe query errors and no citation loss when baseline probes already return citations
- performance gate: post-compaction average probe latency must remain within configured regression ratio
- size gate: compacted index serialized size must be less than or equal to baseline size

If any gate fails, `apply` mode exits non-zero and does not write changes.

## Scheduled Maintenance Window Controls

- `KUJO_RAG_INDEX_MAINTENANCE_ALLOWED_UTC_HOURS`: comma-separated hours/ranges (`0-5,22-23`)
- `KUJO_RAG_INDEX_MAINTENANCE_IGNORE_WINDOW=true`: bypass window check for manual runs

When current UTC hour is outside the allowed window, script exits successfully with `skipped=true` and `reason=outside_maintenance_window`.

## Environment Variables

- `KUJO_RAG_INDEX_MAINTENANCE_MODE=report|apply`
- `KUJO_RAG_INDEX_MAINTENANCE_REPORT_PATH=./results/index_maintenance_report.json`
- `KUJO_RAG_INDEX_MAINTENANCE_ALLOWED_UTC_HOURS=0-23`
- `KUJO_RAG_INDEX_MAINTENANCE_IGNORE_WINDOW=false`
- `KUJO_RAG_INDEX_MAINTENANCE_PROBE_QUERIES_PATH=./config/release_eval_golden_queries.json`
- `KUJO_RAG_INDEX_MAINTENANCE_PROBE_LIMIT=3`
- `KUJO_RAG_INDEX_MAINTENANCE_MAX_LATENCY_REGRESSION_RATIO=2`

## Local Usage

Dry-run/report mode:

```bash
kujo run scripts/maintain_index.kujo --interpreter
```

Apply mode inside maintenance window:

```bash
KUJO_RAG_INDEX_MAINTENANCE_MODE=apply \
kujo run scripts/maintain_index.kujo --interpreter
```
