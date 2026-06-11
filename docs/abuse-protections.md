# Abuse Protections and Anomaly Hooks

This document describes API abuse hardening controls added for burst limiting, IP-aware throttling, and anomaly hook events.

## Controls

Rate limiting now has two layers:

- Window limit: requests per `api_rate_limit_window_sec`.
- Burst limit: short-window requests per `api_rate_limit_burst_window_sec`.

Additional abuse controls:

- Static IP blocklist via configuration.
- Optional anomaly hook event emission into audit logs.
- Optional dynamic auto-block when repeated violations exceed threshold.

## Configuration

Environment variables:

- `KUJO_RAG_API_RATE_LIMIT_WINDOW_SEC`
- `KUJO_RAG_API_RATE_LIMIT_MAX_REQUESTS`
- `KUJO_RAG_API_RATE_LIMIT_BURST_WINDOW_SEC`
- `KUJO_RAG_API_RATE_LIMIT_BURST_MAX_REQUESTS`
- `KUJO_RAG_API_RATE_LIMIT_BUCKET_TTL_SEC`
- `KUJO_RAG_API_RATE_LIMIT_MAX_KEYS`
- `KUJO_RAG_API_ABUSE_BLOCKLIST_IPS` (comma-separated)
- `KUJO_RAG_API_ANOMALY_HOOK_ENABLED`
- `KUJO_RAG_API_ANOMALY_AUTO_BLOCK_ENABLED`
- `KUJO_RAG_API_ANOMALY_VIOLATION_THRESHOLD`
- `KUJO_RAG_API_ANOMALY_BLOCK_TTL_SEC`

## API Error Codes

When abuse protections reject a request, API returns HTTP `429` with structured error codes:

- `rate_limited`: standard window limit exceeded.
- `burst_limited`: burst window exceeded.
- `ip_blocked`: static or dynamic blocklist enforcement.

Error details include configured limits and, when applicable, `blocked_until_unix_ms`.

## Anomaly Hook Events

When `KUJO_RAG_API_ANOMALY_HOOK_ENABLED=true`, anomaly events are emitted via audit logging with type `anomaly_hook` for:

- `static_blocklist`
- `dynamic_block`
- `burst`
- `rate`
- `auto_block`

This provides a hook point for external SIEM/monitoring pipelines through existing audit sinks.
