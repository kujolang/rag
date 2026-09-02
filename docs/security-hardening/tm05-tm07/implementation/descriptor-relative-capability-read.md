# Implementation Plan: Descriptor-relative capability read

## Selected Design And Constraints

Add an additive preview Kujo API that returns bytes from a bounded regular file
reached only through handle-relative, no-follow traversal. Never fall back to a
check-then-open implementation.

## Source Revision And Drift Check

Design evidence: RAG `77e6174`, Kujo `2a5612c`. Refresh both revisions before
editing; material drift in filesystem dispatch or ingest discovery requires the
proposal to be updated.

## Affected Components

Kujo filesystem native functions, capability and arity registries, VM/interpreter
exposure, standard-library docs, and conformance tests; RAG discovery and parser
read paths plus security tests.

## Ordered Work Packages

- Freeze `read_binary_file_beneath(root, relative_path, max_bytes)` and errors.
- Implement Unix descriptor traversal and Windows handle-relative traversal.
- Add native and language-level conformance and race-stress tests.
- Migrate one RAG ingest path, then all remaining parser reads.
- Promote from preview only after cross-platform CI and benchmarks pass.

## Compatibility And Migration

Keep all generic read APIs. RAG retains its current checks during rollout and
can switch back without changing stored data or public HTTP contracts.

## Tactical Protections During Migration

Keep root allowlists, lexical normalization, symlink discovery rejection, file
type allowlists, size limits, and pre-parse rechecks.

## Tests And Security Validation

Cover valid reads, traversal, every symlink/reparse position, rename stress,
special files, size boundaries, capability denial, descriptor cleanup, and
VM/interpreter parity on each supported OS.

## Performance And Resource Benchmarks

Compare current and candidate reads at 1, 5, and 20 path components for 4 KiB,
1 MiB, and 8 MiB files. Record p50/p95 wall time, bytes copied, and peak open
descriptors/handles.

## Rollout And Rollback

Release as preview, canary in RAG, then promote. Rollback caller adoption first;
leave the additive runtime function until a normal compatibility window.

## Acceptance Criteria

- No supported platform resolves any untrusted component after containment proof.
- Symlinks/reparse points and rename races cannot escape the root.
- Reads stay bounded and regular-file-only.
- VM/interpreter and cross-platform tests pass without a weak fallback.
- Existing generic file reads remain compatible.

## Open Decisions

Finalize the public name, bytes-versus-text return, Windows primitive, and
whether a reusable scoped root handle follows in a later API.

