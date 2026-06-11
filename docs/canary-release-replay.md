# Canary Release Evaluation Replay

## Purpose

Canary replay validates candidate builds against production-like sampled queries before promotion.

## Inputs

- Canary sample set: `config/canary_replay_samples.json`
- Canary eval thresholds: `config/canary_replay_eval_thresholds.json`
- Canary acceptance thresholds: `config/canary_replay_thresholds.json`
- Baseline report: `results/release_eval_report.json`

## Command

```bash
KUJO_BIN=/absolute/path/to/kujo kujo run scripts/run_canary_release_replay.kujo --interpreter
```

## Output

- `results/canary_release_replay_report.json`

The report contains:

- Candidate canary metrics
- Baseline metrics snapshot
- Delta and ratio comparisons
- Promotion gates and overall `ok`

## Promotion gates

Candidate promotion requires:

- Canary release evaluation itself passes
- Minimum sample count is met
- Quality/confidence/grounding drops are within configured bounds
- Error-rate increase is within bound
- Average and p95 latency ratios stay within configured bounds

## Configuration

- `KUJO_RAG_CANARY_GOLDEN_PATH`
- `KUJO_RAG_CANARY_EVAL_THRESHOLDS_PATH`
- `KUJO_RAG_CANARY_CORPUS_PATH`
- `KUJO_RAG_CANARY_INDEX_PATH`
- `KUJO_RAG_CANARY_BASELINE_REPORT_PATH`
- `KUJO_RAG_CANARY_ACCEPTANCE_PATH`
- `KUJO_RAG_CANARY_OUTPUT_PATH`
