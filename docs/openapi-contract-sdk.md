# OpenAPI Contract and Generated SDK Workflow

This document defines the UPR-080 API productization workflow for Kujo RAG.

## Canonical Artifacts

- OpenAPI contract: `./openapi/kujo-rag-openapi.json`
- Generated JavaScript SDK: `sdk/javascript/kujo-rag-client.generated.js`
- Contract review runner: `scripts/run_openapi_contract_review.kujo`
- Gate output artifact: `results/api/openapi_contract_status.json`

## Contract Rules

- The OpenAPI document must represent the current HTTP API routes.
- Every required route must declare an `operationId`.
- `info.x-kujo-rag-api-version` must be present and treated as the API contract version marker.
- The generated SDK must remain in sync with the OpenAPI contract.

## SDK Generation and Validation

Regenerate the JavaScript SDK from the OpenAPI contract:

```bash
KUJO_RAG_OPENAPI_REGENERATE=true kujo run scripts/run_openapi_contract_review.kujo --interpreter
```

Validate contract and SDK sync without mutating files:

```bash
kujo run scripts/run_openapi_contract_review.kujo --interpreter
```

The runner exits non-zero when:

- required paths or operation IDs are missing
- OpenAPI metadata is incomplete
- the checked-in SDK is stale relative to the OpenAPI contract
- release/workflow linkage is missing

## CI Workflow

`.github/workflows/openapi-contract-review.yml` runs the same validator on schedule and manual dispatch and publishes:

- `openapi-contract-status.json`
- `results/api/openapi_contract_status.json`
- `openapi/kujo-rag-openapi.json`
- `sdk/javascript/kujo-rag-client.generated.js`

## Release Linkage

Release promotion requires a passing OpenAPI contract/SDK gate through `docs/release-process.md` and `.github/workflows/release-gates.yml`.
