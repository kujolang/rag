# RAG local security test report — 2026-10-22

Status: local automated assessment completed; production certification and release approval are not established by this report.

The repository owner confirmed on 2026-10-22 that the previously referenced penetration tests and incident drills were not performed. The historical May dates, named reviewers, and critical-risk exception must not be used as verified evidence. This report records new execution against baseline `a74f32a74edf10f0b41588fa9fd03f81fd9455a4` plus the redaction fix in this change. Operator: Codex, at the owner's request; no independent human penetration tester participated.

## Scope and method

Checksum-verified Kujo v1.2.3 on macOS x64, disposable repository copies, loopback listeners, generated test credentials and synthetic data. No production credentials or remote data were used. Tests are reproducible with `KUJO_BIN=/absolute/path/to/kujo python3 scripts/run_local_security_exercises.py` in a disposable checkout. This is a bounded application assessment, not an exhaustive repository or infrastructure audit.

The 44 live assertions cover ordinary reader queries; missing authentication; forged admin headers on 12 administrative/privacy/worker routes; revoked bearer replay in both current and next rotation slots; valid replacement credentials; cross-namespace denial; namespace and forwarded-address hopping against a shared peer rate bucket; and forced-unready/recovered readiness states. All passed after the fix. The startup health request consumes one rate-limit allowance; subsequent attempted namespace hops receive the expected 429 responses.

## Finding: error-redaction denial of service

An authenticated reader requesting `/metrics` can reach a multi-field RBAC error. With default redaction enabled, pinned Kujo's bare assignment semantics let nested redaction helpers overwrite caller loop counters. The listener consumed a CPU core and failed to return within 60 seconds. Nested dictionaries and arrays also risked overwriting the caller's output container. Impact: availability failure while formatting rejected requests; the test did not demonstrate unauthorized data access.

The fix declares helper state with explicit local `mut` bindings throughout the recursive redaction path. It preserves error codes, masking, primitive values, safe siblings and disabled-redaction behavior. The original HTTP trigger now returns 403 and the server continues serving requests. `tests/test_redaction_bindings.py` additionally passes nested dict/array, scalar configuration, blank-mask fallback and caller-state preservation checks in interpreter and bridge modes. The existing HTTP redaction suite now includes a bounded multi-field RBAC regression. A separate read-only source reviewer found no concrete surviving bypass or compatibility regression.

## Historical findings

- PT-2026-05-001: new live namespace/forwarded-address hopping attempts remained rate limited. This supports current local control effectiveness; it does not validate the historical remediation dates.
- PT-2026-05-002: new revoked-token replay attempts across 12 privileged routes were rejected in both rotation slots, and replacement credentials worked. The historical report, reproduction and named approval are unverified. Do not silently renew its expired exception or claim an independent retest. Accountable review must reconcile that legacy record with these current results and deployed token-lifecycle behavior.

## Limits

Neither `rag.kujolang.ai` nor `rag-staging.kujolang.ai` resolved during this session; GitHub listed no configured repository environments. These observations do not prove that no deployment exists elsewhere. Production proxy isolation, real JWT identity/role mappings, immutable audit retention, operational ownership and human incident coordination remain unverified. Node v26.12.1 passed all six local Cloudflare proxy tests; that is not deployed-boundary evidence.

Hosted run 39882463502 at fix commit `79cacd2ccff2579b4dfec7961d321d64c85954b1` passed all 73 aggregate tests, nested redaction in both modes, native/bridge runtime checks, descriptor-relative ingestion on Linux/macOS/Windows, proxy tests and supply-chain scanning. Its release job passed the evaluation gates before stopping at overdue threat-model cadence; downstream gates were skipped.

See `penetration-test-remediation-evidence.md`, `incident-local-exercises-2026-10-22.md` and the committed sanitized evidence for results and remaining requirements.

## Local full-suite result

The local full suite completed 72/73 tests; all security tests passed. `test_release_evaluation.kujo` failed and its isolated retry also failed. Separate recovery-evaluation reports show average/p95 latency failures while all quality gates pass. This report does not claim an entirely green local suite. Hosted execution passed 73/73 and the unchanged evaluation gates.
