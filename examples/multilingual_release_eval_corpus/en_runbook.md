# Deployment Runbook (English)

Canary rollout starts with 5 percent of traffic.
Promote from 5 percent to 50 percent only after the error budget stays under 1 percent.
If p95 latency grows above the release threshold, trigger rollback.
