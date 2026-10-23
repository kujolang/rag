# Current local remediation evidence

The new error-redaction denial of service is repaired in `src/query_api.kujo` by explicit per-call bindings. Reproduce the original multi-field error through the bounded regression in `tests/test_redaction_policy.kujo`; nested recursive and compatibility checks are in `tests/test_redaction_bindings.py`. The 44 live assertions are in `scripts/run_local_security_exercises.py`.

Sanitized execution evidence is stored under `docs/security-reviews/evidence/2026-10-22/`. It records local tests, not production approval. The corresponding report describes scope, original failure, preserved legitimate behavior, historical evidence corrections and deployment limitations.

No historical critical-risk exception was renewed. Historical PT-2026-05-001/PT-2026-05-002 dates and approvals remain unverified pending accountable reconciliation. Current negative replay and namespace-hopping results support local controls only.
