# SRE Metrics Expansion

This document defines expanded operational metrics exposed by `GET /metrics`.

## Core Counters

- `ingest_requests`
- `query_requests`
- `ingest_errors`
- `query_errors`
- `auth_failures`

## Latency

- Histogram buckets:
: `ingest_latency_ms`, `query_latency_ms`

- Percentile approximations:
: `ingest_latency_percentiles_ms` (`p50`, `p95`, `p99`)
: `query_latency_percentiles_ms` (`p50`, `p95`, `p99`)

## Query Stage Timings

- `query_stage_timings_ms`

Stage keys:

- `tokenize`
- `embed`
- `retrieve`
- `rerank`
- `synthesize`

Each stage exposes:

- `avg_ms`: rolling average stage duration in milliseconds
- `last_ms`: most recent stage duration in milliseconds
- `samples`: number of observed query executions for the stage

## Saturation and Throughput

- `ingest_queue_depth`
- `ingest_throughput_per_min`

## Cache and Error Surfaces

- `cache_hits`
- `cache_misses`
- `cache_hit_ratio`
- `query_cache_entries`
- `embedding_cache_hits`
- `embedding_cache_misses`
- `embedding_cache_entries`
- `error_cardinality`

## Tenant Quota Controls

- `tenant_quota`

Fields:

- `enabled`
- `query_rate_window_sec`
- `query_rate_max_requests`
- `ingest_max_chunks_per_request`
- `storage_max_chunks`
- `rejections` (per-namespace map keyed by quota type such as `query_rate`, `ingest_volume`, `storage`)

## Tenant-Level Views

`tenant_views` includes per-namespace dimensions:

- `chunks`
- `last_ingest_unix_ms`
- `ingest_requests`
- `query_requests`
- `ingest_errors`
- `query_errors`
- `quota_rejections`
