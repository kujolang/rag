# Chunking Presets and Override Hierarchy

This document describes language- and format-aware chunking presets introduced for UPR-054.

## Why Presets

Different formats need different chunk boundaries for stable retrieval quality:

- structured rows (`json`, `csv`) benefit from smaller line windows
- logs benefit from fixed-width windows
- long prose and markup often work better with larger line-aware spans

## Override Hierarchy

Chunking parameters are resolved in this order (lowest to highest precedence):

1. Global baseline config:
   - `chunk_strategy`
   - `chunk_size`
   - `chunk_overlap`
2. Format/language preset (when enabled):
   - inferred from parser metadata and file extension
3. Per-document explicit override:
   - `doc.meta.chunking_override`

If a per-document override is present, it always wins.

## Runtime Controls

- `KUJO_RAG_CHUNK_PRESETS_ENABLED`
  - `false` (default): baseline-only chunking
  - `true`: apply preset selection + hierarchy
- `KUJO_RAG_CHUNK_PRESETS_JSON`
  - optional JSON object for preset overrides keyed by preset name
  - each preset may include `chunk_strategy`, `chunk_size`, `chunk_overlap`

Example:

```json
{
  "json": {"chunk_strategy": "line", "chunk_size": 220, "chunk_overlap": 40},
  "csv": {"chunk_strategy": "line", "chunk_size": 220, "chunk_overlap": 40},
  "log": {"chunk_strategy": "fixed", "chunk_size": 540, "chunk_overlap": 80}
}
```

## Observability

Each emitted chunk includes resolved profile metadata in `chunk.meta`:

- `chunk_profile_source`
- `chunk_profile_key`
- `chunk_profile_strategy`
- `chunk_profile_size`
- `chunk_profile_overlap`
- `chunk_profile_presets_enabled`

This makes runtime behavior auditable in retrieval traces.

## A/B Evaluation Gate

Run preset-vs-baseline evaluation on the targeted corpus:

```bash
kujo run scripts/run_chunking_preset_ab_evaluation.kujo --interpreter
```

Default assets:

- corpus: `examples/chunking_preset_eval_corpus/`
- cases: `config/chunking_preset_eval_golden_queries.json`
- gate thresholds: `config/chunking_preset_eval_thresholds.json`
- output: `results/chunking_preset_ab_report.json`

The gate fails if preset quality deltas do not meet configured minimums.
