# Async Ingest Workers

UPR-032 introduces a queue-backed ingest worker mode for `POST /ingest/jobs` so heavy ingest requests can be decoupled from request submission.

## Modes

- `inline` (default): `POST /ingest/jobs` executes ingest immediately and returns a completed `job` payload when work finishes.
- `queue`: `POST /ingest/jobs` enqueues a `submitted` job and returns immediately; worker cycles advance jobs through `running` to `succeeded` or `failed`.

Configure mode with:

- `KUJO_RAG_API_INGEST_JOBS_MODE=inline|queue`

## Worker Controls

Queue mode uses cooperative worker cycles. A worker cycle processes up to a bounded number of queued jobs and updates ingest job status.

- `KUJO_RAG_API_INGEST_WORKER_BATCH_SIZE` (default `1`, clamped to `1..20`)
- `KUJO_RAG_API_INGEST_WORKER_MAX_RUNNING` (default `1`, clamped to `1..10`)

## Endpoints

- `POST /ingest/jobs`
  - queue mode: returns `202` with `worker_mode=queue` and `job.status=submitted`
  - inline mode: returns `202` with `worker_mode=inline` and terminal job status
- `POST /ingest/jobs/status`
  - returns current job status
  - in queue mode, also advances one worker cycle before returning
  - includes `worker` metadata (`mode`, `processed_jobs`)
- `POST /ingest/jobs/worker/tick`
  - admin endpoint to explicitly execute one worker cycle
  - returns `processed_jobs` and current `queue_depth`

## Operational Notes

- Queue-mode workers preserve the existing synchronous `/ingest` endpoint for local workflows.
- Ingest idempotency behavior is unchanged: idempotent retries still return the existing job when the key is active.
- Queue depth is reflected in the metrics snapshot under `ingest_queue_depth`.

## Validation

- `tests/test_async_ingest_workers.kujo` verifies queue submission/progression and inline backward compatibility.
- `tests/test_api_contract.kujo` validates API contract remains compatible.
