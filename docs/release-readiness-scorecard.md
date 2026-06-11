# Release Readiness Scorecard

This scorecard provides the final cross-domain go/no-go control before production promotion.

## Source Of Truth

- Baseline scorecard payload: `config/release_readiness_scorecard.json`
- Deterministic validator: `scripts/run_release_readiness_scorecard_review.kujo`
- Gate artifact output: `results/release/release_readiness_scorecard_status.json`

## Weighted Readiness Criteria

Every release candidate must include weighted domain scoring across:

- security
- reliability
- quality
- scalability
- compliance

Scoring rules:

- each domain defines `weight`, `score`, and `min_score`
- domain weights must sum to `100`
- weighted score must meet `minimum_weighted_score`
- each domain must include non-empty reviewer and evidence paths
- evidence paths must resolve to repository-tracked artifacts/docs

## Signoff Requirements

A release candidate is eligible only when:

- scorecard decision is `go`
- release owner is defined (`owner`)
- at least two approvers are recorded (`approvers`)
- explicit signoff actor is recorded (`signed_off_by`)
- review is within cadence window (`review_cadence_days`)

## Validation Command

```bash
kujo run scripts/run_release_readiness_scorecard_review.kujo --interpreter
```

The validator emits structured gate results and exits non-zero when readiness criteria are not met.

## CI Integration

- Dedicated workflow: `.github/workflows/release-readiness-scorecard-review.yml`
- Required release linkage: `.github/workflows/release-gates.yml` and `docs/release-process.md`
