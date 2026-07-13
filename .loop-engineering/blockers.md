# External Blockers

blockers:
  - id: typed-env-default-contract
    command: "env_int/env_float/env_bool"
    evidence: "Kujo now supports typed env defaults for single-name missing/invalid values and the pure boolean wrappers were migrated. RAG still retains domain config parsers that enforce positive bounds, multi-source precedence, and string-to-type normalization across a larger policy surface."
    status: needs-contract-first
    next_action: "Define a documented multi-source/bounded normalization contract or retain the policy helper, then migrate only paths covered by compatibility fixtures."
