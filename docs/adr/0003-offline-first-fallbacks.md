# ADR-0003: Offline-First Fallbacks

- Status: Accepted
- Date: 2026-05-21

## Context

This starter kit should work with no external APIs, no network dependency, and minimal setup friction. Optional AI integration should enhance behavior, not become a hard dependency.

## Decision

Adopt offline-first defaults with explicit fallbacks:

- Hash embeddings are default provider.
- AI embedding/chat configuration is optional.
- Unknown or unavailable AI providers fall back safely to hash mode.
- PDF parsing failures fall back to deterministic text placeholders with error metadata.

## Consequences

- Local development remains reliable and reproducible.
- Security and resilience improve under partial dependency failure.
- Operators can opt into external providers incrementally.
