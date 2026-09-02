# Kujo RAG Runtime Support Matrix

This document defines supported Kujo runtime execution combinations for this repository.

## Scope

This matrix applies to:
- CLI commands in main.kujo
- test wrapper scripts in scripts/
- CI workflows under .github/workflows/

## Supported Modes

| Runtime source | Execution mode | Support level | CI validation | Notes |
|---|---|---|---|---|
| Kujo v1.2.2 signed release commit (`22582e7f0111a1005002579b44f5d03cd2ed1c9c`) | Interpreter (`kujo run ... --interpreter`) | supported | required | Release-artifact CI and Docker source pin; bounds request bodies, honors declared lengths without deadline stalls, enforces read deadlines, and exposes trustworthy peer identity. |
| Kujo v1.2.2 signed release commit (`22582e7f0111a1005002579b44f5d03cd2ed1c9c`) | VM (`kujo run ...`) | supported | required | The same live listener, peer, direct-proxy-bypass, and oversized-body checks run in VM mode. |
| Kujo v1.2.0 signed release commit (`ed51720892d8e475980909dffe54c8fba8731e11`) | Interpreter and VM | compatibility-only | prohibited for production | Contains the initial body bound/deadline work but can wait for the read deadline after a complete declared body. |

## Non-Goals / Unsupported Combinations

| Runtime source | Execution mode | Support level | Reason |
|---|---|---|---|
| Arbitrary unpinned Kujo runtime versions | Interpreter, bridge, or direct native | best-effort | Behavior can drift across upstream changes; release CI only certifies pinned runtime. |

## CI Validation Contract

The release gates workflow validates supported combinations using:
- full release gate suite in interpreter mode
- bridge-mode smoke command through scripts/run_main_auto.kujo
- native-mode core ingest/query parity test through tests/test_native_mode_parity.kujo

If either supported mode fails in CI, release promotion must be blocked until fixed.

## Operational Guidance

- Use interpreter mode for deterministic automation and release gates.
- Use bridge mode for native-first local workflows with safe fallback behavior.
- Use direct native mode for validated core ingest/query flows when pinned runtime parity is required.

## Promotion Rule For New Runtime Modes

A runtime mode can be promoted to supported only when:
- it has dedicated CI validation
- parity behavior is documented
- operational caveats are documented
- at least one release cycle has passed with stable results
