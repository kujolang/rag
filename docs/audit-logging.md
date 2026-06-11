# Immutable Audit Logging

Kujo RAG supports a tamper-evident audit mode for security-sensitive API actions.

## What Is Logged

When enabled, audit events include:

- authentication decisions (`allow`/`deny`)
- RBAC decisions (`allow`/`deny`)
- ingest operations and failures
- admin endpoint access outcomes
- startup configuration snapshots

## Configuration

- `KUJO_RAG_API_AUDIT_ENABLED=true|false`
- `KUJO_RAG_API_AUDIT_PATH=./results/security_audit.log`
- `KUJO_RAG_API_AUDIT_EXTERNAL_SINK_MODE=append_file`

Current sink mode:

- `append_file`: events are appended as one JSON object per line.

## Tamper-Evident Chain

Each event stores:

- `sequence`
- `prev_hash`
- `event_hash`

`event_hash` is computed from the previous chain hash plus event payload. This creates a hash chain that detects modification or deletion of historical events.

A sidecar state file (`<audit_path>.state.json`) tracks the current chain head.

## Verification

Use `verify_audit_chain(cfg)` to validate:

- line-level JSON parse integrity
- `prev_hash` linkage
- `event_hash` correctness
- chain-head match with sidecar state

## External Sink Notes

For production, treat the audit file path as an external append-only sink target (for example, mounted write-only volume or forwarded collector path) and apply filesystem ACLs that prevent non-auditor modification.
