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
