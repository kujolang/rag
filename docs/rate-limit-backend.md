# Distributed Rate-Limit Backend Option

This project supports pluggable API rate-limit state backends.

## Modes

- `memory` (default): per-process in-memory buckets.
- `shared_file`: persists rate-limit state to a shared JSON file for multi-instance coordination on shared storage.

## Configuration

- `KUJO_RAG_API_RATE_LIMIT_BACKEND` (`memory` or `shared_file`)
- `KUJO_RAG_API_RATE_LIMIT_BACKEND_FILE` (path used by `shared_file` mode)

## Operational Notes

- `shared_file` mode is intended for simple multi-instance deployments sharing a filesystem.
- Buckets and dynamic block state are loaded and persisted per request cycle; shared-file state takes precedence over process-local runtime state in `shared_file` mode.
- For higher concurrency and stronger consistency guarantees, use external distributed stores in future backend adapters.
