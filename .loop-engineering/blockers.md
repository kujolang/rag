# External Blockers

blockers:
  - id: typed-env-default-contract
    command: "env_int/env_float/env_bool"
    evidence: "RAG config normalization preserves invalid-value fallback, current-value fallback, and string-to-type conversion across a large policy surface; native typed env accessors do not provide the same default-on-error contract. The two pure boolean environment wrappers were migrated, while domain config parsers remain intentionally retained."
    status: needs-contract-first
    next_action: "Define optional/default typed-env primitives or a documented fallback contract, then migrate the remaining config normalization with compatibility fixtures."
