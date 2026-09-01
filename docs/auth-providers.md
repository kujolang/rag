# Auth Providers

UPR-010 introduces pluggable API auth providers while preserving legacy bearer mode.

## Provider Modes

Configure with `KUJO_RAG_API_AUTH_PROVIDER`:

- `none`: no authentication checks (local/dev only)
- `bearer`: legacy static bearer token validation
- `jwt_proxy`: OIDC/JWT claim validation using trusted proxy-forwarded claims

## Bearer Mode

Environment variables:

- `KUJO_RAG_API_AUTH_PROVIDER=bearer`
- `KUJO_RAG_API_BEARER_TOKEN=<token>`
- `KUJO_RAG_API_BEARER_TOKEN_NEXT=<next_token>` (optional rotation window)
- `KUJO_RAG_API_BEARER_REVOKED_TOKENS=<csv_tokens>` (optional immediate revocation)

Behavior:

- Requires `Authorization: Bearer <token>`
- Rejects missing/invalid tokens with structured auth errors
- Accepts either active or next token during rotation window
- Rejects any token listed in revocation list (`revoked_token`)
- Does not accept caller-supplied RBAC role or namespace headers; the shared
  bearer identity uses the configured default role and namespace

## JWT Proxy Mode

Environment variables:

- `KUJO_RAG_API_AUTH_PROVIDER=jwt_proxy`
- `KUJO_RAG_API_JWT_ISSUER=<expected_issuer>`
- `KUJO_RAG_API_JWT_AUDIENCE=<expected_audience>`
- `KUJO_RAG_API_JWT_CLOCK_SKEW_SEC=60` (optional)
- `KUJO_RAG_API_TRUSTED_PROXY_SECRET=<secret>` (required)
- `KUJO_RAG_API_TRUSTED_PROXY_SECRET_HEADER=x-kujo-proxy-secret`
- `KUJO_RAG_API_TRUSTED_PROXY_IPS=<csv peer IPs>` (required)

Expected request headers:

- `Authorization: Bearer <upstream-valid-token>`
- `x-kujo-claim-iss`
- `x-kujo-claim-aud`
- `x-kujo-claim-exp` (unix seconds)
- `x-kujo-claim-sub` (optional)
- `x-kujo-claim-role` (optional RBAC role)
- `x-kujo-claim-namespace` (optional RBAC namespace scope)
- `x-kujo-proxy-secret` (or configured equivalent; injected only by the proxy)

Validation:

- issuer equality check
- audience inclusion check
- expiry check with configurable clock skew
- peer socket identity must be in the configured trusted-proxy allowlist
- proxy attestation is compared by digest before any forwarded claim is trusted

## Security Notes

- `jwt_proxy` mode requires token signature verification by an upstream trusted proxy/identity layer.
- The trusted proxy must remove client-supplied claim and RBAC headers before
  adding verified identity values, and must replace any client-supplied proxy
  attestation header with the configured secret.
- Direct-backend requests cannot self-assert claims: both trusted peer identity
  and proxy attestation must validate first.
- In strict production mode, `api_auth_provider=none` is rejected.
- In strict production mode, `jwt_proxy` requires issuer, audience, proxy secret,
  and explicit proxy-peer configuration.

## Validation Test

- `tests/test_auth_providers.kujo`
