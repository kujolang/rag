# Graceful Shutdown and Zero-Downtime Safeguards

This guide defines the drain-mode workflow used to remove an instance from traffic before shutdown.

## Drain Controls

The API exposes admin drain endpoints:

- `GET /drain`: current drain state and queue/inflight summary.
- `POST /drain/start`: enable draining and reject mutating traffic.
- `POST /drain/stop`: disable draining and resume normal mutations.

When drain mode is enabled:

- `GET /ready` returns `503` with `reason=draining`.
- `POST /query`, `POST /ingest`, and `POST /ingest/jobs` return `503 service_draining`.
- Health endpoints remain available for control-plane visibility.

## Configuration

- `KUJO_RAG_API_DRAIN_REJECT_MUTATIONS` (default `true`): reject mutating routes while draining.
- `KUJO_RAG_API_DRAIN_PRE_STOP_MS` (default `5000`): operator hint for pre-stop delay budget.

## Rolling Deployment Pattern

1. Call `POST /drain/start` with optional reason.
2. Wait for readiness probe to flip unhealthy (`/ready` -> `503`).
3. Keep instance alive for at least `KUJO_RAG_API_DRAIN_PRE_STOP_MS`.
4. Stop process/container after in-flight and queued work is drained.
5. Replace node and call `POST /drain/stop` only if node remains in service.

## Example

```bash
curl -s -X POST http://127.0.0.1:8787/drain/start -H "Content-Type: application/json" -d '{"reason":"rolling_deploy"}'
curl -s http://127.0.0.1:8787/ready
curl -s http://127.0.0.1:8787/drain
```
