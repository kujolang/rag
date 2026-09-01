# Structured Logs and Correlation IDs

This document defines request-traceable structured logging behavior.

## Access Log Schema

Access logs are emitted as JSON objects under `access` with these core fields:

- `ts`
- `request_id`
- `correlation_id`
- `method`
- `path`
- `ip`
- `status`
- `extra`

## Correlation Rules

- `request_id` resolution order:
: `X-Request-ID` header, then `X-Correlation-ID`, then generated fallback.

- `correlation_id` resolution order:
: `X-Correlation-ID` header, then resolved `request_id`.

## API Response Propagation

All JSON success/error responses include:

- `request_id`
- `correlation_id`

Responses also include the headers:

- `X-Request-ID`
- `X-Correlation-ID`

This enables end-to-end traceability between clients and server logs.

`ip` comes from the Kujo runtime's socket-derived `peer_ip`. Older compatible
runtimes fall back to `remote_addr`; forwarding headers are never used for rate
limiting or audit identity.

In strict production mode, the security audit uses a secret-keyed hash chain,
verifies the log and checkpoint before every append and at startup, and stops
the service on append or checkpoint failure. A missing log or checkpoint is an
integrity failure when the surviving counterpart proves that prior events
existed. Deployments still need an independently protected or immutable sink to
survive an actor that can delete both local files.
