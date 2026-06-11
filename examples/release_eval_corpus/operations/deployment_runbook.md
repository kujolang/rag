# Deployment Runbook

Standard deploy flow:
1. Shift 5 percent of traffic to the canary deployment.
2. Validate error budget and p95 latency for 15 minutes.
3. Increase traffic to 50 percent if canary metrics stay green.
4. Complete full rollout after final smoke checks.

Rollback procedure:
1. Freeze further rollouts.
2. Route all traffic back to the last known good release.
3. Run integrity checks on queue and index state.
