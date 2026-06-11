# Penetration Test Report (Cycle 2026-05)

- Report ID: `PT-2026-05`
- Test window: 2026-05-24 to 2026-05-25
- Owner: Security Team
- Methodology: authenticated API abuse tests, privilege escalation simulation, release-gate bypass attempts

## Scope Covered

- Query API auth/RBAC paths
- Namespace and privacy workflow controls
- Release gate and control-plane security controls

## Findings Summary

| Finding ID | Severity | Status | Backlog Ticket |
|---|---|---|---|
| `PT-2026-05-001` | high | resolved | `SEC-PT-241` |
| `PT-2026-05-002` | critical | accepted_exception | `SEC-PT-242` |

## Notes

- `PT-2026-05-001` remediation was validated in-cycle and marked resolved.
- `PT-2026-05-002` has an approved time-bounded exception with explicit owner and expiry while remediation work continues.
