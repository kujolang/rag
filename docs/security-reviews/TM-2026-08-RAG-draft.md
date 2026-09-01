# Kujo RAG Threat-Model Review Packet (Draft)

> Preparatory evidence only. This document is not a completed Security Team
> review, approval, risk acceptance, or replacement for the cadence record in
> `config/threat_model_review_plan.json`.

## Review metadata

- Review ID: `TM-2026-08-RAG-DRAFT`
- Prepared: 2026-09-01
- Repository: `kujolang/rag`
- Branch: `main`
- Commit reviewed: `86d8a32a772d445e13e748f2018c147f23ca5072`
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
  credentials, missing JWT proxy issuer/audience, disabled at-rest encryption,
  default namespace use, and the default index path (`src/config.kujo`).
- The Kujo runtime enforces a bounded pre-buffer request size, request-body read
  deadline, 408/413 responses, and peer socket identity in interpreter and VM
  paths.
- API JSON parsing applies the smaller application limit configured by
  `api_max_body_bytes` (`src/query_api.kujo`).
- Remote ingestion canonicalizes paths, enforces configured roots, and rejects
  symlink traversal (`validate_api_ingest_path` in `src/query_api.kujo`).
- Local index writes are atomic, retain the last readable index on failure, and
  perform read-after-write schema validation (`src/vector_store.kujo`).
- Rate limiting uses runtime-provided peer socket identity rather than forwarded
  headers (`src/query_api.kujo`).
- Qdrant synchronization is opt-in and can fail closed; local mirror state
  records the most recent synchronization result (`src/vector_backend.kujo`).

## Threat scenarios requiring review

| ID | Scenario and impact | Current control | Decision or evidence required |
|---|---|---|---|
| TM-01 | A deployment intended for loopback accidentally listens on every interface, exposing unauthenticated or privileged routes. | Fixed at the reviewed commit: configured `api_host` is passed to `http_listen`; default is `127.0.0.1`. | Verify the deployed listener and firewall rules. Treat explicit `0.0.0.0` as a security-sensitive configuration choice. |
| TM-02 | A client bypasses the trusted proxy and forges `x-kujo-claim-*` headers. JWT signature verification does not occur inside RAG, so forged issuer, audience, expiry, role, or namespace values could be accepted. | Documentation requires an upstream verifier that strips client-supplied claim headers; strict mode requires issuer and audience. | Prove the backend is unreachable except through the stripping proxy, or require an in-process signed-token verifier before direct exposure. |
| TM-03 | With RBAC enabled but without role-bearing auth context, a bearer-authenticated client supplies `x-kujo-role: admin` or `x-kujo-namespace: *`. | Fixed at the reviewed commit: bearer and unauthenticated development contexts ignore caller-supplied RBAC headers and use the configured default role and namespace; only `jwt_proxy` contexts may consume proxy-provided identity headers. Composed bearer regressions cover role and namespace escalation, while existing JWT-proxy and global job-control behavior remains covered. | Verify the deployed default bearer role and namespace are least-privilege, and prove the JWT proxy strips untrusted identity headers before adding verified claims. |
| TM-04 | Development defaults are promoted or exposed without credentials, encryption, or RBAC. Bearer mode with no configured token behaves as authentication disabled. | Loopback default and strict/production validation. | Verify production always sets `runtime_environment=production` or `strict_config=true`; add deployment policy enforcement if configuration can bypass startup validation. |
| TM-05 | An authorized ingest request reads sensitive local files or traverses a path boundary. | Allowed-root canonicalization, component-wise symlink rejection, file-size and extension limits. | Review the actual service account permissions and allowed roots; ensure writable attacker-controlled parents cannot be swapped after validation. |
| TM-06 | Privacy export or deletion-receipt artifacts expose full namespace contents after the API request completes. | Admin authorization, namespace scoping, deterministic artifact paths, optional at-rest encryption for indexes. | Define permissions, encryption, retention, backup, and publication rules for `results/privacy`; verify these artifacts are never uploaded as generic CI output. |
| TM-07 | A malicious or misconfigured Qdrant URL receives full chunks, vectors, and API credentials, or fail-open behavior hides synchronization loss. | Operator-supplied endpoint, optional API key, timeout, explicit sync toggle, selectable fail-open/fail-closed behavior, local mirror metadata. | Require an allowlisted TLS endpoint and fail-closed mode for authoritative production synchronization; verify secrets are redacted from logs and artifacts. |
| TM-08 | Local indexes, runtime state, backups, or audit data disclose source content at rest. | Strict production mode requires index encryption; audit output is optional and redacted. | Confirm all content-bearing side artifacts and backups receive equivalent protection, not only the primary index. |
| TM-09 | Oversized or slow HTTP bodies exhaust memory or hold connections indefinitely. | Kujo runtime pre-buffer limit and read deadline, plus the smaller RAG JSON limit. | Verify the released runtime version used by production contains the interpreter/VM hardening and that proxy timeouts are no weaker. |
| TM-10 | A failed or oversized index write is reported as successful and later reloads as an empty index. | Atomic persistence, read-after-write validation, explicit errors, last-readable-index preservation, bounded size tests. | Confirm hosted release gates execute the large-index regression against the released runtime. |
| TM-11 | Audit logs are disabled, tampered with, or retained locally after an incident. | Optional hash-chained append-file audit mode and redaction. | Decide when audit is mandatory, who can read/rotate it, and whether production requires an external immutable sink. |

## Proposed reviewer disposition

The preparer proposes the following for Security Team consideration; none is an
approved disposition yet:

- Treat TM-02 as release-blocking for any deployment reachable by untrusted
  clients until the trusted-header boundary is proven or in-process signed-token
  verification is added.
- Treat TM-03 as remediated in source, pending deployment verification of the
  configured bearer defaults and trusted JWT-proxy header stripping.
- Treat TM-01 as remediated in source, pending hosted CI and deployment listener
  verification.
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
- Bearer RBAC escalation regression: passed in interpreter and VM modes with
  the published Kujo v1.2.0 runtime.
- Full repository runner: 65/65 suites passed with zero undefined-function
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
