# Query and Embedding Cache Layers

This document describes cache behavior for query responses and embedding vectors.

## Query Cache

Query cache is request-path caching for `POST /query` responses.

Configuration:

- `KUJO_RAG_API_QUERY_CACHE_ENABLED` (`true|false`)
- `KUJO_RAG_API_QUERY_CACHE_TTL_SEC` (default `300`)
- `KUJO_RAG_API_QUERY_CACHE_MAX_ENTRIES` (default `1000`)

Cache key dimensions:

- namespace
- current namespace index generation
- raw query string
- query filters payload
- session history payload used for contextualization

### Invalidation Policy

On successful index mutation (`POST /ingest`, inline ingest jobs, and queue worker ingest completion):

1. namespace generation is incremented
2. namespace query-cache entries are removed
3. subsequent queries populate fresh entries from the updated index

This guarantees cache correctness after ingest updates.

## Embedding Cache

Embedding cache stores computed vectors keyed by:

- resolved provider name
- embedding dimension
- input text hash

Configuration:

- `KUJO_RAG_EMBEDDING_CACHE_ENABLED` (`true|false`)
- `KUJO_RAG_EMBEDDING_CACHE_MAX_ENTRIES` (default `10000`)

Embedding cache also clears after successful ingest updates so stale vectors are not retained across index generations.

## Metrics

`GET /metrics` includes cache observability fields:

- `cache_hits`
- `cache_misses`
- `cache_hit_ratio`
- `query_cache_entries`
- `embedding_cache_hits`
- `embedding_cache_misses`
- `embedding_cache_entries`

`POST /query` responses include `data.cache.hit` so callers can inspect whether the response came from cache.
