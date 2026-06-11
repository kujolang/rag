# Incident Runbook: Auth Compromise

1. Declare security incident and assign incident commander.
2. Rotate affected bearer tokens, JWT trust settings, and administrative credentials.
3. Enable strict auth mode and temporarily restrict privileged endpoints to break-glass operators.
4. Review recent auth/audit logs for suspicious principals, namespaces, and replay patterns.
5. Revoke impacted sessions/tokens and validate rejected-auth behavior.
6. Capture timeline, blast radius, and containment evidence in the incident record.
7. Define remediation actions with owners and due dates before incident closure.
