# Release Evaluation Trends and Drift Reporting

## Purpose

Release evaluation trend reporting keeps a historical record of quality gates and highlights drift by metric category and domain between consecutive runs.

## Artifacts

- Report output: `./results/release_eval_report.json`
- Trend history: `./results/release_eval_trend.json`

Both paths are configurable via environment variables in `.env.example`.

## What gets tracked

Each release-eval run appends a snapshot containing:

- Dataset version
- Case totals and pass/fail counts
- Aggregate quality metrics (`quality_pass_rate`, `avg_confidence`, `avg_grounding`)
- Reliability/latency metrics (`error_rate`, `avg_latency_ms`, `p95_latency_ms`)
- Domain summary metrics (`quality_pass_rate`, `avg_confidence`, `avg_grounding` per domain)
- Language summary metrics (`quality_pass_rate`, `avg_confidence`, `avg_grounding` per language family)
- Runtime profile metadata (`embedding_provider`, `ai_embed_endpoint`, `ai_embed_model`, `chat_endpoint`, `chat_model`)

## Drift highlights

`trend_report.regressions` is emitted in every report and compares the current run against the previous snapshot.

Categories:

- `quality`: regressions in quality pass rate or average confidence
- `grounding`: regressions in average grounding
- `latency`: regressions in average or p95 latency
- `reliability`: regressions in error rate
- `domain`: regressions in domain-level pass rate or grounding
- `language`: regressions in language-family pass rate or grounding
- `provider_model`: drift in pinned provider/model runtime profile fields across consecutive runs

When one or more regressions are detected, `trend_report.drift_detected` is set to `true`.

## Configuration

- `KUJO_RAG_RELEASE_EVAL_OUTPUT_PATH`
- `KUJO_RAG_RELEASE_EVAL_TREND_PATH`
- `KUJO_RAG_RELEASE_EVAL_TREND_HISTORY_LIMIT`

## Validation

- Run `tests/test_release_evaluation.kujo` for core metrics and domain summary checks.
- Run `tests/test_release_eval_trend_report.kujo` for trend append/report generation checks.
- Run `scripts/run_release_evaluation.kujo --interpreter` to produce report and trend artifacts locally.
