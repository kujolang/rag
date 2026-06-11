# Multilingual Release Evaluation

## Purpose

This gate validates retrieval quality across language families so non-English behavior is measured and release-gated.

## Gate Script

Run:

```bash
kujo run scripts/run_multilingual_release_evaluation.kujo --interpreter
```

The script runs release evaluation against a multilingual corpus/query set and enforces per-language thresholds.

## Inputs

- Golden multilingual cases: `config/multilingual_release_eval_golden_queries.json`
- Multilingual thresholds: `config/multilingual_release_eval_thresholds.json`
- Multilingual corpus: `examples/multilingual_release_eval_corpus`

## Outputs

- Report: `results/multilingual_release_eval_report.json`

The report includes:

- aggregate release-eval metrics
- `language_summary` metrics (`quality_pass_rate`, `avg_confidence`, `avg_grounding`, `total_cases`) per language
- required-language presence checks
- non-English aggregate quality checks

## Threshold Model

`release_eval_thresholds` enforces baseline quality/reliability/latency.

`language_thresholds` enforces multilingual coverage:

- `min_language_count`
- `required_languages`
- `min_language_quality_pass_rate`
- `min_non_english_quality_pass_rate`
- `min_non_english_case_count`

## Validation

- `kujo run tests/test_multilingual_release_evaluation.kujo --interpreter`
- `kujo run scripts/run_multilingual_release_evaluation.kujo --interpreter`
