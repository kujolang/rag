# Startup Configuration Integrity Validation

UPR-005 introduces deterministic startup configuration validation for Kujo RAG.

## Behavior

`main.kujo` validates config before executing any command behavior:

- invalid configuration prints structured JSON diagnostics
- process exits with non-zero status
- no ingest/query/server work starts with invalid config

Error envelope format:

```json
{
  "ok": false,
  "error": "invalid_configuration",
  "message": "Startup configuration validation failed",
  "diagnostics": {
    "ok": false,
    "strict_mode": true,
    "environment": "production",
    "errors": [
      {"code": "strict_requires_api_bearer_token", "field": "api_bearer_token", "message": "..."}
    ]
  }
}
```

## Strict Mode

Strict mode is active when either condition is true:

- `KUJO_RAG_STRICT_CONFIG=true`
- `KUJO_RAG_ENV=production`

Strict mode rejects ambiguous defaults and requires:

- non-empty bearer token (`KUJO_RAG_API_BEARER_TOKEN`)
- non-default namespace
- non-default index path

## Base Integrity Checks

Always validated:

- `index_path` is non-empty
- `api_host` is non-empty
- `api_port` is in range `1..65535`
- `api_ingest_allowed_roots` has at least one entry

## Validation Test

- `tests/test_config_integrity.kujo`
