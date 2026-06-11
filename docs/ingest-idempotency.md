# Ingest Idempotency and Duplicate Job Suppression

This guide documents idempotency-key behavior for `POST /ingest/jobs`.

## Behavior

When idempotency is enabled, repeated `POST /ingest/jobs` requests using the same key within the dedupe window return the original job instead of creating a new one.

- Header key source: configurable via `KUJO_RAG_API_INGEST_IDEMPOTENCY_HEADER` (default `x-idempotency-key`).
- Body fallback key: `idempotency_key` in request JSON payload.
- Scope: key is namespaced internally to avoid cross-namespace collisions.

## Response Metadata

`POST /ingest/jobs` responses now include:

- `idempotency.enabled`
- `idempotency.key`
- `idempotency.deduplicated`
- `idempotency.window_sec`
- `idempotency.expires_at`

## Configuration

- `KUJO_RAG_API_INGEST_IDEMPOTENCY_ENABLED` (default `true`)
- `KUJO_RAG_API_INGEST_IDEMPOTENCY_WINDOW_SEC` (default `900`)
- `KUJO_RAG_API_INGEST_IDEMPOTENCY_HEADER` (default `x-idempotency-key`)
