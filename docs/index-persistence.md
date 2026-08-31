# Local index persistence contract

The `local_json` backend serializes a complete namespace index, validates that payload as a JSON object, replaces the destination atomically, and immediately reloads it through the configured plaintext or encrypted read path. Ingest succeeds only after that read-back validation passes.

Kujo applies the same 8 MiB ceiling to JSON parsing, file reads, and atomic file writes. A candidate above the ceiling returns an `index_serialization_invalid` or `index_persistence_failed` error. The prior readable index remains in place. A malformed, unreadable, or externally oversized persisted file loads an empty safety index with actionable `meta.load_error` metadata; it is never treated as an ordinary missing index.

RAG does not automatically split a single namespace index. Namespace isolation derives stable filenames from the configured namespace, and is the supported deterministic local partitioning contract. Workloads that cannot keep each serialized namespace below the runtime ceiling should select an external vector backend. Automatic chunk sharding would require a separate manifest, atomic multi-file publication, compatibility, and recovery contract.

Operators should alert on failed ingest responses and on `meta.load_error`. They should not publish or query a replacement index when persistence reports failure.
