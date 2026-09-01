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

- authenticated bearer or trusted-proxy mode
- non-default namespace
- non-default index path
- at-rest encryption for indexes, privacy evidence, and runtime state
- RBAC with a non-privileged fallback role
- redaction and keyed, fail-closed audit logging
- HTTPS, host allowlisting, and fail-closed sync for Qdrant

## Base Integrity Checks

Always validated:

- `index_path` is non-empty
- `api_host` is non-empty
- non-loopback `api_host` values require `api_allow_non_loopback=true`
- `api_port` is in range `1..65535`
- `api_ingest_allowed_roots` has at least one entry
- `jwt_proxy` has a proxy secret and explicit trusted peer IPs

## Validation Test

- `tests/test_config_integrity.kujo`
