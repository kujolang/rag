# Incident Runbook: Quality Regression

1. Declare quality incident when release-evaluation quality gates drift below policy thresholds.
2. Identify failing domain/language slices and compare against previous passing trend baseline.
3. Roll back model/config/prompt changes or disable risky feature flags.
4. Re-run release evaluation and targeted corpus checks to verify recovery.
5. Validate citation grounding and no-answer/adversarial protections after mitigation.
6. Document root cause, regression trigger, and affected user journeys.
7. Track corrective actions with owners and due dates in remediation backlog.
