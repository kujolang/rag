# Threat Modeling and Security Review Cadence

This document defines the recurring threat-modeling cadence for Kujo RAG and the release-gating security review checklist.

## Cadence

- Monthly review: run a full threat-model review at least every 30 days.
- Pre-release review: run a focused review before production promotion milestones.
- Triggered review: run an out-of-band review when a major architectural change trigger is hit.

Machine-readable cadence state is stored in `config/threat_model_review_plan.json` and validated by `scripts/run_threat_model_review_cadence.kujo`.

## Threat Model Template

Use the following template for each review entry (store results in the active security review ticket/release notes):

- review_id: unique identifier (`TM-YYYY-MM-<milestone>`)
- review_date_unix_ms: review timestamp
- reviewer: accountable owner/team
- scope: services/routes/components reviewed
- trust_boundaries: network/process/data trust boundaries evaluated
- critical_assets: data and control-plane assets in scope
- threat_scenarios: prioritized abuse/failure scenarios
- mitigations: existing controls and control gaps
- residual_risk: accepted residual risk and rationale
- follow_up_actions: tracked remediation actions and SLAs

## Major Architectural Change Triggers

A triggered threat-model review is required when any of the following occurs:

- introduction of new external connector classes or third-party data ingress patterns
- auth/RBAC/token lifecycle design changes
- privacy, retention, legal-hold, or deletion/export workflow redesign
- network topology or trust-boundary changes (new proxy tiers, service exposure, new control-plane paths)
- major evaluation/release-gate policy changes that affect promotion risk posture

## Security Review Checklist

Attach this checklist to release planning and promotion evidence:

- [ ] Current threat model review is within cadence window.
- [ ] Major architectural change triggers were evaluated since the last review.
- [ ] High-severity threat scenarios have mitigation owners and target dates.
- [ ] Residual risks are explicitly documented and approved.
- [ ] Release process references this checklist and cadence validation gate output.

## Validation and Evidence

Run:

```bash
kujo run scripts/run_threat_model_review_cadence.kujo --interpreter
```

Primary artifact output:

- `results/security/threat_model_review_status.json`

The cadence validation should be included in security review evidence for release milestones.
