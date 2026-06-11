# Sensitive Data Redaction Policy

This document defines redaction behavior for API logs and error payloads.

## Goals

- Prevent leakage of secrets/tokens in access logs.
- Prevent sensitive details in API error payloads.
- Keep behavior configurable for deployment needs.

## Configuration

- `KUJO_RAG_API_REDACTION_ENABLED` (default: `true`)
- `KUJO_RAG_API_REDACTION_MASK` (default: `[REDACTED]`)
- `KUJO_RAG_API_REDACTION_KEYS` (comma-separated key/name patterns)
- `KUJO_RAG_API_REDACTION_VALUES` (comma-separated literal values to scrub)

Defaults redact common secret-bearing keys including:

- `authorization`
- `token`
- `api_key`
- `apikey`
- `secret`
- `password`
- `passphrase`
- `x-api-key`
- `set-cookie`
- `cookie`
- `bearer`
- `openai_api_key`

## Runtime Behavior

- Access logging sanitizes `extra` payload values before emission.
- Error responses sanitize `details` when redaction is enabled.
- In `production` runtime, HTTP `5xx` responses are forced to a generic message and omit details.

## Validation Coverage

- `tests/test_redaction_policy.kujo` validates key/value redaction and disabled-mode pass-through.
- `tests/test_api_contract.kujo` validates production-safe error messaging behavior.
