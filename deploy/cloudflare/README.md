# Temporary Cloudflare Staging Boundary

This deployment is a bounded external security test for the RAG release. It is
not the Kujo Knowledge RAG hosting design and it is not a permanent production
service.

The tested path is:

```text
Cloudflare Access
  -> named Cloudflare Tunnel
  -> 127.0.0.1:8080 Access JWT verifier and claim mapper
  -> 127.0.0.1:8787 Kujo RAG strict-mode origin
```

The GitHub-hosted runner has no public origin listener. `cloudflared` makes an
outbound connection, the verifier accepts only `RS256` application JWTs from
the configured team issuer and application audience, and only explicit
identity mappings can become Kujo roles or namespaces. Client-provided
identity, forwarding, RBAC, and proxy-attestation headers are removed.
The verified user or service-token subject is transformed into a one-way,
deployment-stable SHA-256 pseudonym before it reaches RAG or its audit log.

## Temporary Cloudflare resources

Create these resources only for the external test and record their IDs before
running the workflow:

1. A remotely managed named tunnel with public hostname
   `rag-staging.kujolang.ai` and service `http://localhost:8080`.
2. A self-hosted Access application for the exact staging hostname.
3. An Allow policy limited to named human testers using one-time PIN.
4. A Service Auth policy limited to one temporary service token.
5. A GitHub `cloudflare-staging` environment with required reviewers and the
   secrets named by `.github/workflows/cloudflare-staging-attestation.yml`.

`KUJO_RAG_PROXY_IDENTITY_MAP_JSON` is an explicit JSON object keyed by a
lowercase tester email or the service token Client ID (`common_name`). Each
entry contains only a `role` and `namespace`, for example:

```json
{
  "temporary-service-token-client-id.access": {
    "role": "reader",
    "namespace": "cloudflare_staging"
  }
}
```

Do not commit service-token credentials, tunnel tokens, Access audience values,
identity maps, encryption keys, proxy secrets, or audit integrity keys.

## Execution and teardown

Run `cloudflare-staging-attestation` manually. The job proves that anonymous
requests fail, a mapped service identity can query, forged admin and namespace
headers cannot elevate privilege, the origin remains loopback-only, and audit
artifacts are emitted. The optional hold period permits a named human tester to
complete the browser flow while the tunnel is connected.

After downloading and verifying the evidence artifact:

1. Delete the temporary Access application and both policies.
2. Revoke and delete the temporary service token.
3. Delete the named tunnel and confirm its connector is gone.
4. Confirm `rag-staging.kujolang.ai` no longer resolves or returns content.
5. Delete the GitHub environment secrets; retain only sanitized evidence.

This test supplies proxy-boundary evidence. It does not, by itself, satisfy the
independently protected immutable audit-sink requirements in
`docs/production-security-attestation.md`.
