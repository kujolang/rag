# Latency Alert Runbook

1. Confirm `query_latency_percentiles_ms` and `ingest_queue_depth` trends.
2. Identify saturation source (queue depth, high error rates, or dependency contention).
3. Apply mitigations: scale horizontally, reduce expensive query patterns, or throttle abusive traffic.
4. Verify recovery by observing p95/p99 trend normalization.
5. Capture root cause and long-term remediation tasks.
