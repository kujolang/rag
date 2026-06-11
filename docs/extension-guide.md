# Extension Guide

This guide shows how to extend Kujo RAG with new parsers, embedding providers, and retrieval behavior.

## Extension Workflow

1. Add implementation function(s) in the relevant module.
2. Register the extension in the module registry map.
3. Preserve fallback behavior for unknown/unavailable providers.
4. Add regression tests in `tests/test_unit.kujo` and integration checks when behavior changes.
5. Update README and this guide when public behavior changes.

## Parser Extensions

Parser lookup is registry-based in `src/parsers.kujo`.

Current registry function:

- `get_parser_registry()`

### Example: Add `mdx` Parser Support

A minimal extension can map a new file extension to an existing parser implementation.

Implementation pattern in `src/parsers.kujo`:

- add `"mdx": "markdown"` in `parser_registry()`

Behavior:

- `.mdx` files resolve to the markdown parser
- existing markdown parsing rules (code-fence removal, inline cleanup) apply unchanged

To ingest `.mdx` files through discovery, include `mdx` in `ingest_extensions` (default config now includes it).

Validation:

- unit assertion for registry key presence
- parser smoke assertion: `parse_file("*.mdx", {})` returns markdown kind/metadata

## Embedding Provider Extensions

Embedding lookup is registry-based in `src/embeddings.kujo`.

Current registry function:

- `get_embedding_provider_registry()`

To add a provider:

1. Add provider implementation function.
2. Map provider key to a handler type in registry.
3. Keep unknown-provider behavior deterministic (fallback to hash provider with error metadata).
4. Add tests for provider selection and fallback contract.

## Retrieval Extensions

Retrieval is implemented in `src/retrieval.kujo` and orchestrated by `src/rag_engine.kujo`.

Safe extension points:

- pre-ranking filtering
- score composition
- reranking strategy additions

When adding a retrieval extension:

1. Keep deterministic ordering for ties.
2. Keep existing query payload backwards-compatible.
3. Add focused unit tests for ordering and filter interactions.
4. Add integration tests when query response shape or ranking contract changes.
