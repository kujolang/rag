# Incident Response Tabletop Workflow

This workflow defines recurring incident-response tabletop drills and runbook validation for production readiness.

## Cadence

- Standard cadence: every 30 days and before major release milestones.
- Source of truth: `config/incident_response_tabletop_plan.json`.
- Scheduled automation: `.github/workflows/incident-response-tabletop-review.yml`.

## Required Incident Scenarios

Each tabletop cycle must cover and document:

- auth compromise
- data corruption
- service outage
- quality regression

Required runbooks:

- `docs/runbooks/incident-auth-compromise-runbook.md`
- `docs/runbooks/incident-data-corruption-runbook.md`
- `docs/runbooks/incident-service-outage-runbook.md`
- `docs/runbooks/incident-quality-regression-runbook.md`

## Tabletop Action Report and Follow-up Tracking

Each scenario must include:

- executed tabletop report reference (`tabletop_report_path`)
- lessons learned entries
- follow-up issue tracking with owner, status, and target date

Cycle report artifact:

- `docs/incident-tabletop-action-report-2026-05.md`

## Automated Validation Command

```bash
kujo run scripts/run_incident_response_tabletop_review.kujo --interpreter
```

Primary artifact output:

- `results/security/incident_response_tabletop_status.json`

## Release Linkage

Release process must reference tabletop readiness checks via:

- `scripts/run_incident_response_tabletop_review.kujo`
- `docs/incident-response-tabletop-workflow.md`
