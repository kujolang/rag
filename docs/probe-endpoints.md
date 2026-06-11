# Liveness, Readiness, and Startup Probes

This document defines probe semantics for deployment orchestrators.

## Endpoints

- `GET /live`: process liveness signal.
- `GET /ready`: traffic readiness signal.
- `GET /startup`: startup lifecycle signal.
- `GET /health`: compatibility summary endpoint.

All probe routes support CORS preflight (`OPTIONS`).

## Semantics

- `/live`
: Returns HTTP `200` while the process can serve requests.

- `/startup`
: Returns HTTP `503` with code `startup_incomplete` until startup grace period elapses.
: Returns HTTP `200` once startup is complete.

- `/ready`
: Returns HTTP `200` when startup is complete and required dependencies are ready.
: Returns HTTP `503` with code `service_not_ready` when startup is incomplete, index state is missing, or readiness is intentionally forced off.

## Configuration

- `KUJO_RAG_API_STARTUP_GRACE_MS` (default `1000`)
: Startup readiness grace window in milliseconds.

- `KUJO_RAG_API_READINESS_FORCE_UNREADY` (default `false`)
: Force readiness endpoint to return unready (`503`) for probe/degradation testing.

## Response Fields

Readiness and startup responses include probe diagnostics:

- `status`
- `startup_complete`
- `startup_deadline_ms`
- `now_unix_ms` (startup)
- `has_index` (readiness)
- `forced_unready` (readiness)
- `reason` (readiness)
