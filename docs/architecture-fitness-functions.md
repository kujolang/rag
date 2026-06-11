# Architecture Fitness Functions and Guardrails

This document defines UPR-085 architecture fitness checks that run as deterministic CI gates.

## Objective

- Prevent forbidden dependencies and layer violations before merge.
- Enforce extension points through tests/contracts.
- Keep architecture constraints auditable and machine-validated.

## Rule Source of Truth

- `config/architecture_fitness_rules.json`

The rule set defines:

1. `forbidden_dependencies`: source files and disallowed import tokens.
2. `required_extension_points`: required registry and documentation tokens.

## Required Fitness Domains

1. Layer-violation prevention:
- lower layers must not import API-layer route handlers.
- current baseline disallows `from src.query_api import` in retrieval/ingestion/storage layers.

2. Extension-point contract enforcement:
- parser extensions remain registry-driven (`get_parser_registry`).
- embedding extensions remain registry-driven (`get_embedding_provider_registry`).
- extension onboarding remains documented in `docs/extension-guide.md`.

## Execution Contract

Run architecture fitness review gate:

```bash
kujo run scripts/run_architecture_fitness_review.kujo --interpreter
```

Run pass/fail regression suite:

```bash
kujo run tests/test_architecture_fitness_review.kujo --interpreter
```

Gate output artifact:

- `results/architecture/architecture_fitness_status.json`

## CI Integration

- Dedicated workflow: `.github/workflows/architecture-fitness-review.yml`
- Required release linkage: `.github/workflows/release-gates.yml` and `docs/release-process.md`