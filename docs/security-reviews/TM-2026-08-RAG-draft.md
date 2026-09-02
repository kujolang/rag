# Kujo RAG Threat-Model Review Packet (Draft)

> Preparatory evidence only. This document is not a completed Security Team
> review, approval, risk acceptance, or replacement for the cadence record in
> `config/threat_model_review_plan.json`.

## Review metadata

- Review ID: `TM-2026-08-RAG-DRAFT`
- Prepared: 2026-09-01
- Repository: `kujolang/rag`
- Branch: `main`
- RAG base commit: `b850db11f353a9ffbaea627d1991e62d7c281fb0`
- Kujo runtime release: `v1.2.2` / `22582e7f0111a1005002579b44f5d03cd2ed1c9c`
- Required reviewer: Security Team
- Approval status: awaiting accountable human review
- Scope: HTTP API exposure, authentication, authorization, remote ingestion,
  persistence, external vector synchronization, privacy workflows, audit data,
  and Kujo runtime HTTP controls

## System and trust boundaries

The local-first CLI can ingest and query without a network listener. `serve`
adds an HTTP boundary and routes requests through the controls in
`src/query_api.kujo`. The principal data flow is:

```text
client -> optional trusted proxy -> Kujo RAG HTTP API
                                      |-> allowed local ingest roots
                                      |-> local JSON index and runtime state
                                      |-> optional Qdrant-compatible endpoint
                                      |-> audit, privacy, and release artifacts
```

The review must treat these as separate trust boundaries:

1. The client-to-proxy and client-to-RAG network paths.
2. Proxy-injected identity headers versus attacker-controlled request headers.
3. The RAG process versus local files allowed for ingestion.
4. The RAG process versus optional Qdrant-compatible infrastructure.
5. Runtime indexes and generated privacy/audit artifacts versus other local
   users, backup systems, and artifact publishers.

Critical assets include source documents, index chunks and embeddings,
namespace boundaries, bearer credentials, proxy-derived identity claims,
encryption keys, Qdrant credentials, privacy exports, deletion receipts, audit
logs, and the integrity of persisted indexes.

## Confirmed controls

- `api_host` now controls the socket bind address through
  `http_listen(host, port)`; loopback is the default. Coverage is in
  `tests/test_api_bind_contract.kujo` and `tests/test_api_contract.kujo`.
- Production or strict configuration rejects no-auth operation, missing bearer
  credentials, missing JWT proxy issuer/audience and proxy attestation,
  disabled RBAC/audit/redaction/encryption, fail-open audit or Qdrant behavior,
  privileged fallback roles, default namespace use, and the default index path
  (`src/config.kujo`).
- The Kujo runtime enforces a bounded pre-buffer request size, request-body read
  deadline, 408/413 responses, and peer socket identity in interpreter and VM
  paths.
- API JSON parsing applies the smaller application limit configured by
  `api_max_body_bytes` (`src/query_api.kujo`).
- Remote ingestion canonicalizes paths, enforces configured roots, rejects
  symlink descendants during discovery and immediately before parsing, and
  revalidates queued jobs at execution (`src/query_api.kujo`,
  `src/ingestion.kujo`).
- Local index writes are atomic, retain the last readable index on failure, and
  perform read-after-write schema validation (`src/vector_store.kujo`).
- Rate limiting uses runtime-provided peer socket identity rather than forwarded
  headers (`src/query_api.kujo`).
- Qdrant synchronization is opt-in, HTTPS/host-allowlisted/fail-closed in
  strict mode, keeps credentials out of process arguments, and replaces remote
  collection contents so purge and privacy deletion remove stale vectors
  (`src/vector_backend.kujo`).
- Content-bearing indexes, privacy artifacts, and API runtime state use
  atomic encrypted envelopes with key-bound integrity tags. Strict mode rejects
  plaintext and unsigned downgrade attempts (`src/vector_store.kujo`).
- Strict audit mode uses a secret-keyed chain, verifies the log/checkpoint at
  startup and before append, and exits on append or checkpoint failure.

## Threat scenarios requiring review

