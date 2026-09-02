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
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_SYNC_MODE`: `legacy_replace|staged_alias` (default `legacy_replace`; strict mode requires `staged_alias`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_ALIAS`: stable query alias (default `<collection>__active`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_JOURNAL_PATH`: optional recovery-journal path (default `<mirror>.qdrant-journal.json`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_GC_ENABLED`: enables delayed generation cleanup (default `false`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_GC_GRACE_SEC`: minimum generation age before deletion (default `86400`, bounded to `60..2592000`)
- `KUJO_RAG_VECTOR_BACKEND_QDRANT_GC_MAX_PER_SAVE`: maximum deletions attempted per save (default `1`, bounded to `1..10`)

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

### Staged alias mode

`staged_alias` creates a new generation collection, uploads all candidate points,
performs an exact point-count verification, and then changes visibility with one
Qdrant alias action. It never deletes or mutates the active collection before
verification. An atomic local journal records every phase; a journal left at
`alias_committed` is surfaced as `qdrant_recovery_required` on load instead of
silently treating the prior mirror as current. Empty authoritative indexes use
the configured embedding dimension and follow the same verified alias commit.
The runtime writes `alias_commit_started` before the visibility request; a
timeout or transport failure becomes `alias_commit_ambiguous`. Any unresolved
journal phase blocks subsequent staged saves so a retry cannot overwrite the
only recovery evidence or create an unbounded series of orphan generations.
Before remote mutation, the candidate mirror is persisted atomically beside the
journal. Startup/load recovery resolves the live alias: when it points to the
candidate, the durable candidate mirror is committed forward locally; when it
still points to the recorded prior generation, the candidate is marked abandoned
and queued for later garbage collection. An unrelated alias target fails with
`qdrant_concurrent_writer_detected` instead of guessing through a multi-writer race.

The default alias is `<collection>__active` so it cannot collide with an existing
legacy collection of the configured name. Query clients must use this alias after
migration. `legacy_replace` retains the previous delete-and-recreate behavior for
one non-strict compatibility window and is rejected by strict configuration.

Prior and abandoned managed generations are recorded durably in `gc_pending`.
Optional GC re-resolves the live alias before every bounded deletion, rejects
collection names outside the managed `<collection>__gen_` prefix, honors the
configured grace window, and deletes at most the configured per-save limit.
It is disabled by default. Automated operator-requested rollback remains required
before operators should enable unattended recovery actions. Candidate
verification proves exact cardinality and requires every payload to carry the
expected generation digest. It does not yet read every stored vector back and
rehash it; deployments requiring full storage-level content attestation must
keep staged mode behind an operator gate until vector read-back is implemented.

## Validation

Run backend contract coverage:

```bash
export KUJO_BIN=/path/to/kujo/target/debug/kujo
$KUJO_BIN run tests/test_backend_contract.kujo --interpreter
```

This test verifies backend swap behavior for `local_json`, `memory`, and `qdrant_http` modes.
