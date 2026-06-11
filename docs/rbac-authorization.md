# Namespace-Scoped RBAC Authorization

UPR-011 introduces namespace-scoped role-based authorization for API actions.

## Enable RBAC

Set:

- `KUJO_RAG_API_RBAC_ENABLED=true`

Required config:

- `KUJO_RAG_API_RBAC_DEFAULT_ROLE`
- `KUJO_RAG_API_RBAC_POLICY_JSON` (optional override; defaults are built-in)

Default policy:

- `admin`: `ingest`, `query`, `admin`, `export`
- `writer`: `ingest`, `query`
- `reader`: `query`

## Role and Namespace Resolution

Role is resolved in this order:

1. JWT proxy auth context claim role (`x-kujo-claim-role`)
2. request header (`x-kujo-role` by default)
3. default role (`api_rbac_default_role`)

Namespace scope is resolved in this order:

1. JWT proxy auth context namespace claim (`x-kujo-claim-namespace`)
2. request header (`x-kujo-namespace` by default)

When a namespace scope is provided, requests are rejected if the target namespace does not match.

## Action Mapping

- Ingest endpoints require `ingest`
- Query endpoint requires `query`
- Root and metrics endpoints require `admin`

## Error Codes

- `rbac_forbidden`: role lacks required action
- `rbac_namespace_forbidden`: namespace scope does not include requested namespace

## Validation Test

- `tests/test_rbac_authorization.kujo`
