# ADR-0001: Chunk Strategy

- Status: Accepted
- Date: 2026-05-21

## Context

The project ingests mixed documentation and source files. Retrieval quality depends on chunk boundaries that preserve local meaning while keeping chunk sizes manageable for embedding and ranking.

## Decision

Use two chunking modes:

- `line`: line-aware chunking for precise citations and markdown-heavy corpora.
- `fixed`: character-budget chunking with overlap for denser technical content.

Both strategies must guarantee non-inverted line ranges and stable chunk IDs when chunk content and line ranges remain unchanged.

## Consequences

- Users can tune for citation fidelity (`line`) or throughput (`fixed`).
- Retrieval remains deterministic across repeated indexing runs.
- Chunking complexity is isolated in `src/chunking.kujo` and surfaced through config.
