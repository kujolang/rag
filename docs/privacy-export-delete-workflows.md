# Privacy Export and Deletion Workflows

This document defines namespace-scoped privacy operations for export and deletion evidence handling.

## Scope

Privacy workflows operate on a resolved namespace and include:

- indexed retrieval artifacts (`chunks`, `vectors`, `lexical`, `documents_index`)
- namespace session memory (`sessions` entries scoped by namespace)
- namespace ingest operational state (`ingest_jobs`, `ingest_queue`, `ingest_idempotency`)
- namespace retention and legal-hold state snapshots (`retention_policies`, `legal_holds`)
- namespace runtime metrics and quota buckets tied to tenant-level accounting

Global immutable logs and system-level aggregate counters remain out of deletion scope.

## Endpoints

### POST /privacy/export

Exports namespace data into a timestamped JSON artifact under `./results/privacy/`.

Request body:

```json
{
  "namespace": "tenant-a",
  "export_type": "privacy_request"
}
```

Response highlights:

- `data.export.path`: artifact path
- `data.summary`: snapshot counts (`chunk_count`, `vector_count`, `lexical_count`, `document_count`, `path_count`)
- `data.scope`: export scope list

### POST /privacy/delete

Performs namespace deletion with verifiable evidence.

Request body:

```json
{
  "namespace": "tenant-a",
  "reason": "user_delete_request"
}
```

Delete behavior:

1. Writes a pre-delete export artifact (`delete_preflight`).
2. Rebuilds namespace index as empty (`chunks`, `vectors`, `lexical` cleared).
3. Removes namespace-scoped session, ingest, cache, retention, and tenant-runtime state.
4. Persists the deleted namespace index via configured vector backend.
5. Writes a post-delete receipt artifact (`delete_receipt`).

Response highlights:

- `data.pre_delete_export.path`
- `data.deletion_receipt.path`
- `data.summary_before`
- `data.summary_after`
- `data.deleted_scopes`

## Legal-Hold Interlock

`POST /privacy/delete` is blocked when legal hold is enabled for the namespace.

- HTTP status: `409`
- error code: `legal_hold_active`
- response includes hold reason for auditability

Use `POST /retention/legal-hold/stop` to release a hold before retrying deletion.

## Evidence Artifacts

Artifacts are written to:

- `./results/privacy/<export_type>__<namespace_slug>__<timestamp>.json`

When at-rest encryption is enabled, artifacts are atomically persisted as
`kujo_rag_encrypted_artifact_v1` envelopes. A protection or write failure is an
operation failure; delete never proceeds if its pre-delete evidence cannot be
persisted.

The protected payload contains:

- request metadata (`namespace`, `export_type`, `generated_at_ms`)
- index summary
- full index payload for export/receipt traceability

## Operational Notes

- All privacy routes require API authentication and namespace-scoped `admin` authorization.
- Deletion endpoints are mutation routes and respect drain mode (`service_draining` safeguards).
- Audit events are emitted for both export and deletion operations, including artifact paths and deletion counts.
