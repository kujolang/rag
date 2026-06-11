# Incident Runbook: Data Corruption

1. Freeze mutating traffic for affected namespaces and declare incident severity.
2. Identify corruption window, impacted artifacts, and source signal (ingest bug, operator action, or storage fault).
3. Validate backup integrity and choose the latest safe restore point.
4. Execute restore rehearsal in staging or isolated namespace before production rollback.
5. Restore production data, then run integrity checks for document count, checksum, and query correctness.
6. Re-enable traffic gradually while monitoring error rates and data-quality metrics.
7. Record root cause, data-loss assessment, and follow-up hardening tasks.
