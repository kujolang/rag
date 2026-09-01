# Qdrant-Compatible Vector Backend Adapter

This document describes the `qdrant_http` vector backend mode introduced for UPR-034/L029.

## Why this backend exists

- Provides an ANN-oriented external backend integration path without changing the public API contract.
- Keeps a local JSON mirror for deterministic recovery and offline fallback behavior.
- Allows staged rollout with optional sync (`fail-open` or strict sync-failure behavior).

## Backend mode

Set:

```bash
KUJO_RAG_VECTOR_BACKEND=qdrant_http
```

Supported behavior:

- `load`: reads the local mirror index file.
- `save`: always writes the local mirror index file.
- `save` with sync enabled: replaces the remote collection contents so the
  remote backend is an authoritative mirror, including empty/deleted indexes.

## Environment variables

- `KUJO_RAG_VECTOR_BACKEND_QDRANT_URL`: base URL (example: `http://127.0.0.1:6333`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_COLLECTION`: target collection name
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_API_KEY`: optional API key sent as `api-key` header
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_SYNC_ENABLED`: `true|false` (default `false`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_TIMEOUT_MS`: request timeout in milliseconds
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_FAIL_OPEN`: `true|false` (default `true`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_ALLOWED_HOSTS`: comma-separated endpoint hosts
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_MIRROR_PATH`: optional explicit local mirror file path

## Sync behavior

When `KUJO_RAG_VECTOR_BACKEND_QDRANT_SYNC_ENABLED=true` and URL is configured:

1. Deletes the existing collection, accepting an absent collection as empty.
2. For a non-empty index, recreates the collection and upserts the complete
   current vector set with `wait=true`.
3. For an empty index, leaves the collection absent and records
   `collection_cleared`; this is the deletion contract used by privacy and
   retention workflows.
4. Writes sync metadata in index `meta`:
   - `qdrant_last_sync_ok`
   - `qdrant_last_sync_reason`
   - `qdrant_points_synced`
   - `qdrant_last_sync_at`

If sync fails:

- `KUJO_RAG_VECTOR_BACKEND_QDRANT_FAIL_OPEN=true`: save succeeds using mirror persistence and records sync failure metadata.
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_FAIL_OPEN=false`: save returns failure.

Strict/production mode additionally requires an `https://` URL, an exact host
allowlist match, and fail-closed synchronization. API-key headers are passed to
curl through a short-lived header file rather than process arguments, and the
header and content payload files are created with owner-only permissions in the
OS temporary directory and deleted after both success and failure. HTTP 4xx/5xx
responses fail synchronization rather than being mistaken for successful curl
process execution.

## Validation

Run backend contract coverage:

```bash
export KUJO_BIN=/path/to/kujo/target/debug/kujo
$KUJO_BIN run tests/test_backend_contract.kujo --interpreter
```

This test verifies backend swap behavior for `local_json`, `memory`, and `qdrant_http` modes.
