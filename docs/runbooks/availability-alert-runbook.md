# Availability Alert Runbook

1. Validate current `/health`, `/live`, and `/ready` behavior.
2. Check recent deploys and configuration drift.
3. Inspect rate-limit, auth, and dependency failure patterns in access/audit logs.
4. Mitigate via rollback or traffic shaping if availability remains below page threshold.
5. Record timeline and corrective actions in incident log.
