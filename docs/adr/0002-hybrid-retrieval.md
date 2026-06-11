# ADR-0002: Hybrid Retrieval

- Status: Accepted
- Date: 2026-05-21

## Context

Pure lexical search misses semantic matches; pure dense search can lose exact term intent. The project must support predictable, local-first retrieval without requiring external services.

## Decision

Use weighted hybrid retrieval:

- Dense score weighted by `KUJO_RAG_HYBRID_ALPHA`.
- Lexical score weighted by `KUJO_RAG_HYBRID_BETA`.
- Deterministic top-k ranking and optional MMR reranking.

Filtering by path, extension, and tags is applied before ranking.

## Consequences

- Relevance quality is tunable without changing core code.
- Ranking behavior remains deterministic for regression testing.
- Query behavior scales better under larger corpora with top-k selection.
