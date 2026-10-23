# Local-only RAG 1.1.0 release scope

The repository owner explicitly selected **local-only** operation on 2026-10-22. This is a source/tool release for one trusted OS user's documentation corpus. It is not a public RAG service, multi-tenant deployment, or hosted production promotion.

## Supported boundary and verified controls

The managed documentation service binds only to 127.0.0.1, requires a private bearer credential, uses the built-in reader RBAC policy and an explicit namespace, keeps hash embeddings and local JSON storage, and confines ingestion/index paths to its private data directory. The wrapper rejects incompatible settings, competing `.env` configuration and broadly readable private configuration; it excludes undeclared inherited RAG environment settings. The data directory is owner-only (0700), with configuration0600. Same-OS-user access remains trusted; this profile is not a sandbox against the logged-in owner or their processes.

The actual service was restarted and passed health/readiness, missing/invalid credential rejection, forged-admin rejection, legitimate documentation query, cross-namespace rejection and continued responsiveness. Policy regression tests cover invalid bindings/auth/roles/providers/paths and symlink escapes. Evidence: `evidence/2026-10-22/local-only-service.json`.

Local files are not an independently immutable audit store, and local application-level encryption is not enabled. This scope permits local documentation data under OS file permissions; sensitive/multi-user/remote use needs a separate security review. No tunnel or public listener is part of the approved profile. The unrelated listener on18787 was preserved.

## Evidence and historical records

The error-redaction denial of service is fixed; 44 live abuse checks, six proxy tests, recursive redaction checks and automated recovery drills passed. Hosted CI on79cacd2 passed73/73 aggregate tests. The last full local run passed72/73, with evaluation latency failures on the busy host; unchanged evaluation gates passed in hosted CI. Fresh final-head checks remain required.

The owner confirmed the historical May penetration/drill records were not executed. Those records and their named approvals/exception are unverified, not renewed or converted into approvals. Current token replay and namespace-hopping attempts were rejected, as documented in `../penetration-test-report.md`. No current confirmed unremediated finding was established by these bounded local exercises; this is not an exhaustive vulnerability-free claim.

## Gate applicability

`release-gates` retains the aggregate suite, runtime matrix, supply-chain, evaluations, OpenAPI/SDK, versioning, schema, development environment, chaos, architecture, override ledger, benchmarks and performance/cost checks. It additionally validates this committed local-only scope and startup policy. Artifact creation enforces the same local-only scope.

The four historical enterprise governance checks (threat-model cadence, penetration remediation ledger, human tabletop, production readiness scorecard) are preserved unchanged in the manually invoked `production-readiness` workflow. They are not reported as passed. Their missing historical evidence is not used to certify this local release. A future hosted promotion requires current accountable reviews, real proxy/JWT/isolation evidence, independent immutable audit evidence and a human operations exercise, plus all technical release checks. The production attestation validator remains unchanged.

Before publishing1.1.0: pass the final-head technical CI, rehearse/check release artifacts and finalize release notes. Do not claim hosted readiness or change branch protection to bypass a failing required check.
