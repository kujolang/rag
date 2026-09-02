# Implementation Plan: Staged Qdrant generation and alias commit

## Selected Design And Constraints

Implement the staged-generation protocol for strict mode while preserving the
legacy path as an explicit non-strict compatibility mode for one release.

## Source Revision And Drift Check

Design evidence is anchored to RAG `77e6174`. Refresh `src/vector_backend.kujo`,
configuration validation, privacy deletion callers, and Qdrant docs before code.

## Affected Components

Vector backend configuration, Qdrant transport and save path, local mirror
metadata, journal persistence, startup recovery, privacy/retention handlers,
tests, docs, and operational runbooks.

## Ordered Work Packages

- Freeze the journal and state machine.
- Add alias bootstrap, dimension validation, and generation naming.
- Stage, upload, verify, and atomically switch the alias.
- Commit the local mirror and implement restart reconciliation and rollback.
- Add bounded delayed garbage collection and observability.
- Enforce the mode in strict configuration after compatibility soak.

## Compatibility And Migration

Bootstrap the stable alias to the current collection. No public query or ingest
schema changes. Legacy destructive mode remains opt-in outside strict mode
during the migration release.

## Tactical Protections During Migration

Retain HTTPS, exact host allowlisting, header-file secret handling, fail-closed
strict behavior, HTTP-status validation, local atomic persistence, and operator
alerts for any divergence.

## Tests And Security Validation

Inject failure after every state transition with a fake transport, then repeat
against a pinned live Qdrant container. Verify active remote and prior local data
remain readable for every pre-commit failure and recovery is idempotent.

## Performance And Resource Benchmarks

Measure ingest duration, bytes sent, temporary remote storage, alias query
latency, recovery time, and GC duration for 1k, 100k, and maximum point sets.

## Rollout And Rollback

Canary one namespace, retain at least one prior generation, and promote after
recovery drills. Rollback atomically restores the previous alias target and
reconciles local metadata.

## Acceptance Criteria

- The active collection is never deleted or mutated before candidate verification.
- Alias commit is the only visibility change and is atomic.
- Every phase is durable and idempotently recoverable after restart.
- Successful saves prove matching local and remote generation metadata.
- Empty privacy deletion is committed without a destructive pre-delete window.
- Old-generation GC is bounded, delayed, observable, and never part of commit success.

## Open Decisions

Finalize minimum Qdrant version, vector-dimension source, journal location and
retention, generation storage ceiling, and post-alias local reconciliation rule.

