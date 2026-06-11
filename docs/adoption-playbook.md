# Kujo RAG Adoption Playbook

This guide is for adopting Kujo RAG in an external project with minimal friction.

Verified baseline: offline hash embeddings are the default, external AI providers are optional and config-gated, and the local workflow does not require hosted services or a vector DB.

## Minimum Setup

1. Copy this repository or vendor the core Kujo modules into your project.
2. Create `.env` from `.env.example`.
3. Set only these minimum values:
- `KUJO_RAG_INDEX_PATH`
- `KUJO_RAG_API_INGEST_ALLOWED_ROOTS`
4. Run a first ingest against your project content:
- `kujo run main.kujo --interpreter ingest --path <your-content-path> --recursive true`
5. Run a first query:
- `kujo run main.kujo --interpreter query --question "What does this project do?"`

## Integration Recipes

### Recipe 1: Documentation Corpus

Use when content is mostly markdown and text docs.

- Recommended env:
- `KUJO_RAG_INGEST_EXTENSIONS=md,markdown,txt`
- `KUJO_RAG_CHUNK_STRATEGY=line`
- `KUJO_RAG_TOP_K=6`
- Example command:
- `kujo run main.kujo --interpreter ingest --path ./docs --recursive true`

### Recipe 2: Code Repository

Use when you need retrieval over source files and design docs.

- Recommended env:
- `KUJO_RAG_INGEST_EXTENSIONS=kujo,md,txt`
- `KUJO_RAG_CHUNK_STRATEGY=fixed`
- `KUJO_RAG_CHUNK_SIZE=1100`
- `KUJO_RAG_CHUNK_OVERLAP=180`
- Example command:
- `kujo run main.kujo --interpreter ingest --path ./src --recursive true`

### Recipe 3: Mixed Content Workspace

Use when docs, notes, and source files are combined.

- Recommended env:
- `KUJO_RAG_INGEST_EXTENSIONS=md,markdown,txt,kujo,pdf`
- `KUJO_RAG_CHUNK_STRATEGY=line`
- `KUJO_RAG_TOP_K=8`
- Example command:
- `kujo run main.kujo --interpreter ingest --path ./knowledge --recursive true`

## Deployment Patterns

### Pattern A: Local CLI-Only Workflow

- Use `ingest` and `query` commands directly.
- Best for solo use and offline workflows.
- This is the verified local-first baseline.

### Pattern B: Local API Service

- Start server with:
- `kujo run main.kujo --interpreter serve --host 127.0.0.1 --port 8787`
- Integrate IDE tools, scripts, or local dashboards via `/query`.
- The verified smoke path stays local on loopback and does not require hosted infrastructure.

### Pattern C: CI Refresh Job

- Run periodic ingest in CI after docs/source updates.
- Persist index artifact between runs if desired.

## Troubleshooting

- Symptom: Query returns weak or generic results.
- Check: Ingest path and extension list include your real content.

- Symptom: Ingest is too slow.
- Check: Incremental indexing is enabled (default behavior) and unchanged docs are being reused.

- Symptom: API ingest is rejected.
- Check: `KUJO_RAG_API_INGEST_ALLOWED_ROOTS` includes the requested path.

- Symptom: Browser calls fail.
- Check: CORS is enabled and origin is in `KUJO_RAG_API_CORS_ALLOWED_ORIGINS`.

- Symptom: Requests are throttled.
- Check: `KUJO_RAG_API_RATE_LIMIT_MAX_REQUESTS` and rate-state TTL/cap settings.
