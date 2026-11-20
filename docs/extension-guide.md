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

## Programmatic retrieval adapters

Trusted Kujo code can pass independent functions through the config dictionary.
The CLI environment and HTTP request JSON cannot create these callbacks.

- Set `embedding_adapter` to a function of `(texts, input_type)` returning
  `{"ok": true, "vectors": vectors}` in input order. Use `document` for
  indexing and `query` for searches. Set `embedding_dims` and an
  `embedding_adapter_id` identifying the provider, model and vector contract.
  The identity is persisted. Changing it or the dimension re-embeds the corpus.
  A failed batch leaves the prior index available. Supply the same adapter
  identity and dimensions when opening an index for queries.
- Set `rerank_adapter` to a function of `(query, documents, top_n)` returning
  `{"ok": true, "rankings": [{"index": 0, "score": 0.9}]}`. Indices refer to
  the provided candidate order. The adapter selects and orders citations.
  Hybrid scores retain their original semantics. Federation merges shortlisted
  citations using its existing cross-index ranking policy.
- The reranker receives only filtered candidates, up to
  `rerank_candidate_limit` (default 24, increased to cover `top_k`). The
  embedding adapter bypasses the legacy shared embedding cache.
- Callback errors or invalid outputs stop the operation and return a structured
  error. Provider failure cannot cause vectors from different models or a
  silent rank fallback. Existing built-in providers retain their documented
  fallback behavior.

The example composes Voyage embeddings and Jina reranking using the AI SDK
source checkout and leaves answer generation on RAG's configured path. Set
`VOYAGE_API_KEY` and `JINA_API_KEY` in a trusted environment and use only a
corpus you are authorized to send to those providers. Choose a Voyage model
that supports the example's 256 dimensions. Larger corpora should batch inside
the embedding callback to honor the SDK and service limits.

```sh
KUJO_MODULE_PATH=/path/to/ai-sdk/src kujo run examples/provider_retrieval.kujo --   ./examples/kujo_docs YOUR_VOYAGE_MODEL YOUR_JINA_RERANK_MODEL
```

## Documentation example selection

See [the preference contract and live pilot](RETRIEVAL_PREFERENCES.md) for opt-in fenced-example indexing, upstream selection, cache variants, MIME-aware HTTP ingestion, and measurements.
