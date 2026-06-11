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
| Pinned Kujo runtime commit (7819d1475e909ec88f510c9927445791ea928836) | Interpreter (`kujo run ... --interpreter`) | supported | required | Primary reliability mode for multi-module flows. |
| Pinned Kujo runtime commit (7819d1475e909ec88f510c9927445791ea928836) | Bridge (`scripts/run_main_auto.kujo`) | supported | required | Native-first bridge with automatic interpreter fallback. |
| Pinned Kujo runtime commit (7819d1475e909ec88f510c9927445791ea928836) | Direct native core parity (`kujo run main.kujo ingest/query ...`) | supported-for-core-flows | required | Core ingest/query parity is validated through `tests/test_native_mode_parity.kujo`. |

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