| ID | Scenario and impact | Current control | Decision or evidence required |
|---|---|---|---|
| TM-01 | A deployment intended for loopback accidentally listens on every interface, exposing unauthenticated or privileged routes. | Source-remediated: loopback is default, non-loopback requires explicit opt-in, CLI overrides are revalidated, direct server startup validates again, and Compose publishes only `127.0.0.1`. | Verify the deployed listener and firewall rules. Treat explicit non-loopback opt-in as security-sensitive. |
| TM-02 | A client bypasses the trusted proxy and forges `x-kujo-claim-*` headers. | Source-remediated for direct bypass: claims require both a socket-derived allowlisted proxy peer and a secret proxy attestation; deterministic negative tests reject direct and malformed assertions. | Prove the real proxy verifies JWT signatures, strips all client identity/attestation headers, injects the secret, and is the only reachable backend peer. In-process JWT verification remains the stronger future contract. |
| TM-03 | A bearer client self-asserts admin or wildcard namespace scope. | Source-remediated: bearer/none contexts ignore identity headers, fallback is reader, strict mode requires RBAC and rejects privileged fallback policy, and global job controls retain explicit trusted-admin behavior. | Verify deployed bearer role/namespace and proxy claim mapping are least privilege. |
| TM-04 | Development defaults are promoted or exposed without credentials, encryption, RBAC, audit, or redaction. | Source-remediated: strict/production startup requires the full security baseline and every listener entry path validates after overrides. | Verify production actually enables strict mode and does not replace the loopback Compose publication. |
| TM-05 | An authorized ingest reads sensitive local files or crosses a path boundary. | Partially source-remediated: allowed-root checks, descendant symlink rejection, immediate pre-parse checks, and queued-job execution revalidation reduce known paths. | Review service-account permissions and root ownership. Descriptor-relative no-follow opens are still needed to eliminate the final validation/use race on writable trees. |
| TM-06 | Privacy artifacts expose full namespace contents after the request. | Source-remediated: privacy export, delete preflight, and receipt artifacts use the same atomic encrypted/integrity-tagged contract as indexes; failures are surfaced. | Define permissions, retention, backup, and publication policy for `results/privacy`; ensure CI never uploads it generically. |
| TM-07 | A malicious/misconfigured Qdrant endpoint receives chunks, vectors, or credentials, or stale remote vectors survive deletion. | Source-remediated: strict HTTPS and exact-host allowlist, fail-closed sync, credential header files outside process args, HTTP-status failures, authoritative collection replacement, empty-index clearing, and destructive-handler failure propagation. | Approve the deployed endpoint/DNS/TLS trust and secret manager. Cross-system local/remote writes are not transactional and require monitoring/retry. |
| TM-08 | Indexes, runtime state, backups, or side artifacts disclose source content or accept plaintext downgrade. | Source-remediated for repository-managed content: encrypted atomic envelopes cover index/privacy/runtime state, use keyed integrity tags, and reject plaintext/unsigned strict-mode downgrade. | Verify filesystem/backup permissions and migrate legacy unsigned envelopes before strict mode. Shared rate state and redacted audit metadata are non-content-bearing by contract. |
| TM-09 | Oversized, slow, or complete HTTP bodies exhaust resources or wait for the read deadline. | Source-remediated in signed Kujo v1.2.2: interpreter/VM reject declared overflow before reading, stop at declared lengths, retain bounded unknown-length reads and deadlines, and expose peer identity. RAG pins the checksum-verified release and has live dual-mode regressions. | Verify deployed proxy timeouts are no weaker and prohibit pre-v1.2.2 artifacts in production. |
| TM-10 | A failed/oversized write is reported successful and later reloads empty. | Source-remediated: atomic persistence, read-after-write validation, explicit errors, prior-index preservation, size-range tests, and aggregate-runner inclusion. | Confirm hosted gates run the newly published runtime artifact; an unreadable index must remain a startup/ingest failure. |
| TM-11 | Audit logs are disabled, tampered with, truncated, or silently lose events. | Partially source-remediated: strict mode requires keyed fail-closed audit; startup and pre-append verification detect content, missing-log, missing-checkpoint, and checkpoint-write failures; trace appends use the checked path. | Assign ownership/rotation and deploy an independently protected immutable sink. An actor able to delete both local files remains outside the local-chain guarantee. |

## Proposed reviewer disposition

The preparer proposes the following for Security Team consideration; none is an
approved disposition yet:

- Treat TM-02 as deployment-blocking until the real proxy boundary is proven.
- Treat TM-03 as remediated in source, pending deployment verification of the
  configured bearer defaults and trusted JWT-proxy header stripping.
- Treat TM-01, TM-03, TM-04, TM-06, TM-07, TM-08, and TM-10 as remediated in
  source, pending hosted and deployment verification.
- Treat TM-09 as runtime-remediated by signed Kujo v1.2.2, pending deployed
  proxy-timeout verification. Do not use v1.2.0 for production.
- Keep TM-05 and TM-11 partially open for descriptor-level filesystem defense
  and an external immutable audit sink respectively.
- Require production strict mode, loopback/private binding, TLS termination,
  authenticated access, encrypted persistence, and scoped ingest roots as a
  single deployment baseline.
- Require explicit owners and target dates for any accepted residual risk.

## Verification evidence

Run from the repository root with the release-candidate Kujo binary:

```bash
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run tests/test_api_bind_contract.kujo --interpreter
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run tests/test_api_bind_contract.kujo --vm
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run tests/test_api_contract.kujo --interpreter
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run scripts/run_tests.kujo --interpreter
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run scripts/run_threat_model_review_cadence.kujo --interpreter
```

Local evidence at preparation time:

- `kujo check main.kujo`: passed.
- Bind contract: passed in interpreter and VM modes.
- API integration contract: passed.
- Bearer RBAC escalation and trusted-proxy forgery regressions: passed in
  interpreter and VM modes with signed Kujo v1.2.2 commit `22582e7f0111a1005002579b44f5d03cd2ed1c9c`.
- Full repository runner: 68/68 suites passed with zero undefined-function
  warnings and within the existing warning budget.
- Cadence validation: all gates pass except `review_not_overdue`; this is the
  expected failure until the accountable review occurs.

## Human review completion record

Complete this section only after the accountable review:

- [ ] Reviewer identity and authority recorded.
- [ ] Reviewed commit and deployed runtime version recorded.
- [ ] TM-01 through TM-11 dispositions recorded.
- [ ] TM-02 and TM-03 trust decisions backed by deployment or code evidence.
- [ ] High-severity gaps have owners and target dates.
- [ ] Residual risks are explicitly accepted by the accountable owner.
- [ ] `config/threat_model_review_plan.json` is updated with the real review
  timestamp and review ID.
- [ ] `review_not_overdue` and the complete release gate pass.
