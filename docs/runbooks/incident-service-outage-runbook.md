# Incident Runbook: Service Outage

1. Declare outage incident, assign incident commander, and publish stakeholder status update.
2. Confirm scope of impact (API availability, ingest path, query path, and dependent services).
3. Execute immediate mitigation: rollback recent change, fail over, or enable degraded safe mode.
4. Verify probe endpoints (`/live`, `/ready`, `/startup`) and key error/latency metrics recovery.
5. Restore customer traffic progressively while validating auth, ingest, and query critical paths.
6. Capture timeline, trigger, mitigation effectiveness, and customer impact.
7. Open follow-up issues for preventive controls and runbook updates.
